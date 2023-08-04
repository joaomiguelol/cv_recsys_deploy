from metaflow import FlowSpec, step
import config
import pandas as pd
import os
from data.pre_process import Pre_process
class Recsys23(FlowSpec):
    




    @step
    def start(self):
        """
        Start the flow by running the first step.
        """
        self.next(self.read_data)

    @step
    def preprocess_data(self):
        '''
        Preprocess the data
        '''

        pre_process = Pre_process()
        pre_process.read_data()
        self.train,self.valid,self.test = pre_process.split_based_on_time()
        
        if self.print_stats:
            pre_process.print_stats(self.train,self.valid,self.test)

        self.next(self.train_model)

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
if __name__ == '__main__':
    Recsys23()