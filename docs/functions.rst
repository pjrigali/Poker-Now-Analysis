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
Almost all Analysis functions take either a Game or Player Class Object.

.. :currentmodule:: analysis

.. function:: face_card_in_winning_cards(data):

    Find what percent of the time a face card is used to win.

    :param data: Input data.
    :type data: Union[Game or Player]
    :return: A dict of file_id and face card in winning hand percent.
    :rtype: dict
    :example: *None*
    :note: Percent of all Winning Cards = Total all cards and get percent that include a face card.
        Percent one face in Winning Cards = Percent of all wins hand at least a single face card.

.. function:: longest_streak(data):

    Find the longest winning streak.

    :param data: Input data.
    :type data: Union[Game, Player]
    :return: Longest streak.
    :rtype: dict
    :example: *None*
    :note: *None*

.. function:: raise_signal_winning(data):

    When a player raises, does that mean they are going to win(?).

    :param data: Input data.
    :type data: Union[Game, Player]
    :return: A pd.DataFrame with the percent related to each position.
    :rtype: pd.DataFrame
    :example: *None*
    :note: *None*

.. function:: small_or_big_blind_win(data):

    When a player is small or big blind, does that mean they are going to win(?).

    :param data: Input data.
    :type data: Union[Game, Player]
    :return: A pd.DataFrame with the percent related to each blind.
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

.. function:: player_verse_player(data):

    Find how many times and what value a player called or folded related all other players.

    :param data: Input data.
    :type data: Union[Game, Player]
    :return: A dict of counts and values for each 'Calls', 'Raises', 'Checks', and 'Folds'.
    :rtype: dict
    :example: *None*
    :note: *None*

.. function:: bluff_study(data):

    Compare betting habits when a player is bluffing.

    :param data: Input data.
    :type data: Player
    :return: A dict of counts and values for each position.
    :rtype: dict
    :example: *None*
    :note: Bluff Count Raises and Calls = Average and std count per position when bluffing.
        Bluff Stack = Average and std value per position when bluffing.
        Bluff Stack Raises and Calls = Average and std value for Raises and Calls when bluffing.
        Both = Average and std when they win and loss.
        Loss = Average and std when they loss.
        Win = Average and std when they Win.

.. function:: staticanalysis(data):

    Build a static analysis DataFrame.

    :param data: A Player class object.
    :type data: Player or Dict
    :return: A DataFrame of mean and std values.
    :rtype: pd.DataFrame
    :example: *None*
    :note: If a dict is passed it is intended to be Player.move_dic.

.. function:: tsanalysis(data):

    Build a Time Series DataFrame.

    :param data: A Player class object.
    :type data: Player or Dict
    :return: A DataFrame of various moves over time.
    :rtype: pd.DataFrame
    :example: *None*
    :note: If a dict is passed it is intended to be Player.move_dic.

.. _Base:

Base
----
One off functions for helping analysis.
These are helper functions that were constructed to limit the reliance on other packages.
Most take a list, np.ndarray, or pd.Series and return a list of floats or ints.

.. :currentmodule:: base

.. function:: normalize(data, keep_nan):

    Normalize a list between 0 and 1.

    :param data: Input data to normalize.
    :type data: list, np.ndarray, or pd.Series
    :param keep_nan: If True, will maintain nan values, default is False. *Optional*
    :type keep_nan: bool
    :return: Normalized list.
    :rtype: list
    :example:
        .. code-block:: python

            from poker.base import normalize
            data = [1, 2, 3, None, np.nan, 4]
            # keep_nan set to False (default)
            test = normalize(data, keep_nan=False) # [0.0, 0.3333333333333333, 0.6666666666666666, 1.0]
            # keep_nan set to True
            test = normalize(data, keep_nan=False) # [0.0, 0.3333333333333333, 0.6666666666666666, nan, nan, 1.0]
    :note: If an int or float is passed for keep_nan, that value will be placed where nan's are present.

.. function:: running_mean(data, num):

    Calculate the Running Std on *num* interval.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :param num: Input val used for Running Std window.
    :type num: int
    :return: Running mean for a given  np.ndarray, pd.Series, or list.
    :rtype: List[float]
    :example:
        .. code-block:: python

            from poker.base import running_mean
            data = [1, 2, 3, None, np.nan, 4]
            test = running_mean(data=data, num=2) # [1.5, 1.5, 1.5, 2.5, 2.75, 2.5]
    :note: None and np.nan values are replaced with the mean value.

.. function:: running_std(data, num):

    Calculate the Running Std on *num* interval.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :param num: Input val used for Running Std window.
    :type num: int
    :return: Running mean for a given  np.ndarray, pd.Series, or list.
    :rtype: List[float]
    :example:
        .. code-block:: python

            from poker.base import running_std
            data = [1, 2, 3, None, np.nan, 4]
            test = running_std(data=data, num=2) # [0.7071067811865476, 0.7071067811865476, 0.7071067811865476,
                                                 #  0.7071067811865476, 0.3535533905932738, 0.0]
    :note: None and np.nan values are replaced with the mean value.

.. function:: cumulative_mean(data):

    Calculate the Cumulative Mean.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :return: Cumulative mean for a given np.ndarray, pd.Series, or list.
    :rtype: List[float]
    :example:
        .. code-block:: python

            from poker.base import cumulative_mean
            data = [1, 2, 3, None, np.nan, 4]
            test = cumulative_mean(data=data) # [0.0, 1.0, 1.5, 2.0, 2.125, 2.2]
    :note: None and np.nan values are replaced with the mean value.

.. function:: round_to(data, val, remainder):

    Rounds an np.array, pd.Series, or list of values to the nearest value.

    :param data: Input data.
    :type data: list, np.ndarray, pd.Series, int, float, or any of the numpy int/float variations
    :param val: Value to round to. If decimal, will be that number divided by.
    :type val: int
    :param remainder: If True, will round the decimal, default is False. *Optional*
    :type remainder: bool
    :return: Rounded number.
    :rtype: List[float] or float
    :example:
        .. code-block:: python

            # With remainder set to True.
            lst = [4.3, 5.6]
            round_to(data=lst, val=4, remainder=True) # [4.25, 5.5]

            # With remainder set to False.
            lst = [4.3, 5.6]
            round_to(data=lst, val=4, remainder=False) # [4, 4]
    :note: Single int or float values can be passed.

.. function:: calc_gini(data):

    Calculate the Gini Coef for a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :return: Gini value.
    :rtype: float
    :example:
        >>> lst = [4.3, 5.6]
        >>> calc_gini(data=lst, val=4, remainder=True) # 0.05445544554455435
    :note: The larger the gini coef, the more consolidated the chips on the table are to one person.

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

.. function:: flatten(data, type_used):

    Flattens a list of lists and checks the list.

    :param data: Input data.
    :type data: list
    :param type_used: Type to search for, default is "str". *Optional*
    :type type_used: str
    :param type_used: Either {str, int, or float}
    :type type_used: str
    :return: Returns a flattened list.
    :rtype: list
    :example: *None*
    :note: Will work when lists are mixed with non-list items.

.. function:: native_mode(data):

    Calculate Mode of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :return: Returns the Mode.
    :rtype: float
    :example: *None*
    :note: *None*

.. function:: native_median(data):

    Calculate Median of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :return: Returns the Median.
    :rtype: float
    :example: *None*
    :note: If multiple values have the same count, will return the mean.
        Median is used if there is an odd number of same count values.

.. function:: native_mean(data):

    Calculate Mean of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :return: Returns the mean.
    :rtype: float
    :example: *None*
    :note: *None*

.. function:: native_std(data, ddof):

    Calculate Variance of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :param ddof: Set the degrees of freedom, default is 1. *Optional*
    :type ddof: int
    :return: Returns the Variance.
    :rtype: float
    :example: *None*
    :note: *None*

.. function:: native_variance(data, ddof):

    Calculate Standard Deviation of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :param ddof: Set the degrees of freedom, default is 1. *Optional*
    :type ddof: int
    :return: Returns the Standard Deviation.
    :rtype: float
    :example: *None*
    :note: *None*

.. function:: native_sum(data):

    Calculate Sum of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :return: Returns the Sum.
    :rtype: float
    :example: *None*
    :note: *None*

.. function:: native_max(data):

    Calculate Max of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :return: Returns the Max.
    :rtype: float
    :example: *None*
    :note: *None*

.. function:: unique_values(data, count):

    Get Unique values from a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :param count: Return a dictionary with item and count, default is False. *Optional*
    :type count: bool
    :return: Returns either a list of unique values or a dict of unique values with counts.
    :rtype: Union[list, dict]
    :example:
        .. code-block:: python

            from poker.base import unique_values
            data = [1, 2, 3, None, np.nan, 4]
            # count set to False (default)
            test = normalize(data, keep_nan=False) # [1, 2, 3, 4]
            # count set to True
            test = normalize(data, keep_nan=False) # {1: 1, 2: 1, 3: 1, 4: 1}
    :note: *None*

