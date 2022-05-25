from typing import Union
from dataclasses import dataclass
import datetime
from poker.classes.hand import Hand


def _gini_chips_ids(hands: tuple):
    unique_ids = set(i for h in hands for i in h.order)
    gini, total, chips = [], [], {i: [] for i in unique_ids}
    for h in hands:
        gini.append(h.gini), total.append(h.chip_total)
        for i in unique_ids:
            if i in h.order and i in h.starting_chips:
                chips[i].append(h.starting_chips[i])
            else:
                chips[i].append(0)
    return tuple(gini), tuple(total), {k: tuple(v) for k, v in chips.items()}, tuple(unique_ids)

@dataclass
class Match:
    __slots__ = ('hands', 'game_id', 'start_time', 'end_time', 'match_time', 'gini', 'total_chips', 'current_chips',
                 'players_involved')

    def __init__(self, hands: Union[list, tuple]):
        self.hands = hands
        self.game_id = self.hands[0].game_id
        self.start_time = self.hands[0].start_time
        self.end_time = self.hands[-1].end_time
        self.match_time = datetime.timedelta(seconds=(self.end_time - self.start_time).seconds)
        self.gini, self.total_chips, self.current_chips, self.players_involved = _gini_chips_ids(hands=self.hands)

    def __repr__(self):
        return 'Match: ' + self.game_id
