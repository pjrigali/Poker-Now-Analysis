from dataclasses import dataclass
from typing import Union
from poker.utils.class_functions import _str_nan
from poker.utils.base import native_mean, native_median, native_std, native_percentile


def _player(e, d: dict):
    if e.player_index not in d['player_ids'] and _str_nan(e.player_index):
        d['player_ids'][e.player_index] = True
    if e.player_name not in d['player_names'] and _str_nan(e.player_name):
        d['player_names'][e.player_name] = True
    if e.event not in d['events']:
        d['events'][e.event] = [e]
    else:
        d['events'][e.event].append(e)
    if e.game_id not in d['games']:
        d['games'][e.game_id] = True


# def _total(e, d: dict):
#     if e.event == 'Calls':
#         if e.all_in is not None:
#             d['all_in_call'].append(e.stack)
#         else:
#             d['call'].append(e.stack)
#             d['call_percent_of_pot'].append(e.stack / e.pot_size)
#             if e.current_chips[e.player_index] > 0:
#                 d['call_percent_of_chips'].append(e.stack / e.current_chips[e.player_index])
#             else:
#                 d['call_percent_of_chips'].append(0)
#     elif e.event == 'Bets':
#         if e.all_in is not None:
#             d['all_in_bet'].append(e.stack)
#         else:
#             d['bet'].append(e.stack)
#             d['position'][e.position].append('')
#             d['bet_percent_of_pot'].append(e.stack / e.pot_size)
#             if e.current_chips[e.player_index] > 0:
#                 d['bet_percent_of_chips'].append(e.stack / e.current_chips[e.player_index])
#             else:
#                 d['call_percent_of_chips'].append(0)
#     return d

# def _count(e, d: dict):
#     if e.event == 'Call' and e.all_in is True:
#         d['all_in_call'].append(e.stack)
#     elif e.event == 'Raise' and e.all_in is True:
#         d['all_in_bet'].append(e.stack)


# def _money(e, d: dict):
#     if e.event == 'Wins':
#         d['table_wins'].append(e.stack)
#     elif e.event in {'Quits': True, 'Folds': True}:
#         d['table_losses'].append(e.action_amount)
#     return d

# def _ave(e, d: dict) -> dict:
#     if e.event == 'Call' and e.all_in is True:
#         d['all_in_call'].append(e.stack)
#     elif e.event == 'Raise' and e.all_in is True:
#         d['all_in_bet'].append(e.stack)
# def _per(e, d: dict) -> dict:


def _get_player_data(data: tuple):
    player = {'player_ids': {}, 'player_names': {}, 'games': {}, 'events': {}}
    # total = {'bet': [], 'call': [], 'all_in_call': [], 'all_in_bet': [], 'bet_percent_of_pot': [],
    #          'call_percent_of_pot': [], 'bet_percent_of_chips': [], 'call_percent_of_chips': [],
    #          'position': {'Pre Flop': [], 'Post Flop': [], 'Post Turn': [], 'Post River': []}}
    # money = {'table_wins': [], 'table_losses': []}
    for i in data:
        _player(e=i, d=player)
        # _total(e=i, d=total)
        # _money(e=i, d=money)
    player['events'] = {k: tuple(v) for k, v in player['events'].items()}
    # count = {'hand_count': len(player['events']['PlayerStacks']), 'win_count': len(player['events']['Wins']),
    #          'loss_count': len(player['events']['Quits']), 'all_in_call_count': len(total['all_in_call']),
    #          'all_in_bet_count': len(total['all_in_call'])}
    # return player, {'totals': total, 'money': money, 'counts': count}
    return player, None


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


def _clean_dic(dic) -> tuple:
    return tuple([k for k, v in dic.items()])


@dataclass
class Player:

    __slots__ = ('events', 'player_indexes', 'player_names', 'custom_name', 'games', 'stats', 'money')

    def __init__(self, data: list, name: str):
        self.custom_name = name
        p, stats = _get_player_data(data=tuple(data))
        self.player_indexes = _clean_dic(dic=p['player_ids'])
        self.player_names = _clean_dic(dic=p['player_names'])
        self.events = p['events']
        self.games = _clean_dic(dic=p['games'])
        self.stats = stats
        self.money = None
        # self.hand_count = len(self.events['PlayerStacks'])
        # self.win_percent = _get_win_percent(w_num=self.win_count, h_num=self.hand_count)
        # self.game_count = len(self.games)
        # self.buy_in_amount = _get_stack(self.events, 'Approved')
        # self.leave_table_amount = _get_stack(self.events, 'StandsUp') - _get_stack(self.events, 'SitsIn')
        # self.largest_win, self.largest_loss = _get_start_curr_chips(self.events, self.player_indexes)
        # self.loss_count = len(self.events['Quits'])
        # self.profit = self.leave_table_amount - self.buy_in_amount
        # self.stats =

    def __repr__(self):
        return 'PlayerData'

    def player_stats(self, win_loss_all: str = 'all', stat: str = 'time', method: str = 'average'):
        i_dic, dic = {i: True for i in self.player_indexes}, {}
        if win_loss_all == 'win':
            for i in ('Bets', 'Checks', 'Calls'):
                dic[i] = []
                for j in self.events[i]:
                    if isinstance(j.winner, str):
                        if j.winner in i_dic:
                            dic[i].append(j)
                    elif isinstance(j.winner, (tuple, list)):
                        for k in j.winner:
                            if k in i_dic:
                                dic[i].append(j)
        elif win_loss_all == 'loss':
            for i in ('Bets', 'Checks', 'Calls', 'Folds'):
                dic[i] = []
                for j in self.events[i]:
                    if isinstance(j.winner, str):
                        if j.winner not in i_dic:
                            dic[i].append(j)
                    elif isinstance(j.winner, (tuple, list)):
                        for k in j.winner:
                            if k not in i_dic:
                                dic[i].append(j)
        else:
            for i in ('Bets', 'Checks', 'Calls', 'Folds'):
                dic[i] = self.events[i]

        if stat == 'time':
            t_dic = {}
            for pos in ('Pre Flop', 'Post Flop', 'Post Turn', 'Post River'):
                t_dic[pos] = {}
                for k, v in dic.items():
                    temp = [(j.time - j.previous_time).seconds for j in v if j.position == pos]
                    # temp = [(i.time - i.previous_time).seconds for i in v]
                    t_dic[pos][k] = {'mean': round(native_mean(temp), 2),
                                     'median': native_median(temp),
                                     'std': round(native_std(temp), 2)}
            t_dic
        dic
