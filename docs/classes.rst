.. raw:: html

    <style> .lbi {color:#2980b9; font-weight:400; font-style: italic; font-size:100%; max-width: 100%; font-family: SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,Courier,monospace;} </style>
    <style> .lb {color:#2980b9; font-weight:400; font-size:100%; max-width: 100%; font-family: SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,Courier,monospace;} </style>
    <style> .grey {color:#404040; font-weight:700; font-size:16px; padding: 6px; background:#edf0f2; border-top: 1px solid grey} </style>
    <style> .attribute_table_description {font-family: Lato,proxima-nova,Helvetica Neue,Arial,sans-serif; font-weight: 400; color: #404040; min-height: 100%;} </style>
    <style> .attribute_table_header {font-family: Lato,proxima-nova,Helvetica Neue,Arial,sans-serif; font-weight: 700; color: #404040; min-height: 100%; font-size: 16px} </style>
    <style> .rb {color:#e74c3c; font-size:90%; font-weight:700; background-color:white; padding: 2px 5px; border: 1px solid #e1e4e5; white-space: nowrap; max-width: 100%; overflow-x: auto; font-family: SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,Courier,monospace;} </style>
    <style> .bb {color: #000; font-size:90%; font-weight:700; background-color:white; padding: 2px 5px; border: 1px solid #e1e4e5; white-space: nowrap; max-width: 100%; overflow-x: auto; font-family: SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,Courier,monospace;} </style>

.. role:: grey
.. role:: bb
.. role:: rb
.. role:: lbi
.. role:: attribute_table_description
.. role:: attribute_table_header

.. _Classes:

*******
Classes
*******
.. meta::
   :description: Landing page for poker-now-analysis.
   :keywords: Poker, Python, Analysis, Texas Hold'em

This chapter documents the Classes used in this package.

.. _Poker:

=====
Poker
=====
Class object for running the package.

.. :currentmodule:: poker_class

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

:grey:`Poker Attributes:`

.. list-table::
    :widths: 100 50 200
    :header-rows: 1

    * - :attribute_table_header:`Name`
      - :attribute_table_header:`Type`
      - :attribute_table_header:`Description`
    * - :bb:`Poker.files`
      - :lbi:`List[str]`
      - :attribute_table_description:`Returns list of data files`
    * - :bb:`Poker.matches`
      - :lbi:`dict`
      - :attribute_table_description:`Returns list of data files`
    * - :bb:`Poker.players_money_overview`
      - :lbi:`pd.DataFrame`
      - :attribute_table_description:`Returns summary info for each player across games`
    * - :bb:`Poker.card_distribution`
      - :lbi:`pd.DataFrame`
      - :attribute_table_description:`Returns count and percent for each card that showed up across games`
    * - :bb:`Poker.winning_hand_distribution`
      - :lbi:`pd.DataFrame`
      - :attribute_table_description:`Returns count and percent of each type of winning hand across games`
    * - :bb:`Poker.players_history`
      - :lbi:`dict`
      - :attribute_table_description:`Collects player stats for all matches and groups based on grouper input`

.. _DocumentFilter:

==============
DocumentFilter
==============

Class for getting data from Poker.

The **class_lst** can have any of the following:
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

The **position_lst** can have any of the following:
    * 'Pre Flop'
    * 'Post Flop'
    * 'Post Turn'
    * 'Post River'

The **win_loss_all** can be one of the following:
    * 'Win'
    * 'Loss'
    * 'All'

The **column_lst** can have any of the following:
    * 'All In'
    * 'Bet Amount'
    * 'Class'
    * 'End Time'
    * 'From Person'
    * 'Game Id'
    * 'Player Current Chips'
    * 'Player Index'
    * 'Player Name'
    * 'Player Starting Chips'
    * 'Position'
    * 'Pot Size'
    * 'Previous Time'
    * 'Remaining Players'
    * 'Round'
    * 'Start Time'
    * 'Time'
    * 'Win'
    * 'Win Hand'
    * 'Win Stack'
    * 'Winner'

.. :currentmodule:: document_filter_class

.. class:: DocumentFilter(data):

    Get a selection from the Poker Object.
    Uses a set of filters to return a desired set of data to be used in later analysis.

    :param data: Input Poker object to be filtered.
    :type data: Poker
    :param game_id_lst: Game Id filter, default is None. *Optional*
    :type game_id_lst: Union[List[str], str, None]
    :param player_index_lst: Player Index filter, default is None. *Optional*
    :type player_index_lst: Union[List[str], str, None]
    :param player_name_lst: Player Name filter, default is None. *Optional*
    :type player_name_lst: Union[List[str], str, None]
    :param class_lst: Filter by class objects, default is None. *Optional*
    :type class_lst: Union[List[str], str, None]
    :param position_lst: Filter by position, default is None. *Optional*
    :type position_lst: Union[List[str], str, None]
    :param win_loss_all: Filter by Win, Loss or All, default is None. *Optional*
    :type win_loss_all: Union[str, None]
    :param column_lst: Filter by column name, default is None. *Optional*
    :type column_lst: Union[List[str], str, None]
    :example: *None*
    :note: All inputs, except data, are *Optional* and defaults are set to None.
        Any str inputs are placed in a list.

:grey:`DocumentFilter Attributes:`

.. list-table::
    :widths: 100 50 200
    :header-rows: 1

    * - :attribute_table_header:`Name`
      - :attribute_table_header:`Type`
      - :attribute_table_header:`Description`
    * - :bb:`DocumentFilter.df`
      - :lbi:`pd.DataFrame`
      - :attribute_table_description:`Returns a DataFrame of requested items`
    * - :bb:`DocumentFilter.game_id_lst`
      - :lbi:`Union[List[str], None]`
      - :attribute_table_description:`Returns game id input`
    * - :bb:`DocumentFilter.player_index_lst`
      - :lbi:`Union[List[str], None]`
      - :attribute_table_description:`Returns player index input`
    * - :bb:`DocumentFilter.player_name_lst`
      - :lbi:`Union[List[str], None]`
      - :attribute_table_description:`Returns player name input`
    * - :bb:`DocumentFilter.class_lst`
      - :lbi:`Union[List[str], None]`
      - :attribute_table_description:`Returns class input`
    * - :bb:`DocumentFilter.position_lst`
      - :lbi:`Union[List[str], None]`
      - :attribute_table_description:`Returns position input`
    * - :bb:`DocumentFilter.win_loss_all`
      - :lbi:`Union[List[str], None]`
      - :attribute_table_description:`Returns win loss or all input`
    * - :bb:`DocumentFilter.column_lst`
      - :lbi:`Union[List[str], None]`
      - :attribute_table_description:`Returns column input`

.. _Game:

====
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

:grey:`Game Attributes:`

.. list-table::
    :widths: 100 50 200
    :header-rows: 1

    * - :attribute_table_header:`Name`
      - :attribute_table_header:`Type`
      - :attribute_table_header:`Description`
    * - :bb:`Game.file_name`
      - :lbi:`str`
      - :attribute_table_description:`Returns name of data file`
    * - :bb:`Game.hands_lst`
      - :lbi:`List[Hand]`
      - :attribute_table_description:`Returns list of hands in the game`
    * - :bb:`Game.card_distribution`
      - :lbi:`dict`
      - :attribute_table_description:`Returns count of each card that showed up`
    * - :bb:`Game.winning_hand_distribution`
      - :lbi:`dict`
      - :attribute_table_description:`Returns count of winning hands`
    * - :bb:`Game.players_data`
      - :lbi:`dict`
      - :attribute_table_description:`Returns Player stats for players across hands`
    * - :bb:`Game.game_stats`
      - :lbi:`dict`
      - :attribute_table_description:`Returns Mean stats for Game across hands`

.. _Player:

======
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

:grey:`Player Attributes:`

.. list-table::
    :widths: 100 50 200
    :header-rows: 1

    * - :attribute_table_header:`Name`
      - :attribute_table_header:`Type`
      - :attribute_table_header:`Description`
    * - :bb:`Player.win_percent`
      - :lbi:`dict`
      - :attribute_table_description:`Returns player win percent`
    * - :bb:`Player.win_count`
      - :lbi:`dict`
      - :attribute_table_description:`Returns player win count`
    * - :bb:`Player.largest_win`
      - :lbi:`dict`
      - :attribute_table_description:`Returns players largest win`
    * - :bb:`Player.largest_loss`
      - :lbi:`dict`
      - :attribute_table_description:`Returns players largest loss`
    * - :bb:`Player.hand_count`
      - :lbi:`dict`
      - :attribute_table_description:`Returns total hand count when player involved`
    * - :bb:`Player.all_in`
      - :lbi:`dict`
      - :attribute_table_description:`Returns a dict documenting when the player went all in`
    * - :bb:`Player.player_index`
      - :lbi:`List[str]`
      - :attribute_table_description:`Returns player index or indexes`
    * - :bb:`Player.player_name`
      - :lbi:`List[str]`
      - :attribute_table_description:`Returns player name or names`
    * - :bb:`Player.player_money_info`
      - :lbi:`dict`
      - :attribute_table_description:`Returns a dict of DataFrames documenting player buy-in and loss counts`
    * - :bb:`Player.hand_dic`
      - :lbi:`dict`
      - :attribute_table_description:`Returns a dict of DataFrames documenting hands when the player won`
    * - :bb:`Player.card_dic`
      - :lbi:`dict`
      - :attribute_table_description:`Returns a dict of DataFrames documenting card appearances`
    * - :bb:`Player.line_dic`
      - :lbi:`dict`
      - :attribute_table_description:`Returns a dict with a list of objects where player involved`
    * - :bb:`Player.moves_dic`
      - :lbi:`dict`
      - :attribute_table_description:`Returns a players moves on the table`
    * - :bb:`Player.merged_moves`
      - :lbi:`dict`
      - :attribute_table_description:`Returns a combined dict of player moves`

.. _Hand:

====
Hand
====
Class object used for getting specific hand stats.

.. :currentmodule:: hand_class

.. class:: Hand(lst_hand_objects, file_id, player_dic):

    Organizes a hand with a class and adds the stands to the player_dic.

    :param lst_hand_objects: A list of Class Objects connected to a hand.
    :type lst_hand_objects: list
    :param file_id: Unique file name.
    :type file_id: str
    :param player_dic: Dict of players.
    :type player_dic: dict
    :example: *None*
    :note: This class is intended to be used internally.

:grey:`Hand Attributes:`

.. list-table::
    :widths: 100 50 200
    :header-rows: 1

    * - :attribute_table_header:`Name`
      - :attribute_table_header:`Type`
      - :attribute_table_header:`Description`
    * - :bb:`Hand.merged_moves`
      - :lbi:`list`
      - :attribute_table_description:`Returns a list of actions as objects`
    * - :bb:`Hand.small_blind`
      - :lbi:`SmallBlind`
      - :attribute_table_description:`Returns SmallBlind Class`
    * - :bb:`Hand.big_blind`
      - :lbi:`BigBlind`
      - :attribute_table_description:`Returns BigBlind Class`
    * - :bb:`Hand.winner`
      - :lbi:`Wins`
      - :attribute_table_description:`Returns Wins Class or list of Wins Classes`
    * - :bb:`Hand.starting_players`
      - :lbi:`dict`
      - :attribute_table_description:`Returns dict of name and ID for each player that was present at the hand start`
    * - :bb:`Hand.starting_players_chips`
      - :lbi:`dict`
      - :attribute_table_description:`Returns dict of name and stack amount for each player that was present at the hand start`
    * - :bb:`Hand.flop_cards`
      - :lbi:`Flop`
      - :attribute_table_description:`Returns Flop Class`
    * - :bb:`Hand.turn_card`
      - :lbi:`Turn`
      - :attribute_table_description:`Returns Turn Class`
    * - :bb:`Hand.river_card`
      - :lbi:`River`
      - :attribute_table_description:`Returns River Class`
    * - :bb:`Hand.my_cards`
      - :lbi:`MyCards`
      - :attribute_table_description:`Returns MyCards Class`
    * - :bb:`Hand.chips_on_board`
      - :lbi:`int`
      - :attribute_table_description:`Returns the count of chips on the table`
    * - :bb:`Hand.gini_coef`
      - :lbi:`float`
      - :attribute_table_description:`Returns the gini coef for the board`
    * - :bb:`Hand.pot_size_lst`
      - :lbi:`List[int]`
      - :attribute_table_description:`Returns pot size over course of hand`
    * - :bb:`Hand.players`
      - :lbi:`dict`
      - :attribute_table_description:`Returns dict of player moves`
    * - :bb:`Hand.start_time`
      - :lbi:`TimeStamp`
      - :attribute_table_description:`Returns time of first hand item`
    * - :bb:`Hand.end_time`
      - :lbi:`TimeStamp`
      - :attribute_table_description:`Returns time of last hand item`
    * - :bb:`Hand.win_stack`
      - :lbi:`Union[int, None]`
      - :attribute_table_description:`Returns win amount for the hand`
    * - :bb:`Hand.bet_lst`
      - :lbi:`List[int]`
      - :attribute_table_description:`Returns Raise amounts for the hand`

.. _Processor:

=========
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
    :note: This class is intended to be used internally. All values are set to None or 0 by default.

:grey:`LineAttributes Attributes:`

.. list-table::
    :widths: 100 50 200
    :header-rows: 1

    * - :attribute_table_header:`Name`
      - :attribute_table_header:`Type`
      - :attribute_table_header:`Description`
    * - :bb:`LineAttributes.text`
      - :lbi:`Union[str, None]`
      - :attribute_table_description:`Text input`
    * - :bb:`LineAttributes.player_name`
      - :lbi:`Union[str, None]`
      - :attribute_table_description:`Player Name`
    * - :bb:`LineAttributes.player_index`
      - :lbi:`Union[str, None]`
      - :attribute_table_description:`Player Id`
    * - :bb:`LineAttributes.stack`
      - :lbi:`Union[int, None]`
      - :attribute_table_description:`Amount offered to the table`
    * - :bb:`LineAttributes.position`
      - :lbi:`Union[str, None]`
      - :attribute_table_description:`Position of move in relation to table cards being drawn`
    * - :bb:`LineAttributes.winning_hand`
      - :lbi:`Union[str, None]`
      - :attribute_table_description:`Winning hand`
    * - :bb:`LineAttributes.cards`
      - :lbi:`Union[str, tuple, None]`
      - :attribute_table_description:`Card or cards`
    * - :bb:`LineAttributes.current_round`
      - :lbi:`Union[int, None]`
      - :attribute_table_description:`Round number within the game`
    * - :bb:`LineAttributes.pot_size`
      - :lbi:`Union[int, None]`
      - :attribute_table_description:`Size of pot when move happens`
    * - :bb:`LineAttributes.remaining_players`
      - :lbi:`Union[List[str], None]`
      - :attribute_table_description:`Players left in hand`
    * - :bb:`LineAttributes.action_from_player`
      - :lbi:`Union[str, None]`
      - :attribute_table_description:`Who bet previously`
    * - :bb:`LineAttributes.action_amount`
      - :lbi:`Union[int, None]`
      - :attribute_table_description:`Previous bet amount`
    * - :bb:`LineAttributes.all_in`
      - :lbi:`Union[bool, None]`
      - :attribute_table_description:`Notes if player when all-in`
    * - :bb:`LineAttributes.game_id`
      - :lbi:`Union[str, None]`
      - :attribute_table_description:`File name`
    * - :bb:`LineAttributes.starting_chips`
      - :lbi:`Union[int, None]`
      - :attribute_table_description:`Player's chip count at start of hand`
    * - :bb:`LineAttributes.current_chips`
      - :lbi:`Union[int, None]`
      - :attribute_table_description:`Player's chip count at time of move`
    * - :bb:`LineAttributes.winner`
      - :lbi:`Union[str, None]`
      - :attribute_table_description:`Player Name who wins the hand`
    * - :bb:`LineAttributes.win_stack`
      - :lbi:`Union[int, None]`
      - :attribute_table_description:`Amount won at end of hand`
    * - :bb:`LineAttributes.time`
      - :lbi:`TimeStamp`
      - :attribute_table_description:`Timestamp of action`
    * - :bb:`LineAttributes.previous_time`
      - :lbi:`TimeStamp`
      - :attribute_table_description:`Timestamp of previous action`
    * - :bb:`LineAttributes.start_time`
      - :lbi:`TimeStamp`
      - :attribute_table_description:`Timestamp of the start of the hand`
    * - :bb:`LineAttributes.end_time`
      - :lbi:`TimeStamp`
      - :attribute_table_description:`Timestamp of the end of the hand`

.. _Plot:

============
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

""""
Line
""""
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

:grey:`Line Attributes:`

.. list-table::
    :widths: 100 50 200
    :header-rows: 1

    * - :attribute_table_header:`Name`
      - :attribute_table_header:`Type`
      - :attribute_table_header:`Description`
    * - :bb:`Line.ax`
      - :lbi:`plt`
      - :attribute_table_description:`Returns a Line Plot`

"""""""
Scatter
"""""""
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

:grey:`Scatter Attributes:`

.. list-table::
    :widths: 100 50 200
    :header-rows: 1

    * - :attribute_table_header:`Name`
      - :attribute_table_header:`Type`
      - :attribute_table_header:`Description`
    * - :bb:`Scatter.ax`
      - :lbi:`plt`
      - :attribute_table_description:`Returns a Scatter Plot`

"""""""""
Histogram
"""""""""
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

:grey:`Histogram Attributes:`

.. list-table::
    :widths: 100 50 200
    :header-rows: 1

    * - :attribute_table_header:`Name`
      - :attribute_table_header:`Type`
      - :attribute_table_header:`Description`
    * - :bb:`Histogram.ax`
      - :lbi:`plt`
      - :attribute_table_description:`Returns a Histogram Plot`
