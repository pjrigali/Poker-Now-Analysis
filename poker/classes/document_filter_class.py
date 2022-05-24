from typing import List, Optional, Union, Tuple
from dataclasses import dataclass
import pandas as pd
from poker.classes.poker import Poker
from poker.utils.class_functions import _get_attributes


def _df_convert_list(data: Union[List[str], Tuple[str], str, None]) -> Union[List[str], None]:
    """Converts str to List[str] and raises error"""
    if data is None:
        return None
    elif isinstance(data, list):
        return data
    elif isinstance(data, tuple):
        return list(data)
    elif isinstance(data, str):
        return [data]
    else:
        raise AttributeError('Incorrect input type used')


def _game_id(val: Union[List[str], str, None], data: Poker) -> dict:
    match_names = {k: True for k, v in data.matches.items()}
    if val is None:
        dic = match_names
    elif isinstance(val, str):
        if val in match_names:
            dic = {val: True}
    elif isinstance(val, list):
        dic = {}
        for i in val:
            if i in match_names:
                dic[i] = True
    else:
        raise AttributeError('')
    return dic


def _player_index(val: Union[List[str], str, None], data: Poker) -> dict:
    indexes = {}
    for k, v in data.players.items():
        for i in v.player_indexes:
            indexes[i] = True
    if val is None:
        dic = indexes
    elif isinstance(val, str):
        if val in indexes:
            dic = {val: True}
    elif isinstance(val, list):
        dic = {}
        for i in val:
            if i in indexes:
                dic[i] = True
    else:
        raise AttributeError('')
    return dic


def _event(val: Union[List[str], str, None]) -> dict:
    events = {'Calls': True, 'Checks': True, 'Folds': True, 'Bets': True, 'Shows': True, 'Wins': True,
              'PlayerStacks': True, 'BigBlind': True, 'SmallBlind': True, 'Flop': True, 'Turn': True,
              'River': True, 'MyCards': True, 'Joined': True, 'Requests': True, 'Approved': True,
              'Quits': True, 'Undealt': True, 'StandsUp': True, 'SitsIn': True}
    if val is None:
        dic = events
    elif isinstance(val, str):
        if val in events:
            dic = {val: True}
    elif isinstance(val, list):
        dic = {}
        for i in val:
            if i in events:
                dic[i] = True
    else:
        raise AttributeError('')
    return dic


def _position(val: Union[List[str], str, None]) -> dict:
    positions = {'Pre Flop': True, 'Post Flop': True, 'Post Turn': True, 'Post River': True}
    if val is None:
        dic = positions
    elif isinstance(val, str):
        if val in positions:
            dic = {val: True}
    elif isinstance(val, list):
        dic = {}
        for i in val:
            if i in positions:
                dic[i] = True
    else:
        raise AttributeError('')
    return dic


def _win_loss_all(val: Union[List[str], str, None]) -> tuple:
    if val == 'Win':
        return (True,)
    elif val == 'Loss':
        return (None,)
    else:
        return (True, None)


def _check(val, dic) -> bool:
    if val in dic:
        return True
    else:
        return False


def _get_data(data: Poker, game_id: list, player_index: list, event: list, position: list, win_loss_all: str) -> list:
    game_id = _game_id(val=game_id, data=data)
    player_index = _player_index(val=player_index, data=data)
    event = _event(val=event)
    position = _position(val=position)
    win_loss_all = _win_loss_all(val=win_loss_all)

    table_event = None
    if 'PlayerStacks' in event:
        table_event = True
    elif 'Flop' in event:
        table_event = True
    elif 'Turn' in event:
        table_event = True
    elif 'River' in event:
        table_event = True
    elif 'Undealt' in event:
        table_event = True

    lst = []
    for e in data.events:
        if _check(e.game_id, game_id) is False:
            continue
        elif _check(e.event, event) is False:
            continue
        elif _check(e.position, position) is False:
            continue
        elif e.wins not in win_loss_all:
            continue
        if table_event is not None and _check(e.event, event):
            lst.append((e.time, e))
            continue
        if isinstance(e.player_index, str):
            if _check(e.player_index, player_index) is False:
                continue
        elif isinstance(e.player_index, (list, tuple)):
            for i in e.player_index:
                if _check(e.player_index, player_index):
                    lst.append((e.time, e))
                    break
            continue
        lst.append((e.time, e))
    lst = sorted(lst, key=lambda x: x[0])
    return [i[1] for i in lst]


@dataclass
class DocumentFilter:
    """

    Get a selection from the Poker Object.
    Uses a set of filters to return a desired set of data to be used in later analysis.

    :param data: Input Poker object to be filtered.
    :type data: Poker
    :param game_id: Game Id filter, default is None. *Optional*
    :type game_id: Union[List[str], str, None]
    :param player_index: Player Index filter, default is None. *Optional*
    :type player_index: Union[List[str], str, None]
    :param player_name: Player Name filter, default is None. *Optional*
    :type player_name: Union[List[str], str, None]
    :param event: Filter by class objects, default is None. *Optional*
    :type event: Union[List[str], str, None]
    :param position: Filter by position, default is None. *Optional*
    :type position: Union[List[str], str, None]
    :param win_loss_all: Filter by Win, Loss or All, default is None. *Optional*
    :type win_loss_all: Union[str, None]
    :example: *None*
    :note: All inputs, except data, are *Optional* and defaults are set to None.
        Any str inputs are placed in a list.

    """

    __slots__ = ('game_id', 'player_index', 'event', 'position', 'win_loss_all', 'data')

    def __init__(self, data: Poker,
                 game_id: Optional[Union[List[str], str, None]] = None,
                 player_index: Optional[Union[List[str], str, None]] = None,
                 event: Optional[Union[List[str], str, None]] = None,
                 position: Optional[Union[List[str], str, None]] = None,
                 win_loss_all: Optional[str] = None):
        self.game_id = _df_convert_list(data=game_id)
        self.player_index = _df_convert_list(data=player_index)
        self.event = _df_convert_list(data=event)
        self.position = _df_convert_list(data=position)
        self.win_loss_all = win_loss_all
        self.data = _get_data(data=data, game_id=self.game_id, player_index=self.player_index, event=self.event,
                              position=self.position, win_loss_all=self.win_loss_all)

    def __repr__(self):
        return "DocumentFilter"

    def df(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict([_get_attributes(i) for i in self.data])

