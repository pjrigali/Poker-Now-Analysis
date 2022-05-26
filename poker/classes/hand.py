from typing import Union
from dataclasses import dataclass
from poker.utils.class_functions import _str_nan, _get_attributes, _get_percent_change


def _get_data(events: list):
    o, o_c, c, f_dic, p, a = [], {}, None, {}, [], {}
    for e in events:
        if _str_nan(e.player_index) and e.player_index not in o_c:
            o_c[e.player_index] = True
            o.append(e.player_index)
        if e.event in {'SmallBlind': True, 'BigBlind': True, 'Calls': True, 'Bets': True, 'Checks': True}:
            p.append(e.pot_size)
            continue
        elif e.event == 'Folds':
            f_dic[e.player_index] = {'event_number': e.event_number, 'position': e.position,
                                     'action_from_player': e.action_from_player, 'action_amount': e.action_amount,
                                     'chip_change': e.starting_chips[e.player_index] - e.current_chips[e.player_index]}
            continue
        elif e.event == 'PlayerStacks':
            c = e.cards
            continue
        elif e.event == 'Approved':
            a[e.player_index] = e.stack
            continue
    return tuple(o), c, f_dic, tuple(p)


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
        self.order, self.cards, self.fold_placement, self.pot_size = _get_data(events=self.events)
        self.starting_players = events[0].starting_players
        self.chip_total = sum(events[-1].starting_chips.values())
        self.chip_percent_change = {i: _get_percent_change(self.ending_chips[i], self.starting_chips[i]) for i in self.starting_players}
        self.gini = events[0].gini

    def __repr__(self):
        return 'Hand:  ' + str(self.hand_number)

    def items(self) -> tuple:
        return (self.hand_number, _get_attributes(self))
