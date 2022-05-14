from typing import List, Optional, Union
from dataclasses import dataclass
import datetime
from poker.classes.event import Event
from poker.classes.data import Data


def _unique_ids(data: tuple):
    return tuple(set([i.player_index for i in data if isinstance(i.player_index, str) and i.player_index is not None]))


def _unique_names(data: tuple):
    return tuple(set([i.player_name for i in data if isinstance(i.player_name, str) and i.player_name is not None]))


def _get_player_data(data: tuple):
    win_count, all_in_count, player_ids, player_names, events, games = 0, [], {}, {}, {}, {}
    temp_id = data[0].player_index
    for i in data:
        if i.player_index not in player_ids and isinstance(i.player_index, str):
            player_ids[i.player_index] = True
        if i.player_name not in player_names and isinstance(i.player_name, str):
            player_names[i.player_name] = True
        if i.event == 'Wins':
            win_count += 1
        elif i.event == 'Raises' and i.all_in is not None:
            all_in_count.append(i.stack)
        if isinstance(i.player_index, str) and i.player_index != temp_id:
            temp_id = i.player_index
        if i.event not in events:
            events[i.event] = [i]
        else:
            events[i.event].append(i)
        if i.game_id not in games:
            games[i.game_id] = True
    events = {k: tuple(v) for k, v in events.items()}
    return win_count, tuple(all_in_count), tuple(player_ids.keys()), tuple(player_names.keys()), events, tuple(games.keys())


def _get_win_percent(w_num, h_num) -> float:
    if w_num > 0:
        return round(w_num / h_num, 3)
    else:
        return 0.0


@dataclass
class Player:

    __slots__ = ('events', 'win_percent', 'win_count', 'hand_count', 'all_in', 'player_indexes', 'player_names',
                 'custom_name', 'games')

    def __init__(self, data: list, name: str):
        self.custom_name = name
        self.win_count, self.all_in, self.player_indexes, self.player_names, self.events, self.games = _get_player_data(data=tuple(data))
        self.hand_count = len(self.events['PlayerStacks'])
        self.win_percent = _get_win_percent(w_num=self.win_count, h_num=self.hand_count)

    def __repr__(self):
        return 'PlayerData'
