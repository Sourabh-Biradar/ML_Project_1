
import streamlit as st

import pandas as pd
import os
import sys

from src.pipeline.predict_pipeline import CustomData,PredictPipeline
from src.exception import CustomException

st.title('Math Score Predictor')

gender = st.selectbox("Select Gender",['Male',"Female"])

race_ethnicity = st.selectbox("Select Race Ethnicity",['group B','group C', 'group A' ,'group D', 'group E'])

parental_level_of_education = st.selectbox("Parental Education" ,["bachelor's degree" ,'some college' ,"master's degree" ,"associate's degree",
'high school', 'some high school'])

lunch = st.selectbox('Lunch',['standard','free/reduced'])

test_preparation_course = st.selectbox('Test Preparation Course',['none', 'completed'])

reading_score = st.number_input('Reading Score (0-100)',0, 100, 70)

writing_score = st.number_input('Writing Score (0-100)',0,100,70)

if st.button('Predict Math Score'):
    try:
        data = CustomData(
            gender=gender,
            race_ethnicity=race_ethnicity,
            parental_level_of_education=parental_level_of_education,
            lunch=lunch,
            test_preparation_course=test_preparation_course,
            reading_score=reading_score,
            writing_score=writing_score
        )

        df = data.get_data_as_df()

        pipeline = PredictPipeline()
        prediction = pipeline.predict(df)

        st.success(f"The predicted Math Score is: {prediction[0]:.2f}")

    except CustomException as e:
        st.error(f"An error occurred: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")




