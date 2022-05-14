from dataclasses import dataclass
from typing import Union
from poker.utils.class_functions import _str_nan


def _get_player_data(data: tuple):
    win_count, all_in_count, player_ids, player_names, events, games = 0, {'Calls': [], 'Raises': []}, {}, {}, {}, {}
    temp_id = data[0].player_index
    for i in data:
        if i.player_index not in player_ids and _str_nan(i.player_index):
            player_ids[i.player_index] = True
        if i.player_name not in player_names and _str_nan(i.player_index):
            player_names[i.player_name] = True
        if i.event == 'Wins':
            win_count += 1
        elif i.event in {'Raises': True, 'Calls': True} and i.all_in is not None:
            all_in_count[i.event].append(i.stack)
        if _str_nan(i.player_index) and i.player_index != temp_id:
            temp_id = i.player_index
        if i.event not in events:
            events[i.event] = [i]
        else:
            events[i.event].append(i)
        if i.game_id not in games:
            games[i.game_id] = True
    events, all_in_count = {k: tuple(v) for k, v in events.items()}, {k: tuple(v) for k, v in all_in_count.items()}
    return win_count, all_in_count, tuple(player_ids.keys()), tuple(player_names.keys()), events, tuple(games.keys())


def _get_win_percent(w_num, h_num) -> float:
    if w_num > 0:
        return round(w_num / h_num, 3)
    else:
        return 0.0


def _get_stack(dic: dict, k: str) -> float:
    if k in dic:
        return sum(i.stack for i in dic[k])
    else:
        return 0.0


def _get_start_curr_chips(dic: dict, ind: Union[str, tuple]):
    low_lst, high_lst = [], []
    low, high = 0, 0
    curr_game = dic['PlayerStacks'][0].game_id
    for i in dic['PlayerStacks']:
        if i.game_id != curr_game:
            curr_game = i.game_id
            low_lst.append(low), high_lst.append(high)
            low, high = 0, 0

        for _id in ind:
            if _id in i.starting_chips.keys():
                break
        if _id in i.current_chips.keys():
            val = i.current_chips[_id] - i.starting_chips[_id]
        else:
            val = 0 - i.starting_chips[_id]

        if val > high:
            high = val
        elif val < low:
            low = val
    low_lst.append(low), high_lst.append(high)
    return high_lst, low_lst


@dataclass
class Player:

    __slots__ = ('events', 'win_percent', 'win_count', 'hand_count', 'all_in', 'player_indexes', 'player_names',
                 'custom_name', 'games', 'largest_loss', 'largest_win', 'loss_count', 'buy_in_amount', 'game_count',
                 'leave_table_amount', 'profit')

    def __init__(self, data: list, name: str):
        self.custom_name = name
        self.win_count, self.all_in, self.player_indexes, self.player_names, self.events, self.games = _get_player_data(data=tuple(data))
        self.hand_count = len(self.events['PlayerStacks'])
        self.win_percent = _get_win_percent(w_num=self.win_count, h_num=self.hand_count)
        self.game_count = len(self.games)
        self.buy_in_amount = _get_stack(self.events, 'Approved')
        self.leave_table_amount = _get_stack(self.events, 'StandsUp') - _get_stack(self.events, 'SitsIn')
        self.largest_win, self.largest_loss = _get_start_curr_chips(self.events, self.player_indexes)
        self.loss_count = len(self.events['Quits'])
        self.profit = self.leave_table_amount - self.buy_in_amount

    def __repr__(self):
        return 'PlayerData'
