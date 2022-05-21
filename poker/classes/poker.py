from typing import List, Optional, Union
from dataclasses import dataclass
import pandas as pd
import datetime
from poker.utils.base import flatten, unique_values, round_to, native_max
from poker.classes.data import Data
from poker.classes.player import Player
from poker.utils.class_functions import _str_nan, _get_attributes
from poker.utils.base import unique_values


# def _poker_build_player_dic(data: dict, matches: list) -> dict:
#     """Updates Player Class"""
#     player_dic = {}
#     for match in matches:
#         for player_index in data.keys():
#             for key in match.players_data[player_index].player_money_info.keys():
#                 temp_df = match.players_data[player_index].player_money_info[key]
#                 if player_index in player_dic.keys():
#                     if key not in player_dic[player_index]['Games']:
#                         val = player_dic[player_index]
#                         val['Player Names'] = list(set(val['Player Names'] + list(temp_df['Player Names'][0])))
#                         val['Player Ids'] = list(set(val['Player Ids'] + [player_index]))
#                         val['Buy in Total'] += int(temp_df['Buy in Total'])
#                         val['Loss Count'] += int(temp_df['Loss Count'][0])
#                         val['Leave Table Amount'] += temp_df['Leave Table Amount'][0]
#                         val['Game Count'] += 1
#                         val['Games'].append(key)
#                 else:
#                     player_dic[player_index] = {'Player Names': list(temp_df['Player Names'][0]),
#                                                 'Player Ids': [player_index],
#                                                 'Buy in Total': int(temp_df['Buy in Total'][0]),
#                                                 'Loss Count': int(temp_df['Loss Count'][0]),
#                                                 'Leave Table Amount': temp_df['Leave Table Amount'][0],
#                                                 'Game Count': 1,
#                                                 'Games': [key]}
#     return player_dic



# def _poker_get_dist(matches: list) -> List[pd.DataFrame]:
#     """Calculate distributions"""
#     hand_ind = unique_values(data=flatten(data=[list(match.winning_hand_distribution.keys()) for match in matches]))
#     hand_dic = {item: 0 for item in hand_ind}
#     card_dic = {item: {} for item in ('Flop Count', 'Turn Count', 'River Count', 'Win Count', 'My Cards Count')}
#     for match in matches:
#         for key, val in match.winning_hand_distribution.items():
#             hand_dic[key] += val
#         for item in card_dic.keys():
#             if item in match.card_distribution.keys():
#                 for key, val in match.card_distribution[item].items():
#                     if key in card_dic[item].keys():
#                         card_dic[item][key] += val
#                     else:
#                         card_dic[item][key] = val
#     c_dist = pd.DataFrame.from_dict(card_dic).dropna()
#     for col in c_dist.columns:
#         s = sum(c_dist[col].tolist())
#         c_dist[col.replace("Count", "Percent")] = round_to(data=[val / s if val != 0 else 0 for val in c_dist[col]], val=1000, remainder=True)
#
#     w_dist = pd.DataFrame.from_dict(hand_dic, orient='index', columns=['Count']).sort_values('Count', ascending=False)
#     w_dist['Percent'] = (w_dist / w_dist.sum()).round(3)
#     return [c_dist, w_dist]


def _get_players(grouped: dict, events: tuple, threshold: int = 20) -> dict:
    my_ids = {i: True for i in grouped[list(grouped.keys())[0]]}
    id_dic, id_check = {i: [] for k, v in grouped.items() for i in v}, {i: True for k, v in grouped.items() for i in v}
    for i in events:
        if i.event == 'MyCards':
            for name in i.starting_players.keys():
                if name in my_ids:
                    id_dic[name].append(i)
                    break
        else:
            if _str_nan(i.player_index) and i.player_index in id_check:
                id_dic[i.player_index].append(i)
            elif _str_nan(i.player_index) and i.player_index not in id_check:
                id_dic[i.player_index], id_check[i.player_index] = [i], True
            else:
                for p in i.starting_players.keys():
                    id_dic[p].append(i)

    player_dic, player_check = {}, {i: True for k, v in grouped.items() for i in v}
    for name, vals in grouped.items():
        player_dic[name] = []
        for _id in vals:
            player_dic[name] += id_dic[_id]


    for _id, vals in id_dic.items():
        if _id not in player_check:
            player_dic[_id] = vals
    return {k: Player(data=v, name=k) for k, v in player_dic.items() if len(v) >= threshold}


def _get_dist(lst: Union[list, tuple], e: str, criteria: str) -> dict:
    vals, count = [], 0
    if criteria == 'winning_hand':
        for i in lst:
            if i.event == e and i.winning_hand is not None:
                vals.append(i.winning_hand)
                count += 1
    elif criteria == 'cards':
        for i in lst:
            if i.event == e and i.cards is not None:
                for c in i.cards:
                    vals.append(c)
                    count += 1
    vals = unique_values(data=vals, count=True)
    return {k: (v, round(v / count, 3)) for k, v in vals.items()}


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

    __slots__ = ('repo_location', 'matches', 'player_money_df', 'card_distribution', 'winning_hand_dist',
                 'players', 'events', 'multi')

    def __init__(self, repo_location: str, grouped: Optional[Union[list, dict]] = None, money_multi: int = 100,
                 threshold: int = 20):
        self.repo_location = repo_location
        self.multi = money_multi
        self.events, self.matches = Data(repo_location=repo_location).items()
        self.players = _get_players(grouped=grouped, events=self.events, threshold=threshold)
        self.winning_hand_dist = _get_dist(self.events, 'Wins', 'winning_hand')
        self.card_distribution = _get_dist(self.events, 'PlayerStacks', 'cards')
        self.player_money_df = None

    def __repr__(self):
        return "Poker"

    def events_to_df(self) -> pd.DataFrame:
        """creates a dataframe from event objects"""
        return pd.DataFrame([_get_attributes(val=i) for i in self.events])

    def players_to_df(self) -> pd.DataFrame:
        """creates a dataframe from event objects"""
        return pd.DataFrame([_get_attributes(val=v) for k, v in self.players.items()])

    def total_return_df(self, multi: int = None) -> pd.DataFrame:
        if multi is None:
            multi = self.multi
        dic = {'Name': [], 'Player Names': [], 'Player Indexes': [], 'Buy In Amount': [], 'Leave Table Amount': [],
               'Profit': [], 'Game Count': [], 'Play Time': [], 'Profit Per Hour': []}
        for k, v in self.players.items():
            dic['Name'].append(k)
            dic['Game Count'].append(len(v.games))
            dic['Player Names'].append(v.player_names)
            dic['Player Indexes'].append(v.player_indexes)
            lst = []
            for k1, v1 in v.money['approved'].items():
                for val in v1:
                    lst.append(val)
            dic['Buy In Amount'].append(sum(lst) / multi)
            lst = []
            for k1, v1 in v.money['joined'].items():
                for val in v1:
                    lst.append(val)
            temp = sum(lst) / multi
            lst = []
            for k1, v1 in v.money['leaves'].items():
                for val in v1:
                    lst.append(val)
            dic['Leave Table Amount'].append(sum(lst) / multi - temp)
            dic['Profit'].append(dic['Leave Table Amount'][-1] - dic['Buy In Amount'][-1])
            lst = []
            for k1, v1 in v.money['time'].items():
                for val in v1:
                    lst.append(val)
            dic['Play Time'].append(str(datetime.timedelta(seconds=sum(lst))))
            dic['Profit Per Hour'].append(round(dic['Profit'][-1] / (sum(lst) / 60 / 60), 2))
        self.player_money_df = pd.DataFrame.from_dict(dic).set_index('Name').sort_values('Profit', ascending=False)
        return self.player_money_df
