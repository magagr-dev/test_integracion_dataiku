from ks_dataxform.dataxform import *
from TransformationUtils import *
from VisualizationUtils import *

from dataiku.customrecipe import *
from dataiku import insights

# get recipe.json elements values
input_dataset = dataiku.Dataset(get_input_names_for_role("inputDataset")[0])
output_dataset = dataiku.Dataset(get_output_names_for_role("transformedDataset")[0])
recipe_config = get_recipe_config()

# create the output dataset as a copy
transformed_df = input_dataset.get_dataframe()

# get the transformations selected and the order they have to be applied
apply_trans = get_selected_transforms(recipe_config)
trans_sorting = get_sorting(recipe_config, apply_trans)
plot_viz = get_selected_visualizations(recipe_config)

if apply_trans:
    pipeline_features = pipeline_features(recipe_config, trans_sorting)
    transformed_df = DataXForm.apply_pipeline(pipeline_features, transformed_df)

if plot_viz:
    for viz in plot_viz:
        plot_visualization(transformed_df, viz, recipe_config)
        insights.save_figure(viz)

output_dataset.write_with_schema(transformed_df)
