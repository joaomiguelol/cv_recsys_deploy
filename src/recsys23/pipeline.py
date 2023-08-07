from metaflow import FlowSpec, step
import config
import pandas as pd
import os
from data.pre_process import Pre_process
from features.feature_eng import Feature_eng
from models.train import Two_tower_model
import tensorflow as tf
import mlflow




class Recsys23(FlowSpec):

    @step
    def start(self):
        """
        Start the flow by running the first step.
        """
        self.print_stats = True
        self.save_data = True
        self.parameters = {}
        self.artifacts = {}
        self.metrics = {}
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
            config = pre_process.print_stats(self.train,self.valid,self.test)
            self.parameters.update(config)

        self.next(self.feature_eng)

    @step
    def feature_eng(self):
        feature_eng = Feature_eng()
        self.train, self.valid, self.test, artifacts = feature_eng.baseline(self.train,self.valid,self.test, self.save_data)
        
        self.artifacts.update(artifacts)
        self.next(self.train_model)

    # run with gpu
    @step
    def train_model(self):
        '''
        Train the model
        '''

        model = Two_tower_model(self.train, self.valid, self.test)
        model.define_model_configs()
        history = model.fit()
        metrics = model.evaluate()
        self.metrics.update(metrics)
        self.metrics.update(history)
        # self.artifacts.update(model.model)
        self.next(self.end)

    @step
    def end(self):
        '''
        End the flow
        '''
        mlflow.set_experiment('merlin')
        with mlflow.start_run(run_name="Two_tower"):
            mlflow.log_params(self.parameters)
            # mlflow.log_artifacts(self.artifacts)
            # mlflow.log_metrics(self.metrics)
            for metric_name, metric_values in self.metrics.items():
             # Use the index-based names for metrics with multiple values (e.g., loss_0, loss_1)
                if isinstance(metric_values, list):
                    for idx, value in enumerate(metric_values):
                        mlflow.log_metric(metric_name, value)
                else:
                    mlflow.log_metric(metric_name, metric_values)
if __name__ == '__main__':

    teste = Recsys23()

