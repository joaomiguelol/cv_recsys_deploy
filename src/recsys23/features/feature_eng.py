import warnings
warnings.filterwarnings("ignore")
import nvtabular as nvt
import cudf
import config
import os
from merlin.schema.tags import Tags
from nvtabular.ops import *
from merlin.io.dataset import Dataset
from transformers4rec.utils.data_utils import save_time_based_splits

class Feature_eng_transformers:
    def __init__(self):
        self.customer_features = ["customer_id", "age"]
        self.article_features = [
            "article_id",
            "product_code",
            "product_type_no",
            "graphical_appearance_no",
            "colour_group_code",
            "perceived_colour_value_id",
            "perceived_colour_master_id",
            "department_no",
            "index_code",
            "index_group_no",
            "section_no",
            "garment_group_no",
        ]

        self.SESSIONS_MAX_LENGTH = 30
        self.SESSIONS_MIN_LENGTH = 2

    def merge_article_customer_data(self):
        train = nvt.Dataset(
            os.path.join(config.data_processed_dir, "train.parquet"), engine="parquet", part_mem_fraction=0.1
        )

        articles = cudf.read_parquet(os.path.join(config.data_raw_dir, "articles.parquet"))[self.article_features]
        customers = cudf.read_parquet(os.path.join(config.data_processed_dir, "customers_enc.parquet"))[
            self.customer_features
        ]

        articles = nvt.Dataset(articles)
        customers = nvt.Dataset(customers)

        train = Dataset.merge(train, articles, on="article_id", how="inner")
        train = Dataset.merge(train, customers, on="customer_id", how="inner")
        train.to_parquet(os.path.join(config.data_processed_dir, "transformer4rec", "train.parquet"))

    def feature_eng_pipeline(self):
        article_id = ["article_id"] >> Categorify()
        customer_id = ["customer_id"] >> Categorify() >> TagAsUserID()
        price = ["price"] >> LogOp() >> Normalize() >> TagAsItemFeatures()
        week_split = ["week"]
        time_features = ["t_dat"]
        session_time = (
            time_features
            >> nvt.ops.LambdaOp(lambda col: cudf.to_datetime(col, unit="s"))
            >> nvt.ops.Rename(name="event_time_dt")
        )

        day = (
            session_time
            >> nvt.ops.LambdaOp(lambda col: col.dt.day)
            >> nvt.ops.Rename(name="day")
            >> Categorify()
            >> TagAsUserFeatures()
        )
        week = (
            session_time
            >> nvt.ops.LambdaOp(lambda col: col.dt.weekday)
            >> nvt.ops.Rename(name="week_day")
            >> Categorify()
            >> TagAsUserFeatures()
        )
        month = (
            session_time
            >> nvt.ops.LambdaOp(lambda col: col.dt.month)
            >> nvt.ops.Rename(name="month")
            >> Categorify()
            >> TagAsUserFeatures()
        )
        year = (
            session_time
            >> nvt.ops.LambdaOp(lambda col: col.dt.year)
            >> nvt.ops.Rename(name="year")
            >> Categorify()
            >> TagAsUserFeatures()
        )

        age = ["age"] >> LogOp() >> Normalize() >> TagAsUserFeatures() >> AddTags([Tags.USER, Tags.CONTINUOUS])

        cat_article_columns = self.article_features >> Categorify() >> TagAsItemFeatures()
        filtered_articles = article_id + customer_id + [
            "t_dat"
        ] + price + day + week + month + year + age + cat_article_columns + week_split >> Filter(
            f=lambda df: df["article_id"] != 0
        )
        groupby_features = filtered_articles >> Groupby(
            groupby_cols=["customer_id", "week"],
            aggs={
                "article_id": ["list", "count"],
                "price": ["list", "mean", "std", "max"],
                "product_code": ["list"],
                "product_type_no": ["list"],
                "graphical_appearance_no": ["list"],
                "colour_group_code": ["list"],
                "perceived_colour_value_id": ["list"],
                "perceived_colour_master_id": ["list"],
                "department_no": ["list"],
                "index_code": ["list"],
                "index_group_no": ["list"],
                "section_no": ["list"],
                "garment_group_no": ["list"],
                "day": ["list"],
                "week_day": ["list"],
                "month": ["list"],
                "year": ["list"],
            },
            sort_cols=["t_dat"],
            name_sep="_",
        )
        list_columns = [
            "price_list",
            "day_list",
            "week_day_list",
            "month_list",
            "year_list",
            "product_code_list",
            "product_type_no_list",
            "graphical_appearance_no_list",
            "colour_group_code_list",
            "perceived_colour_value_id_list",
            "perceived_colour_master_id_list",
            "department_no_list",
            "index_code_list",
            "index_group_no_list",
            "section_no_list",
            "garment_group_no_list",
        ]

        groupby_features_articles_id = groupby_features["article_id_list"] >> AddTags(
            [Tags.ITEM, Tags.ITEM_ID, Tags.SEQUENCE]
        )
        groupby_features_articles_features = groupby_features[list_columns] >> AddTags([Tags.ITEM, Tags.SEQUENCE])
        truncated_features = groupby_features_articles_id + groupby_features_articles_features >> ListSlice(
            -self.SESSIONS_MAX_LENGTH
        )
        stat_features = (
            groupby_features["article_id_count", "price_max", "price_mean", "price_std"]
            >> LogOp()
            >> Normalize()
            >> Rename(postfix="_norm")
            >> AddTags([Tags.ITEM, Tags.CONTINUOUS])
        )

        output = groupby_features[
            "customer_id", "article_id_count"
        ] + truncated_features + stat_features + week_split >> Filter(
            f=lambda df: df["article_id_count"] >= self.SESSIONS_MIN_LENGTH
        )
        train = nvt.Dataset(os.path.join(config.data_processed_dir,'transformer4rec', 'train.parquet'),engine="parquet",)
        valid = nvt.Dataset(os.path.join(config.data_processed_dir,'transformer4rec', 'valid.parquet'),engine="parquet")
        print(len(train.to_ddf()), len(valid.to_ddf()))

        wf = nvt.Workflow(output)
        train = wf.fit_transform(train)
        print(len(train.to_ddf()), len(valid.to_ddf()))

        train.to_parquet(os.path.join(config.data_final,'transformer4rec', 'train.parquet'))
        valid.to_parquet(os.path.join(config.data_final,'transformer4rec', 'valid.parquet'))
        wf.save(os.path.join(config.data_final,'transformer4rec', 'workflow'))

        
        save_time_based_splits(train,
                            output_dir=os.path.join(config.data_final,'time'),
                            partition_col='week',
                            timestamp_col='customer_id', 
                            )
        print("Done!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")