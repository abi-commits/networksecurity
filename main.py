import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngetionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngetionConfig(training_pipeline_config)
        data_ingetsion = DataIngestion(data_ingestion_config)
        logging.info(f"Initialized Data Ingestion")
        data_ingetsion_artifact = data_ingetsion.initiate_data_ingestion()
        print(data_ingetsion_artifact)
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)