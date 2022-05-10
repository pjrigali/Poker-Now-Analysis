from typing import List
from dataclasses import dataclass
import pandas as pd
from poker.processor import Approved, SmallBlind, BigBlind, Raises, Wins, Quits
from poker.processor import StandsUp, SitsIn, PlayerStacks
from poker.base import flatten, unique_values, round_to, native_sum, native_mean
from poker.hand_class import Hand
from poker.player_class import Player
pd.set_option('use_inf_as_na', True)


def _game_calc_money(lst: list, ind: str) -> pd.DataFrame:
    """Returns a dataframe recording player action related to money on the table for a game."""
    dic = {'Player Names': [], 'Player Stack': [], 'Player Quits': [], 'Player Stands Up': [], 'Player Sits In': []}
    for line in lst:
        if isinstance(line, Approved):
            dic['Player Names'].append(line.player_name)
            dic['Player Stack'].append(line.stack)
        elif isinstance(line, Quits):
            dic['Player Quits'].append(line.stack)
        elif isinstance(line, StandsUp):
            dic['Player Stands Up'].append(line.stack)
        elif isinstance(line, SitsIn):
            dic['Player Sits In'].append(line.stack)

    temp_df = pd.DataFrame(index=[ind])
    temp_df['Player Names'] = [list(set(dic['Player Names']))]
    temp_df['Buy in Total'] = native_sum(data=dic['Player Stack'])
    temp_df['Loss Count'] = len(dic['Player Quits'])
    temp_df['player stands up sum'] = native_sum(data=dic['Player Stands Up'])
    temp_df['player sits in sum'] = native_sum(data=dic['Player Sits In'])
    temp_df['Leave Table Amount'] = temp_df['player stands up sum'] - temp_df['player sits in sum']
    return temp_df[['Player Names', 'Buy in Total', 'Loss Count', 'Leave Table Amount']]


def _game_line_to_df(line_lst: list) -> pd.DataFrame:
    """Takes line info and converts to a pd.dataframe"""
    lst = []
    for line in line_lst:
        temp_win = False
        if line.player_index in line.winner:
            temp_win = True
        dic = {'Player Index': line.player_index, 'Player Name': line.player_name, 'Cards': line.cards,
               'Position': line.position, 'Round': line.current_round, 'Player Starting Chips': line.starting_chips,
               'Player Current Chips': line.current_chips, 'Class': repr(line), 'Winner': line.winner, 'Win': temp_win,
               'Win Stack': line.win_stack, 'Win Hand': line.winning_hand, 'All In': line.all_in,
               'Pot Size': line.pot_size, 'Remaining Players': line.remaining_players,
               'From Person': line.action_from_player, 'Game Id': line.game_id, 'Time': line.time,
               'Previous Time': line.previous_time, 'Start Time': line.start_time, 'End Time': line.end_time}
        if isinstance(line, (Raises, PlayerStacks, SmallBlind, BigBlind, Wins)):
            dic['Bet Amount'] = line.stack
        else:
            dic['Bet Amount'] = line.action_amount
        lst.append(dic)
    return pd.DataFrame(lst)


def _game_build_players_data(player_dic: dict, players_data: dict, file_id: str) -> dict:
    """Updates Player Class"""
    dic = {}
    for key, val in player_dic.items():
        if key not in {'Flop': True, 'Turn': True, 'River': True, 'Win': True, 'My Cards': True}:
            dic[key] = val
    t_dic = dict(zip(list(players_data.keys()), [True] * len(list(players_data.keys()))))
    for p_ind in dic.keys():
        if p_ind not in t_dic:
            players_data[p_ind] = Player(player_index=p_ind)
        players_data[p_ind].line_dic = [file_id, dic[p_ind]['Lines']]
        players_data[p_ind].player_money_info = [file_id, _game_calc_money(lst=dic[p_ind]['Lines'], ind=file_id)]
        players_data[p_ind].hand_dic = [file_id, pd.DataFrame.from_dict(unique_values(data=dic[p_ind]['Hands'], count=True), orient='index', columns=['Count']).sort_values('Count', ascending=False)]
        players_data[p_ind].card_dic = [file_id, pd.DataFrame.from_dict(unique_values(data=[item for sublist in dic[p_ind]['Cards'] for item in sublist], count=True), orient='index', columns=['Count']).fillna(0.0).astype(int)]
        players_data[p_ind].moves_dic = [file_id, _game_line_to_df(line_lst=dic[p_ind]['Lines'])]
    return players_data


def _game_count_cards(dic: dict) -> dict:
    """Counts cards"""
    n_dic = {}
    for key in dic.keys():
        if key in {'Flop': True, 'Turn': True, 'River': True, 'Win': True, 'My Cards': True}:
            if key in {'Flop': True, 'Win': True, 'My Cards': True}:
                lst = flatten(data=dic[key]['Cards'])
            else:
                lst = dic[key]['Cards']
            n_dic[key + ' Count'] = unique_values(data=flatten(data=lst), count=True)
    return n_dic


def _game_game_stats(hand_lst: list) -> dict:
    dic = {'Average Hand Time': [], 'Average Win Amount': [], 'Average Bet Size': [], 'Average Pot Size': [],
           'Average Gini Coef': []}
    for hand in hand_lst:
        dic['Average Hand Time'].append((hand.end_time - hand.start_time).total_seconds())
        dic['Average Win Amount'].append(hand.win_stack)
        dic['Average Bet Size'].append(hand.bet_lst)
        dic['Average Pot Size'].append(hand.pot_size_lst[-1])
        dic['Average Gini Coef'].append(hand.gini_coef)
    for key, val in dic.items():
        if key == 'Average Bet Size':
            val = flatten(data=val, type_used='int')
        if key == 'Average Gini Coef':
            dic[key] = round_to(data=native_mean(data=val), val=100, remainder=True)
        else:
            dic[key] = round_to(data=native_mean(data=val), val=1)
    return dic


@dataclass
class Game:
    """

    Calculate stats for a game.

    :param hand_lst: List of dict's from the csv.
    :type hand_lst: List[dict]
    :param file_id: Name of file.
    :type file_id: str
    :param players_data: A dict of player data.
    :type players_data: dict
    :example: *None*
    :note: This class is intended to be used internally.

    """

    __slots__ = ('file_name', 'hand_lst', 'card_distribution', 'winning_hand_distribution', 'players_data',
                 'game_stats')

    def __init__(self, hand_lst: List[dict], file_id: str, players_data: dict):
        self.file_name = file_id
        player_dic = {}
        self.hand_lst = [Hand(lst_hand_objects=h, file_id=file_id, player_dic=player_dic) for h in hand_lst]
        self.players_data = _game_build_players_data(player_dic=player_dic, players_data=players_data, file_id=file_id)
        self.card_distribution = _game_count_cards(dic=player_dic)
        self.winning_hand_distribution = unique_values(data=player_dic['Win']['Hands'], count=True)
        self.game_stats = _game_game_stats(hand_lst=self.hand_lst)

    def __repr__(self):
        return self.file_name
