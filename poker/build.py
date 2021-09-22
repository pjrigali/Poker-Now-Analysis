from typing import List, Union
import pandas as pd
import numpy as np
from collections import Counter

from poker.processor import Approved, Quits, StandsUp, SitsIn
from poker.base import flatten


def _convert_shapes(data: List[str]) -> List[str]:
    """Converts card icons into shapes"""
    return [row.replace("â£", " Clubs").replace("â¦", " Diamonds").replace("â¥", " Hearts").replace("â", " Spades") for row in data]


def _get_hands(repo_location: str, file: str) -> List[str]:
    """Split game into list of hands"""
    df = pd.read_csv(repo_location + file, encoding='latin1')['entry']
    lst = _convert_shapes(list(df.reindex(index=df.index[::-1]).reset_index(drop=True)))
    hands, hand_lst = [], []
    for item in lst:
        if ' starting hand ' in item:
            if ' hand #1 ' in item:
                hands.append(hand_lst)
            hand_lst = [item]
            hands.append(hand_lst)
        else:
            hand_lst.append(item)
    return hands


def _add_to_dic(item, player_dic: dict, location: str, player_index: str):
    if type(item) == tuple:
        item = list(item)
    if player_index in player_dic.keys():
        if location in player_dic[player_index].keys():
            player_dic[player_index][location].append(item)
        else:
            player_dic[player_index][location] = [item]
    else:
        player_dic[player_index] = {'Cards': [], 'Hands': [], 'Lines': []}
        player_dic[player_index][location].append(item)


def _calc_money(lst: list, ind: str) -> pd.DataFrame:
    """Returns a dataframe recording player action related to money on the table for a game."""
    player_money_dic = {'Player Names': [], 'Player Stack': [], 'Player Quits': [], 'Player Stands Up': [],
                        'Player Sits In': []}
    for line in lst:
        if type(line) == Approved:
            player_money_dic['Player Names'].append(line.player_name)
            player_money_dic['Player Stack'].append(line.stack)
        elif type(line) == Quits:
            player_money_dic['Player Quits'].append(line.stack)
        elif type(line) == StandsUp:
            player_money_dic['Player Stands Up'].append(line.stack)
        elif type(line) == SitsIn:
            player_money_dic['Player Sits In'].append(line.stack)

    temp_df = pd.DataFrame(index=[ind])
    temp_df['Player Names'] = [list(set(player_money_dic['Player Names']))]
    temp_df['Buy in Total'] = np.sum(player_money_dic['Player Stack'])
    temp_df['Loss Count'] = len(player_money_dic['Player Quits'])
    temp_df['player stands up sum'] = np.sum(player_money_dic['Player Stands Up'])
    temp_df['player sits in sum'] = np.sum(player_money_dic['Player Sits In'])
    temp_df['Leave Table Amount'] = temp_df['player stands up sum'] - temp_df['player sits in sum']
    return temp_df[['Player Names', 'Buy in Total', 'Loss Count', 'Leave Table Amount']]


def _line_to_df(line_lst: list) -> pd.DataFrame:
    lst = []
    for line in line_lst:
        temp_win = False
        # for player in player_index:
        if line.player_index in line.winner:
            temp_win = True
            # break
        lst.append({'Player Index': line.player_index, 'Player Name': line.player_name, 'Bet Amount': line.stack,
                    'Position': line.position, 'Round': line.current_round, 'Player Reserve': line.chips,
                    'Class': repr(line),  'Winner': line.winner, 'Win': temp_win, 'Win Stack': line.win_stack,
                    'Win Hand': line.winning_hand, 'All In': line.all_in, 'Pot Size': line.pot_size,
                    'Remaining Players': line.remaining_players, 'From Person': line.action_from_player})
    return pd.DataFrame(lst).bfill()


def _count_cards(dic: dict) -> dict:
    card_count_dic = {}
    for key in dic.keys():
        if key in ['Flop', 'Turn', 'River', 'Win', 'My Cards']:
            if key in ['Flop', 'Win', 'My Cards']:
                lst = [item for sublist in dic[key]['Cards'] for item in sublist]
            else:
                lst = dic[key]['Cards']
            card_count_dic[key + ' Count'] = dict(Counter(flatten(data=lst)))
    return card_count_dic


def _build_player_dic(data: dict, matches: list) -> dict:
    player_dic = {}
    for match in matches:
        for player_index in data.keys():
            for key in match.players_data[player_index].player_money_info.keys():
                temp_df = match.players_data[player_index].player_money_info[key]
                if player_index in player_dic.keys():
                    if key not in player_dic[player_index]['Games']:
                        player_dic[player_index]['Player Names'] = list(
                            set(player_dic[player_index]['Player Names'] + temp_df['Player Names'][0]))
                        player_dic[player_index]['Player Ids'] = player_index
                        player_dic[player_index]['Buy in Total'] += int(temp_df['Buy in Total'])
                        player_dic[player_index]['Loss Count'] += temp_df['Loss Count'][0]
                        player_dic[player_index]['Leave Table Amount'] += temp_df['Leave Table Amount'][0]
                        player_dic[player_index]['Game Count'] += 1
                        player_dic[player_index]['Games'].append(key)
                else:
                    player_dic[player_index] = {'Player Names': temp_df['Player Names'][0],
                                                'Player Ids': [player_index],
                                                'Buy in Total': int(temp_df['Buy in Total'][0]),
                                                'Loss Count': temp_df['Loss Count'][0],
                                                'Leave Table Amount': temp_df['Leave Table Amount'][0],
                                                'Game Count': 1, 'Games': [key]}
    return player_dic


def _group_money(data: pd.DataFrame, grouped: Union[list, None], multi: Union[int, None]) -> pd.DataFrame:
    if grouped is not None:
        final_lst = []
        for ind_group in grouped:
            temp_df = data.loc[ind_group]
            temp_dic = {}
            for col in temp_df.columns:
                if col in ['Player Names', 'Player Ids', 'Games']:
                    vals = []
                    for item in list(temp_df[col]):
                        if type(item) == list:
                            vals.append(item)
                        elif type(item) == str:
                            vals.append([item])
                    temp_dic[col] = flatten(data=vals, return_unique=True)
                else:
                    temp_dic[col] = np.sum(temp_df[col])
            final_lst.append(temp_dic)

        grouped_lst = flatten(data=grouped)
        for ind in list(data.index):
            if ind not in grouped_lst:
                temp_dic = {}
                for col in data.columns:
                    val = data.loc[ind][col]
                    if col in ['Player Names', 'Player Ids', 'Games']:
                        if type(val) == list:
                            temp_dic[col] = val
                        elif type(val) == str:
                            temp_dic[col] = [val]
                    else:
                        temp_dic[col] = int(val)
                final_lst.append(temp_dic)
        final_df = pd.DataFrame(final_lst).set_index('Player Ids', drop=False)
    else:
        final_df = data

    final_df['Profit'] = final_df['Leave Table Amount'] - final_df['Buy in Total']
    if multi:
        final_df['Buy in Total'] = (final_df['Buy in Total'] / 100).astype(int)
        final_df['Leave Table Amount'] = (final_df['Leave Table Amount'] / 100).astype(int)
        final_df['Profit'] = (final_df['Profit'] / 100).astype(int)
    return final_df.sort_values('Profit', ascending=False)


def _get_dist(matches: list) -> List[pd.DataFrame]:
    hand_ind = flatten(data=[list(match.winning_hand_distribution.keys()) for match in matches], return_unique=True)
    hand_dic = {item: 0 for item in hand_ind}
    card_dic = {item: {} for item in ['Flop Count', 'Turn Count', 'River Count', 'Win Count', 'My Cards Count']}
    for match in matches:
        for key, val in match.winning_hand_distribution.items():
            hand_dic[key] += val
        for item in card_dic.keys():
            if item in match.card_distribution.keys():
                for key, val in match.card_distribution[item].items():
                    if key in card_dic[item].keys():
                        card_dic[item][key] += val
                    else:
                        card_dic[item][key] = val

    card_distribution = pd.DataFrame.from_dict(card_dic).dropna()
    for col in card_distribution.columns:
        s = np.sum(card_distribution[col])
        arr = np.around([val / s if val != 0 else 0 for val in card_distribution[col]], 3)
        card_distribution[col.replace("Count", "Percent")] = arr

    winning_hand_dist = pd.DataFrame.from_dict(hand_dic,
                                               orient='index',
                                               columns=['Count']).sort_values('Count', ascending=False)
    winning_hand_dist['Percent'] = (winning_hand_dist / winning_hand_dist.sum()).round(3)
    return [card_distribution, winning_hand_dist]


def _build_players(data: dict, money_df: pd.DataFrame) -> None:
    for key1, val1 in data.items():
        for i, j in enumerate(money_df['Player Ids']):
            if key1 in j:
                val1.player_index = j
                val1.player_name = list(money_df['Player Names'])[i]

        for key2, val2 in val1.moves_dic.items():
            val1.win_percent = [key2, round(len((val2[val2['Win'] is True])) / len(val2), 3)]
            val1.win_count = [key2, len(val2[val2['Win'] is True])]
            val1.largest_win = [key2, np.max(val2[val2['Win'] is True]['Win Stack'])]
            lst = list(val2[val2['Class'] == 'Player Stacks']['Player Reserve'])
            temp = 0
            for i, j in enumerate(lst):
                if i > 1:
                    previous = lst[i - 1]
                    if j - previous < temp:
                        temp = j - previous
            val1.largest_loss = [key2, temp]
            val1.hand_count = [key2, np.max(val2['Round'])]
            val1.all_in = [key2, int(np.nan_to_num(np.mean(val2[val2['All In'] is True]['Bet Amount'])))]


def _combine_dic(data: dict, grouped: list) -> dict:
    completed_lst = []
    completed_dic = {}
    for key1, val in data.items():
        for gr in grouped:
            if key1 in gr and key1 not in completed_lst:
                completed_lst += gr
                for key2 in gr:
                    if key2 != key1:
                        for key3 in data[key2].win_percent.keys():
                            data[key1].win_percent = [key3, data[key2].win_percent[key3]]
                            data[key1].win_count = [key3, data[key2].win_count[key3]]
                            data[key1].largest_win = [key3, data[key2].largest_win[key3]]
                            data[key1].largest_loss = [key3, data[key2].largest_loss[key3]]
                            data[key1].hand_count = [key3, data[key2].hand_count[key3]]
                            data[key1].all_in = [key3, data[key2].all_in[key3]]
                            data[key1].player_money_info = [key3, data[key2].player_money_info[key3]]
                            data[key1].hand_dic = [key3, data[key2].hand_dic[key3]]
                            data[key1].card_dic = [key3, data[key2].card_dic[key3]]
                            data[key1].line_dic = [key3, data[key2].line_dic[key3]]
                            data[key1].moves_dic = [key3, data[key2].moves_dic[key3]]
                    completed_dic[key1] = data[key1]
        if key1 not in flatten(data=grouped):
            completed_dic[key1] = data[key1]
    return completed_dic
