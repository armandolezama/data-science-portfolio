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
    self.categorical_short_description:list = []

    #This variable will contain references to any subset created
    self.subset_data:dict = {}

    self.start_config()

  def start_config(self):

    self.create_data_dictionary()
    
    self.salary_survey_data.rename(columns=self.salary_survey_colnames, inplace=True)

    self.set_categorical_variables_names()

    self.set_continuous_variables_names()

    self.set_categorical_short_description()

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
  
  def set_categorical_short_description(self):
    self.categorical_short_description =  {

      self.categorical_variables_names[0] : {
        'name' : 'Age',
        'answers' : {
          '25-34' : '25-34',
          '45-54' : '45-54',
          '35-44' : '35-44',
          '18-24' : '18-24',
          '65 or over' : '>=65',
          '55-64' : '55-64',
          'under 18' : '<=18',
        }
      },

      self.categorical_variables_names[7] : {
        'name' : 'Total years of work',
        'answers' : {
          '5-7 years': '5-7',
          '2 - 4 years': '2-4',
          '8 - 10 years': '8-10',
          '21 - 30 years': '21-30',
          '11 - 20 years': '11-20',
          '41 years or more': '>=41',
          '31 - 40 years': '31-40',
          '1 year or less': '<=1',
        }
      },

      self.categorical_variables_names[8] : {
        'name' : 'Current field years of work',
        'answers' : {
          '5-7 years': '5-7',
          '2 - 4 years': '2-4',
          '21 - 30 years': '21-30',
          '11 - 20 years': '11-20',
          '8 - 10 years': '8-10',
          '1 year or less': '<=1',
          '31 - 40 years': '31-40',
          '41 years or more': '>=41',
        }
      },

      self.categorical_variables_names[9] : {
        'name' : 'Education level',
        'answers' :{
          "Master's degree" : 'Master',
          'College degree' : 'College',
          'PhD' : 'PhD',
          '-99' : 'Missing',
          'Some college' : 'Some',
          'High School' : 'High school',
          'Professional degree (MD, JD, etc.)' : 'Professional',
        }
      },

      self.categorical_variables_names[10] : {
        'name' : 'Gender',
        'answers' : {
          'Woman' : 'Woman',
          'Man' : 'Man',
          'Non-binary' : 'Non-binary',
          '-99' : 'Missing',
          'Other or prefer not to answer' : 'Other',
          'Prefer not to answer' : 'Prefer not answer',
        }
      },
    }

  def set_continuous_variables_as_numbers(self):
    for i in range(len(self.salary_survey_data.index)):
      if isinstance(self.salary_survey_data.col_5[i], str):
        current_value = self.salary_survey_data.col_5[i]
        current_value = float(current_value.replace(",", ""))
        self.salary_survey_data.loc.__setitem__((slice(None), ('col_5', i)), current_value)

      if isinstance(self.salary_survey_data.col_6[i], str):
        current_value = self.salary_survey_data.col_6[i]
        current_value = float(current_value.replace(",", ""))
        self.salary_survey_data.loc.__setitem__((slice(None), ('col_6', i)), current_value)
  
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
  
  def get_sorted_data_dictionary(self, as_data_frame = True):
    created_df:pd.DataFrame
    if(as_data_frame):
      created_df = pd.DataFrame.from_dict(self.data_dictionary, orient='index')
      created_df = created_df.sort_values(by=['values_count'])
    else:
      created_df = self.data_dictionary

    return created_df
  
  def create_crosstab_instance(self, x_cat, y_cat, use_full_data:bool = False, data_name:str = ''):
    crosstab_instance:pd.DataFrame

    if(use_full_data):
      crosstab_instance = pd.crosstab(self.salary_survey_data[x_cat], self.salary_survey_data[y_cat])
    else:
      crosstab_instance = pd.crosstab(self.subset_data[data_name][x_cat],self.subset_data[data_name][y_cat])
    
    crosstab_instance.rename(
      index=self.categorical_short_description[x_cat]['answers'],
      columns=self.categorical_short_description[y_cat]['answers'],
      inplace=True,
    )

    crosstab_instance.rename_axis(
      index=self.categorical_short_description[x_cat]['name'],
      columns=self.categorical_short_description[y_cat]['name'],
      inplace=True,
    )

    return crosstab_instance

