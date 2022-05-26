from dataclasses import dataclass
from poker.utils.class_functions import _str_nan, _get_percent, tdict, _dict
from poker.utils.base import native_mean, native_median, native_std


CLASS_TUP = ('Calls', 'Checks', 'Folds', 'Bets', 'Shows', 'Wins', 'PlayerStacks', 'BigBlind', 'SmallBlind', 'Flop',
             'Turn', 'River', 'MyCards', 'Joined', 'Requests', 'Approved', 'Quits', 'Undealt', 'StandsUp', 'SitsIn',
             'Raises')


# def _count(e, d: dict):
#     if e.event == 'Call' and e.all_in is True:
#         d['all_in_call'].append(e.stack)
#     elif e.event == 'Raise' and e.all_in is True:
#         d['all_in_bet'].append(e.stack)


# def _ave(e, d: dict) -> dict:
#     if e.event == 'Call' and e.all_in is True:
#         d['all_in_call'].append(e.stack)
#     elif e.event == 'Raise' and e.all_in is True:
#         d['all_in_bet'].append(e.stack)
# def _per(e, d: dict) -> dict:

def _data(data: tuple, games: tuple):
    d = {'player_names': {}, 'events': tdict(CLASS_TUP, []), 'bet': [], 'call': [], 'raises': [],
         'all_in_call': [], 'all_in_bet': [], 'bet_percent_of_pot': [], 'call_percent_of_pot': [],
         'bet_percent_of_chips': [], 'call_percent_of_chips': [], 'raise_percent_of_pot': [],
         'raise_percent_of_chips': [], 'raise_percent_of_action': [], 'position': {'Pre Flop': [], 'Post Flop': [],
                                                                                   'Post Turn': [], 'Post River': []},
         'table_wins': [], 'table_losses': [], 'joined': tdict(games, []), 'leaves': tdict(games, []),
         'approved': tdict(games, []), 'time': tdict(games, [])}
    game, temp_time = data[0], []
    for e in data:
        if e.event in {'Folds': True, 'Wins': True, 'StandsUp': True, 'Calls': True, 'Checks': True, 'Bets': True}:
            temp_time.append((e.time - e.start_time).seconds)
            if e.current_round != game.current_round:
                temp_time.append((game.time - game.start_time).seconds), d['time'][game.game_id].append(max(temp_time))
                game, temp_time = e, []
            else:
                if game.time - game.start_time < e.time - e.start_time:
                    game = e
        d['events'][e.event].append(e)
        if _str_nan(e.player_name):
            d['player_names'] = _dict(e.player_name, d['player_names'])
        if e.event == 'Calls':
            if e.all_in is not None:
                d['all_in_call'].append(e.stack)
            else:
                d['call'].append(e.stack), d['call_percent_of_pot'].append(round(e.stack / e.pot_size, 2))
                if e.current_chips[e.player_index] > 0:
                    d['call_percent_of_chips'].append(round(e.stack / e.current_chips[e.player_index], 2))
                else:
                    d['call_percent_of_chips'].append(0.0)
                if e.raises is not None:
                    d['events']['Raises'].append(e), d['raises'].append(e.raises)
                    d['raise_percent_of_pot'].append(round(e.raises / e.pot_size, 2))
                    d['raise_percent_of_action'].append(round(e.raises / e.action_amount, 2))
                    if e.current_chips[e.player_index] > 0:
                        d['raise_percent_of_chips'].append(round(e.raises / e.current_chips[e.player_index], 2))
                    else:
                        d['raise_percent_of_chips'].append(0.0)
            continue
        elif e.event == 'Bets':
            if e.all_in is not None:
                d['all_in_bet'].append(e.stack)
            else:
                d['bet'].append(e.stack), d['bet_percent_of_pot'].append(round(e.stack / e.pot_size, 2))
                if e.current_chips[e.player_index] > 0:
                    d['bet_percent_of_chips'].append(round(e.stack / e.current_chips[e.player_index], 2))
                else:
                    d['call_percent_of_chips'].append(0.0)
                if e.raises is not None:
                    d['events']['Raises'].append(e), d['raises'].append(e.raises)
                    d['raise_percent_of_pot'].append(round(e.raises / e.pot_size, 2))
                    d['raise_percent_of_action'].append(round(e.raises / e.action_amount, 2))
                    if e.current_chips[e.player_index] > 0:
                        d['raise_percent_of_chips'].append(round(e.raises / e.current_chips[e.player_index], 2))
                    else:
                        d['raise_percent_of_chips'].append(0.0)
            continue
        elif e.event == 'StandsUp':
            d['leaves'][e.game_id].append(e.stack)
            continue
        elif e.event == 'SitsIn':
            d['joined'][e.game_id].append(e.stack)
            continue
        elif e.event == 'Approved':
            d['approved'][e.game_id].append(e.stack)
            continue
        elif e.event == 'Quits':
            if e.stack > 0:
                if e.stack not in d['leaves'][e.game_id]:
                    d['leaves'][e.game_id].append(e.stack)
            continue
    for i in ('joined', 'leaves', 'approved', 'time', 'position', 'events'):
        d[i] = {k: tuple(v) for k, v in d[i].items()}
    d = {k: tuple(v) if isinstance(v, list) else v for k, v in d.items()}
    # count = {'hand_count': len(player['events']['PlayerStacks']), 'win_count': len(player['events']['Wins']),
    #          'loss_count': len(player['events']['Quits']), 'all_in_call_count': len(total['all_in_call']),
    #          'all_in_bet_count': len(total['all_in_call'])}
    # return player, {'totals': total, 'money': money, 'counts': count}
    return d


@dataclass
class Player:

    __slots__ = ('events', 'player_indexes', 'player_names', 'custom_name', 'games', 'stats', 'money', 'win_matrix')

    def __init__(self, dic: dict, name: str):
        self.custom_name = name
        self.games = dic['games']
        p = _data(data=tuple(dic['events']), games=self.games)
        self.stats = {i: p[i] for i in ('bet', 'call', 'raises', 'all_in_call', 'all_in_bet', 'bet_percent_of_pot',
                                        'call_percent_of_pot', 'bet_percent_of_chips', 'call_percent_of_chips',
                                        'raise_percent_of_pot', 'raise_percent_of_chips', 'raise_percent_of_action',
                                        'position')}
        self.money = {i: p[i] for i in ('table_wins', 'table_losses', 'joined', 'leaves', 'approved', 'time')}
        self.events = p['events']
        self.player_indexes = dic['ids']
        self.player_names = tuple(p['player_names'].keys())
        self.win_matrix = dic['beat']

    def __repr__(self):
        if len(self.custom_name) == 10 and len(self.player_names) == 1:
            return self.player_names[0]
        return self.custom_name

    def player_stats(self, win_loss_all: str = 'all', time: bool = False, method: str = 'average', position: str = 'all') -> dict:
        if position == 'all':
            position = ('Pre Flop', 'Post Flop', 'Post Turn', 'Post River')
        else:
            position = (position,)
        i_dic, dic = tdict(self.player_indexes, True), {'Raises': []}
        if win_loss_all == 'win':
            for i in ('Bets', 'Checks', 'Calls'):
                dic[i] = []
                if i == 'Bets':
                    for j in self.events[i]:
                        if isinstance(j.winner, str):
                            if j.winner in i_dic:
                                dic[i].append(j)
                                if j.raises is not None:
                                    dic['Raises'].append(j)
                        elif isinstance(j.winner, (tuple, list)):
                            for k in j.winner:
                                if k in i_dic:
                                    dic[i].append(j)
                                    if j.raises is not None:
                                        dic['Raises'].append(j)
                else:
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
                if i == 'Bets':
                    for j in self.events[i]:
                        if isinstance(j.winner, str):
                            if j.winner not in i_dic:
                                dic[i].append(j)
                                if j.raises is not None:
                                    dic['Raises'].append(j)
                        elif isinstance(j.winner, (tuple, list)):
                            for k in j.winner:
                                if k not in i_dic:
                                    dic[i].append(j)
                                    if j.raises is not None:
                                        dic['Raises'].append(j)
        else:
            for i in ('Bets', 'Checks', 'Calls', 'Folds'):
                dic[i] = self.events[i]
                if i == 'Bets':
                    for j in self.events[i]:
                        if j.raises is not None:
                            dic['Raises'].append(j)

        if time:
            t_dic = {}
            for pos in position:
                t_dic[pos] = {}
                for k, v in dic.items():
                    temp = [(j.time - j.previous_time).seconds for j in v if j.position == pos]
                    t_dic[pos][k] = {'mean': round(native_mean(temp), 2),
                                     'median': native_median(temp),
                                     'std': round(native_std(temp), 2)}
        else:
            t_dic = {}
            for pos in position:
                t_dic[pos] = {}
                for k, v in dic.items():
                    if k == 'Raises':
                        stack = [j.raises for j in v if j.position == pos]
                        pot = [_get_percent(j.raises, j.pot_size) for j in v if j.position == pos]
                        chip = [_get_percent(j.raises, j.current_chips[j.player_index]) for j in v if j.position == pos]
                    elif k == 'Folds':
                        stack = [j.action_amount for j in v if j.position == pos and j.action_amount is not None]
                        pot = [_get_percent(j.action_amount, j.pot_size) for j in v if j.position == pos and j.action_amount is not None]
                        chip = [_get_percent(j.action_amount, j.current_chips[j.player_index]) for j in v if j.position == pos and j.action_amount is not None]
                    elif k == 'Checks':
                        continue
                    else:
                        stack = [j.stack for j in v if j.position == pos and j.stack is not None]
                        pot = [_get_percent(j.stack, j.pot_size) for j in v if j.position == pos and j.stack is not None]
                        chip = [_get_percent(j.stack, j.current_chips[j.player_index]) for j in v if j.position == pos and j.stack is not None]
                    t_dic[pos][k] = {'mean_amount': int(native_mean(stack)),
                                     'median_amount': native_median(stack),
                                     'std_amount': int(native_std(stack)),
                                     'mean_pot_percent': int(native_mean(pot)),
                                     'median_pot_percent': native_median(pot),
                                     'std_pot_percent': int(native_std(pot)),
                                     'mean_chip_percent': int(native_mean(chip)),
                                     'median_chip_percent': native_median(chip),
                                     'std_chip_percent': int(native_std(chip))}
        return dic
