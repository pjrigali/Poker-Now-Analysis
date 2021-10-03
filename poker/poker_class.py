from typing import List, Optional, Union
from dataclasses import dataclass
import pandas as pd
import datetime
from os import walk
from poker.base import flatten, unique_values, round_to, native_max
from poker.game_class import Game


def _poker_convert_shape(data: List[str]) -> list:
    """Converts card icons into shapes"""
    return [row.replace("â£", " Clubs").replace("â¦", " Diamonds").replace("â¥", " Hearts").replace("â", " Spades") for row in data]


def _poker_convert_timestamp(data: List[str]) -> list:
    """Converts strs to timestamps"""
    return [datetime.datetime.strptime(i.replace('T', ' ').split('.')[0], '%Y-%m-%d %H:%M:%S') for i in data]


def _poker_collect_data(repo_location: str) -> dict:
    """Open file, clean data and return a dict"""
    files = next(walk(repo_location))[2]
    file_dic = {}
    for file in files:
        df = pd.read_csv(repo_location + file, encoding='latin1')
        time_lst = _poker_convert_timestamp(data=df['at'].tolist())
        entry_lst = _poker_convert_shape(data=df['entry'].tolist())
        time_lst.reverse()
        entry_lst.reverse()
        hands, hand_lst = [], []
        for ind, item in enumerate(entry_lst):
            if ' starting hand ' in item:
                if ' hand #1 ' in item:
                    hands.append(hand_lst)
                hand_lst = [ind]
                hands.append(hand_lst)
            else:
                hand_lst.append(ind)
        hand_dic = []
        for hand in hands:
            temp_entry_lst, temp_time_lst = [], []
            for ind in hand:
                temp_entry_lst.append(entry_lst[ind]), temp_time_lst.append(time_lst[ind])
            hand_dic.append({'lines': temp_entry_lst, 'times': temp_time_lst})
        file_dic[file.split(".")[0]] = hand_dic
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


def _poker_group_money(data: dict, grouped: Union[list, None], multi: Union[int, None]) -> pd.DataFrame:
    """Groups players by id and tally's earnings"""
    data = pd.DataFrame.from_dict(data, orient='index')
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
                    temp_dic[col] = unique_values(data=flatten(data=vals))
                else:
                    temp_dic[col] = sum(temp_df[col].tolist())
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
    return final_df.sort_values('Profit', ascending=False).reset_index(drop=True)


def _poker_get_dist(matches: list) -> List[pd.DataFrame]:
    """Calculate distributions"""
    hand_ind = unique_values(data=flatten(data=[list(match.winning_hand_distribution.keys()) for match in matches]))
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
        s = sum(card_distribution[col].tolist())
        arr = round_to(data=[val / s if val != 0 else 0 for val in card_distribution[col]], val=1000, remainder=True)
        card_distribution[col.replace("Count", "Percent")] = arr

    winning_hand_dist = pd.DataFrame.from_dict(hand_dic,
                                               orient='index',
                                               columns=['Count']).sort_values('Count', ascending=False)
    winning_hand_dist['Percent'] = (winning_hand_dist / winning_hand_dist.sum()).round(3)
    return [card_distribution, winning_hand_dist]


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


def _poker_combine_dic(data: dict, grouped: list) -> dict:
    """Setter function"""
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
    :type grouped: str
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
    def __init__(self, repo_location: str, grouped: Optional[list] = None, money_multi: Optional[int] = 100):
        self._repo_location = repo_location

        self._grouped = None
        if grouped:
            self._grouped = grouped

        game_hand_time_lst_dic = _poker_collect_data(repo_location=repo_location)
        self._files = list(game_hand_time_lst_dic.keys())
        players_data = {}
        self._matches = {file: Game(hand_lst=game_hand_time_lst_dic[file], file_id=file, players_data=players_data) for file in self._files}
        player_dic = _poker_build_player_dic(data=players_data, matches=list(self._matches.values()))
        self._player_money_df = _poker_group_money(data=player_dic, grouped=self._grouped, multi=money_multi)
        self._card_distribution, self._winning_hand_dist = _poker_get_dist(matches=list(self._matches.values()))
        _poker_build_players(data=players_data, money_df=self._player_money_df)
        self._players = _poker_combine_dic(data=players_data, grouped=self._grouped)
        _poker_add_merged_moves(player_dic=self._players)

    def __repr__(self):
        return "Poker"

    @property
    def files(self) -> List[str]:
        """Returns list of data files"""
        return self._files

    @property
    def matches(self) -> dict:
        """Returns list of games"""
        return self._matches

    @property
    def players_money_overview(self) -> pd.DataFrame:
        """Returns summary info for each player across games"""
        return self._player_money_df

    @property
    def card_distribution(self) -> pd.DataFrame:
        """Returns count and percent for each card that showed up across games"""
        return self._card_distribution

    @property
    def winning_hand_distribution(self) -> pd.DataFrame:
        """Returns count and percent of each type of winning hand across games"""
        return self._winning_hand_dist

    @property
    def players_history(self) -> dict:
        """Collects player stats for all matches and groups based on grouper input"""
        return self._players
