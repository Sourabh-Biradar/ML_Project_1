import os
import sys
import pandas as pd
import numpy as np

from src.logger import logging
from src.exception import CustomException

from src.utils import save_obj

from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from sklearn.impute import SimpleImputer
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path : str = os.path.join('artifacts','preprocessor.pkl')


class DataTransformation:

    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformation_object(self):
        
        logging.info('Data preprocessing underway...')

        try:
            logging.info('separating numerical & categorical features')
            numerical_columns=['reading_score', 'writing_score']
            categorical_columns=['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

            logging.info('creating numerical pipeline')
            num_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())
                ]
            )

            logging.info('creating categorical pipeline')
            cat_pipeline=Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('oh-encoder',OneHotEncoder(handle_unknown='ignore',sparse_output=False))
                ]
            )

            preprocessor = ColumnTransformer(
                [
                    ('numerical pipeline',num_pipeline,numerical_columns),
                    ('categorical pipeline',cat_pipeline,categorical_columns)
                ]
            )
            logging.info('Pipleline & ColumnTransformer configured successfully')

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
        

    
    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('Read train-test data completed')

            logging.info('Obtaining preprocessing object')

            preprocessing_obj = self.get_data_transformation_object()

            target_column_name = 'math_score'
            numerical_features = ['reading_score', 'writing_score']

            input_features_train_df = train_df.drop(target_column_name,axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_features_test_df = test_df.drop(target_column_name,axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing object on training & test dataframes ")

            input_features_train_arr = preprocessing_obj.fit_transform(input_features_train_df)
            input_features_test_arr = preprocessing_obj.transform(input_features_test_df)

            train_arr = np.c_[
                input_features_train_arr,
                np.array(target_feature_train_df)
            ]

            test_arr=np.c_[
                input_features_test_arr,
                np.array(target_feature_test_df)
            ]

            logging.info("Saved preprocessing object")

            save_obj (
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e,sys)
        
        # utils.py
        # export to data_ingestion.py