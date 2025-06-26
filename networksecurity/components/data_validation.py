from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils import read_yaml_file, write_yaml_file
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from scipy.stats import ks_2samp
import pandas as pd
import numpy as np
import os, sys

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema = read_yaml_file(SCHEMA_FILE_PATH)
            self.numeric_columns = self.schema['numerical_columns']
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            expected_columns = self.schema['columns']
            return len(dataframe.columns) == len(expected_columns)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def numeric_column_validation(self, dataframe: pd.DataFrame) -> bool:
        try:
            for column in self.numeric_columns:
                if column not in dataframe.columns or not pd.api.types.is_numeric_dtype(dataframe[column]):
                    return False
            return True
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_data_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold: float = 0.05) -> bool:
        try:
            drift_report = {}
            drift_status = True

            for column in base_df.columns:
                p_value = ks_2samp(base_df[column], current_df[column]).pvalue
                drift_found = p_value < threshold
                drift_status = drift_status and not drift_found  # If drift found, set to False

                drift_report[column] = {
                    "p_value": float(p_value),
                    "drift_detected": drift_found
                }

            write_yaml_file(self.data_validation_config.drift_report_file_path, drift_report)
            return drift_status
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            if not self.validate_number_of_columns(train_df):
                raise NetworkSecurityException("Train data columns do not match schema", sys)
            if not self.validate_number_of_columns(test_df):
                raise NetworkSecurityException("Test data columns do not match schema", sys)

            if not self.numeric_column_validation(train_df):
                raise NetworkSecurityException("Train data has non-numeric columns", sys)
            if not self.numeric_column_validation(test_df):
                raise NetworkSecurityException("Test data has non-numeric columns", sys)

            drift_status = self.validate_data_drift(train_df, test_df)

            os.makedirs(os.path.dirname(self.data_validation_config.valid_train_file_path), exist_ok=True)
            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False)

            return DataValidationArtifact(
                validation_status=drift_status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)
