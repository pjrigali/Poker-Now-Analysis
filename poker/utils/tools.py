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
