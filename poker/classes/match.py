from typing import Union
from dataclasses import dataclass
import datetime
from poker.utils.class_functions import tdict


def _data(hands: tuple):
    unique_ids = set(i for h in hands for i in h.order)
    gini, total, chips = [], [], tdict(unique_ids, [])
    for h in hands:
        gini.append(h.gini), total.append(h.chip_total)
        for i in unique_ids:
            if i in h.order:
                if i in h.starting_chips:
                    chips[i].append(h.starting_chips[i])
            else:
                chips[i].append(0)
    dic = {}
    for k, v in chips.items():
        v = v[1:]
        low, high = 0, 0
        for ind, val in enumerate(v):
            if v[ind - 1] != 0:
                if val - v[ind - 1] > high:
                    high = val - v[ind - 1]
                elif val - v[ind - 1] < low:
                    low = val - v[ind - 1]
        dic[k] = {'largest_stack': max(v), 'largest_loss': low, 'largest_win': high}
    return tuple(gini), tuple(total), {k: tuple(v) for k, v in chips.items()}, tuple(unique_ids), dic


@dataclass
class Match:
    __slots__ = ('hands', 'game_id', 'start_time', 'end_time', 'match_time', 'gini', 'total_chips', 'current_chips',
                 'players_involved', 'players')

    def __init__(self, hands: Union[list, tuple]):
        self.hands = hands
        self.game_id = self.hands[0].game_id
        self.start_time = self.hands[0].start_time
        self.end_time = self.hands[-1].end_time
        self.match_time = datetime.timedelta(seconds=(self.end_time - self.start_time).seconds)
        self.gini, self.total_chips, self.current_chips, self.players_involved, self.players = _data(hands=self.hands)

    def __repr__(self):
        return 'Match: ' + self.game_id
