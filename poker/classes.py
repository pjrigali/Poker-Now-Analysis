from typing import List, Optional, Union
from dataclasses import dataclass
import pandas as pd
from os import walk
from collections import Counter
from poker.processor import Approved, MyCards, SmallBlind, BigBlind, Folds, Calls, Raises, Checks, Wins, Shows, Quits
from poker.processor import Flop, Turn, River, Undealt, StandsUp, SitsIn, PlayerStacks, parser
from poker.base import calc_gini
from poker.build import _add_to_dic, _line_to_df, _count_cards, _calc_money, _get_hands, _build_player_dic, _get_dist
from poker.build import _group_money, _build_players, _combine_dic


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
    def my_cards(self) -> Optional[MyCards]:
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
        """Returns total hand count when player involved"""
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
        """Returns player name or names"""
        return self._player_money_dic

    @player_money_info.setter
    def player_money_info(self, val):
        self._player_money_dic[val[0]] = val[1]

    @property
    def hand_dic(self) -> dict:
        """Returns player name or names"""
        return self._hand_dic

    @hand_dic.setter
    def hand_dic(self, val):
        self._hand_dic[val[0]] = val[1]

    @property
    def card_dic(self) -> dict:
        """Returns player name or names"""
        return self._card_dic

    @card_dic.setter
    def card_dic(self, val):
        self._card_dic[val[0]] = val[1]

    @property
    def line_dic(self) -> dict:
        """Returns player name or names"""
        return self._line_dic

    @line_dic.setter
    def line_dic(self, val):
        self._line_dic[val[0]] = val[1]

    @property
    def moves_dic(self) -> dict:
        """Returns player name or names"""
        return self._line_dic

    @moves_dic.setter
    def moves_dic(self, val):
        self._line_dic[val[0]] = val[1]


@dataclass
class Game:
    """

    Calculate stats for a game.

    :param hand_lst: List of strs from the csv.
    :type hand_lst: List[str]
    :param file_id: Name of file.
    :type file_id: str
    :param players_data: A dict of player data.
    :type players_data: dict
    :example: *None*
    :note: This class is intended to be used internally.

    """
    def __init__(self, hand_lst: List[str], file_id: str, players_data: dict):
        self._file_id = file_id
        player_dic = {}
        self._parsed_hands = [Hand(lst_hand_objects=[line for line in parser(hand=hand)],
                                   file_id=file_id, player_dic=player_dic) for hand in hand_lst]

        player_info_dic = {}
        for key, val in player_dic.items():
            if key not in ['Flop', 'Turn', 'River', 'Win', 'My Cards']:
                player_info_dic[key] = val

        for player_index in player_info_dic.keys():
            val = _calc_money(lst=player_info_dic[player_index]['Lines'], ind=self._file_id)
            card_dic = dict(Counter([item for sublist in player_info_dic[player_index]['Cards'] for item in sublist]))
            card_df = pd.DataFrame.from_dict(card_dic, orient='index', columns=['Count']).fillna(0.0).astype(int)
            hand_df = pd.DataFrame.from_dict(dict(Counter(player_info_dic[player_index]['Hands'])),
                                             orient='index',
                                             columns=['Count']).sort_values('Count', ascending=False)
            line_dic = player_info_dic[player_index]['Lines']
            if player_index not in players_data.keys():
                players_data[player_index] = Player(player_index=player_index)
            players_data[player_index].line_dic = [self._file_id, line_dic]
            players_data[player_index].player_money_info = [self._file_id, val]
            players_data[player_index].hand_dic = [self._file_id, hand_df]
            players_data[player_index].card_dic = [self._file_id, card_df]
            players_data[player_index].moves_dic = [self._file_id, _line_to_df(line_lst=line_dic)]

        self._players_data = players_data
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
        """Returns Player objects for players across games"""
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

        game_hands_lst_dic = {file: _get_hands(repo_location=self._repo_location, file=file) for file in self._files}
        players_data = {}
        self._matches = [Game(hand_lst=game_hands_lst_dic[file_id], file_id=file_id,
                              players_data=players_data) for file_id in game_hands_lst_dic.keys()]
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
        """Collects player stats for all matches"""
        return self._players
