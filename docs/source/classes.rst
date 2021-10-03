.. _Classes:

Classes
*******
.. meta::
   :description: Landing page for poker-now-analysis.
   :keywords: Poker, Python, Analysis, Texas Hold'em

This chapter documents the Classes used in this package.

.. _Poker:

Poker
=====
Class object for running the package.

.. :currentmodule:: poker.poker_class

.. class:: Poker(repo_location, grouped, money_multi):

    Calculate stats for all games and players.

    :param repo_location: Location of data folder.
    :type repo_location: str
    :param grouped: List of lists, filled with unique player Ids that are related to the same person. *Optional*
    :type grouped: str
    :param money_multi: Multiple to divide the money amounts to translate them to dollars *Optional*
    :type money_multi: int
    :example:
        .. code-block:: python

            from poker.poker_class import Poker
            repo = 'location of your previous game'
            grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
                        ['48QVRRsiae', 'u8_FUbXpAz']]
            poker = Poker(repo_location=repo, grouped=grouped)
    :note: Grouped will need to be figured out by the player.
        The grouped stats are only taken into account within this class

.. autosummary::
    poker.poker_class.Poker.files
    poker.poker_class.Poker.matches
    poker.poker_class.Poker.players_money_overview
    poker.poker_class.Poker.card_distribution
    poker.poker_class.Poker.winning_hand_distribution
    poker.poker_class.Poker.players_history

.. _Game:

Game
====
Class object used for getting specific game stats.

.. :currentmodule:: game_class

.. class:: Game(hand_lst, file_id, players_data):

    Calculate stats for a game.

    :param hand_lst: List of dict's from the csv.
    :type hand_lst: List[dict]
    :param file_id: Name of file.
    :type file_id: str
    :param players_data: A dict of player data.
    :type players_data: dict
    :example: *None*
    :note: This class is intended to be used internally.

.. autosummary::
    poker.game_class.Game.file_name
    poker.game_class.Game.hands_lst
    poker.game_class.Game.card_distribution
    poker.game_class.Game.winning_hand_distribution
    poker.game_class.Game.players_data
    poker.game_class.Game.game_stats

.. _Player:

Player
======
Class object used for getting specific player stats.

.. :currentmodule:: player_class

.. class:: Player(player_index):

    Calculate stats for a player.

    :param player_index: A unique player ID.
    :type player_index: str or List[str]
    :example: *None*
    :note: This class is intended to be used internally.

.. autosummary::
    poker.player_class.Player.win_percent
    poker.player_class.Player.win_count
    poker.player_class.Player.largest_win
    poker.player_class.Player.largest_loss
    poker.player_class.Player.hand_count
    poker.player_class.Player.all_in
    poker.player_class.Player.player_index
    poker.player_class.Player.player_name
    poker.player_class.Player.player_money_info
    poker.player_class.Player.hand_dic
    poker.player_class.Player.card_dic
    poker.player_class.Player.line_dic
    poker.player_class.Player.moves_dic
    poker.player_class.Player.merged_moves

.. _Hand:

Hand
====
Class object used for getting specific hand stats.

.. :currentmodule:: hand_class

.. class:: Hand(hand):

    Organizes a hand with a class and adds the stands to the player_dic.

    :param lst_hand_objects: A list of Class Objects connected to a hand.
    :type lst_hand_objects: list
    :param file_id: Unique file name.
    :type file_id: str
    :param player_dic: Dict of players.
    :type player_dic: dict
    :example: *None*
    :note: This class is intended to be used internally.

.. autosummary::
    poker.hand_class.Hand.parsed_hand
    poker.hand_class.Hand.small_blind
    poker.hand_class.Hand.big_blind
    poker.hand_class.Hand.winner
    poker.hand_class.Hand.starting_players
    poker.hand_class.Hand.starting_players_chips
    poker.hand_class.Hand.flop_cards
    poker.hand_class.Hand.turn_card
    poker.hand_class.Hand.river_card
    poker.hand_class.Hand.my_cards
    poker.hand_class.Hand.chips_on_board
    poker.hand_class.Hand.gini_coef
    poker.hand_class.Hand.pot_size_lst
    poker.hand_class.Hand.players
    poker.hand_class.Hand.start_time
    poker.hand_class.Hand.end_time
    poker.hand_class.Hand.win_stack
    poker.hand_class.Hand.bet_lst

.. _Processor:

Processor
=========
Class object for holding information from lines.

The following child classes use this framework:
    * Requests
    * Approved
    * Joined
    * MyCards
    * SmallBlind
    * BigBlind
    * Folds
    * Calls
    * Raises
    * Checks
    * Wins
    * Shows
    * Quits
    * Flop
    * Turn
    * River
    * Undealt
    * StandsUp
    * SitsIn
    * PlayerStacks

.. :currentmodule:: processor

.. class:: LineAttributes:

    Applies attributes to a respective Class object.

    :param text: A line of text from the data.
    :type text: str
    :example: *None*
    :note: This class is intended to be used internally.

.. autosummary::

    poker.processor.LineAttributes.text
    poker.processor.LineAttributes.player_name
    poker.processor.LineAttributes.player_index
    poker.processor.LineAttributes.stack
    poker.processor.LineAttributes.position
    poker.processor.LineAttributes.winning_hand
    poker.processor.LineAttributes.cards
    poker.processor.LineAttributes.current_round
    poker.processor.LineAttributes.pot_size
    poker.processor.LineAttributes.remaining_players
    poker.processor.LineAttributes.action_from_player
    poker.processor.LineAttributes.action_amount
    poker.processor.LineAttributes.all_in
    poker.processor.LineAttributes.game_id
    poker.processor.LineAttributes.winner
    poker.processor.LineAttributes.win_stack
    poker.processor.LineAttributes.time
    poker.processor.LineAttributes.previous_time
    poker.processor.LineAttributes.starting_chips
    poker.processor.LineAttributes.current_chips

.. _Plot:

Plot Classes
============
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
    :param corr: Pass two strings to return the correlation. *Optional*
    :type corr: List[str]

    :example:
        .. code-block:: python

            from poker.plot import Line
            Line(data=val[['Pot Size', 'Win Stack']],
                 normalize_x=['Pot Size', 'Win Stack'],
                 color_lst=['tab:orange', 'tab:blue'],
                 title='Pot Size and Winning Stack Amount (Player: ' + key + ')',
                 ylabel='Value',
                 xlabel='Time Periods',
                 corr=['Pot Size', 'Win Stack'])
            plt.show()
        .. image:: https://miro.medium.com/max/700/1*t4UJOrLU5ahOeBmQ-wmkoA.png
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
            Scatter(data=val,
                    compare_two=['Round Seconds', 'Player Reserve'],
                    normalize_x=['Round Seconds', 'Player Reserve'],
                    color_lst=['tab:orange'],
                    regression_line=['Player Reserve'],
                    regression_line_color='tab:blue',
                    title='Time per Hand vs Player Reserve (Player: ' + key + ')',
                    ylabel='Player Chip Count',
                    xlabel='Total Round Seconds')
            plt.show()
        .. image:: https://miro.medium.com/max/1400/1*RIz78uu27Fr5dTf_EHUOnA.png
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
            Histogram(data=val,
                      label_lst=['Move Seconds'],
                      include_norm='Move Seconds',
                      title='Move Second Histogram (Player: ' + key + ')')
            plt.show()
        .. image:: https://miro.medium.com/max/700/1*1oTyksxTA7ZTyG-dJ0XMVw.png
    :note: *None*

.. autosummary::
    poker.plot.Histogram.ax
