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
