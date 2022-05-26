from typing import Optional, Union
from dataclasses import dataclass
import pandas as pd
from poker.classes.poker import Poker
from poker.utils.class_functions import _get_attributes, _str_nan


def _df_convert_list(data: Optional[Union[list, tuple, str]]) -> Optional[list]:
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


def _game_id(val: Optional[Union[list, str]], data: Poker) -> dict:
    match_names = {k: True for k, v in data.matches.items()}
    if val is None:
        return match_names
    elif isinstance(val, str):
        if val in match_names:
            return {val: True}
    elif isinstance(val, list):
        return {i: True for i in val if i in match_names}
    else:
        raise AttributeError('')


def _player_index(val: Optional[Union[list, str]], data: Poker) -> dict:
    indexes = {}
    for k, v in data.players.items():
        for i in v.player_indexes:
            indexes[i] = True
    if val is None:
        return indexes
    elif isinstance(val, str):
        if val in indexes:
            return {val: True}
    elif isinstance(val, list):
        return {i: True for i in val if i in indexes}
    else:
        raise AttributeError('')


def _event(val: Optional[Union[list, str]]) -> dict:
    events = {'Calls': True, 'Checks': True, 'Folds': True, 'Bets': True, 'Shows': True, 'Wins': True,
              'PlayerStacks': True, 'BigBlind': True, 'SmallBlind': True, 'Flop': True, 'Turn': True,
              'River': True, 'MyCards': True, 'Joined': True, 'Requests': True, 'Approved': True,
              'Quits': True, 'Undealt': True, 'StandsUp': True, 'SitsIn': True}
    if val is None:
        return events
    elif isinstance(val, str):
        if val in events:
            return {val: True}
    elif isinstance(val, list):
        return {i: True for i in val if i in events}
    else:
        raise AttributeError('')


def _position(val: Optional[Union[list, str]]) -> dict:
    positions = {'Pre Flop': True, 'Post Flop': True, 'Post Turn': True, 'Post River': True, 'Flop': True, 'Turn': True,
                 'River': True}
    if val is None:
        return positions
    elif isinstance(val, str):
        if val in positions:
            return {val: True}
    elif isinstance(val, list):
        return {i: True for i in val if i in positions}
    else:
        raise AttributeError('')


def _win_loss_all(val: Optional[Union[list, str]]) -> tuple:
    if val == 'Win':
        return (True,)
    elif val == 'Loss':
        return (None,)
    else:
        return (True, None)


def _check(val, dic: dict) -> bool:
    """Checks if val in a dict"""
    if val in dic:
        return True
    else:
        return False


def _get_data(data: Poker, game_id: Optional[list], player_index: Optional[list], event: Optional[list],
              position: Optional[list], win_loss_all: Optional[str]) -> list:
    """Filters events based on criteria"""
    game_id = _game_id(val=game_id, data=data)
    player_index = _player_index(val=player_index, data=data)
    event = _event(val=event)
    position = _position(val=position)
    win_loss_all = _win_loss_all(val=win_loss_all)

    lst = []
    for e in data.events:
        if _check(e.game_id, game_id):
            if _check(e.event, event):
                if _check(e.position, position):
                    if e.wins in win_loss_all:
                        if e.player_index is None:
                            for i in e.remaining_players:
                                if _check(i, player_index):
                                    lst.append((e.time, e))
                                    break
                        elif isinstance(e.player_index, str):
                            if _check(e.player_index, player_index):
                                lst.append((e.time, e))
                        elif isinstance(e.player_index, (list, tuple)):
                            for i in e.player_index:
                                if _check(i, player_index):
                                    lst.append((e.time, e))
                                    break
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
    :type game_id: Optional[Union[list, tuple, str]]
    :param player_index: Player Index filter, default is None. *Optional*
    :type player_index: Optional[Union[list, tuple, str]]
    :param event: Filter by class objects, default is None. *Optional*
    :type event: Optional[Union[list, tuple, str]]
    :param position: Filter by position, default is None. *Optional*
    :type position: Optional[Union[list, tuple, str]]
    :param win_loss_all: Filter by Win, Loss or All, default is None. *Optional*
    :type win_loss_all: Optional[str]
    :example: *None*
    :note: All inputs, except data, are *Optional* and defaults are set to None.
        Any str inputs are placed in a list.

    """

    __slots__ = ('game_id', 'player_index', 'event', 'position', 'win_loss_all', 'data')

    def __init__(self, data: Poker,
                 game_id: Optional[Union[list, tuple, str]] = None,
                 player_index: Optional[Union[list, tuple, str]] = None,
                 event: Optional[Union[list, tuple, str]] = None,
                 position: Optional[Union[list, tuple, str]] = None,
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
        """Returns a DataFrame"""
        return pd.DataFrame([_get_attributes(i) for i in self.data])

    def unique_ids(self) -> tuple:
        """Returns tuple of unique ids"""
        ids = set()
        for e in self.data:
            if _str_nan(e.player_index):
                ids.add(e.player_index)
        return tuple(ids)

    def update_data_game_id(self, val: tuple) -> tuple:
        """Returns a tuple with new filter criteria"""
        val = {i: True for i in val}
        return tuple(e for e in self.data if e.game_id in val)

    def update_data_player_index(self, val: tuple) -> tuple:
        """Returns a tuple with new filter criteria"""
        val = {i: True for i in val}
        return tuple(e for e in self.data if _str_nan(e.player_index) and e.player_index in val)

    def update_data_event(self, val: tuple) -> tuple:
        """Returns a tuple with new filter criteria"""
        val = {i: True for i in val}
        return tuple(e for e in self.data if e.event in val)

    def update_data_position(self, val: tuple) -> tuple:
        """Returns a tuple with new filter criteria"""
        val = {i: True for i in val}
        return tuple(e for e in self.data if e.position in val)
