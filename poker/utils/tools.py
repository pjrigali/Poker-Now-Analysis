from typing import Union, List, Optional
from collections.abc import KeysView, ValuesView
import numpy as np
import pandas as pd


def _to_list(data: Union[list, np.ndarray, pd.Series, int, float, tuple]) -> Union[List[int], List[float], float, int]:
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


def _to_type(data: Union[list, np.float64, np.float32, np.float16, np.float_, np.int64, np.int32, np.int16, np.int8,
                         np.int_, float, int], new_type: str) -> Union[List[int], List[float], int, float]:
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


def calculate_hand(cards: Union[tuple, list]) -> str:
    cards, l = list(cards), len(cards)
    
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
    c_num, c_suit = [int(card.split(' ')[0]) for card in cards], [card.split(' ')[1] for card in cards]

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
        return values == list(range(values[0], values[0] - 5, -1))

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
        return {14: 'A High', 13: 'K High', 12: 'Q High', 11: 'J High', 10: '10 High', 9: '9 High', 8: '8 High',
                7: '7 High', 6: '6 High', 5: '5 High', 4: '4 High', 3: '3 High', 2: '2 High'}[max(c_num)]
