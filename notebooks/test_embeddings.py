# %%
from transformers4rec import torch as tr
import warnings
warnings.filterwarnings('ignore')
import nvtabular as nvt
import cudf
import config
import os
# ignore warnings
from merlin.core.dispatch import get_lib
from merlin.schema.tags import Tags
from transformers4rec.torch.utils.examples_utils import fit_and_evaluate
import time
import merlin.models.tf as mm
from tensorflow.keras.callbacks import EarlyStopping

from merlin.schema.tags import Tags
from nvtabular.ops import *

from merlin.schema.tags import Tags
from merlin.io.dataset import Dataset
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np


# %%
dir = os.path.join(config.data_final,'time',)
train = Dataset(os.path.join(config.data_final,'transformer4rec','train.parquet'),engine="parquet",  part_size="1GB")
# valid = Dataset(os.path.join(config.data_final,'transformer4rec', 'valid.parquet/*.parquet'),engine="parquet", part_size="1GB")

# %%
schema = train.schema.select_by_tag(Tags.SEQUENCE)


# %%
path= os.path.join(config.data_raw_dir, 'image_embeddings_norm.parquet')
image_embeddings = cudf.read_parquet(path)

max_sequence_length, d_model = 64, 64
# Define input module to process tabular input-features and to prepare masked inputs
input_module = tr.TabularSequenceFeatures.from_schema(
    schema,
    max_sequence_length=30,
    # continuous_projection=512,
    # categorical_projection=256,
    aggregation="concat",
    d_output=d_model,
    masking="mlm",
)
# Define Next item prediction-task 
prediction_task = tr.NextItemPredictionTask(weight_tying=True,)

# # Define the config of the XLNet Transformer architecture
transformer_config = tr.XLNetConfig.build(
    d_model=d_model, n_head=8, n_layer=5, 
)

# # Get the end-to-end model 
model = transformer_config.to_torch_model(input_module, prediction_task)



# %%
training_args = tr.trainer.T4RecTrainingArguments(
            output_dir="./tmp",
            max_sequence_length=30,
            data_loader_engine='merlin',
            num_train_epochs=200, 
            dataloader_drop_last=False,
            per_device_train_batch_size = 1024,
            per_device_eval_batch_size = 1024,
            learning_rate=0.0005,
            fp16=True,
            report_to = [],
            logging_steps=200
        )

# %%
trainer = tr.Trainer(
    model=model,
    args=training_args,
    schema=schema,
    compute_metrics=True)

# %%
start_time_window_index = 81
final_time_window_index = 104
import glob
import os
import config

train_window = 3
for time_index in range(start_time_window_index, final_time_window_index - train_window + 1):

    # Set data 
    time_index_train = time_index
    time_index_eval = time_index + train_window

    # train paths for time_index time_index+1 time_index+2
    # eval paths for time_index+3
    train_paths = []
    for i in range(time_index,time_index + train_window):
        train_paths.append(os.path.join(config.data_final,'time', f"{i}/train.parquet"))

    # train_paths = glob.glob(os.path.join(config.data_final,'time', f"{time_index_train}/train.parquet"))
    eval_paths = glob.glob(os.path.join(config.data_final,'time' , f"{time_index_eval}/valid.parquet"))

    # Train on day related to time_index 
    print('*'*20)
    print("Launch training for day %s are:" %time_index)
    print('*'*20 + '\n')
    trainer.train_dataset_or_path = train_paths
    trainer.reset_lr_scheduler()
    trainer.train()
    trainer.state.global_step +=1
    # Evaluate on the following day
    trainer.eval_dataset_or_path = eval_paths
    train_metrics = trainer.evaluate(metric_key_prefix='eval')
    print('*'*20)
    print("Eval results for day %s are:\t" %time_index_eval)
    print('\n' + '*'*20 + '\n')
    for key in sorted(train_metrics.keys()):
        print(" %s = %s" % (key, str(train_metrics[key]))) 


