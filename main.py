import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import (
    DataIngetionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    TrainingPipelineConfig
)

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

if __name__ == "__main__":
    try:
        logging.info("Pipeline execution started.")

        # Initialize pipeline config
        training_pipeline_config = TrainingPipelineConfig()

        # Data Ingestion
        logging.info("Initializing Data Ingestion...")
        data_ingestion_config = DataIngetionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info(f"Data Ingestion completed. Artifact: {data_ingestion_artifact}")

        # Data Validation
        logging.info("Initializing Data Validation...")
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info(f"Data Validation completed. Artifact: {data_validation_artifact}")

        # Data Transformation
        logging.info("Initializing Data Transformation...")
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_transformation_config, data_validation_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info(f"Data Transformation completed. Artifact: {data_transformation_artifact}")

        # Model Trainer
        logging.info("Initializing Model Trainer...")
        model_trainer_config = ModelTrainerConfig(training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info(f"Model Trainer completed. Artifact: {model_trainer_artifact}")

        logging.info("Pipeline execution completed successfully.")
        print(f"Final Model Path: {model_trainer_artifact.trained_model_file_path}")

    except Exception as e:
        raise NetworkSecurityException(e, sys)