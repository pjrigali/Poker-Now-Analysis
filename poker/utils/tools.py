"""
"""
from typing import Union, List, Optional
from collections.abc import KeysView, ValuesView
import numpy as np
import pandas as pd


def _to_list(data: Union[list, np.ndarray, pd.Series, int, float, tuple]
             ) -> Union[List[int], List[float], float, int]:
    """Converts list adjacent objects to a list and passes int/float objects"""
    if isinstance(data, list):
        return data
    elif isinstance(data, (np.ndarray, pd.Series)):
        return data.tolist()
    elif isinstance(data, (int, float)):
        return data
    elif isinstance(data, (KeysView, ValuesView, tuple)):
        return list(data)
    else:
        raise AttributeError('data needs to have a type of {np.ndarray, pd.Series, list}')


def _remove_nan(data: list, replace_val: Optional[Union[int, float, str]] = None,
                keep_nan: Optional[bool] = False) -> list:
    """Remove or replace nan values"""
    if replace_val:
        if replace_val == 'mean':
            replace_val = native_mean(data=_remove_nan(data=data))
        elif isinstance(replace_val, (int, float)):
            pass
        else:
            raise AttributeError('replace_val needs to be an int or float. If "mean" is passed, will use mean.')
        return [i if i == i and i is not None else replace_val for i in data]
    if keep_nan is False:
        return [i for i in data if i == i and i is not None]
    else:
        return [i if i == i and i is not None else None for i in data]


def _to_type(data: Union[list, np.float64, np.float32, np.float16,
                         np.float_, np.int64, np.int32, np.int16,
                         np.int8, np.int_, float, int], new_type: str
             ) -> Union[List[int], List[float], int, float]:
    """Converts objects to a set item"""
    if new_type == 'int':
        if isinstance(data, (tuple, list)):
            return [int(i) for i in data]
        else:
            return int(data)
    elif new_type == 'float':
        if isinstance(data, (tuple, list)):
            return [float(i) for i in data]
        else:
            return float(data)
    else:
        raise AttributeError('new_type can be "int" or "float.')


def native_median(data: Union[list, np.ndarray, pd.Series]) -> float:
    """

    Calculate Median of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :return: Returns the Median.
    :rtype: float
    :example: *None*
    :note: If multiple values have the same count, will return the mean.
        Median is used if there is an odd number of same count values.

    """
    data = _to_type(data=_remove_nan(data=_to_list(data=data)), new_type='float')
    sorted_lst, lst_len = sorted(data), len(data)
    index = (lst_len - 1) // 2
    if lst_len % 2:
        return sorted_lst[index]
    else:
        return native_mean(data=[sorted_lst[index]] + [sorted_lst[index + 1]])


def native_mean(data: Union[list, np.ndarray, pd.Series]) -> float:
    """

    Calculate Mean of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :return: Returns the mean.
    :rtype: float
    :example: *None*
    :note: *None*

    """
    data = _remove_nan(data=_to_list(data=data))
    if len(data) != 0:
        return sum(data) / len(data)
    else:
        return 0.0


def native_variance(data: Union[list, np.ndarray, pd.Series], ddof: int = 1) -> float:
    """

    Calculate Variance of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :param ddof: Set the degrees of freedom, default is 1. *Optional*
    :type ddof: int
    :return: Returns the Variance.
    :rtype: float
    :example: *None*
    :note: *None*

    """
    data = _remove_nan(data=_to_list(data=data))
    mu = native_mean(data=data)
    return sum((x - mu) ** 2 for x in data) / (len(data) - ddof)


def native_std(data: Union[list, np.ndarray, pd.Series], ddof: Optional[int] = 1) -> float:
    """

    Calculate Standard Deviation of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :param ddof: Set the degrees of freedom, default is 1. *Optional*
    :type ddof: int
    :return: Returns the Standard Deviation.
    :rtype: float
    :example: *None*
    :note: *None*

    """
    return native_variance(data=_to_list(data=data), ddof=ddof) ** .5


def native_sum(data: Union[list, np.ndarray, pd.Series]) -> float:
    """

    Calculate Sum of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :return: Returns the Sum.
    :rtype: float
    :example: *None*
    :note: *None*

    """
    data = _to_type(data=_remove_nan(data=_to_list(data=data)), new_type='float')
    if len(data) > 1:
        return sum(data)
    elif len(data) == 0:
        return 0.0
    else:
        return data


def calc_gini(data: Union[list, np.ndarray, pd.Series, tuple]) -> float:
    """

    Calculate the Gini Coef for a list.

    :param data: Input data.
    :type data: list, np.ndarray, pd.Series, or tuple
    :return: Gini value.
    :rtype: float
    :example:
        >>> lst = [4.3, 5.6]
        >>> calc_gini(data=lst, val=4, remainder=True) # 0.05445544554455435
    :note: The larger the gini coef, the more consolidated the chips on the table are to one person.

    """
    data = _to_list(data=data)
    if native_sum(data=data) == 0:
        return 0.0
    l = sorted(data)
    h, a = 0, 0
    for v in l:
        h += v
        a += h - v / 2.
    fa = h * len(data) / 2.
    return round((fa - a) / fa, 3)


def native_max(data: Union[list, np.ndarray, pd.Series]) -> float:
    """

    Calculate Max of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :return: Returns the max value.
    :rtype: float
    :example: *None*
    :note: *None*

    """
    data = _to_type(data=_remove_nan(data=_to_list(data=data)), new_type='float')

    if len(data) > 1:
        largest = 0
        for i in data:
            if i > largest:
                largest = i
        return largest
    elif len(data) == 0:
        return 0.0
    else:
        return data


def unique_values(data: Union[list, np.ndarray, pd.Series],
                  count: Optional[bool] = None,
                  order: Optional[bool] = None,
                  indexes: Optional[bool] = None,
                  keep_nan: Optional[bool] = False) -> Union[list, dict]:
    """

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
    :example: *None*
    :note: Ordered may not appear accurate if viewing in IDE.

    """
    data = _remove_nan(data=_to_list(data=data), keep_nan=keep_nan)

    if order:
        temp_dic, temp_lst = {}, []
        for item in data:
            if item not in temp_dic:
                temp_dic[item] = True
                temp_lst.append(item)
        return temp_lst
    if count:
        temp_data = list(set(data))
        temp_data = sorted([(data.count(i), i) for i in temp_data], reverse=True)
        return {i[1]: i[0] for i in temp_data}
    if indexes:
        temp_dic, ind_dic = {}, {}
        for ind, item in enumerate(data):
            if item in temp_dic:
                ind_dic[item].append(ind)
            else:
                temp_dic[item] = True
                ind_dic[item] = [ind]
        return ind_dic
    return list(set(data))


def round_to(data: Union[list, np.ndarray, pd.Series, np.float64,
                         np.float32, np.float16, np.float_, np.int64,
                         np.int32, np.int16, np.int8, np.int_,
                         float, int],
             val: Union[int, float],
             remainder: Optional[bool] = False
             ) -> Union[List[float], float]:
    """

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
        >>> # With remainder set to True.
        >>> lst = [4.3, 5.6]
        >>> round_to(data=lst, val=4, remainder=True) # [4.25, 5.5]
        >>>
        >>>  # With remainder set to False.
        >>> lst = [4.3, 5.6]
        >>> round_to(data=lst, val=4, remainder=False) # [4, 4]
        >>>
    :note: Single int or float values can be passed.

    """
    if isinstance(val, int):
        val = float(val)

    if type(data) not in [list, pd.Series, np.ndarray]:
        data = _to_type(data=data, new_type='float')
        if remainder is True:
            return round(data * val) / val
        else:
            return round(data / val) * val
    else:
        data = _to_type(data=_remove_nan(data=_to_list(data=data), replace_val=0), new_type='float')
        if remainder is True:
            return [round(item * val) / val for item in data]
        else:
            return [round(item / val) * val for item in data]


def native_skew(data: Union[list, np.ndarray, pd.Series]) -> float:
    """

    Calculate Skew of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :return: Returns the skew value.
    :rtype: float
    :example: *None*
    :note: *None*

    """
    data = _remove_nan(data=_to_list(data=data), replace_val=0.0)
    n = len(data)
    mu = native_mean(data=data)
    stdn = native_std(data=data, ddof=1)**3
    nn = ((n * (n-1))**.5) / (n - 2)
    return (((native_sum(data=[i - mu for i in data])**3) / n) / stdn) * nn


def native_kurtosis(data: Union[list, np.ndarray, pd.Series]) -> float:
    """

    Calculate Kurtosis of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :return: Returns the kurtosis value.
    :rtype: float
    :example: *None*
    :note: *None*

    """
    data = _remove_nan(data=_to_list(data=data), replace_val=0.0)
    n = len(data)
    mu = native_mean(data=data)
    stdn = native_std(data=data, ddof=1)**4
    return (((native_sum(data=[i - mu for i in data])**4) / n) / stdn) - 3


def native_percentile(data: Union[list, np.ndarray, pd.Series], q: float) -> Union[int, float]:
    """

    Calculate Percentile of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :param q: Percentile percent.
    :type q: float
    :return: Returns the percentile value.
    :rtype: float
    :example: *None*
    :note: If input values are floats, will return float values.

    """
    data = _remove_nan(data=_to_list(data=data))
    if len(data) == 0:
        return 0
    data_type = False
    if isinstance(data[0], float):
        data_type = True
        data = [item * 1000 for item in data]
    data = round_to(data=data, val=1)
    ind = int(round_to(data=len(data) * q, val=1))
    data.sort()
    for item in data:
        if item >= data[ind]:
            break
    if data_type:
        return item / 1000
    else:
        return item


def percent(v1: Union[float, int], v2: Union[float, int]) -> float:
    if v2 != 0.0:
        return round(v1 / v2, 3)
    else:
        return None


def calculate_hand(cards: Union[tuple, list]) -> str:
    ace, cards = [], list(cards)
    if not cards:
        return None
    for ind, card in enumerate(cards):
        if 'J' in card:
            cards[ind] = card.replace('J', '11')
        elif 'Q' in card:
            cards[ind] = card.replace('Q', '12')
        elif 'K' in card:
            cards[ind] = card.replace('K', '13')
        elif 'A' in card:
            cards[ind] = card.replace('A', '14')
            ace.append(card.replace('A', '1'))
    if ace:
        cards.extend(ace)
    cards = list(set(cards))
    l = len(cards)
    c_num = [int(card.split(' ')[0]) for card in cards]
    c_suit = [card.split(' ')[1] for card in cards]


    def find_pair(cards: List[int]) -> bool:
        for card in cards:
            if cards.count(card) == 2:
                return True
        return False


    def find_two_pair(cards: List[int]) -> bool:
        pair = 0
        for card in cards:
            if cards.count(card) == 2:
                pair += 1
                if pair == 2:
                    return True
        return False


    def find_three_of_a_kind(cards: List[int]) -> bool:
        for card in cards:
            if cards.count(card) == 3:
                return True
        return False


    def find_full_house(cards: List[int]) -> bool:
        three, two = False, False
        for card in cards:
            if cards.count(card) == 3:
                three = True
            elif cards.count(card) == 2:
                two = True

        if three is True and two is True:
            return True
        else:
            return False


    def find_flush(cards: List[str]) -> bool:
        for card in cards:
            if cards.count(card) == 5:
                return True
        return False


    def find_straight(cards: List[int]) -> bool:
        values = sorted(cards, reverse=True)
        t = []
        for i, j in enumerate(values[:-1]):
            if j - 1 == values[i + 1]:
                t.append(j)
        t.append(values[-1])
        return t == list(range(t[0], t[0] - 5, -1))


    def find_four_of_a_kind(cards: List[int]) -> bool:
        for card in cards:
            if cards.count(card) == 4:
                return True
        return False


    def find_straight_flush(nums, suits):
        if find_flush(cards=suits):
            cards = []
            for ind, card in enumerate(suits):
                if suits.count(card) == 5:
                    cards.append(nums[ind])
            if find_straight(cards=cards):
                return True
        return False


    def find_royal_flush(nums, suits):
        if find_flush(cards=suits) and find_straight(cards=nums):
            cards = sorted(tuple(zip(c_num, c_suit)), key=lambda x: x[0], reverse=True)[:5]
            lst, suit = (14, 13, 12, 11, 10), cards[0][1]
            for ind, card in enumerate(cards):
                if card[0][0] != lst[0]:
                    return False
        else:
            return False
        return True


    if l >= 5 and find_royal_flush(nums=c_num, suits=c_suit):
        return 'Royal Flush'
    elif l >= 5 and find_straight_flush(nums=c_num, suits=c_suit):
        return 'Straight Flush'
    elif l >= 4 and find_four_of_a_kind(cards=c_num):
        return 'Four of a Kind'
    elif l >= 5 and find_full_house(cards=c_num):
        return 'Full House'
    elif l >= 5 and find_flush(cards=c_suit):
        return 'Flush'
    elif l >= 5 and find_straight(cards=c_num):
        return 'Straight'
    elif l >= 3 and find_three_of_a_kind(cards=c_num):
        return 'Three of a Kind'
    elif l >= 4 and find_two_pair(cards=c_num):
        return 'Two Pair'
    elif l >= 2 and find_pair(cards=c_num):
        return 'Pair'
    else:
        return {14: 'A High', 13: 'K High', 12: 'Q High', 11: 'J High',
                10: '10 High', 9: '9 High', 8: '8 High', 7: '7 High',
                6: '6 High', 5: '5 High', 4: '4 High', 3: '3 High',
                2: '2 High'}[max(c_num)]
