from typing import List, Optional, Union
from dataclasses import dataclass
import pandas as pd
import datetime
from os import walk
import csv
from poker.base import flatten, unique_values, round_to, native_max
from poker.game_class import Game


# def _poker_convert_shape(data: List[str]) -> list:
#     """Converts card icons into shapes"""
#     return [row.replace("â£", " Clubs").replace("â¦", " Diamonds").replace("â¥", " Hearts").replace("â", " Spades") for row in data]
#
#
# def _poker_convert_timestamp(data: List[str]) -> list:
#     """Converts strs to timestamps"""
#     return [datetime.datetime.strptime(i.replace('T', ' ').split('.')[0], '%Y-%m-%d %H:%M:%S') for i in data]


def _convert(data: List[str], dic: dict):
    dic['Event'].append(data[0].replace("â£", " Clubs").replace("â¦", " Diamonds").replace("â¥", " Hearts").replace("â", " Spades"))
    dic['Time'].append(datetime.datetime.strptime(data[1].replace('T', ' ').split('.')[0], '%Y-%m-%d %H:%M:%S'))


def rev(lst: list) -> list:
    lst.reverse()
    return lst


def _get_rows(file: str) -> dict:
    dic = {'Event': [], 'Time': []}
    with open(file, 'r', encoding='latin1') as file:
        my_reader = csv.reader(file, delimiter=',')
        for ind, row in enumerate(my_reader):
            if ind > 0:
                _convert(data=row, dic=dic)
    dic['Event'], dic['Time'] = rev(dic['Event']), rev(dic['Time'])
    return dic


def _poker_collect_data(repo_location: str) -> dict:
    """Open file, clean data and return a dict"""
    files, file_dic = next(walk(repo_location))[2], {}
    for file in files:
        temp, v, t, d = [], [], [], _get_rows(file=repo_location + file)
        for ind, val in enumerate(d['Event']):
            if ' starting hand ' in val:
                if ' hand #1 ' in val:
                    temp.append({'lines': v, 'times': t})
                v, t = [val], [d['Time'][ind]]
                temp.append({'lines': v, 'times': t})
            else:
                v.append(val), t.append(d['Time'][ind])
        file_dic[file.split(".")[0]] = temp
    return file_dic


def _poker_build_player_dic(data: dict, matches: list) -> dict:
    """Updates Player Class"""
    player_dic = {}
    for match in matches:
        for player_index in data.keys():
            for key in match.players_data[player_index].player_money_info.keys():
                temp_df = match.players_data[player_index].player_money_info[key]
                if player_index in player_dic.keys():
                    if key not in player_dic[player_index]['Games']:
                        val = player_dic[player_index]
                        val['Player Names'] = list(set(val['Player Names'] + list(temp_df['Player Names'][0])))
                        val['Player Ids'] = list(set(val['Player Ids'] + [player_index]))
                        val['Buy in Total'] += int(temp_df['Buy in Total'])
                        val['Loss Count'] += int(temp_df['Loss Count'][0])
                        val['Leave Table Amount'] += temp_df['Leave Table Amount'][0]
                        val['Game Count'] += 1
                        val['Games'].append(key)
                else:
                    player_dic[player_index] = {'Player Names': list(temp_df['Player Names'][0]),
                                                'Player Ids': [player_index],
                                                'Buy in Total': int(temp_df['Buy in Total'][0]),
                                                'Loss Count': int(temp_df['Loss Count'][0]),
                                                'Leave Table Amount': temp_df['Leave Table Amount'][0],
                                                'Game Count': 1,
                                                'Games': [key]}
    return player_dic


def _poker_group_money(data: dict, grouped: Optional[Union[list, dict]] = None, multi: int = None) -> pd.DataFrame:
    """Groups players by id and tally's earnings"""
    data, g = pd.DataFrame.from_dict(data, orient='index'), tuple(grouped.values())
    g_unique, all_ids = {k: True for i in g for k in i}, tuple(unique_values(data=list(data.index)))
    if grouped is not None:
        final_lst = []
        for player_id in all_ids:
            if player_id in g_unique:
                for key, val in grouped.items():
                    if player_id in {i: True for i in val}:
                        ind_group = list(grouped[key])
                        break

            else:
                ind_group = player_id

        # for ind_group in g:
            temp_df, temp_dic = data.loc[ind_group], {}
            if isinstance(temp_df, pd.DataFrame):
                col_lst = tuple(temp_df.columns)
            else:
                col_lst = tuple(temp_df.index)
            for col in col_lst:
                if col in ['Player Names', 'Player Ids', 'Games']:
                    vals = []
                    for i in tuple(temp_df[col]):
                        if isinstance(i, list):
                            vals.append(i)
                        elif isinstance(i, str):
                            vals.append([i])
                    temp_dic[col] = unique_values(data=flatten(data=vals))
                else:
                    if isinstance(temp_df, pd.DataFrame):
                        temp_dic[col] = sum(temp_df[col])
                    else:
                        temp_dic[col] = temp_df[col]
            final_lst.append(temp_dic)
        final_df = pd.DataFrame(final_lst).set_index('Player Ids', drop=False)
    else:
        final_df = data

    final_df['Profit'] = final_df['Leave Table Amount'] - final_df['Buy in Total']
    if multi:
        final_df['Buy in Total'] = (final_df['Buy in Total'] / 100).astype(int)
        final_df['Leave Table Amount'] = (final_df['Leave Table Amount'] / 100).astype(int)
        final_df['Profit'] = (final_df['Profit'] / 100).astype(int)
    final_df['str'] = [str(i) for i in final_df['Player Names']]
    final_df = final_df.sort_values('Profit', ascending=False).drop_duplicates('str')[['Player Names', 'Player Ids',
                                                                                       'Buy in Total', 'Loss Count',
                                                                                       'Leave Table Amount', 'Profit',
                                                                                       'Game Count',  'Games']]
    return final_df.reset_index(drop=True)


def _poker_get_dist(matches: list) -> List[pd.DataFrame]:
    """Calculate distributions"""
    hand_ind = unique_values(data=flatten(data=[list(match.winning_hand_distribution.keys()) for match in matches]))
    hand_dic = {item: 0 for item in hand_ind}
    card_dic = {item: {} for item in ('Flop Count', 'Turn Count', 'River Count', 'Win Count', 'My Cards Count')}
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

    c_dist = pd.DataFrame.from_dict(card_dic).dropna()
    for col in c_dist.columns:
        s = sum(c_dist[col].tolist())
        c_dist[col.replace("Count", "Percent")] = round_to(data=[val / s if val != 0 else 0 for val in c_dist[col]], val=1000, remainder=True)

    w_dist = pd.DataFrame.from_dict(hand_dic, orient='index', columns=['Count']).sort_values('Count', ascending=False)
    w_dist['Percent'] = (w_dist / w_dist.sum()).round(3)
    return [c_dist, w_dist]


def _poker_build_players(data: dict, money_df: pd.DataFrame) -> None:
    """Update Player Class"""
    for key1, val1 in data.items():
        for i, j in enumerate(money_df['Player Ids']):
            if key1 in j:
                val1.player_index = j
                val1.player_name = list(money_df['Player Names'])[i]

        for key2, val2 in val1.moves_dic.items():
            val1.win_percent = [key2, round(len((val2[val2['Win'] == True])) / len(val2), 3)]
            val1.win_count = [key2, len(val2[val2['Win'] == True])]
            val1.largest_win = [key2, native_max(data=val2[val2['Win'] == True]['Win Stack'])]
            temp_df = val2[val2['Class'] == 'Player Stacks']
            temp_player_index_lst = temp_df['Player Index'].tolist()
            temp_player_stack_lst = temp_df['Player Current Chips'].tolist()
            index_lst = []
            for i in temp_player_index_lst:
                for j in i:
                    if key1 == j:
                        index_lst.append(i.index(key1))
            temp = 0
            for i, j in enumerate(temp_player_stack_lst):
                val = j[index_lst[i]]
                if val > 1:
                    previous = temp_player_stack_lst[i - 1][index_lst[i - 1]]
                    if val - previous < temp:
                        temp = val - previous
            val1.largest_loss = [key2, temp]
            val1.hand_count = [key2, max(val2['Round'].tolist())]
            val1.all_in = [key2, list(val2[val2['All In'] == True]['Bet Amount'])]


def _poker_combine_dic(data: dict, grouped: Union[list, dict]) -> dict:
    """Setter function"""
    c_dic, dic, n_dic = {}, {}, {}
    for key, val in grouped.items():
        val = {i: True for i in val}
        for key1, val1 in data.items():
            if key1 in val and key1 not in c_dic:
                c_dic[key1] = True
                if key not in n_dic:
                    n_dic[key], dic[key] = True, data[key1]
                else:
                    for match in data[key1].win_percent.keys():
                        dic[key].win_percent = [match, data[key1].win_percent[match]]
                        dic[key].win_count = [match, data[key1].win_count[match]]
                        dic[key].largest_win = [match, data[key1].largest_win[match]]
                        dic[key].largest_loss = [match, data[key1].largest_loss[match]]
                        dic[key].hand_count = [match, data[key1].hand_count[match]]
                        dic[key].all_in = [match, data[key1].all_in[match]]
                        dic[key].player_money_info = [match, data[key1].player_money_info[match]]
                        dic[key].hand_dic = [match, data[key1].hand_dic[match]]
                        dic[key].card_dic = [match, data[key1].card_dic[match]]
                        dic[key].line_dic = [match, data[key1].line_dic[match]]
                        dic[key].moves_dic = [match, data[key1].moves_dic[match]]
    for key, val in data.items():
        if key not in c_dic:
            c_dic[key], dic[key] = True, data[key]
    return dic


def _poker_add_merged_moves(player_dic: dict):
    """Flattens all Player.moves_dic into one"""
    for key, val in player_dic.items():
        if player_dic[key].merged_moves is None:
            player_dic[key].merged_moves = {}
        all_dic, win_dic, loss_dic = {}, {}, {}
        for key1, val1 in val.moves_dic.items():
            for key2, val2 in val1.to_dict(orient='list').items():
                if key2 in all_dic.keys():
                    all_dic[key2] += val2
                else:
                    all_dic[key2] = val2
        player_dic[key].merged_moves['All'] = all_dic
        for key1, val1 in val.moves_dic.items():
            for key2, val2 in val1[val1['Win'] == True].to_dict(orient='list').items():
                if key2 in win_dic.keys():
                    win_dic[key2] += val2
                else:
                    win_dic[key2] = val2
        player_dic[key].merged_moves['Win'] = win_dic
        for key1, val1 in val.moves_dic.items():
            for key2, val2 in val1[val1['Win'] == False].to_dict(orient='list').items():
                if key2 in loss_dic.keys():
                    loss_dic[key2] += val2
                else:
                    loss_dic[key2] = val2
        player_dic[key].merged_moves['Loss'] = loss_dic


@dataclass
class Poker:
    """

    Calculate stats for all games and players.

    :param repo_location: Location of data folder.
    :type repo_location: str
    :param grouped: List of lists, filled with unique player Ids that are related to the same person. *Optional*
    :type grouped: Union[list, dict]
    :param money_multi: Multiple to divide the money amounts to translate them to dollars *Optional*
    :type money_multi: int
    :example:
        >>> from poker.poker_class import Poker
        >>> repo = 'location of your previous game'
        >>> grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
        >>>             ['48QVRRsiae', 'u8_FUbXpAz']]
        >>> poker = Poker(repo_location=repo, grouped=grouped)
    :note: Grouped will need to be figured out by the player.
        The grouped stats are only taken into account within this class

    """

    __slots__ = ('repo_location', 'files', 'matches', 'player_money_df', 'card_distribution', 'winning_hand_dist',
                 'players')

    def __init__(self, repo_location: str, grouped: Optional[Union[list, dict]] = None, money_multi: int = 100):
        self.repo_location = repo_location
        x = _poker_collect_data(repo_location=repo_location)
        self.files = tuple(x.keys())
        players_data = {}
        self.matches = {file: Game(hand_lst=x[file], file_id=file, players_data=players_data) for file in self.files}
        player_dic = _poker_build_player_dic(data=players_data, matches=list(self.matches.values()))
        self.player_money_df = _poker_group_money(data=player_dic, grouped=grouped, multi=money_multi)
        self.card_distribution, self.winning_hand_dist = _poker_get_dist(matches=list(self.matches.values()))
        _poker_build_players(data=players_data, money_df=self.player_money_df)
        self.players = _poker_combine_dic(data=players_data, grouped=grouped)
        _poker_add_merged_moves(player_dic=self.players)

    def __repr__(self):
        return "Poker"
