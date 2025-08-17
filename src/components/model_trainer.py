import os
import sys

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor,GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor

from xgboost import XGBRegressor
from catboost import CatBoostRegressor

from sklearn.metrics import r2_score

from src.logger import logging
from src.exception import CustomException
from src.utils import save_obj,evaluate_models

from dataclasses import dataclass


@dataclass
class ModelTrainerConfig:
    train_model_file_path = os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    
    def initiate_model_trainer(self,train_arr,test_arr):

        try :
            logging.info("Splitting train and test input & target features")
            X_train,y_train,X_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            logging.info("Defining candidate models for training")
            models = {
                'Linear_Regressor' : LinearRegression(),
                'KN_Regressor' : KNeighborsRegressor(),
                'DT_Regressor' : DecisionTreeRegressor(),
                'RF_Regressor' : RandomForestRegressor(),
                'AdaB_Regressor' : AdaBoostRegressor(),
                'XGB_Regressor' : XGBRegressor(),
                'CatB_Regressor':CatBoostRegressor(verbose=False)
            }

            logging.info("Evaluating models on training and testing dataset")
            model_report : dict=evaluate_models(X_train,y_train,X_test,y_test,models)

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model = models[best_model_name]

            logging.info("Saving best model object")
            save_obj (
                file_path = self.model_trainer_config.train_model_file_path,
                obj=best_model
            )

            logging.info("Generating predictions with the best model")
            predicted = best_model.predict(X_test)

            r2_score_ = r2_score(y_test,predicted)

            return f'{best_model_name} has best performance with r2_score = {r2_score_}'

        except Exception as e:
            logging.error("Exception occurred in ModelTrainer")
            raise CustomException(e,sys)
    