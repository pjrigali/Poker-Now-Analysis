from typing import List, Optional, Union
import numpy as np
import pandas as pd
from poker.processor import class_object_lst


def _to_list(data: Union[list, np.ndarray, pd.Series, int, float]) -> Union[List[int], List[float], float, int]:
    """Converts list adjacent objects to a list and passes int/float objects"""
    if type(data) == list:
        return data
    elif type(data) in [np.ndarray, pd.Series]:
        return data.tolist()
    elif type(data) in [int, float]:
        return data
    else:
        raise AttributeError('data needs to have a type of {np.ndarray, pd.Series, list}')


def _remove_nan(data: list, replace_val: Optional[Union[int, float, str]] = None) -> list:
    """Remove or replace nan values"""
    if replace_val:
        if type(replace_val) == 'mean':
            replace_val = native_mean(data=data)
        elif type(replace_val) in [int, float]:
            pass
        else:
            raise AttributeError('replace_val needs to be an int or float. If "mean" is passed, will use mean.')
        return [i if i == i else replace_val for i in data]
    return [i for i in data if i == i]


def _to_type(data: Union[list, np.float64, np.float32, np.float16, np.float_, np.int64, np.int32, np.int16, np.int8,
                         np.int_, float, int], new_type: str) -> Union[List[int], List[float], int, float]:
    """Converts objects to a set item"""
    if new_type == 'int':
        if type(data) == list:
            return [int(i) for i in data]
        else:
            return int(data)
    elif new_type == 'float':
        if type(data) == list:
            return [float(i) for i in data]
        else:
            return float(data)
    else:
        raise AttributeError('new_type can be "int" or "float.')


def normalize(data: Union[list, np.ndarray, pd.Series], keep_nan: Optional[Union[bool, int, float]] = False) -> list:
    """

    Normalize a list between 0 and 1.

    :param data: Input data to normalize.
    :type data: list, np.ndarray, or pd.Series
    :param keep_nan: If True, will maintain nan values, default is False. *Optional*
    :type keep_nan: bool
    :return: Normalized list.
    :rtype: list
    :example: *None*
    :note: If an int or float is passed for keep_nan, that value will be placed where nan's are present.

    """
    temp_data = _remove_nan(data=_to_list(data=data))
    max_val, min_val = max(temp_data), min(temp_data)
    max_min_val = max_val - min_val
    if max_min_val == 0:
        max_min_val = 1
    if keep_nan is False:
        return [(item - min_val) / max_min_val for item in temp_data]
    elif type(keep_nan) in [float, int]:
        data = _remove_nan(data=data, replace_val=keep_nan)
        return [(item - min_val) / max_min_val for item in data]
    else:
        return [(item - min_val) / max_min_val if item == item else np.nan for item in data]


def running_mean(data: Union[list, np.ndarray, pd.Series], num: int) -> Union[np.ndarray, pd.Series, list]:
    """

    Calculate the Running Mean on *num* interval.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :param num: Input val used for running mean.
    :type num: int
    :return: Running mean for a given  np.ndarray, pd.Series, or list.
    :rtype: np.ndarray, pd.Series, or list
    :example: *None*
    :note: Maintains the input data type in output.

    """
    data = _to_list(data=data)
    pre, ran = [native_mean(data=data[:num])] * num, range(num, len(data))
    return pre + [native_mean(data=data[i - num:i]) for i in ran]


def running_std(data: Union[list, np.ndarray, pd.Series], num: int) -> List[float]:
    """

    Calculate the Running Std on *num* interval.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :param num: Input val used for Running Std window.
    :type num: int
    :return: Running mean for a given  np.ndarray, pd.Series, or list.
    :rtype: List[float]
    :example: *None*
    :note: Maintains the input data type in output.

    """
    data = _to_list(data=data)
    pre, ran = [native_std(data=data[:num])] * num, range(num, len(data))
    return pre + [native_std(data=data[i - num:i]) for i in ran]


def cumulative_mean(data: Union[list, np.ndarray, pd.Series]) -> List[float]:
    """

    Calculate the Cumulative Mean.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :return: Cumulative mean for a given np.ndarray, pd.Series, or list.
    :rtype: List[float]
    :example: *None*
    :note: Maintains the input data type in output.

    """
    data = _to_list(data=data)
    ran = range(1, len(data))
    return [0.0] + [native_mean(data=data[:i]) for i in ran]


def round_to(data: Union[list, np.ndarray, pd.Series, np.float64, np.float32, np.float16, np.float_, np.int64, np.int32,
                         np.int16, np.int8, np.int_, float, int], val: Union[int, float],
             remainder: Optional[bool] = False) -> Union[List[float], float]:
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
    if type(val) == int:
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


def calc_gini(data: Union[list, np.ndarray, pd.Series]) -> float:
    """

    Calculate the Gini Coef for a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :return: Gini value.
    :rtype: float
    :example:
        >>> lst = [4.3, 5.6]
        >>> calc_gini(data=lst, val=4, remainder=True) # 0.05445544554455435
    :note: The larger the gini coef, the more consolidated the chips on the table are to one person.

    """
    data = _to_list(data=data)
    sorted_list = sorted(data)
    height, area = 0, 0
    for value in sorted_list:
        height += value
        area += height - value / 2.
    fair_area = height * len(data) / 2.
    return (fair_area - area) / fair_area


def search_dic_values(dic: dict, item: Union[str, int, float]) -> Union[str, float, int]:
    """

    Searches a dict using the values.

    :param dic: Input data.
    :type dic: dict
    :param item: Search item.
    :type item: str, float or int
    :return: Key value connected to the value.
    :rtype: str, float or int
    :example: *None*
    :note: *None*

    """
    return list(dic.keys())[list(dic.values()).index(item)]


def flatten(data: list, type_used: str = 'str') -> list:
    """

    Flattens a list and checks the list.

    :param data: Input data.
    :type data: list
    :param type_used: Type to search for, default is "str". *Optional*
    :type type_used: str
    :param type_used: Either {str, int, or float}
    :type type_used: str
    :return: Returns a flattened list.
    :rtype: list
    :example: *None*
    :note: *None*

    """
    new_type = {'str': [str], 'int': [int], 'float': [float], 'class objects': class_object_lst}[type_used]
    lst = [item1 for item1 in data if type(item1) in new_type]
    missed = [item1 for item1 in data if type(item1) not in new_type]
    temp_lst = [item2 for item1 in missed for item2 in item1]
    return lst + temp_lst


def native_mode(data: Union[list, np.ndarray, pd.Series]) -> float:
    """

    Calculate Mode of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :return: Returns the Mode.
    :rtype: float
    :example: *None*
    :note: *None*

    """
    count_dic = unique_values(data=_remove_nan(data=_to_list(data=data)), count=True)
    count_dic_values = list(count_dic.values())
    dic_max = max(count_dic_values)
    lst = []
    for i in count_dic_values:
        val = search_dic_values(dic=count_dic, item=dic_max)
        lst.append((val, i))
        del count_dic[val]
        count_dic_values = list(count_dic.values())

    first_val, second_val = lst[0][0], lst[0][1]
    equal_lst = [i[0] for i in lst if second_val == i[1]]
    if len(equal_lst) == 1:
        return float(first_val)
    elif len(equal_lst) % 2 == 0:
        return native_mean(data=equal_lst)
    else:
        return native_median(data=equal_lst)


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
    return sum(data) / len(data)


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


def native_max(data: Union[list, np.ndarray, pd.Series]) -> float:
    """

    Calculate Max of a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :return: Returns the Max.
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


def unique_values(data: Union[list, np.ndarray, pd.Series], count: Optional[bool] = False) -> Union[list, dict]:
    """

    Get Unique values from a list.

    :param data: Input data.
    :type data: list, np.ndarray, or pd.Series
    :param count: Return a dictionary with item and count, default is False. *Optional*
    :type count: bool
    :return: Returns either a list of unique values or a dict of unique values with counts.
    :rtype: Union[list, dict]
    :example: *None*
    :note: *None*

    """
    data = _remove_nan(data=_to_list(data=data))
    if count is False:
        return list(set(data))
    else:
        temp_data = list(set(data))
        return {i: data.count(i) for i in temp_data}


# def calculate_hand(cards: Union[tuple, list]) -> str:
#
#     card_lst = []
#     for card in cards:
#         if 'J' in card:
#             card_lst.append(card.replace('J', '11'))
#         elif 'Q' in card:
#             card_lst.append(card.replace('Q', '12'))
#         elif 'K' in card:
#             card_lst.append(card.replace('K', '13'))
#         elif 'A' in card:
#             card_lst.append(card.replace('A' '14'))
#         else:
#             card_lst.append(card)
#
#     card_lst_num = [int(card.split(' ')[0]) for card in card_lst]
#     card_lst_suit = [card.split(' ')[1] for card in card_lst]
#
#     def find_pair(cards: List[int]) -> bool:
#         for card in cards:
#             if cards.count(card) == 2:
#                 return True
#         return False
#
#     def find_two_pair(cards: List[int]) -> bool:
#         pair = 0
#         for card in cards:
#             if cards.count(card) == 2:
#                 pair += 1
#         if pair == 2:
#             return True
#         return False
#
#     def find_three_of_a_kind(cards: List[int]) -> bool:
#         for card in cards:
#             if cards.count(card) == 3:
#                 return True
#         return False
#
#     def find_full_house(cards: List[int]) -> bool:
#         three, two = False, False
#         for card in cards:
#             if cards.count(card) == 3:
#                 three = True
#             elif cards.count(card) == 2:
#                 two = True
#
#         if three is True and two is True:
#             return True
#         else:
#             return False
#
#     def find_four_of_a_kind(cards: List[int]) -> bool:
#         for card in cards:
#             if cards.count(card) == 4:
#                 return True
#         return False
#
#     def find_flush(cards: List[str]) -> bool:
#         for card in cards:
#             if cards.count(card) == 5:
#                 return True
#         return False
#
#     def find_straight(cards: List[int]) -> bool:
#         values = sorted(cards, reverse=True)
#         return values == list(range(values[0], values[0] - 5, -1))
#
#     return
