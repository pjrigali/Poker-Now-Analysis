# pylint: disable=no-name-in-module
# pylint: disable=bad-plugin-value
"""
"""
from dataclasses import dataclass
from poker.utils.class_functions import _get_attributes
from poker.utils.tools import calc_gini, calculate_hand


@dataclass
class Hand:
    """
    A class representing a rectangle in a 2D plane.

    Attributes:
        width (float): The width of the rectangle.
        height (float): The height of the rectangle.

    Methods:
        area(): Calculate the area of the rectangle.
        perimeter(): Calculate the perimeter of the rectangle.
    """
    def __init__(self, d: dict):
        """
        Initialize a Rectangle instance.

        Args:
            width (float): The width of the rectangle.
            height (float): The height of the rectangle.
        """
        self.event_lst = d['event_lst']
        self.event_dct = d['event_dct']
        self.game_id = d['game_id']
        self.winner = d['winner']
        self.win_hand = d['win_hand']
        # Calculates winning hand if not given.
        if not self.win_hand:
            cards = []
            for i in ('winner', 'flop', 'turn', 'river'):
                if d['table_cards'].get(i):
                    cards.extend(d['table_cards'][i])
            self.win_hand = calculate_hand(set(cards))
        self.win_stack = d['win_stack']
        self.win_cards = d['win_cards']
        self.hand_time = d['hand_time']
        self.start_time = d['start_time']
        self.end_time = d['end_time']
        self.hand_number = d['hand_number']
        self.starting_chips = d['starting_chips']
        self.ending_chips = d['ending_chips']
        self.ending_players = d['ending_players']
        self.position = d['position']
        self.all_cards = d['all_cards']
        self.table_cards = d['table_cards']
        self.table_cards['winner'] = list(set(self.table_cards['winner']))
        self.pot_size = d['pot_size']
        self.total_chips = d['total_chips']
        self.start_gini = calc_gini(list(d['starting_chips'].values()))
        self.end_gini = calc_gini(list(d['ending_chips'].values()))
        self.joined = d['joined']
        self.flop = d['table_cards'].get('flop')
        self.turn = d['table_cards'].get('turn')
        self.river = d['table_cards'].get('river')
        self.undealt = d['table_cards'].get('undealt')
        # Place undealt cards.
        if self.undealt:
            if len(self.undealt) == 1:
                self.table_cards['river'], self.river = self.undealt, self.undealt
            elif len(self.undealt) == 2:
                self.table_cards['turn'], self.turn = [self.undealt[0]], [self.undealt[0]]
                self.table_cards['river'], self.river = [self.undealt[1]], [self.undealt[1]]
            elif len(self.undealt) == 5:
                self.table_cards['flop'], self.flop = self.undealt[:3], self.undealt[:3]
                self.table_cards['turn'], self.turn = [self.undealt[-2]], [self.undealt[-2]]
                self.table_cards['river'], self.river = [self.undealt[-1]], [self.undealt[-1]]
        self.mycards = d['table_cards'].get('your_cards')

    def __repr__(self):
        return f"Game: ({self.game_id}), Hand: ({self.hand_number})"

    def items(self):
        """
        Calculate the area of the rectangle.

        Returns:
            float: The area of the rectangle.
        """
        return _get_attributes(self)
