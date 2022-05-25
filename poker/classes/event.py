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
        return int(text.split(' stack of ')[1].split('.')[0])
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
                 'end_time', 'starting_players', 'event', 'wins', 'gini', 'raises', 'event_number')

    def __init__(self, text: str, event: str, position=None, winning_hand=None, cards=None, current_round=None,
                 pot_size=0, starting_players=None, remaining_players=None, action_from_player=None, action_amount=None,
                 all_in=None, game_id=None, starting_chips=None, current_chips=None, winner=None, win_stack=None,
                 time=None, previous_time=None, start_time=None, end_time=None, wins=None, gini=None, raises=None,
                 event_number=None):
        self.text = text
        self.event = event
        self.player_name = _player_name(self.text)
        self.player_index = _player_index(self.text)
        self.stack = _stack(self.text)
        self.position = position
        self.winning_hand = winning_hand
        self.cards = cards
        self.current_round = current_round
        self.pot_size = pot_size
        self.starting_players = starting_players
        self.remaining_players = remaining_players
        self.action_from_player = action_from_player
        self.action_amount = action_amount
        self.all_in = all_in
        self.game_id = game_id
        self.starting_chips = starting_chips
        self.current_chips = current_chips
        self.winner = winner
        self.win_stack = win_stack
        self.time = time
        self.previous_time = previous_time
        self.start_time = start_time
        self.end_time = end_time
        self.wins = wins
        self.gini = gini
        self.raises = raises
        self.event_number = event_number

    def __repr__(self):
        return self.event

    def _add_stack(self, val, ret=None):
        self.stack = val
        if ret is None:
            return self

    def _add_cards(self, val, ret=None):
        self.cards = val
        if ret is None:
            return self

    def _add_stack_to_pot(self, ret=None):
        self.pot_size += self.stack
        if ret is None:
            return self
        else:
            return self, self.pot_size

    def _add_all_in(self):
        self.all_in = True

    def _add_raise(self, val):
        self.raises = val - self.action_amount

    def _add_remaining(self, players_left, ret=None):
        self.remaining_players = tuple([p for p in players_left if p != self.player_index])
        if ret is None:
            return self
        else:
            return self, self.remaining_players

    def _add_chips(self, current_chips, calc: str = '+', ret=None):
        if calc == '+':
            current_chips[self.player_index] += self.stack
        else:
            current_chips[self.player_index] -= self.stack
        self.current_chips = current_chips
        if ret is None:
            return current_chips
        else:
            return self

    def _update_pot_curr(self, current_chips, calc: str = '+', ret=None):
        if calc == '+':
            current_chips[self.player_index] += self.stack
        else:
            current_chips[self.player_index] -= self.stack
        self.current_chips = current_chips
        self.pot_size += self.stack
        if ret is None:
            return self.pot_size, current_chips
        else:
            return self, self.pot_size, current_chips

    def _get_cards_allcards(self, cards=None, all_cards=None):
        if self.cards is not None and all_cards is not None:
            if isinstance(self.cards, str):
                all_cards.append(self.cards)
            else:
                for i in self.cards:
                    all_cards.append(i)
        elif self.cards is not None and cards is not None:
            if isinstance(self.cards, str):
                cards.append(self.cards)
            else:
                for i in self.cards:
                    cards.append(i)
        if cards is not None and all_cards is not None:
            return cards, all_cards
        elif cards is not None and all_cards is None:
            return cards
        else:
            return all_cards
