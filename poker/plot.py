from typing import List, Optional
from dataclasses import dataclass
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import norm
from poker.base import normalize, running_mean, cumulative_mean
from scipy import stats

fonts = ['xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large']
location = ['best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left',  'center right', 'lower center', 'upper center', 'center']


@dataclass
class Line:
    """

    Class for plotting line plots.

    :param data: Input data.
    :type data: pd.DataFrame,
    :param limit: Limit the length of data. *Optional*
    :type limit: int
    :param label_lst: List of labels to include, if None will include all columns. *Optional*
    :type label_lst: List[str]
    :param color_lst: List of colors to graph, needs to be same length as label_lst. *Optional*
    :type color_lst: List[str]
    :param normalize_x: List of columns to normalize. *Optional*
    :type normalize_x: List[str]
    :param running_mean_x: List of columns to calculate running mean. *Optional*
    :type running_mean_x: List[str]
    :param running_mean_value: Value used when calculating running mean, default = 50. *Optional*
    :type running_mean_value: int
    :param cumulative_mean_x: List of columns to calculate cumulative mean. *Optional*
    :type cumulative_mean_x: List[str]
    :param fig_size: Figure size, default = (10, 7). *Optional*
    :type fig_size: tuple
    :param ylabel: Y axis label. *Optional*
    :type ylabel: str
    :param ylabel_color: Y axis label color, default = 'black'. *Optional*
    :type ylabel_color: str
    :param ylabel_size: Y label size, default = 'medium'. *Optional*
    :type ylabel_size: str
    :param xlabel: X axis label. *Optional*
    :type xlabel: str
    :param xlabel_color: X axis label color, default = 'black'. *Optional*
    :type xlabel_color: str
    :param xlabel_size: X label size, default = 'medium'. *Optional*
    :type xlabel_size: str
    :param title: Graph title, default = 'Line Plot'. *Optional*
    :type title: str
    :param title_size: Title size, default = 'xx-large'. *Optional*
    :type title_size: str
    :param grid: If True will show grid, default = true. *Optional*
    :type grid: bool
    :param grid_alpha: Grid alpha, default = 0.75. *Optional*
    :type grid_alpha: float
    :param grid_dash_sequence: Grid dash sequence, default = (3, 3). *Optional*
    :type grid_dash_sequence: tuple
    :param grid_lineweight: Grid lineweight, default = 0.5. *Optional*
    :type grid_lineweight: float
    :param legend_fontsize: Legend fontsize, default = 'medium'. *Optional*
    :type legend_fontsize: str
    :param legend_transparency: Legend transparency, default = 0.75. *Optional*
    :type legend_transparency: float
    :param legend_location: legend location, default = 'lower right'. *Optional*
    :type legend_location: str
    :example: *None*
    :note: *None*

    """
    def __init__(self,
                 data: pd.DataFrame,
                 limit: Optional[int] = None,
                 label_lst: Optional[List[str]] = None,
                 color_lst: Optional[List[str]] = None,
                 normalize_x: Optional[List[str]] = None,
                 running_mean_x: Optional[List[str]] = None,
                 running_mean_value: Optional[int] = 50,
                 cumulative_mean_x: Optional[List[str]] = None,
                 fig_size: Optional[tuple] = (10, 7),
                 ylabel: Optional[str] = None,
                 ylabel_color: Optional[str] = 'black',
                 ylabel_size: Optional[str] = 'medium',
                 xlabel: Optional[str] = None,
                 xlabel_color: Optional[str] = 'black',
                 xlabel_size: Optional[str] = 'medium',
                 title: Optional[str] = 'Line Plot',
                 title_size: Optional[str] = 'xx-large',
                 grid: Optional[bool] = True,
                 grid_alpha: Optional[float] = 0.75,
                 grid_dash_sequence: Optional[tuple] = (3, 3),
                 grid_lineweight: Optional[float] = 0.5,
                 legend_fontsize: Optional[str] = 'medium',
                 legend_transparency: Optional[float] = 0.75,
                 legend_location: Optional[str] = 'lower right',
                 ):

        if label_lst is None:
            label_lst = list(data.columns)

        if color_lst is None:
            n = len(label_lst)
            if n == 1:
                color_lst = ['tab:orange']
            else:
                color_lst = [plt.get_cmap('viridis')(1. * i / n) for i in range(n)]

        if normalize_x is None:
            normalize_x = []

        if running_mean_x is None:
            running_mean_x = []

        if cumulative_mean_x is None:
            cumulative_mean_x = []

        fig, ax = plt.subplots(figsize=fig_size)

        if limit:
            data = data[:limit]

        count = 0
        for ind in label_lst:

            d = data[ind]
            if ind in normalize_x:
                d = normalize(np.array(d))
            elif ind in running_mean_x:
                d = running_mean(np.array(d), running_mean_value)
            elif ind in cumulative_mean_x:
                d = cumulative_mean(np.array(d))

            ax.plot(d, color=color_lst[count], label=ind)
            count += 1

        ax.set_ylabel(ylabel, color=ylabel_color, fontsize=ylabel_size)
        ax.tick_params(axis='y', labelcolor=ylabel_color)
        ax.set_title(title, fontsize=title_size)

        if grid:
            ax.grid(alpha=grid_alpha, linestyle=(0, grid_dash_sequence), linewidth=grid_lineweight)

        ax.set_xlabel(xlabel, color=xlabel_color, fontsize=xlabel_size)
        ax.legend(fontsize=legend_fontsize, framealpha=legend_transparency, loc=legend_location, frameon=True)
        self._ax = ax

    def __repr__(self):
        return 'Line Plot'

    @property
    def ax(self):
        """Returns a plot"""
        return self._ax


@dataclass
class Scatter:
    """

    Class for plotting scatter plots.

    :param data: Input data.
    :type data: pd.DataFrame,
    :param limit: Limit the length of data. *Optional*
    :type limit: int
    :param label_lst: List of labels to include, if None will include all columns. *Optional*
    :type label_lst: List[str]
    :param color_lst: List of colors to graph, needs to be same length as label_lst. *Optional*
    :type color_lst: List[str]
    :param normalize_x: List of columns to normalize. *Optional*
    :type normalize_x: List[str]
    :param regression_line:  If included, requires a column str or List[str], default = None. *Optional*
    :type regression_line: List[str]
    :param regression_line_color: Color of regression line, default = 'red'. *Optional*
    :type regression_line_color: str
    :param regression_line_lineweight: Regression lineweight, default = 2.0. *Optional*
    :type regression_line_lineweight: float
    :param running_mean_x: List of columns to calculate running mean. *Optional*
    :type running_mean_x: List[str]
    :param running_mean_value: List of columns to calculate running mean. *Optional*
    :type running_mean_value: Optional[int] = 50,
    :param cumulative_mean_x: List of columns to calculate cumulative mean. *Optional*
    :type cumulative_mean_x: List[str]
    :param fig_size: default = (10, 7), *Optional*
    :type fig_size: tuple
    :param ylabel: Y axis label. *Optional*
    :type ylabel: str
    :param ylabel_color: Y axis label color, default = 'black'. *Optional*
    :type ylabel_color: str
    :param ylabel_size: Y label size, default = 'medium'. *Optional*
    :type ylabel_size: str
    :param xlabel: X axis label. *Optional*
    :type xlabel: str
    :param xlabel_color: X axis label color, default = 'black'. *Optional*
    :type xlabel_color: str
    :param xlabel_size: X label size, default = 'medium'. *Optional*
    :type xlabel_size: str
    :param title: Graph title, default = 'Scatter Plot'. *Optional*
    :type title: str
    :param title_size: Title size, default = 'xx-large'. *Optional*
    :type title_size: str
    :param grid: If True will show grid, default = true. *Optional*
    :type grid: bool
    :param grid_alpha: Grid alpha, default = 0.75. *Optional*
    :type grid_alpha: float
    :param grid_dash_sequence: Grid dash sequence, default = (3, 3). *Optional*
    :type grid_dash_sequence: tuple
    :param grid_lineweight: Grid lineweight, default = 0.5. *Optional*
    :type grid_lineweight: float
    :param legend_fontsize: Legend fontsize, default = 'medium'. *Optional*
    :type legend_fontsize: str
    :param legend_transparency: Legend transparency, default = 0.75. *Optional*
    :type legend_transparency: float
    :param legend_location: legend location, default = 'lower right'. *Optional*
    :type legend_location: str
    :param compare_two: If given will return a scatter comparing two variables, default is None. *Optional*
    :type compare_two: List[str]
    :param y_limit: If given will limit the y axis.
    :type y_limit: List[float]
    :example: *None*
    :note: *None*

    """
    def __init__(self,
                 data: pd.DataFrame,
                 limit: Optional[int] = None,
                 label_lst: Optional[List[str]] = None,
                 color_lst: Optional[List[str]] = None,
                 normalize_x: Optional[List[str]] = None,
                 regression_line: Optional[List[str]] = None,
                 regression_line_color: Optional[str] = 'r',
                 regression_line_lineweight: Optional[float] = 2.0,
                 running_mean_x: Optional[List[str]] = None,
                 running_mean_value: Optional[int] = 50,
                 cumulative_mean_x: Optional[List[str]] = None,
                 fig_size: Optional[tuple] = (10, 7),
                 ylabel: Optional[str] = None,
                 ylabel_color: Optional[str] = 'black',
                 ylabel_size: Optional[str] = 'medium',
                 xlabel: Optional[str] = None,
                 xlabel_color: Optional[str] = 'black',
                 xlabel_size: Optional[str] = 'medium',
                 title: Optional[str] = 'Scatter Plot',
                 title_size: Optional[str] = 'xx-large',
                 grid: Optional[bool] = True,
                 grid_alpha: Optional[float] = 0.75,
                 grid_dash_sequence: Optional[tuple] = (3, 3),
                 grid_lineweight: Optional[float] = 0.5,
                 legend_fontsize: Optional[str] = 'medium',
                 legend_transparency: Optional[float] = 0.75,
                 legend_location: Optional[str] = 'lower right',
                 compare_two: Optional[List[str]] = None,
                 y_limit: Optional[List[float]] = None
                 ):

        if label_lst is None:
            label_lst = list(data.columns)

        if color_lst is None:
            n = len(label_lst)
            if n == 1:
                color_lst = ['tab:orange']
                regression_line_color = 'tab:blue'
            else:
                color_lst = [plt.get_cmap('viridis')(1. * i / n) for i in range(n)]

        if normalize_x is None:
            normalize_x = []

        if running_mean_x is None:
            running_mean_x = []

        if cumulative_mean_x is None:
            cumulative_mean_x = []

        if regression_line is None:
            regression_line = []

        fig, ax = plt.subplots(figsize=fig_size)

        if limit:
            data = data[:limit]

        x_axis = range(len(data))

        if compare_two:
            label_lst = [compare_two[1]]
            x_axis = data[compare_two[0]]
            if compare_two[0] in normalize_x:
                x_axis = normalize(x_axis)
            elif compare_two[0] in running_mean_x:
                x_axis = running_mean(x_axis, running_mean_value)
            elif compare_two[0] in cumulative_mean_x:
                x_axis = cumulative_mean(x_axis)

        count = 0
        for ind in label_lst:

            d = data[ind]
            if ind in normalize_x:
                d = normalize(np.array(d))
            elif ind in running_mean_x:
                d = running_mean(np.array(d), running_mean_value)
            elif ind in cumulative_mean_x:
                d = cumulative_mean(np.array(d))

            ax.scatter(x=x_axis, y=d, color=color_lst[count], label=ind)

            if ind in regression_line:
                slope, intercept, r_value, p_value, std_err = stats.linregress(x_axis, d)

                if len(label_lst) == 1:
                    c = regression_line_color
                else:
                    c = color_lst[count]

                ax.plot(x_axis, intercept + slope * x_axis, color=c, label=ind+'_ols_'+str(round(slope, 2)),
                        linestyle='--', linewidth=regression_line_lineweight)
            count += 1

        ax.set_ylabel(ylabel, color=ylabel_color, fontsize=ylabel_size)
        ax.tick_params(axis='y', labelcolor=ylabel_color)
        ax.set_title(title, fontsize=title_size)

        if grid:
            ax.grid(alpha=grid_alpha, linestyle=(0, grid_dash_sequence), linewidth=grid_lineweight)

        ax.set_xlabel(xlabel, color=xlabel_color, fontsize=xlabel_size)
        ax.legend(fontsize=legend_fontsize, framealpha=legend_transparency, loc=legend_location, frameon=True)

        if y_limit:
            ax.set_ylim(bottom=y_limit[0], top=y_limit[1])

        self._ax = ax

    def __repr__(self):
        return 'Scatter Plot'

    @property
    def ax(self):
        """Returns a plot"""
        return self._ax


@dataclass
class Histogram:
    """

    Class for plotting histograms.

    :param data: Input data.
    :type data: pd.DataFrame,
    :param limit: Limit the length of data. *Optional*
    :type limit: int
    :param label_lst: List of labels to include, if None will include all columns. *Optional*
    :type label_lst: List[str]
    :param color_lst: List of colors to graph, needs to be same length as label_lst. *Optional*
    :type color_lst: List[str]
    :param include_norm: Include norm. If included, requires a column str, default = None. *Optional*
    :type include_norm: str
    :param norm_color: Norm color, default = 'red'. *Optional*
    :type norm_color: str
    :param norm_lineweight: Norm lineweight, default = 1.0. *Optional*
    :type norm_lineweight: float
    :param norm_ylabel: Norm Y axis label. *Optional*
    :type norm_ylabel: str
    :param norm_legend_location: Location of norm legend, default = 'upper right'. *Optional*
    :type norm_legend_location: str
    :param fig_size: default = (10, 7), *Optional*
    :type fig_size: tuple
    :param bins: Way of calculating bins, default = 'sturges'. *Optional*
    :type bins: str
    :param hist_type: Type of histogram, default = 'bar'. *Optional*
    :type hist_type: str
    :param stacked: If True, will stack histograms, default = False. *Optional*
    :type stacked: bool
    :param ylabel: Y axis label. *Optional*
    :type ylabel: str
    :param ylabel_color: Y axis label color, default = 'black'. *Optional*
    :type ylabel_color: str
    :param ylabel_size: Y label size, default = 'medium'. *Optional*
    :type ylabel_size: str
    :param ytick_rotation:
    :type ytick_rotation: Optional[int] = 0,
    :param xlabel: X axis label. *Optional*
    :type xlabel: str
    :param xlabel_color: X axis label color, default = 'black'. *Optional*
    :type xlabel_color: str
    :param xlabel_size: X label size, default = 'medium'. *Optional*
    :type xlabel_size: str
    :param xtick_rotation:
    :type xtick_rotation: Optional[int] = 0,
    :param title: Graph title, default = 'Histogram'. *Optional*
    :type title: str
    :param title_size: Title size, default = 'xx-large'. *Optional*
    :type title_size: str
    :param grid: If True will show grid, default = true. *Optional*
    :type grid: bool
    :param grid_alpha: Grid alpha, default = 0.75. *Optional*
    :type grid_alpha: float
    :param grid_dash_sequence: Grid dash sequence, default = (3, 3). *Optional*
    :type grid_dash_sequence: tuple
    :param grid_lineweight: Grid lineweight, default = 0.5. *Optional*
    :type grid_lineweight: float
    :param legend_fontsize: Legend fontsize, default = 'medium'. *Optional*
    :type legend_fontsize: str
    :param legend_transparency: Legend transparency, default = 0.75. *Optional*
    :type legend_transparency: float
    :param legend_location: legend location, default = 'lower right'. *Optional*
    :type legend_location: str
    :example: *None*
    :note: *None*

    """
    def __init__(self,
                 data: pd.DataFrame,
                 color_lst: Optional[List[str]] = None,
                 label_lst: Optional[List[str]] = None,
                 limit: Optional[int] = None,
                 include_norm: Optional[str] = None,
                 norm_color: Optional[str] = 'r',
                 norm_lineweight: Optional[float] = 1.0,
                 norm_ylabel: Optional[str] = None,
                 norm_legend_location: Optional[str] = 'upper right',
                 fig_size: Optional[tuple] = (10, 7),
                 bins: Optional[str] = 'sturges',
                 hist_type: Optional[str] = 'bar',
                 stacked: Optional[bool] = False,
                 ylabel: Optional[str] = None,
                 ylabel_color: Optional[str] = 'black',
                 ylabel_size: Optional[str] = 'medium',
                 ytick_rotation: Optional[int] = 0,
                 xlabel: Optional[str] = None,
                 xlabel_color: Optional[str] = 'black',
                 xlabel_size: Optional[str] = 'medium',
                 xtick_rotation: Optional[int] = 0,
                 title: Optional[str] = 'Histogram',
                 title_size: Optional[str] = 'xx-large',
                 grid: Optional[bool] = True,
                 grid_alpha: Optional[float] = 0.75,
                 grid_dash_sequence: Optional[tuple] = (3, 3),
                 grid_lineweight: Optional[float] = 0.5,
                 legend_fontsize: Optional[str] = 'medium',
                 legend_transparency: Optional[float] = 0.75,
                 legend_location: Optional[str] = 'lower right',
                 ):

        if label_lst is None:
            label_lst = list(data.columns)

        if color_lst is None:
            n = len(label_lst)
            if n == 1:
                color_lst = ['tab:orange']
                norm_color = 'tab:blue'
            else:
                color_lst = [plt.get_cmap('viridis')(1. * i / n) for i in range(n)]

        fig, ax = plt.subplots(figsize=fig_size)

        if limit:
            data = data[:limit]

        count = 0
        for ind in label_lst:
            ax.hist(data[ind], bins=bins, color=color_lst[count], label=ind, stacked=stacked, histtype=hist_type)
            count += 1

        ax.set_ylabel(ylabel, color=ylabel_color, fontsize=ylabel_size)
        ax.tick_params(axis='y', labelcolor=ylabel_color, rotation=ytick_rotation)
        ax.set_title(title, fontsize=title_size)

        if grid:
            ax.grid(alpha=grid_alpha, linestyle=(0, grid_dash_sequence), linewidth=grid_lineweight)

        ax.set_xlabel(xlabel, color=xlabel_color, fontsize=xlabel_size)
        ax.tick_params(axis='x', labelcolor=ylabel_color, rotation=xtick_rotation)
        ax.legend(fontsize=legend_fontsize, framealpha=legend_transparency, loc=legend_location, frameon=True)

        ax1 = None
        if include_norm:
            d = data[include_norm]
            norm_data = np.random.normal(np.mean(d), np.std(d, ddof=1), len(d))
            _mu, _std = norm.fit(norm_data)
            xmin, xmax = plt.xlim()
            x = np.linspace(xmin, xmax, 100)
            ax1 = ax.twinx()
            ax1.plot(x, norm.pdf(x, _mu, _std), color=norm_color, linewidth=norm_lineweight, linestyle='--',
                     label="Fit Values: mu {:.2f} and std {:.2f}".format(_mu, _std))
            ax1.set_ylabel(norm_ylabel, color=norm_color)
            ax1.tick_params(axis='y', labelcolor=norm_color)
            ax1.legend(fontsize=legend_fontsize, framealpha=legend_transparency, loc=norm_legend_location, frameon=True)
        self._ax = ax
        self._ax1 = ax1

    def __repr__(self):
        return 'Histogram Plot'

    @property
    def ax(self):
        """Returns a plot"""
        return self._ax, self._ax1
