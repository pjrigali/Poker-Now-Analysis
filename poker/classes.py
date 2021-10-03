from typing import List, Optional, Union
from dataclasses import dataclass
import pandas as pd
# import numpy as np
import datetime
from os import walk
from poker.processor import Approved, MyCards, SmallBlind, BigBlind, Folds, Calls, Raises, Checks, Wins, Shows, Quits
from poker.processor import Flop, Turn, River, Undealt, StandsUp, SitsIn, PlayerStacks, parser, class_object_lst
from poker.base import calc_gini, flatten, unique_values, round_to, native_sum, native_max, native_mean


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
    return final_df.sort_values('Profit', ascending=False)


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
            lst.append({'Player Index': line.player_index, 'Player Name': line.player_name, 'Bet Amount': line.stack,
                        'Position': line.position, 'Round': line.current_round, 'Player Starting Chips': line.starting_chips, 'Player Current Chips': line.current_chips,
                        'Class': repr(line), 'Winner': line.winner, 'Win': temp_win, 'Win Stack': line.win_stack,
                        'Win Hand': line.winning_hand, 'All In': line.all_in, 'Pot Size': line.pot_size,
                        'Remaining Players': line.remaining_players, 'From Person': line.action_from_player,
                        'Game Id': line.game_id, 'Time': line.time, 'Previous Time': line.previous_time})
        else:
            lst.append({'Player Index': line.player_index, 'Player Name': line.player_name,
                        'Bet Amount': line.action_amount, 'Position': line.position, 'Round': line.current_round, 'Player Starting Chips': line.starting_chips,
                        'Player Current Chips': line.current_chips, 'Class': repr(line), 'Winner': line.winner, 'Win': temp_win,
                        'Win Stack': line.win_stack, 'Win Hand': line.winning_hand, 'All In': line.all_in,
                        'Pot Size': line.pot_size, 'Remaining Players': line.remaining_players,
                        'From Person': line.action_from_player, 'Game Id': line.game_id, 'Time': line.time,
                        'Previous Time': line.previous_time})
    return pd.DataFrame(lst).bfill()


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


def _hand_add_to_dic(item, player_dic: dict, location: str, player_index: str):
    """Updates Player Class"""
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


def _hand_copy_line_to_line(original_object, new_object):
    new_object.action_amount = original_object.action_amount
    new_object.action_from_player = original_object.action_from_player
    new_object.all_in = original_object.all_in
    new_object.current_chips = original_object.current_chips
    new_object.current_round = original_object.current_round
    new_object.game_id = original_object.game_id
    new_object.player_index = original_object.player_index
    new_object.player_name = original_object.player_name
    new_object.position = original_object.position
    new_object.pot_size = original_object.pot_size
    new_object.previous_time = original_object.previous_time
    new_object.remaining_players = original_object.remaining_players
    new_object.stack = original_object.stack
    new_object.starting_chips = original_object.starting_chips
    new_object.text = original_object.text
    new_object.time = original_object.time
    new_object.win_stack = original_object.win_stack
    new_object.winner = original_object.winner
    new_object.winning_hand = original_object.winning_hand
    return new_object


@dataclass
class Hand:
    """

    Organizes a hand with a class and adds the stands to the player_dic.

    :param lst_hand_objects: A list of Class Objects connected to a hand.
    :type lst_hand_objects: dict
    :param file_id: Unique file name.
    :type file_id: str
    :param player_dic: Dict of players.
    :type player_dic: dict
    :example: *None*
    :note: This class is intended to be used internally.

    """
    def __init__(self, lst_hand_objects: dict, file_id: str, player_dic: dict):
        parsed_hand = parser(lines=lst_hand_objects['lines'], times=lst_hand_objects['times'], game_id=file_id)
        self._parsed_hand = [line for line in parsed_hand]
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
        self._hand_start_time = self._parsed_hand[0].time
        self._hand_end_time = self._parsed_hand[-1].time
        self._bet_lst = []
        self._win_amount = None

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
        if winner_stack != 0:
            self._win_amount = winner_stack

        for line in self._parsed_hand:
            line_type = type(line)
            self._pot_size_lst.append(line.pot_size)
            line.winner = winner_lst
            line.winning_hand = winner_hand
            line.win_stack = winner_stack
            if line_type == SmallBlind:
                self._small_blind = line
                _hand_add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=line.player_index)
                continue
            elif line_type == BigBlind:
                self._big_blind = line
                _hand_add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=line.player_index)
                continue
            elif line_type == Wins:
                _hand_add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=line.player_index)
                if line.cards is not None:
                    _hand_add_to_dic(item=line.cards, player_dic=player_dic, location='Cards',
                                     player_index=line.player_index)
                    _hand_add_to_dic(item=line.cards, player_dic=player_dic, location='Cards', player_index='Win')
                _hand_add_to_dic(item=line.winning_hand, player_dic=player_dic, location='Hands',
                                 player_index=line.player_index)
                _hand_add_to_dic(item=line.winning_hand, player_dic=player_dic, location='Hands', player_index='Win')
                winner_line_lst.append(line)
                continue
            elif line_type == PlayerStacks:
                self._starting_players = dict(zip(line.player_index, line.player_name))
                self._starting_player_chips = dict(zip(line.player_index, line.starting_chips))
                self._total_chips_in_play = sum(line.starting_chips)
                self._gini_value = calc_gini(data=line.starting_chips)
                for player in self._starting_players.keys():
                    _hand_add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=player)
                continue
            elif line_type == Flop:
                self._flop = line
                _hand_add_to_dic(item=line.cards, player_dic=player_dic, location='Cards', player_index='Flop')
                continue
            elif line_type == Turn:
                self._turn = line
                _hand_add_to_dic(item=line.cards, player_dic=player_dic, location='Cards', player_index='Turn')
                continue
            elif line_type == River:
                self._river = line
                _hand_add_to_dic(item=line.cards, player_dic=player_dic, location='Cards', player_index='River')
                continue
            elif line_type == MyCards:
                self._my_cards = line
                _hand_add_to_dic(item=line.cards, player_dic=player_dic, location='Cards', player_index='My Cards')
                continue
            elif line_type == Undealt:
                if len(line.cards) == 1:
                    river_val = line.cards[0]
                    if self._river is None:
                        self._river = _hand_copy_line_to_line(new_object=River(text=None), original_object=line)
                        self._river.cards = river_val
                        self._parsed_hand.append(self._river)
                elif len(line.cards) == 2:
                    if type(line.cards[0]) == list:
                        turn_val = line.cards[0][0]
                    else:
                        turn_val = line.cards[0]
                    if self._turn is None:
                        self._turn = _hand_copy_line_to_line(new_object=Turn(text=None), original_object=line)
                        self._turn.cards = turn_val
                        self._parsed_hand.append(self._turn)
                    if type(line.cards[1]) == list:
                        river_val = line.cards[1][0]
                    else:
                        river_val = line.cards[1]
                    if self._river is None:
                        self._river = _hand_copy_line_to_line(new_object=River(text=None), original_object=line)
                        self._river.cards = river_val
                        self._parsed_hand.append(self._river)
                else:
                    flop_vals = line.cards[:3]
                    if self._flop is None:
                        self._flop = _hand_copy_line_to_line(new_object=Flop(text=None), original_object=line)
                        self._flop.cards = flop_vals
                        self._parsed_hand.append(self._flop)
                    if type(line.cards[3]) == list:
                        turn_val = line.cards[3][0]
                    else:
                        turn_val = line.cards[3]
                    if self._turn is None:
                        self._turn = _hand_copy_line_to_line(new_object=Turn(text=None), original_object=line)
                        self._turn.cards = turn_val
                        self._parsed_hand.append(self._turn)
                    if type(line.cards[4]) == list:
                        river_val = line.cards[4][0]
                    else:
                        river_val = line.cards[4]
                    if self._river is None:
                        self._river = _hand_copy_line_to_line(new_object=River(text=None), original_object=line)
                        self._river.cards = river_val
                        self._parsed_hand.append(self._river)
                continue
            elif line_type == Raises:
                self._bet_lst.append(line.stack)
                _hand_add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=line.player_index)
                continue
            elif line_type == Calls:
                _hand_add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=line.player_index)
                continue
            elif line_type == Folds:
                _hand_add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=line.player_index)
                continue
            elif line_type == StandsUp:
                _hand_add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=line.player_index)
                continue
            elif line_type == Quits:
                _hand_add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=line.player_index)
                continue
            elif line_type in [SitsIn, Shows, Approved, Checks]:
                _hand_add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=line.player_index)
                continue

        for winner in winner_line_lst:
            if winner.cards is None:
                for temp_line in self.parsed_hand:
                    if type(temp_line) == Shows and temp_line.player_index == winner.player_index:
                        winner.cards = temp_line.cards
                        _hand_add_to_dic(item=temp_line.cards, player_dic=player_dic, location='Cards', player_index='Win')
                        _hand_add_to_dic(item=temp_line.cards, player_dic=player_dic, location='Cards',
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

    @property
    def start_time(self):
        """Returns time of first hand item"""
        return self._hand_start_time

    @property
    def end_time(self):
        """Returns time of last hand item"""
        return self._hand_end_time

    @property
    def win_stack(self) -> Union[int, None]:
        """Returns win amount for the hand"""
        return self._win_amount

    @property
    def bet_lst(self) -> list[int]:
        """Returns Raise amounts for the hand"""
        return self._bet_lst


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
        self._player_merged_moves = None

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

    @property
    def merged_moves(self) -> Union[dict, None]:
        """Returns a combined dict of player moves"""
        return self._player_merged_moves

    @merged_moves.setter
    def merged_moves(self, val):
        self._player_merged_moves = val


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
