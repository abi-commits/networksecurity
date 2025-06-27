import os, sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact)

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.utils.main_utils import save_numpy_array_data, save_object


class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfig,
                 data_validation_artifacts: DataValidationArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifacts = data_validation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def get_data_transformation_pipeline(self) -> Pipeline:
        try:
            logging.info("Initializing KNN Imputer for data transformation")
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            pipeline = Pipeline([("imputer", imputer)])
            logging.info("Data transformation pipeline created successfully.")
            return pipeline
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    

        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Starting data transformation process.")
            train_df = DataTransformation.read_data(self.data_validation_artifacts.valid_test_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifacts.valid_test_file_path)
            
            #Training dataframe
            input_features_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            traget_feature_train_df = train_df[TARGET_COLUMN]
            traget_feature_train_df = traget_feature_train_df.replace(-1, 0) #Replacing -1 with 0 
            #Testing dataframe
            input_features_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            preprocessor_object = self.get_data_transformation_pipeline()
            transformed_input_features_train = preprocessor_object.fit_transform(input_features_train_df)
            transformed_input_features_test = preprocessor_object.transform(input_features_test_df)

            train_arr = np.column_stack((transformed_input_features_train, traget_feature_train_df))
            test_arr = np.column_stack((transformed_input_features_test, target_feature_test_df))

            #saving numpy array data
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
            #saving preprocessor object
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)

            #preparing artifacts
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path= self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path= self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path= self.data_transformation_config.transformed_test_file_path 
            )
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        