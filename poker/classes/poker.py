from dataclasses import dataclass
from poker.utils.load import collect_data
from poker.utils.parse import parser


def _players_events(repo: str, group: dict):
    """loads data, parses data and splits based on player"""
    files = collect_data(repo_location=repo)
    players, p_dic = {}, {}
    if group is not None:
        for k, v in group.items():
            for i in v:
                players[i], p_dic[i] = ([], []), True

    event_lst, count = [], 0
    for k, v in files.items():
        for i in v:
            hand_lst = parser(lines=i['lines'], times=i['times'], game_id=k)
            for event in hand_lst:
                if event.player_index is not None:
                    if event.player_index in p_dic and isinstance(event.player_index, str):
                        players[event.player_index][0].append(event), players[event.player_index][1].append(count)
                    elif event.player_index not in p_dic and isinstance(event.player_index, str):
                        players[event.player_index] = ([event], [count])
                event_lst.append(event)
                count += 1
    return players, tuple(event_lst)


@dataclass
class Poker:
    """
    Builds the Poker Class
    """

    __slots__ = ('repo', 'group', 'players', 'events')

    def __init__(self, repo: str, group: dict, multi: int = 100):
        self.repo = repo
        self.group = group
        self.players, self.events = _players_events(repo=repo, group=group)

    def __repr__(self):
        return 'Poker Class'
