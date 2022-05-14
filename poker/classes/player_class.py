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

    __slots__ = ('player_index', 'other_player_indexes', 'player_money_info', 'hand_dic', 'card_dic', 'line_dic',
                 'moves_dic', 'win_percent', 'win_count', 'largest_win', 'largest_loss', 'hand_count', 'all_in',
                 'player_name', 'merged_moves', 'custom_name')

    def __init__(self, player_index: Union[str, List[str]]):
        if type(player_index) == str:
            self.player_index = [player_index]
        else:
            self.player_index = player_index
        self.other_player_indexes = self.player_index
        self.player_money_info = {}
        self.hand_dic = {}
        self.card_dic = {}
        self.line_dic = {}
        self.moves_dic = {}
        self.win_percent = {}
        self.win_count = {}
        self.largest_win = {}
        self.largest_loss = {}
        self.hand_count = {}
        self.all_in = {}
        self.player_name = []
        self.merged_moves = None
        self.custom_name = None

    def __repr__(self):
        if self.custom_name is None:
            return str(self.player_name)
        else:
            return self.custom_name
