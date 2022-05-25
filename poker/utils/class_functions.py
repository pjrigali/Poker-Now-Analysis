from typing import Union, Optional


def _str_nan(val) -> bool:
    """Check is str type and is not None"""
    if isinstance(val, str) and val is not None:
        return True
    else:
        return False


def _get_attributes(val) -> dict:
    """Return Class attributes as a dict"""
    return {i: getattr(val, i) for i in dir(val) if '__' not in i and i[0] != '_'}


def _get_keys(dic: dict) -> tuple:
    """Creates tuple of keys"""
    return tuple([k for k, v in dic.items()])


def _get_percent(w_num: Union[int, float], h_num: Union[int, float], ret: Optional[float] = 0.0) -> float:
    """Catches division by zero and zero divided by a number"""
    if w_num != 0 and h_num != 0:
        return round(w_num / h_num, 2)
    else:
        return ret


def _get_percent_change(new: Union[int, float], old: Union[int, float], ret: Optional[float] = 0.0) -> float:
    """Returns the percent cahnage between two ints or floats"""
    if old != 0:
        return round((new - old) / old, 2)
    else:
        return ret