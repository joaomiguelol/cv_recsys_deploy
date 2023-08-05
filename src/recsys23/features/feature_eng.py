
import os
import config
import nvtabular as nvt
from merlin.io.dataset import Dataset
from nvtabular.ops import *

class Feature_eng():

    def baseline(self, train, valid, test, save = True):
        """
        Create a baseline model
        """

        train = Dataset(train)
        valid = Dataset(valid)
        test = Dataset(test)

        article_id = ["article_id"] >> Categorify() >> TagAsItemID()
        customer_id = ["customer_id"] >> Categorify() >> TagAsUserID()
        
        price = ["price"] >> FillMissing(fill_val=0) >> Normalize() >> TagAsItemFeatures()
        week = ["week"] >> FillMissing(fill_val=0) >> Normalize() >> TagAsUserFeatures()


        features = article_id + customer_id + price + week

        wf = nvt.Workflow(features)

        train = wf.fit_transform(train)
        valid = wf.transform(valid)
        test = wf.transform(test)

        if save:
            train.to_parquet(os.path.join(config.data_final, 'train_processed'))
            valid.to_parquet(os.path.join(config.data_final, 'validation_processed'))
            test.to_parquet(os.path.join(config.data_final, 'test_processed'))
        
        return train, valid, test