import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from dython.nominal import associations
from pathlib import Path  

class Data_analyzer:
  def __init__(self, data_path) -> None:
    self.salary_survey_data:pd.DataFrame = pd.read_csv(data_path, sep=',')
    self.original_colnames:list = [*self.salary_survey_data.columns]
    self.data_dictionary:dict = {}
    self.salary_survey_colnames:dict = {}
    self.categorical_variables_names:list = []
    self.continuous_variables_names:list = []

    self.start_config()

  def start_config(self):

    self.create_data_dictionary()
    
    self.salary_survey_data.rename(columns=self.salary_survey_colnames, inplace=True)

    self.set_categorical_variables_names()

    self.set_continuous_variables_names()

    self.set_continuous_variables_as_numbers()

    self.replace_nan_values()
    
  
  def create_data_dictionary(self):

    for col_index in range(len(self.original_colnames)):
    
      resetted_col_name = f'col_{col_index}'
      original_name = self.original_colnames[col_index]
      col_values = self.salary_survey_data[self.original_colnames[col_index]].unique()
      frequencies = self.salary_survey_data[self.original_colnames[col_index]].value_counts()
      unique_count_values = len(col_values)
      
      self.data_dictionary[resetted_col_name] = {
        'original_name' : original_name,
        'values' : col_values,
        'frequencies': frequencies,
        'values_count': unique_count_values,
      }

      self.salary_survey_colnames[self.original_colnames[col_index]] = resetted_col_name
  
  def set_categorical_variables_names(self):
    self.categorical_variables_names = [
      self.salary_survey_colnames[self.original_colnames[1]],
      self.salary_survey_colnames[self.original_colnames[2]],
      self.salary_survey_colnames[self.original_colnames[3]],
      self.salary_survey_colnames[self.original_colnames[7]],
      self.salary_survey_colnames[self.original_colnames[10]],
      self.salary_survey_colnames[self.original_colnames[11]],
      self.salary_survey_colnames[self.original_colnames[12]],
      self.salary_survey_colnames[self.original_colnames[13]],
      self.salary_survey_colnames[self.original_colnames[14]],
      self.salary_survey_colnames[self.original_colnames[15]],
      self.salary_survey_colnames[self.original_colnames[16]],
    ]

  def set_continuous_variables_names(self):
    self.continuous_variables_names = [
      self.salary_survey_colnames[self.original_colnames[5]],
      self.salary_survey_colnames[self.original_colnames[6]],
    ]
  
  def set_continuous_variables_as_numbers(self):
    for i in range(len(self.salary_survey_data.col_5)):
      if isinstance(self.salary_survey_data.col_5[i], str):
        self.salary_survey_data.col_5[i] = float(self.salary_survey_data.col_5[i].replace(",", ""))

    for i in range(len(self.salary_survey_data.col_6)):
      if isinstance(self.salary_survey_data.col_6[i], str):
        self.salary_survey_data.col_6[i] = float(self.salary_survey_data.col_6[i].replace(",", ""))
  
  def replace_nan_values(self):
    self.salary_survey_data.col_5.fillna(0, inplace=True)
    self.salary_survey_data.col_6.fillna(0, inplace=True)
    self.salary_survey_data.fillna('-99', inplace=True)
  
  def create_correlation_matrix(self):
    salary_survey_features_names = [*self.categorical_variables_names, *self.continuous_variables_names]

    salary_survey_features = self.salary_survey_data.loc[:, salary_survey_features_names].copy()

    salary_survey_features.rename(columns = {
      salary_survey_features_names[0] : 'age',
      salary_survey_features_names[1] : 'industry',
      salary_survey_features_names[2] : 'job title',
      salary_survey_features_names[3] : 'currency',
      salary_survey_features_names[4] : 'country',
      salary_survey_features_names[5] : 'us state',
      salary_survey_features_names[6] : 'city',
      salary_survey_features_names[7] : 'total years of work',
      salary_survey_features_names[8] : 'current field years of work',
      salary_survey_features_names[9] : 'education level',
      salary_survey_features_names[10] : 'gender',
      salary_survey_features_names[11] : 'annual salary',
      salary_survey_features_names[12] : 'monetary compensation',
    }, inplace=True)

    return associations(
      dataset = salary_survey_features,
      nominal_columns = [
          'age',
          'industry',
          'job title',
          'currency',
          'country',
          'us state',
          'city',
          'total years of work',
          'current field years of work',
          'education level',
          'gender',
      ],
      figsize=(10,10)
    )