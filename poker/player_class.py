from typing import List, Union
from dataclasses import dataclass


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
