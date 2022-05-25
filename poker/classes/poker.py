from typing import Optional, Union
from dataclasses import dataclass
import pandas as pd
import datetime
from classes.data import Data
from classes.player import Player
from utils.class_functions import _str_nan, _get_attributes, _get_percent
from utils.base import unique_values


def _get_players(grouped: dict, events: tuple, threshold: int = 20) -> dict:
    my_ids = {i: True for i in grouped[list(grouped.keys())[0]]}
    id_dic = {i: [] for k, v in grouped.items() for i in v}
    id_check = {i: True for k, v in grouped.items() for i in v}
    id_game_dic = {i: set() for k, v in grouped.items() for i in v}
    id_win_dic = {i: {} for k, v in grouped.items() for i in v}
    for i in events:
        if i.event == 'MyCards':
            for name in i.starting_players.keys():
                if name in my_ids:
                    id_dic[name].append(i)
                    break
        else:
            if _str_nan(i.player_index) and i.player_index in id_check:
                id_dic[i.player_index].append(i)
                id_game_dic[i.player_index].add(i.game_id)
            elif _str_nan(i.player_index) and i.player_index not in id_check:
                id_dic[i.player_index], id_check[i.player_index], id_game_dic[i.player_index] = [i], True, {i.game_id}
            else:
                for p in i.starting_players.keys():
                    id_dic[p].append(i)
        if i.event == 'Wins':
            for _id in i.winner:
                if _id not in id_win_dic:
                    id_win_dic[_id] = {}
                for k, v in i.current_chips.items():
                    if k in id_win_dic[_id]:
                        id_win_dic[_id][k].append(v - i.starting_chips[k])
                    else:
                        id_win_dic[_id][k] = [v - i.starting_chips[k]]

    player_dic, player_check = {}, {i: True for k, v in grouped.items() for i in v}
    for name, vals in grouped.items():
        player_dic[name] = {'ids': set(), 'games': set(), 'events': [], 'beat': {}}
        for _id in vals:
            player_dic[name]['ids'].add(_id)
            player_dic[name]['events'] += id_dic[_id]
            for k, v in id_win_dic[_id].items():
                if k in player_dic[name]['beat']:
                    player_dic[name]['beat'][k] += v
                else:
                    player_dic[name]['beat'][k] = v
            for i in id_game_dic[_id]:
                player_dic[name]['games'].add(i)

    for _id, vals in id_dic.items():
        if _id not in player_check:
            player_dic[_id] = {'ids': set(), 'games': set(), 'events': vals, 'beat': {}}
            player_dic[_id]['ids'].add(_id)
            if _id in id_win_dic:
                for k, v in id_win_dic[_id].items():
                    if k in player_dic[name]['beat']:
                        player_dic[name]['beat'][k] += v
                    else:
                        player_dic[name]['beat'][k] = v
            for i in id_game_dic[_id]:
                player_dic[_id]['games'].add(i)

    # Check who beat who and group names
    for k, v in player_dic.items():
        temp = {}
        for k1, v1 in v['beat'].items():
            for name, vals in grouped.items():
                temp[name] = []
                for _id in vals:
                    if _id in v['beat']:
                        temp[name] += v['beat'][_id]
            if k1 not in player_check:
                temp[k1] = v1
        player_dic[k]['beat'] = {k1: tuple(v1) for k1, v1 in temp.items()}

    return {k: Player(dic=v, name=k) for k, v in player_dic.items() if len(v['events']) >= threshold}


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
        >>> from classes.poker import Poker
        >>> repo = 'location of your previous game'
        >>> grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
        >>>             ['48QVRRsiae', 'u8_FUbXpAz']]
        >>> poker = Poker(repo_location=repo, grouped=grouped)
    :note: Grouped will need to be figured out by the player.
        The grouped stats are only taken into account within this class

    """

    __slots__ = ('repo_location', 'matches', 'player_money_df', 'card_distribution', 'winning_hand_dist',
                 'players', 'events', 'multi', 'win_matrix')

    def __init__(self, repo_location: str, grouped: Optional[Union[list, dict]] = None, money_multi: int = 100,
                 threshold: int = 20):
        self.repo_location = repo_location
        self.multi = money_multi
        self.events, self.matches = Data(repo_location=repo_location).items()
        self.players = _get_players(grouped=grouped, events=self.events, threshold=threshold)
        self.winning_hand_dist = _get_dist(self.events, 'Wins', 'winning_hand')
        self.card_distribution = _get_dist(self.events, 'PlayerStacks', 'cards')
        self.player_money_df = None
        self.win_matrix = None

    def __repr__(self):
        return "Poker"

    def events_to_df(self) -> pd.DataFrame:
        """creates a dataframe from event objects"""
        return pd.DataFrame([_get_attributes(val=i) for i in self.events])

    def players_to_df(self) -> pd.DataFrame:
        """creates a dataframe from event objects"""
        return pd.DataFrame([_get_attributes(val=v) for k, v in self.players.items()])

    def total_return_df(self, multi: int = None) -> pd.DataFrame:
        """Total return from all players"""
        if multi is None:
            multi = self.multi
        dic = {'Name': [], 'Player Names': [], 'Player Indexes': [], 'Buy In Amount': [], 'Leave Table Amount': [],
               'Profit': [], 'Game Count': [], 'Play Time': [], 'Profit Per Hour': []}
        for k, v in self.players.items():
            dic['Name'].append(k), dic['Game Count'].append(len(v.games)), dic['Player Names'].append(v.player_names), dic['Player Indexes'].append(v.player_indexes)
            dic['Buy In Amount'].append(sum(val for k1, v1 in v.money['approved'].items() for val in v1) / multi)
            temp = sum(val for k1, v1 in v.money['joined'].items() for val in v1) / multi
            dic['Leave Table Amount'].append(sum(val for k1, v1 in v.money['leaves'].items() for val in v1) / multi - temp)
            dic['Profit'].append(dic['Leave Table Amount'][-1] - dic['Buy In Amount'][-1])
            temp = sum(val for k1, v1 in v.money['time'].items() for val in v1)
            dic['Play Time'].append(str(datetime.timedelta(seconds=temp)))
            dic['Profit Per Hour'].append(round(dic['Profit'][-1] / (temp / 60 / 60), 2))
        self.player_money_df = pd.DataFrame.from_dict(dic).set_index('Name').sort_values('Profit', ascending=False)
        return self.player_money_df

    def win_matrix_df(self) -> pd.DataFrame:
        """
        How much you have taken from other players, negative is good.
        Positive means some of your wins were pot splits and the other person ended up winning even when you won.
        """
        dic = {k: [] for k, v in self.players.items()}
        dic['Name'] = []
        for k, v in self.players.items():
            dic['Name'].append(k)
            for k1, v1 in self.players.items():
                if k == k1:
                    dic[k1].append(None)
                else:
                    if k1 in v.win_matrix:
                        dic[k1].append(_get_percent(sum(v.win_matrix[k1]), self.multi, None))
                    else:
                        dic[k1].append(None)
        self.win_matrix = pd.DataFrame.from_dict(dic).set_index('Name')
        return self.win_matrix