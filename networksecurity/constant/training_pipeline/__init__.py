import os 
import numpy as np

"""
Data Ingestion constant variables for training pipeline.
"""
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_DATABASE_NAME:str = "abiml"
DATA_INGESTION_COLLECTION_NAME:str = "network_data"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2

""""
Defining the common constants for training pipeline
"""
TARGET_COLUMN:str = "Result"
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACT_DIR:str = "Artifact"
FILE_NAME:str = "phisingData.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"

SCHEMA_FILE_PATH:str = os.path.join("data_schema", "schema.yaml")

SAVED_MODEL_DIR = os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"


"""
Defining the constants for data validation
"""
DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_DIR:str = "valid"
DATA_VALIDATION_INVALID_DIR:str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = "report.yaml"
PREPROCESSING_FILE_NAME:str = "preprocessing.pkl"


"""
Defining the constants for data transformation
"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJ_DIR: str = "transformed_object"

DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform"
}

"""
Defining the model trainer related constants
"""
MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float = 0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THERSHOLD:float = 0.5

TRAINING_BUCKET_NAME = "networksecurity"




