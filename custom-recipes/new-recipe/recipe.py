from dataxform import CorrelatedColumnDropper, LowVarianceColumnDropper, DataFrameScaler, DataFrameNormalization, \
    ColumnDropper

import pandas as pd
from sklearn.datasets import load_boston
from sklearn.pipeline import make_pipeline

input_dataset = dataiku.Dataset(get_input_names_for_role("inputDataset")[0])
transformed_dataset = dataiku.Dataset(get_output_names_for_role("transformedDataset")[0])
recipe_config = get_recipe_config()

transforms = recipe_config["transform_list"]
transformed_dataset = input_dataset.copy()

def switch_transform(transform):
  switcher = {
    "CCD": CorrelatedColumnDropper,
    "LVCC": LowVarianceColumnDropper
  }
  return switcher.get(transform, "Invalid transformation")

iter = 0
while iter < recipe_config["numTransform"]:
  apply_transform = switch_transform(transforms[iter])
  transformed_dataset = apply_transform(transformed_dataset)
  iter += 1