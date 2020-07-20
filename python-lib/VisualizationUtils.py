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


def switch_visualizations(viz):
    """
        Function to call the developed visualizations based on the interface selections

        Parameters
        ---------------
        viz: visualization to plot


        Returns
        ---------------
        selected visualization function
    """
    switcher = {
        "vizCorMat": [__correlation_matrix, "CorrelationMatrix", ["-method"]],
        "vizDist": [__distribution, "Distribution", ["-ncols", "-figsize"]],
        "vizPairPlot": [__pair_plot, "PairPlot", []],
        "vizUniqueCount": [__unique, "UniqueCount", []],
        "vizFrequency": [__frequency, "Frequency", ["-ncols", "-figsize"]]
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
    selected_viz, name, config = switch_visualizations(viz)
    cols = recipe_config[str(viz + '-cols')]
    params = []
    for c in config:
        if "figsize" in c:
            param = recipe_config[str(viz + c)].replace("(", "").replace(")", "").split(",")
            tuple_items = []
            for p in param:
                if isinstance(p, int):
                    tuple_items += [int(p)]
            params += [tuple(tuple_items)]
        else:
            params += [recipe_config[str(viz + c)]]
    selected_viz(df, cols, params)
    return name + '_' + str(cols).replace("[", "").replace("]", "").replace(", ", "-").replace("'", "")


def __correlation_matrix(df, cols, params):
    if not cols:
        cols = df.columns
    if params:
        df[cols].visualizations.plot_correlation_matrix(method=params)
    else:
        df[cols].visualizations.plot_correlation_matrix()


def __distribution(df, cols, params):
    if not cols:
        cols = df.columns
    if len(params) == 2:
        df[cols].visualizations.plot_distribution(n_cols=params[0], fig_size=params[1])
    elif len(params) == 1:
        if isinstance(params[0], int):
            df[cols].visualizations.plot_distribution(n_cols=params[0])
        else:
            df[cols].visualizations.plot_distribution(fig_size=params[0])
    else:
        df[cols].visualizations.plot_distribution()


def __pair_plot(df, cols, params):
    if not cols:
        cols = df.columns
    df[cols].visualizations.plot_pair_plot()


def __unique(df, cols, params):
    if not cols:
        cols = df.columns
    df[cols].visualizations.plot_unique_count()


def __frequency(df, cols, params):
    if not cols:
        cols = df.columns
    if len(params) == 2:
        df[cols].visualizations.plot_frequency_count(n_cols=params[0], fig_size=params[1])
    elif len(params) == 1:
        if isinstance(params[0], int):
            df[cols].visualizations.plot_frequency_count(n_cols=params[0])
        else:
            df[cols].visualizations.plot_frequency_count(fig_size=params[0])
    else:
        df[cols].visualizations.plot_distribution()
