from dataxform import CorrelatedColumnDropper, LowVarianceColumnDropper, DataFrameScaler, DataFrameNormalization, \
    ColumnDropper

import pandas as pd
from sklearn.datasets import load_boston
from sklearn.pipeline import make_pipeline

input_dataset = dataiku.Dataset(get_input_names_for_role("inputDataset")[0])
transformed_dataset = dataiku.Dataset(get_output_names_for_role("transformedDataset")[0])
recipe_config = get_recipe_config()

transformed_dataset = input_dataset.copy()
apply_trans = list(trans for trans, select in recipe_config.items() if select == True)

def switch_transform(transform):
  switcher = {
    "CCD": CorrelatedColumnDropper,
    "LVCD": LowVarianceColumnDropper,
    "DFS": DataFrameScaler,
    "DFN": DataFrameNormalization,
    "CD": ColumnDropper
  }
  return switcher.get(transform, "Invalid transformation")

for i, trans in enumerate(apply_trans):
    key = trans + '-params'
    if isinstance(recipe_config[key], str):
        params = list(map(str.strip, recipe_config[key].split(";")))
    else:
        params = recipe_config[key]
    apply_transform = switch_transform(trans, params)
    transformed_dataset = apply_transform(transformed_dataset)

  #{key: value for key,value in sorted(dic.items(), key = lambda item: item[1])}