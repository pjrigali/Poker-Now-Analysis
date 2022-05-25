from typing import Union
from dataclasses import dataclass
from poker.utils.class_functions import _str_nan, _get_attributes, _get_percent_change


def _order(events: list) -> tuple:
    ord, ord_check = [], {}
    for e in events:
        if _str_nan(e.player_index):
            if e.player_index not in ord_check:
                ord_check[e.player_index] = True
                ord.append(e.player_index)
            else:
                break
    return tuple(ord)


def _cards(events: list) -> tuple:
    for e in events:
        if e.event == 'PlayerStacks':
            return e.cards


def _fold(events: list) -> dict:
    return {e.player_index: {'event_number': e.event_number,
                             'position': e.position,
                             'action_from_player': e.action_from_player,
                             'action_amount': e.action_amount,
                             'chip_change': e.starting_chips[e.player_index] - e.current_chips[e.player_index],
                             } for e in events if e.event == 'Folds'}


def _pot_size(events: list) -> tuple:
    lst = []
    for e in events:
        if e.event == 'Wins':
            break
        else:
            lst.append(e.pot_size)
    return tuple(lst)


@dataclass
class Hand:

    __slots__ = ('events', 'game_id', 'winner', 'winning_hand', 'win_stack', 'hand_time', 'start_time', 'end_time',
                 'hand_number', 'starting_chips', 'ending_chips', 'ending_players', 'position', 'order', 'cards',
                 'fold_placement', 'starting_players', 'pot_size', 'chip_total', 'chip_percent_change', 'gini')

    def __init__(self, events: Union[list, tuple]):
        self.events = events
        self.game_id = events[0].game_id
        self.winner = events[0].winner
        self.winning_hand = events[0].winning_hand
        self.win_stack = events[0].win_stack
        self.hand_time = (events[-1].time - events[0].time).seconds
        self.start_time = events[0].start_time
        self.end_time = events[-1].end_time
        self.hand_number = events[0].current_round
        self.starting_chips = events[0].starting_chips
        self.ending_chips = events[-1].current_chips
        self.ending_players = events[-1].remaining_players
        self.position = events[-1].position
        self.order = _order(events)
        self.cards = _cards(events)
        self.fold_placement = _fold(events)
        self.starting_players = events[0].starting_players
        self.pot_size = _pot_size(events)
        self.chip_total = sum(events[-1].starting_chips.values())
        self.chip_percent_change = {i: _get_percent_change(self.ending_chips[i], self.starting_chips[i]) for i in self.starting_players}
        self.gini = events[0].gini

    def __repr__(self):
        return 'Hand:  ' + str(self.hand_number)

    def items(self) -> tuple:
        return (self.hand_number, _get_attributes(self))
