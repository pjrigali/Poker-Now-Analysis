# from typing import List, Optional, Union
from dataclasses import dataclass
from poker.processor import Approved, MyCards, SmallBlind, BigBlind, Folds, Calls, Raises, Checks, Wins, Shows, Quits
from poker.processor import Flop, Turn, River, Undealt, StandsUp, SitsIn, PlayerStacks, parser
from poker.base import calc_gini


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
    """Copies one class object attributes to another class object"""
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
    new_object.start_time = original_object.start_time
    new_object.end_time = original_object.end_time
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

    __slots__ = ('parsed_hand', 'small_blind', 'big_blind', 'winner', 'starting_players', 'starting_player_chips',
                 'flop_cards', 'turn_card', 'river_card', 'my_cards', 'chips_on_board', 'gini_coef', 'pot_size_lst',
                 'start_time', 'end_time', 'bet_lst', 'win_stack', 'players')

    def __init__(self, lst_hand_objects: dict, file_id: str, player_dic: dict):
        parsed_hand = parser(lines=lst_hand_objects['lines'], times=lst_hand_objects['times'], game_id=file_id)
        self.parsed_hand = [line for line in parsed_hand]
        self.small_blind = None
        self.big_blind = None
        self.winner = []
        self.starting_players = None
        self.starting_player_chips = None
        self.flop_cards = None
        self.turn_card = None
        self.river_card = None
        self.my_cards = None
        self.chips_on_board = None
        self.gini_coef = None
        self.pot_size_lst = []
        self.start_time = self.parsed_hand[0].start_time
        self.end_time = self.parsed_hand[0].end_time
        self.bet_lst = []
        self.win_stack = None

        winner_lst = []
        winner_line_lst = []
        winner_hand = None
        winner_stack = 0
        for line in self.parsed_hand:
            if type(line) == Wins:
                winner_lst.append(line.player_index)
                if line.winning_hand is not None:
                    winner_hand = line.winning_hand
                if line.stack is not None:
                    winner_stack += line.stack
        if winner_stack != 0:
            self.win_stack = winner_stack

        for line in self.parsed_hand:
            line.start_time = self.start_time
            line.end_time = self.end_time
            line_type = type(line)
            self.pot_size_lst.append(line.pot_size)
            line.winner = winner_lst
            line.winning_hand = winner_hand
            line.win_stack = winner_stack
            if line_type == SmallBlind:
                self.small_blind = line
                _hand_add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=line.player_index)
                continue
            elif line_type == BigBlind:
                self.big_blind = line
                _hand_add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=line.player_index)
                continue
            elif line_type == Wins:
                _hand_add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=line.player_index)
                if line.cards is not None:
                    line.cards = list(line.cards)
                    _hand_add_to_dic(item=line.cards, player_dic=player_dic, location='Cards',
                                     player_index=line.player_index)
                    _hand_add_to_dic(item=line.cards, player_dic=player_dic, location='Cards', player_index='Win')
                _hand_add_to_dic(item=line.winning_hand, player_dic=player_dic, location='Hands',
                                 player_index=line.player_index)
                _hand_add_to_dic(item=line.winning_hand, player_dic=player_dic, location='Hands', player_index='Win')
                winner_line_lst.append(line)
                continue
            elif line_type == PlayerStacks:
                self.starting_players = dict(zip(line.player_index, line.player_name))
                self.starting_player_chips = dict(zip(line.player_index, line.starting_chips))
                self.chips_on_board = sum(line.starting_chips)
                self.gini_coef = calc_gini(data=line.starting_chips)
                for player in self.starting_players.keys():
                    _hand_add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=player)
                continue
            elif line_type == Flop:
                self.flop_cards = line
                _hand_add_to_dic(item=line.cards, player_dic=player_dic, location='Cards', player_index='Flop')
                for player in self.starting_players.keys():
                    _hand_add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=player)
                continue
            elif line_type == Turn:
                self.turn_card = line
                _hand_add_to_dic(item=line.cards, player_dic=player_dic, location='Cards', player_index='Turn')
                for player in self.starting_players.keys():
                    _hand_add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=player)
                continue
            elif line_type == River:
                self.river_card = line
                _hand_add_to_dic(item=line.cards, player_dic=player_dic, location='Cards', player_index='River')
                for player in self.starting_players.keys():
                    _hand_add_to_dic(item=line, player_dic=player_dic, location='Lines', player_index=player)
                continue
            elif line_type == MyCards:
                self.my_cards = line
                _hand_add_to_dic(item=line.cards, player_dic=player_dic, location='Cards', player_index='My Cards')
                continue
            elif line_type == Undealt:
                if len(line.cards) == 1:
                    river_val = line.cards[0]
                    if self.river_card is None:
                        self.river_card = _hand_copy_line_to_line(new_object=River(text=None), original_object=line)
                        self.river_card.cards = river_val
                        self.parsed_hand.append(self.river_card)
                elif len(line.cards) == 2:
                    if type(line.cards[0]) == list:
                        turn_val = line.cards[0][0]
                    else:
                        turn_val = line.cards[0]
                    if self.turn_card is None:
                        self.turn_card = _hand_copy_line_to_line(new_object=Turn(text=None), original_object=line)
                        self.turn_card.cards = turn_val
                        self.parsed_hand.append(self.turn_card)
                    if type(line.cards[1]) == list:
                        river_val = line.cards[1][0]
                    else:
                        river_val = line.cards[1]
                    if self.river_card is None:
                        self.river_card = _hand_copy_line_to_line(new_object=River(text=None), original_object=line)
                        self.river_card.cards = river_val
                        self.parsed_hand.append(self.river_card)
                else:
                    flop_vals = line.cards[:3]
                    if self.flop_cards is None:
                        self.flop_cards = _hand_copy_line_to_line(new_object=Flop(text=None), original_object=line)
                        self.flop_cards.cards = flop_vals
                        self.parsed_hand.append(self.flop_cards)
                    if type(line.cards[3]) == list:
                        turn_val = line.cards[3][0]
                    else:
                        turn_val = line.cards[3]
                    if self.turn_card is None:
                        self.turn_card = _hand_copy_line_to_line(new_object=Turn(text=None), original_object=line)
                        self.turn_card.cards = turn_val
                        self.parsed_hand.append(self.turn_card)
                    if type(line.cards[4]) == list:
                        river_val = line.cards[4][0]
                    else:
                        river_val = line.cards[4]
                    if self.river_card is None:
                        self.river_card = _hand_copy_line_to_line(new_object=River(text=None), original_object=line)
                        self.river_card.cards = river_val
                        self.parsed_hand.append(self.river_card)
                continue
            elif line_type == Raises:
                self.bet_lst.append(line.stack)
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
                        _hand_add_to_dic(item=temp_line.cards, player_dic=player_dic, location='Cards',
                                         player_index='Win')
                        _hand_add_to_dic(item=temp_line.cards, player_dic=player_dic, location='Cards',
                                         player_index=temp_line.player_index)
                        break
        self.winner = winner_lst
        self.players = player_dic

    def __repr__(self):
        return "Hand " + str(self.parsed_hand[0].current_round)
