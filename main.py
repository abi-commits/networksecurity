import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation, DataTransformationArtifact
from networksecurity.entity.config_entity import DataIngetionConfig, DataValidationConfig, DataTransformationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngetionConfig(training_pipeline_config)
        data_ingetsion = DataIngestion(data_ingestion_config)
        logging.info(f"Initialized Data Ingestion")
        data_ingestion_artifact = data_ingetsion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logging.info(f"Data Ingestion completed successfully")

        data_validation_config=DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        logging.info(f"Initialized Data Validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info(f"Data Validation completed successfully")

        data_tranformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_tranformation_config, data_validation_artifact)
        logging.info(f"Initialized Data Transformation")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info(f"Data Transformation completed successfully")

        
   
    except Exception as e:
        raise NetworkSecurityException(e, sys)