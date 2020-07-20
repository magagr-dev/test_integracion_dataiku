from ks_dataxform.dataxform import *


def get_selected_visualizations(recipe_config):
    """
        Function to get the visualizations selected by the user in the plugin interface

        Parameters
        ---------------
        recipe_config: dictionary with the recipe configuration parameters and their values

        Returns
        ---------------
        list of selected visualizations
    """
    return list(trans for trans, select in recipe_config.items() if
                select and len(trans.split('-')) == 1 and "viz" in trans)


def switch_visualizations(viz, df, cols, params):
    """
        Function to call the developed visualizations based on the interface selections

        Parameters
        ---------------
        viz: visualization to plot
        df: DataFrame containing the data
        cols: DataFrame's columns to plot
        params: extra configuration parameters


        Returns
        ---------------
        selected visualization class
    """
    switcher = {
        "vizCorMat": df[cols].visualizations.plot_correlation_matrix(params),
        "vizDist": df[cols].visualizations.plot_distribution(params),
        "vizPairPlot": df[cols].visualizations.plot_pair_plot(),
        "vizUniqueCount": df[cols].visualizations.plot_unique_count(),
        "vizFrequency": df[cols].visualizations.plot_frequency_count(params)
    }
    return switcher.get(viz, "Invalid visualization")


def plot_visualization(df, viz, recipe_config):
    """
        Function to plot the selected visualization

        Parameters
        ---------------
        df: DtaFrame containing the data to plot
        viz: visualization to plot
        recipe_config: dictionary containing the recipe configuration

        Returns
        ---------------
        selected visualization plot image
    """
    cols = recipe_config[str(viz + '-cols')]
    params = None
    switch_visualizations(viz, df, cols, params)
