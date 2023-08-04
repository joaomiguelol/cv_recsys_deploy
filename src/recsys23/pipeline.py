from metaflow import FlowSpec, step
import config
import pandas as pd
import os

class Recsys23(FlowSpec):

    @step
    def start(self):
        """
        Start the flow by running the first step.
        """
        self.next(self.read_data)

    @step
    def read_data(self):
        '''
        Read data from the source
        '''
        train = pd.read_parquet(os.path.join(config.data_raw_dir,'transactions.parquet'))
        customers = pd.read_parquet(os.path.join(config.data_raw_dir,'customers.parquet'))

        

        pass
    @step
    def preprocess_data(self):
        '''
        Preprocess the data
        '''
        pass
    @step
    def train_model(self):
        '''
        Train the model
        '''
        pass
    @step
    def evaluate_model(self):
        '''
        Evaluate the model
        '''
        pass
    @step
    def end(self):
        '''
        End the flow
        '''
        pass
