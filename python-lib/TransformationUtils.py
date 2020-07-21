from ks_dataxform.dataxform import *
from sklearn.pipeline import Pipeline


def get_selected_transforms(recipe_config):
    """
        Function to get the transformations selected by the user in the plugin interface

        Parameters:
            recipe_config (dict): dictionary with the recipe configuration parameters and their values

        Returns:
            (list) list of selected transformations
    """
    return list(trans for trans, select in recipe_config.items() if select and len(trans.split('-')) == 1
                and "viz" not in trans)


def get_sorting(recipe_config, apply_trans):
    """
            Function returning the selected transformations sorted

            Parameters:
                recipe_config (dict): dictionary with the recipe configuration parameters and their values
                apply_trans (list): list of selected transformations

            Returns:
                (dict) dictionary with the selected transformations sorted
        """
    return {trans: value for trans, value in recipe_config.items() if
            "order" in trans and trans.split('-')[0] in apply_trans}


def switch_transform(transform):
    """
        Function to call the developed transformations based on the interface selections

        Parameters:
            transform (str): transformation to apply

        Returns:
            (class) selected transformation class
    """
    switcher = {
        "CCD": CorrelatedColumnDropper,
        "LVCD": LowVarianceColumnDropper,
        "DFS": DataFrameScaler,
        "DFN": DataFrameNormalization,
        "CD": ColumnDropper,
        "CS": ColumnSelector,
        "UC": UnicodeConversion,
        "YJT": YJTransformer
    }
    return switcher.get(transform, "Invalid transformation")


def sort_transforms(trans_sorting):
    """
        Function to sort the transformations to apply based on the interface selections

        Parameter:
            transform_order (dict): dictionary with the transformation and the preference order

        Returns:
            (dict) dictionary with the transformations sorted
    """
    return {key.split('-')[0]: value for key, value in sorted(trans_sorting.items(), key=lambda item: item[1])}


def pipeline_features(recipe_config, trans_sorting):
    """
        Function to call the developed visualizations based on the interface selections

        Parameters:
            recipe_config (dict): dictionary with the recipe configuration parameters and their values
            trans_sorting (dict): dictionary with the selected transformations sorted

        Returns:
            (list) List of transformations to apply to the original dataset
    """
    steps = []
    for i, trans in enumerate(sort_transforms(trans_sorting)):
        key = trans + '-params'
        params = recipe_config[key]
        apply_transform = switch_transform(trans)
        try:
            steps += [(apply_transform.__name__.lower(), apply_transform(params))]
        except KeyError:
            raise KeyError("Transformation %s is not available" % apply_transform.__name__)
    return steps
