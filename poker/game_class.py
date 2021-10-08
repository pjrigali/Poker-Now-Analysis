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
    temp_df['Buy in Total'] = native_sum(data=player_money_dic['Player Stack'])
    temp_df['Loss Count'] = len(player_money_dic['Player Quits'])
    temp_df['player stands up sum'] = native_sum(data=player_money_dic['Player Stands Up'])
    temp_df['player sits in sum'] = native_sum(data=player_money_dic['Player Sits In'])
    temp_df['Leave Table Amount'] = temp_df['player stands up sum'] - temp_df['player sits in sum']
    return temp_df[['Player Names', 'Buy in Total', 'Loss Count', 'Leave Table Amount']]


def _game_line_to_df(line_lst: list) -> pd.DataFrame:
    """Takes line info and converts to a pd.dataframe"""
    lst = []
    for line in line_lst:
        temp_win = False
        if line.player_index in line.winner:
            temp_win = True
        if type(line) in [Raises, PlayerStacks, SmallBlind, BigBlind, Wins]:
            lst.append({'Player Index': line.player_index, 'Player Name': line.player_name, 'Bet Amount': line.stack, 'Cards': line.cards,
                        'Position': line.position, 'Round': line.current_round, 'Player Starting Chips': line.starting_chips, 'Player Current Chips': line.current_chips,
                        'Class': repr(line), 'Winner': line.winner, 'Win': temp_win, 'Win Stack': line.win_stack,
                        'Win Hand': line.winning_hand, 'All In': line.all_in, 'Pot Size': line.pot_size,
                        'Remaining Players': line.remaining_players, 'From Person': line.action_from_player,
                        'Game Id': line.game_id, 'Time': line.time, 'Previous Time': line.previous_time, 'Start Time': line.start_time, 'End Time': line.end_time})
        else:
            lst.append({'Player Index': line.player_index, 'Player Name': line.player_name, 'Cards': line.cards,
                        'Bet Amount': line.action_amount, 'Position': line.position, 'Round': line.current_round, 'Player Starting Chips': line.starting_chips,
                        'Player Current Chips': line.current_chips, 'Class': repr(line), 'Winner': line.winner, 'Win': temp_win,
                        'Win Stack': line.win_stack, 'Win Hand': line.winning_hand, 'All In': line.all_in,
                        'Pot Size': line.pot_size, 'Remaining Players': line.remaining_players,
                        'From Person': line.action_from_player, 'Game Id': line.game_id, 'Time': line.time,
                        'Previous Time': line.previous_time, 'Start Time': line.start_time, 'End Time': line.end_time})
    return pd.DataFrame(lst)


def _game_build_players_data(player_dic: dict, players_data: dict, file_id: str) -> dict:
    """Updates Player Class"""
    player_info_dic = {}
    for key, val in player_dic.items():
        if key not in ['Flop', 'Turn', 'River', 'Win', 'My Cards']:
            player_info_dic[key] = val

    for player_index in player_info_dic.keys():
        val = _game_calc_money(lst=player_info_dic[player_index]['Lines'], ind=file_id)
        card_dic = unique_values(data=[item for sublist in player_info_dic[player_index]['Cards'] for item in sublist],
                                 count=True)
        card_df = pd.DataFrame.from_dict(card_dic, orient='index', columns=['Count']).fillna(0.0).astype(int)
        hand_df = pd.DataFrame.from_dict(unique_values(data=player_info_dic[player_index]['Hands'], count=True),
                                         orient='index',
                                         columns=['Count']).sort_values('Count', ascending=False)
        line_dic = player_info_dic[player_index]['Lines']
        if player_index not in players_data.keys():
            players_data[player_index] = Player(player_index=player_index)
        players_data[player_index].line_dic = [file_id, line_dic]
        players_data[player_index].player_money_info = [file_id, val]
        players_data[player_index].hand_dic = [file_id, hand_df]
        players_data[player_index].card_dic = [file_id, card_df]
        players_data[player_index].moves_dic = [file_id, _game_line_to_df(line_lst=line_dic)]
    return players_data


def _game_count_cards(dic: dict) -> dict:
    """Counts cards"""
    card_count_dic = {}
    for key in dic.keys():
        if key in ['Flop', 'Turn', 'River', 'Win', 'My Cards']:
            if key in ['Flop', 'Win', 'My Cards']:
                lst = flatten(data=dic[key]['Cards'])
            else:
                lst = dic[key]['Cards']
            card_count_dic[key + ' Count'] = unique_values(data=flatten(data=lst), count=True)
    return card_count_dic


def _game_game_stats(hand_lst: list) -> dict:
    temp_dic = {'Average Hand Time': [], 'Average Win Amount': [], 'Average Bet Size': [], 'Average Pot Size': [],
                'Average Gini Coef': []}
    for hand in hand_lst:
        temp_dic['Average Hand Time'].append((hand.end_time - hand.start_time).total_seconds())
        temp_dic['Average Win Amount'].append(hand.win_stack)
        temp_dic['Average Bet Size'].append(hand.bet_lst)
        temp_dic['Average Pot Size'].append(hand.pot_size_lst[-1])
        temp_dic['Average Gini Coef'].append(hand.gini_coef)
    for key, val in temp_dic.items():
        if key == 'Average Bet Size':
            val = flatten(data=val, type_used='int')
        if key == 'Average Gini Coef':
            temp_dic[key] = round_to(data=native_mean(data=val), val=100, remainder=True)
        else:
            temp_dic[key] = round_to(data=native_mean(data=val), val=1)
    return temp_dic


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
    def __init__(self, hand_lst: List[dict], file_id: str, players_data: dict):
        self._file_id = file_id
        player_dic = {}
        self._parsed_hands = [Hand(lst_hand_objects=hand, file_id=file_id, player_dic=player_dic) for hand in hand_lst]
        self._players_data = _game_build_players_data(player_dic=player_dic, players_data=players_data, file_id=file_id)
        self._card_dist = _game_count_cards(dic=player_dic)
        self._winning_hand_dist = unique_values(data=player_dic['Win']['Hands'], count=True)
        self._game_stats = _game_game_stats(hand_lst=self._parsed_hands)

    def __repr__(self):
        return self._file_id

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
        return self._card_dist

    @property
    def winning_hand_distribution(self) -> dict:
        """Returns count of winning hands"""
        return self._winning_hand_dist

    @property
    def players_data(self) -> dict:
        """Returns Player stats for players across hands"""
        return self._players_data

    @property
    def game_stats(self) -> dict:
        """Returns Mean stats for Game across hands"""
        return self._game_stats
