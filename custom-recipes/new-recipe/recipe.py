from dataxform import CorrelatedColumnDropper, LowVarianceColumnDropper, DataFrameScaler, DataFrameNormalization, \
    ColumnDropper

import pandas as pd
from dataiku.customrecipe import *
from sklearn.datasets import load_boston
from sklearn.pipeline import make_pipeline

# get recipe.json elements values
input_dataset = dataiku.Dataset(get_input_names_for_role("inputDataset")[0])
transformed_dataset = dataiku.Dataset(get_output_names_for_role("transformedDataset")[0])
recipe_config = get_recipe_config()

# create the output dataset as a copy
transformed_dataset = input_dataset.copy()

# get the transformations selected and the order they have to be applied
apply_trans = list(trans for trans, select in recipe_config.items() if select == True)
trans_order = list(trans+'-order' for trans in apply_trans)

def switch_transform(transform):
  """
    Function to call the developed transformations based on the interface selections
    :param transform: transformation to apply
    :return: selected transformation function
  """
  switcher = {
    "CCD": CorrelatedColumnDropper,
    "LVCD": LowVarianceColumnDropper,
    "DFS": DataFrameScaler,
    "DFN": DataFrameNormalization,
    "CD": ColumnDropper
  }
  return switcher.get(transform, "Invalid transformation")

def order_transforms(transform_order):
   """
    Function to order the transformations to apply based on the interface selections
    :param transform_order: dictionary with the transformation and the preference order
    :return: dictionary with the transformations sorted
   """
   return {key.split('-')[0]: value for key,value in sorted(transform_order.items(), key = lambda item: item[1])}

for i,trans in enumerate(order_transforms(trans_order)):
    key = trans + '-params'
    if isinstance(recipe_config[key], str):
        params = list(map(str.strip, recipe_config[key].split(";")))
    else:
        params = recipe_config[key]
    apply_transform = switch_transform(trans, params)
    transformed_dataset = apply_transform(transformed_dataset)