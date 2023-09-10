FROM nvcr.io/nvidia/merlin/merlin-tensorflow:nightly
# FROM nvcr.io/nvidia/merlin/merlin-pytorch:nightly
RUN pip install python-dotenv metaflow mlflow torch torchmetrics