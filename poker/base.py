from typing import List, Optional, Union
import numpy as np
import pandas as pd


def normalize(data: Union[np.ndarray, pd.Series, list]) -> Union[np.ndarray, pd.Series, list]:
    """

    Normalize an np.ndarray, pd.Series, or list between 0 and 1.

    :param data: Input data to normalize.
    :type data: np.ndarray, pd.Series, or list
    :return: Normalized np.ndarray, pd.Series, or list.
    :rtype: np.ndarray, pd.Series, or list
    :example: *None*
    :note: Maintains the input data type in output.

    """
    max_val, min_val = np.max(data), np.min(data)
    max_min_val = max_val - min_val
    if type(data) == np.ndarray:
        return (data - min_val) / max_min_val
    elif type(data) == pd.Series:
        return (data - min_val) / max_min_val
    elif type(data) == list:
        return [(item - min_val) / max_min_val if ~np.isnan(item) else np.nan for item in data]
    else:
        raise AttributeError('data needs to have a type of {np.ndarray, pd.Series, list}')


def running_mean(data: Union[np.ndarray, pd.Series, list], num: int) -> Union[np.ndarray, pd.Series, list]:
    """

    Calculate the running mean on *num* interval

    :param data: Input data.
    :type data: np.ndarray, pd.Series, or list
    :param num: Input val used for running mean.
    :type num: int
    :return: Running mean for a given  np.ndarray, pd.Series, or list.
    :rtype: np.ndarray, pd.Series, or list
    :example: *None*
    :note: Maintains the input data type in output.

    """
    if type(data) == np.ndarray:
        cum_sum = np.cumsum(np.insert(arr=data, values=0, obj=0))
        return (cum_sum[num:] - cum_sum[:-num]) / float(num)
    elif type(data) == pd.Series:
        return data.rolling(num).mean().iloc[num-1:].reset_index(drop=True)
    elif type(data) == list:
        return [sum(data[i - num:i]) / num for i, j in enumerate(data) if i >= num] + [np.mean(data[-num:])]
    else:
        raise AttributeError('data needs to have a type of {np.ndarray, pd.Series, list}')


def cumulative_mean(data: Union[np.ndarray, pd.Series, list]) -> Union[np.ndarray, pd.Series, list]:
    """

    Calculate the cumulative mean.

    :param data: Input data.
    :type data: np.ndarray, pd.Series, or list
    :return: Cumulative mean for a given np.ndarray, pd.Series, or list.
    :rtype: np.ndarray, pd.Series, or list
    :example: *None*
    :note: Maintains the input data type in output.

    """
    if type(data) == np.ndarray:
        cum_sum = np.cumsum(data, axis=0)
        for i in range(cum_sum.shape[0]):
            cum_sum[i] = cum_sum[i] / (i + 1)
        return cum_sum
    elif type(data) == pd.Series:
        return data.expanding().mean()
    elif type(data) == list:
        return [sum(data[:i]) / len(data[:i]) if i > 0 else 0 for i, j in enumerate(data) ]
    else:
        raise AttributeError('data needs to have a type of {np.ndarray, pd.Series, list}')


def round_to(data: Union[np.ndarray, pd.Series, list], val: int,
             remainder: Optional[bool] = False) -> Union[np.ndarray, pd.Series, list]:
    """

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
        >>> # With remainder set to True.
        >>> lst = [4.3, 5.6]
        >>> round_to(data=lst, val=4, remainder=True) # [4.25, 5.5]
        >>>
        >>>  # With remainder set to False.
        >>> lst = [4.3, 5.6]
        >>> round_to(data=lst, val=4, remainder=False) # [4, 4]
        >>>
    :note: Maintains the input data type in output.

    """
    if remainder:
        if type(data) == np.ndarray:
            return np.around(data * val) / val
        elif type(data) == pd.Series:
            return (data * val).round() / val
        elif type(data) == list:
            return [round(item * val) / val if ~np.isnan(item) else np.nan for item in data]
        else:
            raise AttributeError('data needs to have a type of {np.ndarray, pd.Series, list}')
    else:
        if type(data) == np.ndarray:
            return np.transpose(np.around(data / val) * val)
        elif type(data) == pd.Series:
            return (data / val).round() * val
        elif type(data) == list:
            return [round(item / val) * val if ~np.isnan(item) else np.nan for item in data]
        else:
            raise AttributeError('data needs to have a type of {np.ndarray, pd.Series, list}')


def calc_gini(data: Union[np.ndarray, pd.Series, list]) -> float:
    """

    Calculate the Gini Coef for a np.ndarray, pd.Series, or list.

    :param data: Input data.
    :type data: np.ndarray, pd.Series, or list
    :return: Gini value.
    :rtype: float
    :example:
        >>> lst = [4.3, 5.6]
        >>> calc_gini(data=lst, val=4, remainder=True) # 0.05445544554455435
    :note: The larger the gini coef, the more consolidated the chips on the table are to one person.

    """
    if type(data) == list:
        pass
    elif type(data) in [np.ndarray, pd.Series]:
        data = list(data)
    else:
        raise AttributeError('Invalid input data type')

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


def calculate_hand(cards: Union[tuple, list]) -> str:

    card_lst = []
    for card in cards:
        if 'J' in card:
            card_lst.append(card.replace('J', '11'))
        elif 'Q' in card:
            card_lst.append(card.replace('Q', '12'))
        elif 'K' in card:
            card_lst.append(card.replace('K', '13'))
        elif 'A' in card:
            card_lst.append(card.replace('A' '14'))
        else:
            card_lst.append(card)

    card_lst_num = [int(card.split(' ')[0]) for card in card_lst]
    card_lst_suit = [card.split(' ')[1] for card in card_lst]

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

    def find_four_of_a_kind(cards: List[int]) -> bool:
        for card in cards:
            if cards.count(card) == 4:
                return True
        return False

    def find_flush(cards: List[str]) -> bool:
        for card in cards:
            if cards.count(card) == 5:
                return True
        return False

    def find_straight(cards: List[int]) -> bool:
        values = sorted(cards, reverse=True)
        return values == list(range(values[0], values[0] - 5, -1))

    return
