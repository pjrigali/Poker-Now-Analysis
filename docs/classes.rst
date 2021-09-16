.. _Classes:

Classes
*******

.. meta::
   :description: Landing page for poker-now-analysis.
   :keywords: Poker, Python, Analysis, Texas Hold'em

This chapter documents the Classes used in this package.

.. _Poker:

Poker
-----
Class object for running the package.

.. :currentmodule:: base

.. class:: Poker(repo_location, grouped):

    Calculate stats for all games and players.

    :param repo_location: Location of data folder.
    :type repo_location: str
    :param grouped: List of lists, filled with unique player Ids that are related to the same person. *Optional*
    :type grouped: str
    :param money_multi: Multiple to divide the money amounts to translate them to dollars *Optional*
    :type money_multi: int
    :example:
        .. code-block:: python

            from poker.base import Poker
            repo = 'location of your previous game'
            grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
                        ['48QVRRsiae', 'u8_FUbXpAz']]
            poker = Poker(repo_location=repo, grouped=grouped)
    :note: Grouped will need to be figured out by the player.
        The grouped stats are only taken into account within this class

.. autosummary::
    poker.base.Poker.files
    poker.base.Poker.matches
    poker.base.Poker.players_info
    poker.base.Poker.card_distribution
    poker.base.Poker.winning_hand_distribution

.. _Game:

Game
----
Class object used for getting specific game stats.

.. :currentmodule:: base

.. class:: Game(repo_location, file):

    Calculate stats for a game.

    :param repo_location: Location of data folder.
    :type repo_location: str
    :param file: Name of file.
    :type file: str
    :example: *None*
    :note: This class is intended to be used internally.

.. autosummary::
    poker.base.Game.file_name
    poker.base.Game.hands_lst
    poker.base.Game.players_info
    poker.base.Game.card_distribution
    poker.base.Game.winning_hand_distribution
    poker.base.Game.players

.. _Player:

Player
------
Class object used for getting specific player stats.

.. :currentmodule:: base

.. class:: Player(player_index, hands):

    Calculate stats for a player. Stats are for a single match.

    :param player_index: A unique player ID.
    :type player_index: str
    :param hands: list of Hand objects related to a game.
    :type hands: List[Hand]
    :example: *None*
    :note: This class is intended to be used internally.

.. autosummary::
    poker.base.Player.win_df
    poker.base.Player.win_per
    poker.base.Player.win_count
    poker.base.Player.largest_win
    poker.base.Player.largest_loss
    poker.base.Player.winning_habits
    poker.base.Player.normal_habits
    poker.base.Player.win_position_distribution
    poker.base.Player.win_hand_distribution
    poker.base.Player.win_card_distribution
    poker.base.Player.reaction

.. _Hand:

Hand
----
Class object used for getting specific hand stats.

.. :currentmodule:: base

.. class:: Hand(hand):

    Calculate stats for a Hand.

    :param hand: A list of strings associated with a hand.
    :type hand: List[str]
    :example: *None*
    :note: This class is intended to be used internally.

.. autosummary::
    poker.base.Hand.parsed_hand
    poker.base.Hand.small_blind
    poker.base.Hand.big_blind
    poker.base.Hand.winner
    poker.base.Hand.winning_cards
    poker.base.Hand.winning_hand
    poker.base.Hand.starting_players
    poker.base.Hand.starting_players_chips
    poker.base.Hand.flop_cards
    poker.base.Hand.turn_card
    poker.base.Hand.river_card
    poker.base.Hand.my_cards

.. _Plot:

Plot Classes
------------
Plot Class objects.

Possible Font Size Strings:
    * 'xx-small'
    * 'x-small'
    * 'small'
    * 'medium'
    * 'large'
    * 'x-large'
    * 'xx-large'

Possible Legend Locations:
    * 'best'
    * 'upper right'
    * 'upper left'
    * 'lower left'
    * 'lower right'
    * 'right'
    * 'center left'
    * 'center right'
    * 'lower center'
    * 'upper center'
    * 'center

.. :currentmodule:: plot

.. class:: Line(data):

    Class for Line plots.

    :param data: Input data.
    :type data: pd.DataFrame
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
    :example:
        .. code-block:: python

            from poker.plot import Line
            Line(data=data,
                 color_lst=['tab:orange', 'tab:blue'],
                 title='Weapon Preference',
                 ylabel='Percent',
                 xlabel='Date')
            plt.show()
        .. image:: https://miro.medium.com/max/700/1*qMtEJwbMB9DpOOUKx5VDtg.png
    :note: *None*

.. autosummary::
    poker.plot.Line.ax

.. class:: Scatter(data):

    Class for Scatter plots.

    :param data: Input data.
    :type data: pd.DataFrame,
    :param limit: Limit the length of data. *Optional*
    :type limit: int
    :param label_lst: List of labels to include, if None will include all columns. *Optional*
    :type label_lst: List[str]
    :param color_lst: List of colors to graph. *Optional*
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
    :param y_limit: If given will limit the y axis, default is None. *Optional*
    :type y_limit: float
    :example:
        .. code-block:: python

            from poker.plot import Scatter
            Scatter(data=data,
                     compare_two=['teamSurvivalTime', 'placementPercent'],
                     normalize_x=['teamSurvivalTime'],
                     color_lst=['tab:orange'],
                     regression_line=['placementPercent'],
                     regression_line_color='tab:blue',
                     title='Team Survival Time vs Placement Percent',
                     ylabel='Placement Percent',
                     xlabel='Team Survival Time (seconds)')
             plt.show()
        .. image:: https://miro.medium.com/max/700/1*w0T6lztljOKIAFbeSR3ayQ.png
    :note: Slope of the regression line is noted in he legend.

.. autosummary::
    poker.plot.Scatter.ax

.. class:: Histogram(data):

    Class for Histogram plots.

    :param data: Input data.
    :type data: pd.DataFrame,
    :param limit: Limit the length of data. *Optional*
    :type limit: int
    :param label_lst: List of labels to include, if None will include all columns. *Optional*
    :type label_lst: List[str]
    :param color_lst: List of colors to graph. *Optional*
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
    :example:
        .. code-block:: python

            from poker.plot import Histogram
            Histogram(data=data,
                      label_lst=['kills_log'],
                      include_norm='kills_log',
                      title='Kills Histogram')
            plt.show()
        .. image:: https://miro.medium.com/max/700/1*gzO4N258m-0pEb-5pmaKFA.png
    :note: *None*

.. autosummary::
    poker.plot.Histogram.ax
