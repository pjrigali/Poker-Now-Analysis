from typing import List, Optional, Union
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
