def _str_nan(val) -> bool:
    """Check is str type and is not None"""
    if isinstance(val, str) and val is not None:
        return True
    else:
        return False


def _get_attributes(val) -> dict:
    """Return Class attributes as a dict"""
    return {att: getattr(val, att) for att in dir(val) if '__' not in att and att[0] != '_'}


def _get_keys(dic: dict) -> tuple:
    """Creates tuple of keys"""
    return tuple([k for k, v in dic.items()])


def _get_percent(w_num, h_num, ret=0.0) -> float:
    """Catches division by zero and zero divided by a number"""
    if w_num != 0 and h_num != 0:
        return round(w_num / h_num, 2)
    else:
        return ret
