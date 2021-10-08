.. _Functions:

*********
Functions
*********
.. meta::
   :description: Landing page for poker-now-analysis.
   :keywords: Poker, Python, Analysis, Texas Hold'em

This chapter documents the Functions used in this package.

.. _Analysis:

========
Analysis
========
One off functions for various analysis.
Almost all Analysis functions take either a Game or Player Class Object.

.. :currentmodule:: analysis

.. function:: face_card_in_winning_cards(data):

    Find what percent of the time a face card is used to win.

    :param data: Input data.
    :type data: DocumentFilter
    :return: A dict of file_id and face card in winning hand percent.
    :rtype: dict
    :example:
        .. code-block:: python

            # This function requires Player Stacks and Wins to be included in the DocumentFilter.
            from poker.poker_class import Poker
            from poker.analysis import face_card_in_winning_cards
            from poker.document_filter_class import DocumentFilter
            repo = 'location of your previous game'
            grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
                        ['48QVRRsiae', 'u8_FUbXpAz']]
            poker = Poker(repo_location=repo, grouped=grouped)
            face_card_in_winning_cards(data=DocumentFilter(data=poker, class_lst=['Player Stacks', 'Wins']))
    :note: Percent of all Winning Cards = Total all cards and get percent that include a face card.
        Percent one face in Winning Cards = Percent of all wins hand at least a single face card.

.. function:: longest_streak(data):

    Find the longest winning streak.

    :param data: Input data.
    :type data: DocumentFilter
    :return: Longest streak.
    :rtype: pd.DataFrame
    :example:
        .. code-block:: python

            # This function requires Wins to be included in the DocumentFilter.
            from poker.poker_class import Poker
            from poker.analysis import longest_streak
            from poker.document_filter_class import DocumentFilter
            repo = 'location of your previous game'
            grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
                        ['48QVRRsiae', 'u8_FUbXpAz']]
            poker = Poker(repo_location=repo, grouped=grouped)
            longest_streak(data=DocumentFilter(data=poker, class_lst=['Wins']))
    :note: DocumentFilter requires class_lst=['Wins']

.. function:: raise_signal_winning(data):

    When a player raises, does that mean they are going to win(?).

    :param data: Input data.
    :type data: DocumentFilter
    :return: A pd.DataFrame with the percent related to each position.
    :rtype: pd.DataFrame
    :example:
        .. code-block:: python

            # This function requires Raises to be included in the DocumentFilter.
            from poker.poker_class import Poker
            from poker.analysis import raise_signal_winning
            from poker.document_filter_class import DocumentFilter
            repo = 'location of your previous game'
            grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
                        ['48QVRRsiae', 'u8_FUbXpAz']]
            poker = Poker(repo_location=repo, grouped=grouped)
            raise_signal_winning(data=DocumentFilter(data=poker, class_lst=['Raises']))
    :note: DocumentFilter requires class_lst=['Raises']

.. function:: small_or_big_blind_win(data):

    When a player is small or big blind, does that mean they are going to win(?).

    :param data: Input data.
    :type data: DocumentFilter
    :return: A pd.DataFrame with the percent related to each blind.
    :rtype: pd.DataFrame
    :example:
        .. code-block:: python

            # This function requires Small Blind and Big Blind to be included in the DocumentFilter.
            from poker.poker_class import Poker
            from poker.analysis import small_or_big_blind_win
            from poker.document_filter_class import DocumentFilter
            repo = 'location of your previous game'
            grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
                        ['48QVRRsiae', 'u8_FUbXpAz']]
            poker = Poker(repo_location=repo, grouped=grouped)
            small_or_big_blind_win(data=DocumentFilter(data=poker, class_lst=['Small Blind', 'Big Blind']))
    :note: DocumentFilter requires class_lst=['Small Blind', 'Big Blind']

.. function:: player_verse_player(data):

    Find how many times and what value a player called or folded related all other players.

    :param data: Input data.
    :type data: DocumentFilter
    :return: A dict of counts and values for each 'Calls', 'Raises', 'Checks', and 'Folds'.
    :rtype: dict
    :example:
        .. code-block:: python

            # This function requires 'Calls', 'Raises', 'Checks', and 'Folds' to be included in the DocumentFilter.
            from poker.poker_class import Poker
            from poker.analysis import player_verse_player
            from poker.document_filter_class import DocumentFilter
            repo = 'location of your previous game'
            grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
                        ['48QVRRsiae', 'u8_FUbXpAz']]
            poker = Poker(repo_location=repo, grouped=grouped)
            player_verse_player(data=DocumentFilter(data=poker, class_lst=['Calls', 'Raises', 'Checks', 'Folds']))
    :note: DocumentFilter requires class_lst=['Calls', 'Raises', 'Checks', 'Folds']

.. function:: bluff_study(data, position_lst):

    Compare betting habits when a player is bluffing.

    :param data: Input data.
    :type data: DocumentFilter
    :param position_lst:
    :type position_lst: Union[List[str], str]
    :return: A pd.DataFrame of counts and values for each position.
    :rtype: pd.DataFrame
    :example:
        .. code-block:: python

            # This function requires a single player_index to be included in the DocumentFilter.
            from poker.poker_class import Poker
            from poker.analysis import bluff_study
            from poker.document_filter_class import DocumentFilter
            repo = 'location of your previous game'
            grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
                        ['48QVRRsiae', 'u8_FUbXpAz']]
            poker = Poker(repo_location=repo, grouped=grouped)
            bluff_study(data=DocumentFilter(data=poker, player_index_lst=['DZy-22KNBS']))
    :note: This function requires a single player_index to be included in the DocumentFilter.

.. function:: static_analysis(data):

    Build a static analysis DataFrame.

    :param data: Input data.
    :type data: DocumentFilter
    :return:  A dict of stats.
    :rtype: dict
    :example:
        .. code-block:: python

            # This function requires a single player_index to be included in the DocumentFilter.
            from poker.poker_class import Poker
            from poker.analysis import static_analysis
            from poker.document_filter_class import DocumentFilter
            repo = 'location of your previous game'
            grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
                        ['48QVRRsiae', 'u8_FUbXpAz']]
            poker = Poker(repo_location=repo, grouped=grouped)
            static_analysis(data=DocumentFilter(data=poker, player_index_lst=['DZy-22KNBS']))
    :note: This function requires a single player_index to be included in the DocumentFilter.

.. function:: pressure_or_hold(data, bet, position):

    Check how a player has responded to a bet in the past.

    :param data: Input data.
    :type data: DocumentFilter
    :paran bet: Proposed bet amount.
    :type bet: int
    :param position: Location in the hand, default is None. *Optional*
    :type position: str
    :return: A dict of Call Counts, Fold Counts, Total Count, and Call Percent.
    :rtype: dict
    :example:
        .. code-block:: python

            # This function requires a single player_index to be included in the DocumentFilter.
            from poker.poker_class import Poker
            from poker.analysis import pressure_or_hold
            from poker.document_filter_class import DocumentFilter
            repo = 'location of your previous game'
            grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
                        ['48QVRRsiae', 'u8_FUbXpAz']]
            poker = Poker(repo_location=repo, grouped=grouped)
            pressure_or_hold(data=DocumentFilter(data=poker, player_index_lst=['DZy-22KNBS']), bet=500, position='Pre Flop')
    :note: *None*

.. function:: ts_analysis(data, window):

    Build a Time Series DataFrame.

    :param data: A Player class object.
    :type data: DocumentFilter
    :param window: Rolling window value, default is 5. *Optional*
    :type window: int
    :return: A DataFrame of various moves over time.
    :rtype: pd.DataFrame
    :example:
        .. code-block:: python

            # This function requires a single player_index to be included in the DocumentFilter.
            from poker.poker_class import Poker
            from poker.analysis import ts_analysis
            from poker.document_filter_class import DocumentFilter
            repo = 'location of your previous game'
            grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
                        ['48QVRRsiae', 'u8_FUbXpAz']]
            poker = Poker(repo_location=repo, grouped=grouped)
            ts_analysis(data=DocumentFilter(data=poker, player_index_lst=['DZy-22KNBS']))
    :note: This is a function version of the TSanalysis class.

.. _Base:

====
Base
====
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

.. function:: standardize(data, keep_nan):

    Standardize a list with a mean of zero and std of 1.

    :param data: Input data to standardize.
    :type data: list, np.ndarray, or pd.Series
    :param keep_nan: If True, will maintain nan values, default is False. *Optional*
    :type keep_nan: bool
    :return: Standardized list.
    :rtype: list
    :example: *None*
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

.. function:: running_median(data, num):

    Calculate the Running Median on *num* interval.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :param num: Input val used for Running median window.
    :type num: int
    :return: list.
    :rtype: List[float]
    :example: *None*
    :note: None and np.nan values are replaced with the mean value.

.. function:: running_percentile(data, num):

    Calculate the Running Percentile on *num* interval.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :param num: Input val used for Running Percentile window.
    :type num: int
    :param q: Percent of data.
    :type q: float
    :return: Running percentile for a given  np.ndarray, pd.Series, or list.
    :rtype: List[float]
    :example: *None*
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

.. function:: native_variance(data, ddof):

    Calculate Variance of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :param ddof: Set the degrees of freedom, default is 1. *Optional*
    :type ddof: int
    :return: Returns the Variance.
    :rtype: float
    :example: *None*
    :note: *None*

.. function:: native_std(data, ddof):

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
    :return: Returns the max value.
    :rtype: float
    :example: *None*
    :note: *None*

.. function:: unique_values(data, count, order, indexes, keep_nan):

    Get Unique values from a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :param count: Return a dictionary with item and count, default is None. *Optional*
    :type count: bool
    :param order: If True will maintain the order, default is None. *Optional*
    :type order: bool
    :param indexes: If True will return index of all similar values, default is None. *Optional*
    :type indexes: bool
    :param keep_nan: If True will keep np.nan and None values, converting them to None, default is False. *Optional*
    :type keep_nan: bool
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
    :note: Ordered may not appear accurate if viewing in IDE.

.. function:: native_skew(data):

    Calculate Skew of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :return: Returns the skew value.
    :rtype: float
    :example: *None*
    :note: *None*

.. function:: native_kurtosis(data):

    Calculate Kurtosis of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :return: Returns the kurtosis value.
    :rtype: float
    :example: *None*
    :note: *None*

.. function:: native_percentile(data, q):

    Calculate Percentile of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :param q: Percentile percent.
    :type q: float
    :return: Returns the percentile value.
    :rtype: float
    :example: *None*
    :note: If input values are floats, will return float values.
