from ks_dataxform.dataxform import *


def get_selected_visualizations(recipe_config):
    """
        Function to get the visualizations selected by the user in the plugin interface

        Parameters:
            recipe_config (dict): dictionary with the recipe configuration parameters and their values

        Returns:
            (list) list of selected visualizations
    """
    return list(trans for trans, select in recipe_config.items() if
                select and len(trans.split('-')) == 1 and "viz" in trans)


def switch_visualizations(viz):
    """
        Function to call the developed visualizations based on the interface selections

        Parameters:
            viz (str): visualization to plot

        Returns:
            (class) selected visualization class
    """
    switcher = {
        "vizCorMat": CorrelationMatrixPlot,
        "vizDist": DistributionPlot,
        "vizPairPlot": PairPlot
    }
    return switcher.get(viz, "Invalid visualization")
