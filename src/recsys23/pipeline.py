from metaflow import FlowSpec, step
import config
import pandas as pd
import os
from data.pre_process import Pre_process
from features.feature_eng import Feature_eng
from models.train import two_tower_model
import tensorflow as tf
class Recsys23(FlowSpec):


    @step
    def start(self):
        """
        Start the flow by running the first step.
        """
        self.print_stats = True
        self.save_data = True
        self.next(self.preprocess_data)

    @step
    def preprocess_data(self):
        '''
        Preprocess the data
        '''

        pre_process = Pre_process()
        pre_process.read_data()
        self.train, self.valid, self.test = pre_process.split_based_on_time()
        
        if self.print_stats:
            pre_process.print_stats(self.train,self.valid,self.test)

        self.next(self.feature_eng)

    @step
    def feature_eng(self):
        feature_eng = Feature_eng()
        self.train, self.valid, self.test = feature_eng.baseline(self.train,self.valid,self.test, self.save)
        self.next(self.train_model)

    @step
    def train_model(self):
        '''
        Train the model
        '''
        model = two_tower_model(self.train, self.valid, self.test)
        model.define_model_configs()
        model.fit()
        model.evaluate()

        self.next(self.end)

    @step
    def end(self):
        '''
        End the flow
        '''
        pass
if __name__ == '__main__':
    Recsys23()