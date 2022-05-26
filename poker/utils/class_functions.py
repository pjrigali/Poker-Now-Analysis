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
    return tuple(k for k, v in dic.items())


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


def tdict(k: Union[list, tuple], v=True) -> dict:
    """Creates a dict with a specific value"""
    if isinstance(v, bool):
        return {i: True for i in k}
    elif isinstance(v, list):
        return {i: [] for i in k}
    elif isinstance(v, dict):
        return {i: {} for i in k}


def _dict(val, d: dict, kv: str = 'k') -> dict:
    """Checks if a value is in a true dict and adds the value if it isnt"""
    if _str_nan(val) and val not in d:
        return {**d, **{val: True}}
    elif isinstance(val, (list, tuple)):
        return {**d, **{i: True for i in val if i not in d}}
    elif isinstance(val, dict):
        if kv == 'k':
            return {**d, **{k for k, v in val.items() if k not in d}}
        else:
            return {**d, **{v for k, v in val.items() if k not in d}}
    else:
        return d
