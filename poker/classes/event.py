"""
Event Class

This Class is the smallest unit used in this package. Denotes a single occurrence that happened on the table.
"""
from dataclasses import dataclass


def _player_name(text: str):
    if ' @ ' in text:
        return text.split('"')[1].split('@')[0].strip()
    else:
        return None


def _player_index(text: str):
    if ' @ ' in text:
        return text.split('@')[1].split('"')[0].strip()
    else:
        return None


def _stack(text: str):
    if 'stack of ' in text:
        return int(text.split('stack of ')[1].split('.')[0])
    else:
        return None


@dataclass
class Event:
    """
    Applies attributes to a respective Class object.

    :param text: A line of text from the data.
    :type text: str
    :example: *None*
    :note: This class is intended to be used internally.
    """

    __slots__ = ('text', 'player_name', 'player_index', 'stack', 'position', 'winning_hand', 'cards', 'current_round',
                 'pot_size', 'remaining_players', 'action_from_player', 'action_amount', 'all_in', 'game_id',
                 'starting_chips', 'current_chips', 'winner', 'win_stack', 'time', 'previous_time', 'start_time',
                 'end_time', 'starting_players', 'event')

    def __init__(self, text: str, event: str):
        self.text = text
        self.player_name = _player_name(self.text)
        self.player_index = _player_index(self.text)
        self.stack = _stack(self.text)
        self.position = None
        self.winning_hand = None
        self.cards = None
        self.current_round = None
        self.pot_size = 0
        self.starting_players = None
        self.remaining_players = None
        self.action_from_player = None
        self.action_amount = 0
        self.all_in = None
        self.game_id = None
        self.starting_chips = 0
        self.current_chips = 0
        self.winner = None
        self.win_stack = None
        self.time = None
        self.previous_time = None
        self.start_time = None
        self.end_time = None
        self.event = event

    def __repr__(self):
        return self.event
