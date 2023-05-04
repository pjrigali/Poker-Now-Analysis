def _clean_print(o, line_lim: int, item_lim: int, new_line: bool = True) -> str:
    """
    Controls what is displayed when a class is called.

    Parameters
    ----------
    o : list, dict or other.
        Item to be shortened.
    line_lim : int
        Desired line length.
    item_lim : int
        Desired amount of items to show.
    new_line : bool, optional
        If you would like each item to be displayed in a new line, by default True

    Returns
    -------
    str
        Returns a str of the object.
    """
    if new_line:
        s = '\n\t'
    else:
        s = ', '
    
    if isinstance(o, list):
        k = o[:item_lim]
        s = s.join(str(i)[:line_lim] + ' ...' if len(str(i)) > line_lim else str(i) for i in k)
        if len(o) > len(k):
            s = s + '\n\t... item limit ' + f'({item_lim})' + ' reached ...'
        return s
    elif isinstance(o, dict):
        k = list(o.keys())[:item_lim]
        s = s.join(str(o[i])[:line_lim] + ' ...' if len(str(o[i])) > line_lim else str(o[i]) for i in k)
        if len(o) > len(k):
            s = s + '\n\t... item limit ' + f'({item_lim})' + ' reached ...'
        return s
    else:
        return str(o)[:line_lim]


def _get_attributes(val) -> dict:
    """
    Returns the attributes of a class.

    Parameters
    ----------
    val : A custom class.
        Desired input class you would like attributes of.

    Returns
    -------
    dict
        Returns the attributes in dictionary format.
    """
    return {i: getattr(val, i) for i in dir(val) if '__' not in i and i[0] != '_' and i != 'items'}


def _flatten_group(d: dict) -> dict:
    """
    Returns a flattened list of Id's and respective name.

    Parameters
    ----------
    d : dict.
        Desired input grouped users by name, followed by list or tuple of Id's.

    Returns
    -------
    dict
        Returns a dictionary of Id's and Name.
    """
    if d:
        n_d = {}
        for k, v in d.items():
            for i in v:
                n_d[i] = k
    else:
        n_d = {}
    return n_d

def _group_name_blank(d: dict, val) -> dict:
    """
    Returns a blank dictionary of names.

    Parameters
    ----------
    d : dict.
        Desired input grouped users by name, followed by list or tuple of Id's.
    val:
        Desired value.

    Returns
    -------
    dict
        Returns a dictionary of Names and an empty list.
    """
    if d:
        return {i: val for i in d}
    else:
        return {}
