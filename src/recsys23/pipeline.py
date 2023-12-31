from metaflow import FlowSpec, step
import config
import pandas as pd
import os
from data.pre_process import Pre_process
from features.feature_eng import Feature_eng_transformers
from models.transformer import Transformer
# from models.train import Two_tower_model
import tensorflow as tf
import mlflow
import json


class Recsys23(FlowSpec):
    @step
    def start(self):
        """
        Start the flow by running the first step.
        """
        # config_path = os.path.join(config.configs_dir, 'config.json')
        # self.configs = json.load(open('config.json'))
        self.print_stats = True
        self.save_data = True
        self.parameters = {}
        self.artifacts = {}
        self.metrics = {}
        self.next(self.preprocess_data)

    @step
    def preprocess_data(self):
        """
        Preprocess the data
        """
        pre_process = Pre_process()
        pre_process.read_data()
        pre_process.split_temporal_transformers(start=90, end=106)

        self.next(self.feature_eng)

    @step
    def feature_eng(self):
        feature_eng = Feature_eng_transformers()
        feature_eng.merge_article_customer_data()
        feature_eng.feature_eng_pipeline()
        # self.artifacts.update(artifacts)V
        self.next(self.train_model)

    # run with gpu
    @step
    def train_model(self):
        """
        Train the model
        """

        model = Transformer(self.train, self.valid, self.test)
        model.define_model_configs()
        model.fit()
        # metrics = model.evaluate()
        # self.metrics.update(metrics)
        # self.metrics.update(history)
        # self.artifacts.update(model.model)
        self.next(self.end)

    @step
    def end(self):
        """
        End the flow
        """
        mlflow.set_experiment("merlin")
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


if __name__ == "__main__":
    # Run the Metaflow flow with Hydra
    # with hydra.initialize_config_module(config_module="your_config_module"):
    #     hydra.main(config_name="config")(Recsys23)()
    Recsys23()

    # how to run the flow
    # python src/recsys23/run.py --max_workers 1 --with batch
