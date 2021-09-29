from typing import List, Optional, Union
from dataclasses import dataclass
import pandas as pd
import numpy as np
import datetime
from os import walk
from collections import Counter
from poker.processor import Approved, MyCards, SmallBlind, BigBlind, Folds, Calls, Raises, Checks, Wins, Shows, Quits
from poker.processor import Flop, Turn, River, Undealt, StandsUp, SitsIn, PlayerStacks, parser
from poker.base import calc_gini, flatten, native_mean, native_mode, unique_values


def _convert_shapes(data: List[str]) -> List[str]:
    """Converts card icons into shapes"""
    return [row.replace("â£", " Clubs").replace("â¦", " Diamonds").replace("â¥", " Hearts").replace("â", " Spades")
            for row in data]


def _get_data(repo_location: str, file: str) -> pd.DataFrame:
    """Load data and parse timestamps"""
    df = pd.read_csv(repo_location + file, encoding='latin1')
    time_lst = df['at'].to_list()
    df['at'] = [datetime.datetime.strptime(i.replace('T', ' ').split('.')[0], '%Y-%m-%d %H:%M:%S') for i in time_lst]
    return df.reindex(index=df.index[::-1]).reset_index(drop=True)


def _get_hands(data: pd.DataFrame) -> List[dict]:
    """Split game into list of hands"""
    data['entry'] = _convert_shapes(data=data['entry'].to_list())
    hands, hand_lst = [], []
    for ind, row in data.iterrows():
        if ' starting hand ' in row['entry']:
            if ' hand #1 ' in row['entry']:
                hands.append(hand_lst)
            hand_lst = [ind]
            hands.append(hand_lst)
        else:
            hand_lst.append(ind)

    dic_lst = []
    for hand in hands:
        temp_df = data.iloc[hand]
        dic_lst.append({'lines': temp_df['entry'].to_list(), 'times': temp_df['at'].to_list()})
    return dic_lst


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
        if line.player_index in line.winner:
            temp_win = True
        if type(line) in [Raises, PlayerStacks, SmallBlind, BigBlind, Wins]:
            lst.append({'Player Index': line.player_index, 'Player Name': line.player_name, 'Bet Amount': line.stack,
                        'Position': line.position, 'Round': line.current_round, 'Player Reserve': line.chips,
                        'Class': repr(line), 'Winner': line.winner, 'Win': temp_win, 'Win Stack': line.win_stack,
                        'Win Hand': line.winning_hand, 'All In': line.all_in, 'Pot Size': line.pot_size,
                        'Remaining Players': line.remaining_players, 'From Person': line.action_from_player,
                        'Game Id': line.game_id})
        else:
            lst.append({'Player Index': line.player_index, 'Player Name': line.player_name,
                        'Bet Amount': line.action_amount, 'Position': line.position, 'Round': line.current_round,
                        'Player Reserve': line.chips, 'Class': repr(line), 'Winner': line.winner, 'Win': temp_win,
                        'Win Stack': line.win_stack, 'Win Hand': line.winning_hand, 'All In': line.all_in,
                        'Pot Size': line.pot_size, 'Remaining Players': line.remaining_players,
                        'From Person': line.action_from_player, 'Game Id': line.game_id})
    return pd.DataFrame(lst).bfill()


def _count_cards(dic: dict) -> dict:
    card_count_dic = {}
    for key in dic.keys():
        if key in ['Flop', 'Turn', 'River', 'Win', 'My Cards']:
            if key in ['Flop', 'Win', 'My Cards']:
                lst = flatten(data=dic[key]['Cards'])
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
            val1.win_percent = [key2, round(len((val2[val2['Win'] == True])) / len(val2), 3)]
            val1.win_count = [key2, len(val2[val2['Win'] == True])]
            val1.largest_win = [key2, np.max(val2[val2['Win'] == True]['Win Stack'])]
            lst = list(val2[val2['Class'] == 'Player Stacks']['Player Reserve'])
            temp = 0
            for i, j in enumerate(lst):
                if i > 1:
                    previous = lst[i - 1]
                    if j - previous < temp:
                        temp = j - previous
            val1.largest_loss = [key2, temp]
            val1.hand_count = [key2, np.max(val2['Round'])]
            # val1.all_in = [key2, int(np.nan_to_num(np.mean(val2[val2['All In'] == True]['Bet Amount'])))]
            val1.all_in = [key2, list(val2[val2['All In'] == True]['Bet Amount'])]


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


def _build_players_data(player_dic: dict, players_data: dict, file_id: str) -> dict:
    player_info_dic = {}
    for key, val in player_dic.items():
        if key not in ['Flop', 'Turn', 'River', 'Win', 'My Cards']:
            player_info_dic[key] = val

    for player_index in player_info_dic.keys():
        val = _calc_money(lst=player_info_dic[player_index]['Lines'], ind=file_id)
        card_dic = dict(Counter([item for sublist in player_info_dic[player_index]['Cards'] for item in sublist]))
        card_df = pd.DataFrame.from_dict(card_dic, orient='index', columns=['Count']).fillna(0.0).astype(int)
        hand_df = pd.DataFrame.from_dict(dict(Counter(player_info_dic[player_index]['Hands'])),
                                         orient='index',
                                         columns=['Count']).sort_values('Count', ascending=False)
        line_dic = player_info_dic[player_index]['Lines']
        if player_index not in players_data.keys():
            players_data[player_index] = Player(player_index=player_index)
        players_data[player_index].line_dic = [file_id, line_dic]
        players_data[player_index].player_money_info = [file_id, val]
        players_data[player_index].hand_dic = [file_id, hand_df]
        players_data[player_index].card_dic = [file_id, card_df]
        players_data[player_index].moves_dic = [file_id, _line_to_df(line_lst=line_dic)]
    return players_data


@dataclass
class Hand:
    """

    Organizes a hand with a class and adds the stands to the player_dic.

    :param lst_hand_objects: A list of Class Objects connected to a hand.
    :type lst_hand_objects: list
    :param file_id: Unique file name.
    :type file_id: str
    :param player_dic: Dict of players.
    :type player_dic: dict
    :example: *None*
    :note: This class is intended to be used internally.

    """
    def __init__(self, lst_hand_objects: list, file_id: str, player_dic: dict):
        self._parsed_hand = lst_hand_objects
        self._small_blind = None
        self._big_blind = None
        self._wins = []
        self._starting_players = None
        self._starting_player_chips = None
        self._flop = None
        self._turn = None
        self._river = None
        self._my_cards = None
        self._total_chips_in_play = None
        self._gini_value = None
        self._pot_size_lst = []

        presser = None
        presser_amount = None
        players_left = []
        winner_lst = []
        winner_line_lst = []
        winner_hand = None
        winner_stack = 0
        for line in self._parsed_hand:
            if type(line) == Wins:
                winner_lst.append(line.player_index)
                if line.winning_hand is not None:
                    winner_hand = line.winning_hand
                if line.stack is not None:
                    winner_stack += line.stack

        for line in self._parsed_hand:
            line_type = type(line)
            self._pot_size_lst.append(line.pot_size)
            line.action_from_player = presser
            line.game_id = file_id
            line.remaining_players = players_left
            line.winner = winner_lst
            line.winning_hand = winner_hand
            line.win_stack = winner_stack
            if line.player_index is not None and self._starting_player_chips is not None:
                if line.player_index in self._starting_player_chips.keys():
                    line.chips = self._starting_player_chips[line.player_index]
            if line_type == SmallBlind:
                presser = line.player_index
                presser_amount = line.stack
                line.action_from_player = presser
                self._small_blind = line
                _add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=line.player_index)
                continue
            elif line_type == BigBlind:
                presser = line.player_index
                presser_amount = line.stack
                line.action_from_player = presser
                self._big_blind = line
                _add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=line.player_index)
                continue
            elif line_type == Wins:
                _add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=line.player_index)
                if line.cards is not None:
                    _add_to_dic(item=line.cards, player_dic=player_dic, location='Cards',
                                player_index=line.player_index)
                    _add_to_dic(item=line.cards, player_dic=player_dic, location='Cards', player_index='Win')
                _add_to_dic(item=line.winning_hand, player_dic=player_dic, location='Hands',
                            player_index=line.player_index)
                _add_to_dic(item=line.winning_hand, player_dic=player_dic, location='Hands', player_index='Win')
                winner_line_lst.append(line)
                continue
            elif line_type == PlayerStacks:
                self._starting_players = dict(zip(line.player_index, line.player_name))
                players_left = line.player_index
                self._starting_player_chips = dict(zip(line.player_index, line.stack))
                self._total_chips_in_play = sum(line.stack)
                self._gini_value = calc_gini(data=line.stack)
                for player in self._starting_players.keys():
                    _add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=player)
                continue
            elif line_type == Flop:
                self._flop = line
                _add_to_dic(item=line.cards, player_dic=player_dic, location='Cards', player_index='Flop')
                presser = None
                presser_amount = None
                continue
            elif line_type == Turn:
                self._turn = line
                _add_to_dic(item=line.cards, player_dic=player_dic, location='Cards', player_index='Turn')
                presser = None
                presser_amount = None
                continue
            elif line_type == River:
                self._river = line
                _add_to_dic(item=line.cards, player_dic=player_dic, location='Cards', player_index='River')
                presser = None
                presser_amount = None
                continue
            elif line_type == MyCards:
                self._my_cards = line
                _add_to_dic(item=line.cards, player_dic=player_dic, location='Cards', player_index='My Cards')
                continue
            elif line_type == Undealt:
                if len(line.cards) == 1:
                    # if self._river is None:
                    #     self._river = River
                    self._river = line.cards[0]
                    _add_to_dic(item=line.cards, player_dic=player_dic, location='Cards', player_index='River')
                elif len(line.cards) == 2:
                    if type(line.cards[0]) == list:
                        turn_val = line.cards[0][0]
                    else:
                        turn_val = line.cards[0]
                    # if self._turn is None:
                    #     self._turn = Turn
                    self._turn = turn_val
                    if type(line.cards[1]) == list:
                        river_val = line.cards[1][0]
                    else:
                        river_val = line.cards[1]
                    # if self._river is None:
                    #     self._river = River
                    self._river = river_val
                    _add_to_dic(item=turn_val, player_dic=player_dic, location='Cards', player_index='Turn')
                    _add_to_dic(item=river_val, player_dic=player_dic, location='Cards', player_index='River')
                else:
                    # if self._flop is None:
                    #     self._flop = Flop
                    self._flop = line.cards[:3]
                    if type(line.cards[3]) == list:
                        turn_val = line.cards[3][0]
                    else:
                        turn_val = line.cards[3]
                    # if self._turn is None:
                    #     self._turn = Turn
                    self._turn = turn_val
                    if type(line.cards[4]) == list:
                        river_val = line.cards[4][0]
                    else:
                        river_val = line.cards[4]
                    # if self._river is None:
                    #     self._river = River
                    self._river = river_val
                    _add_to_dic(item=line.cards[:3], player_dic=player_dic, location='Cards', player_index='Flop')
                    _add_to_dic(item=turn_val, player_dic=player_dic, location='Cards', player_index='Turn')
                    _add_to_dic(item=river_val, player_dic=player_dic, location='Cards', player_index='River')
                continue
            elif line_type == Raises:
                presser = line.player_index
                presser_amount = line.stack
                line.action_from_player = presser
                _add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=line.player_index)
                continue
            elif line_type == Calls:
                line.action_amount = presser_amount
                _add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=line.player_index)
                continue
            elif line_type == Folds:
                line.action_amount = presser_amount
                players_left = [player for player in players_left if player != line.player_index]
                line.remaining_players = players_left
                _add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=line.player_index)
                continue
            elif line_type == StandsUp:
                players_left = [player for player in players_left if player != line.player_index]
                line.remaining_players = players_left
                _add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=line.player_index)
                continue
            elif line_type == Quits:
                players_left = [player for player in players_left if player != line.player_index]
                line.remaining_players = players_left
                _add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=line.player_index)
                continue
            elif line_type in [SitsIn, Shows, Approved, Checks]:
                line.action_amount = 0
                _add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=line.player_index)
                continue

        for winner in winner_line_lst:
            if winner.cards is None:
                for temp_line in self.parsed_hand:
                    if type(temp_line) == Shows and temp_line.player_index == winner.player_index:
                        winner.cards = temp_line.cards
                        _add_to_dic(item=temp_line.cards, player_dic=player_dic, location='Cards', player_index='Win')
                        _add_to_dic(item=temp_line.cards, player_dic=player_dic, location='Cards',
                                    player_index=temp_line.player_index)
                        break

        self._wins = winner_lst
        self._players = player_dic

    def __repr__(self):
        return "Hand " + str(self.parsed_hand[0].current_round)

    @property
    def parsed_hand(self) -> list:
        """Returns a list of actions as objects"""
        return self._parsed_hand

    @property
    def small_blind(self) -> Optional[SmallBlind]:
        """Returns SmallBlind Class"""
        return self._small_blind

    @property
    def big_blind(self) -> Optional[BigBlind]:
        """Returns BigBlind Class"""
        return self._big_blind

    @property
    def winner(self) -> Optional[Union[Wins, List[Wins]]]:
        """Returns Wins Class or list of Wins Classes"""
        return self._wins

    @property
    def starting_players(self) -> Optional[dict]:
        """Returns dict of name and ID for each player that was present at the hand start"""
        return self._starting_players

    @property
    def starting_players_chips(self) -> Optional[dict]:
        """Returns dict of name and stack amount for each player that was present at the hand start"""
        return self._starting_player_chips

    @property
    def flop_cards(self) -> Union[Flop, None]:
        """Returns Flop Class"""
        return self._flop

    @property
    def turn_card(self) -> Union[Turn, None]:
        """Returns Turn Class"""
        return self._turn

    @property
    def river_card(self) -> Union[River, None]:
        """Returns River Class"""
        return self._river

    @property
    def my_cards(self) -> Union[MyCards, None]:
        """Returns MyCards Class"""
        return self._my_cards

    @property
    def chips_on_board(self) -> int:
        """Returns the count of chips on the table"""
        return self._total_chips_in_play

    @property
    def gini_coef(self) -> float:
        """Returns the gini coef for the board"""
        return self._gini_value

    @property
    def pot_size_lst(self) -> List[int]:
        """Returns pot size over course of hand"""
        return self._pot_size_lst

    @property
    def players(self) -> dict:
        """Returns dict of player moves"""
        return self._players


@dataclass
class Player:
    """

    Calculate stats for a player.

    :param player_index: A unique player ID.
    :type player_index: str or List[str]
    :example: *None*
    :note: This class is intended to be used internally.

    """
    def __init__(self, player_index: Union[str, List[str]]):
        if type(player_index) == str:
            self._player_index = [player_index]
        else:
            self._player_index = player_index
        self._other_player_indexes = self._player_index
        self._player_money_dic = {}
        self._hand_dic = {}
        self._card_dic = {}
        self._line_dic = {}
        self._moves_dic = {}
        self._win_percent = {}
        self._win_count = {}
        self._largest_win = {}
        self._largest_loss = {}
        self._hand_count = {}
        self._all_in = {}
        self._player_name = []

    def __repr__(self):
        return str(self._player_name)

    @property
    def win_percent(self) -> dict:
        """Returns player win percent"""
        return self._win_percent

    @win_percent.setter
    def win_percent(self, val):
        self._win_percent[val[0]] = val[1]

    @property
    def win_count(self) -> dict:
        """Returns player win count"""
        return self._win_count

    @win_count.setter
    def win_count(self, val):
        self._win_count[val[0]] = val[1]

    @property
    def largest_win(self) -> dict:
        """Returns players largest win"""
        return self._largest_win

    @largest_win.setter
    def largest_win(self, val):
        self._largest_win[val[0]] = val[1]

    @property
    def largest_loss(self) -> dict:
        """Returns players largest loss"""
        return self._largest_loss

    @largest_loss.setter
    def largest_loss(self, val):
        self._largest_loss[val[0]] = val[1]

    @property
    def hand_count(self) -> dict:
        """Returns total hand count when player involved"""
        return self._hand_count

    @hand_count.setter
    def hand_count(self, val):
        self._hand_count[val[0]] = val[1]

    @property
    def all_in(self) -> dict:
        """Returns a dict documenting when the player went all in"""
        return self._all_in

    @all_in.setter
    def all_in(self, val):
        self._all_in[val[0]] = val[1]

    @property
    def player_index(self) -> List[str]:
        """Returns player index or indexes"""
        return self._player_index

    @player_index.setter
    def player_index(self, val):
        self._player_index = val

    @property
    def player_name(self) -> List[str]:
        """Returns player name or names"""
        return self._player_name

    @player_name.setter
    def player_name(self, val):
        self._player_name = val

    @property
    def player_money_info(self) -> dict:
        """Returns a dict of DataFrames documenting player buy-in and loss counts"""
        return self._player_money_dic

    @player_money_info.setter
    def player_money_info(self, val):
        self._player_money_dic[val[0]] = val[1]

    @property
    def hand_dic(self) -> dict:
        """Returns a dict of DataFrames documenting hands when the player won"""
        return self._hand_dic

    @hand_dic.setter
    def hand_dic(self, val):
        self._hand_dic[val[0]] = val[1]

    @property
    def card_dic(self) -> dict:
        """Returns a dict of DataFrames documenting card appearances"""
        return self._card_dic

    @card_dic.setter
    def card_dic(self, val):
        self._card_dic[val[0]] = val[1]

    @property
    def line_dic(self) -> dict:
        """Returns a dict with a list of objects where player involved"""
        return self._line_dic

    @line_dic.setter
    def line_dic(self, val):
        self._line_dic[val[0]] = val[1]

    @property
    def moves_dic(self) -> dict:
        """Returns a players moves on the table"""
        return self._moves_dic

    @moves_dic.setter
    def moves_dic(self, val):
        self._moves_dic[val[0]] = val[1]


@dataclass
class Game:
    """

    Calculate stats for a game.

    :param hand_lst: List of str's from the csv.
    :type hand_lst: List[str]
    :param file_id: Name of file.
    :type file_id: str
    :param players_data: A dict of player data.
    :type players_data: dict
    :example: *None*
    :note: This class is intended to be used internally.

    """
    def __init__(self, hand_lst: List[dict], file_id: str, players_data: dict):
        self._file_id = file_id
        player_dic = {}
        self._parsed_hands = [Hand(lst_hand_objects=[line for line in parser(lines=hand['lines'], times=hand['times'])],
                                   file_id=file_id, player_dic=player_dic) for hand in hand_lst]
        self._players_data = _build_players_data(player_dic=player_dic, players_data=players_data,
                                                 file_id=self._file_id)
        self._card_distribution = _count_cards(dic=player_dic)
        self._winning_hand_dist = dict(Counter(player_dic['Win']['Hands']))

    def __repr__(self):
        val = self._file_id
        if "." in val:
            val = self._file_id.split(".")[0]
        return val

    @property
    def file_name(self) -> str:
        """Returns name of data file"""
        return self._file_id

    @property
    def hands_lst(self) -> List[Hand]:
        """Returns list of hands in the game"""
        return self._parsed_hands

    @property
    def card_distribution(self) -> dict:
        """Returns count of each card that showed up"""
        return self._card_distribution

    @property
    def winning_hand_distribution(self) -> dict:
        """Returns count of winning hands"""
        return self._winning_hand_dist

    @property
    def players_data(self) -> dict:
        """Returns Player stats for players across games"""
        return self._players_data


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
        >>> from poker.classes import Poker
        >>> repo = 'location of your previous game'
        >>> grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
        >>>             ['48QVRRsiae', 'u8_FUbXpAz']]
        >>> poker = Poker(repo_location=repo, grouped=grouped)
    :note: *None*

    """
    def __init__(self, repo_location: str, grouped: Optional[list] = None, money_multi: Optional[int] = 100):
        self._repo_location = repo_location
        self._files = next(walk(self._repo_location))[2]

        self._grouped = None
        if grouped:
            self._grouped = grouped

        file_dic = {file: _get_data(repo_location=self._repo_location, file=file) for file in self._files}
        game_hand_time_lst_dic = {file: _get_hands(data=file_dic[file]) for file in self._files}
        # game_hands_lst_dic, game_times_lst_dic = {}, {}
        # for file in self._files:
        #     line_lst, time_lst = [], []
        #     for dic in game_hand_time_lst_dic[file]:
        #         line_lst.append(dic['lines'])
        #         time_lst.append(dic['times'])
        #     game_hands_lst_dic[file] = line_lst
        #     game_times_lst_dic[file] = time_lst

        players_data = {}
        self._matches = [Game(hand_lst=game_hand_time_lst_dic[file_id], file_id=file_id,
                              players_data=players_data) for file_id in self._files]
        player_dic = _build_player_dic(data=players_data, matches=self._matches)
        self._player_money_df = _group_money(data=pd.DataFrame.from_dict(player_dic, orient='index'),
                                             grouped=self._grouped, multi=money_multi)
        self._card_distribution, self._winning_hand_dist = _get_dist(matches=self._matches)
        _build_players(data=players_data, money_df=self._player_money_df)
        self._players = _combine_dic(data=players_data, grouped=self._grouped)

    def __repr__(self):
        return "Poker"

    @property
    def files(self) -> List[str]:
        """Returns list of data files"""
        return self._files

    @property
    def matches(self) -> List[Game]:
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
