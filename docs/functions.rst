.. _Functions:

Functions
*********
.. meta::
   :description: Landing page for poker-now-analysis.
   :keywords: Poker, Python, Analysis, Texas Hold'em

This chapter documents the Functions used in this package.

.. _Analysis:

Analysis
--------
One off functions for various analysis.

.. :currentmodule:: analysis

.. function:: face_card_in_winning_cards(hands):

    Find what percent of the time a face card is used to win.

    :param hands: Input data.
    :type hands: List[Hand] or Game
    :return: A percent.
    :rtype: float
    :example: *None*
    :note: *None*

.. function:: longest_streak(data):

    Find the longest winning streak.

    :param data: Input data.
    :type data: Player, pd.DataFrame, pd.Series, or np.ndarray
    :return: Longest streak.
    :rtype: int
    :example: *None*
    :note: *None*

.. function:: raise_signal_winning(data, player_index):

    When a player raises, does that mean they are going to win(?).

    :param data: Input data.
    :type data: Game
    :param player_index: ID of specific player, default is None. *Optional*
    :type player_index: str
    :return: A pd.DataFrame with the count and percent related to each position.
    :rtype: pd.DataFrame
    :example: *None*
    :note: *None*

.. function:: small_or_big_blind_win(data, player_index):

    When a player is small or big blind, does that mean they are going to win(?).

    :param data: Input data.
    :type data: Game
    :param player_index: ID of specific player, default is None. *Optional*
    :type player_index: str
    :return: A pd.DataFrame with the count and percent related to each blind.
    :rtype: pd.DataFrame
    :example: *None*
    :note: *None*

.. function:: best_cards(data, player_index):

    Find the most common winning cards and respective money earned.

    :param data: Input data.
    :type data: Game
    :param player_index: ID of a specific player or players, default is None. *Optional*
    :type player_index: str or List[str]
    :return: A pd.DataFrame with the count and money earned related to each blind.
    :rtype: pd.DataFrame
    :example: *None*
    :note: *None*

.. function:: player_verse_player_reaction(data):

    Find how many times and what value a player called or folded related to each player.

    :param data: Input data.
    :type data: Game
    :return: A dict of counts and values for each call and fold.
    :rtype: dict
    :example: *None*
    :note: *None*

.. _Base:

Base
----
One off functions for helping analysis.

.. :currentmodule:: base

.. function:: normalize(data):

    Normalize an np.ndarray, pd.Series, or list between 0 and 1.

    :param data: Input data to normalize.
    :type data: np.ndarray, pd.Series, or list
    :return: Normalized np.ndarray, pd.Series, or list.
    :rtype: np.ndarray, pd.Series, or list
    :example: *None*
    :note: Maintains the input data type in output.

.. function:: running_mean(data, num):

    Calculate the running mean on *num* interval

    :param data: Input data.
    :type data: np.ndarray, pd.Series, or list
    :param num: Input val used for running mean.
    :type num: int
    :return: Running mean for a given  np.ndarray, pd.Series, or list.
    :rtype: np.ndarray, pd.Series, or list
    :example: *None*
    :note: Maintains the input data type in output.

.. function:: cumulative_mean(data):

    Calculate the cumulative mean.

    :param data: Input data.
    :type data: np.ndarray, pd.Series, or list
    :return: Cumulative mean for a given np.ndarray, pd.Series, or list.
    :rtype: np.ndarray, pd.Series, or list
    :example: *None*
    :note: Maintains the input data type in output.

.. function:: round_to(data, val, remainder):

    Rounds an np.array, pd.Series, or list of values to the nearest value.

    :param data: Input data.
    :type data: np.ndarray, pd.Series, or list
    :param val: Value to round to. If decimal, will be that number divided by.
    :type val: int
    :param remainder: If True, will round the decimal, default is False. *Optional*
    :type remainder: bool
    :return: Rounded number.
    :rtype: np.ndarray, pd.Series or list
    :example:
        .. code-block:: python

            # With remainder set to True.
            lst = [4.3, 5.6]
            round_to(data=lst, val=4, remainder=True) # [4.25, 5.5]

            # With remainder set to False.
            lst = [4.3, 5.6]
            round_to(data=lst, val=4, remainder=False) # [4, 4]
    :note: Maintains the input data type in output.

.. function:: search_dic_values(dic, item):

    Searches a dict using the values.

    :param dic: Input data.
    :type dic: dict
    :param item: Search item.
    :type item: str, float or int
    :return: Key value connected to the value.
    :rtype: str, float or int
    :example: *None*
    :note: *None*
