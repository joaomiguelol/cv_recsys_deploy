import pandas as pd
import os
import config
from sklearn.preprocessing import LabelEncoder
import mlflow


class Pre_process:
    def __init__(self):
        self.transactions = None
        pass

    def read_data(self):
        """
        Read data from the source
        """

        self.transactions = pd.read_parquet(os.path.join(config.data_raw_dir, "transactions.parquet"))
        customers = pd.read_parquet(os.path.join(config.data_raw_dir, "customers.parquet"))

        # Encode customer_id, at it is a hash string
        encoder = LabelEncoder()
        merged_ids = pd.concat([self.transactions["customer_id"], customers["customer_id"]])
        encoder.fit(merged_ids)
        self.transactions["customer_id"] = encoder.transform(self.transactions["customer_id"])
        customers["customer_id"] = encoder.transform(customers["customer_id"])

        customers.to_parquet(os.path.join(config.data_processed_dir, "customers_enc.parquet"))

    def split_based_on_time(self, train_start=50, valid_start=90, test_start=100, test_end=104):
        transactions = pd.read_parquet(os.path.join(config.data_processed_dir, "transactions_enc.parquet"))

        transactions["t_dat"] = pd.to_datetime(transactions["t_dat"])
        transactions["week"] = 104 - (transactions["t_dat"].max() - transactions["t_dat"]).dt.days // 7

        train = transactions[(transactions.week > train_start) & (transactions.week <= valid_start)]
        valid = transactions[(transactions.week > valid_start) & (transactions.week <= test_start)]
        test = transactions[(transactions.week > test_start) & (transactions.week <= test_end)]

        # TODO: Use cold start,
        valid = valid[valid["customer_id"].isin(train["customer_id"])]
        test = test[test["customer_id"].isin(train["customer_id"])]

        return train, valid, test

    def split_temporal_transformers(self, start, end):
        self.transactions["t_dat"] = pd.to_datetime(self.transactions["t_dat"])
        self.transactions["week"] = 104 - (self.transactions["t_dat"].max() - self.transactions["t_dat"]).dt.days // 7

        train = self.transactions[(self.transactions.week > start) & (self.transactions.week <= end)]
        save_dir = os.path.join(config.data_processed_dir, "train.parquet")
        del self.transactions
        train.to_parquet(save_dir)

    def print_stats(self, train, valid, test):
        common = set(train["customer_id"]).intersection(set(valid["customer_id"]))
        common_items = set(train["article_id"]).intersection(set(valid["article_id"]))

        print("Number of common customers in train and valid: ", len(common))
        print(
            "Number of common customers in train and test: ",
            len(set(train["customer_id"]).intersection(set(test["customer_id"]))),
        )
        print(
            "Number of common customers in valid and test: ",
            len(set(valid["customer_id"]).intersection(set(test["customer_id"]))),
        )

        print("Number of common items between train and valid: ", len(common_items))
        print("\n\nNumber of customers in train: ", len(train["customer_id"].unique()))
        print("Number of customers in valid: ", len(valid["customer_id"].unique()))
        print("\n\nNumber of items in train: ", len(train["article_id"].unique()))
        print("Number of items in valid: ", len(valid["article_id"].unique()))
        print(
            "Number of customers in valid but not in train: ",
            len(set(valid["customer_id"]) - set(train["customer_id"])),
        )
        print(
            "Number of customers in train but not in test: ", len(set(train["customer_id"]) - set(test["customer_id"]))
        )

        print("Number of items in valid but not in train: ", len(set(valid["article_id"]) - set(train["article_id"])))

        print("\n\ntrain shape: ", train.shape)
        print("valid shape: ", valid.shape)
        print("test shape: ", test.shape)

        parameters = {}
        parameters["Number of common customers in train and valid "] = len(common)
        parameters["Number of common customers in train and test "] = len(
            set(train["customer_id"]).intersection(set(test["customer_id"]))
        )
        parameters["Number of common customers in valid and test "] = len(
            set(valid["customer_id"]).intersection(set(test["customer_id"]))
        )
        parameters["Number of common items between train and valid "] = len(common_items)
        parameters["Number of customers in train "] = len(train["customer_id"].unique())
        parameters["Number of customers in valid "] = len(valid["customer_id"].unique())
        parameters["Number of items in train "] = len(train["article_id"].unique())
        parameters["Number of items in valid"] = len(valid["article_id"].unique())
        parameters["Number of customers in valid but not in train "] = len(
            set(valid["customer_id"]) - set(train["customer_id"])
        )
        parameters["Number of customers in train but not in test"] = len(
            set(train["customer_id"]) - set(test["customer_id"])
        )
        parameters["Number of items in valid but not in train "] = len(
            set(valid["article_id"]) - set(train["article_id"])
        )
        parameters["train shape "] = train.shape
        parameters["valid shape "] = valid.shape
        parameters["test shape "] = test.shape

        return parameters
