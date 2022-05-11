"""
Created on Sat Aug 15 14:27:18 2021

@author: Peter
"""
from dataclasses import dataclass
from typing import Optional, Union, List


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
class LineAttributes:
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
                 'end_time', 'starting_players')

    def __init__(self, text: Optional[str]):
        if text is not None:
            self.text = text
            self.player_name = _player_name(self.text)
            self.player_index = _player_index(self.text)
            self.stack = _stack(self.text)
        else:
            self.text, self.player_name, self.player_index, self.stack = None, None, None, None
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


@dataclass
class Requests(LineAttributes):
    """Class for players Requesting a seat."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self) -> str:
        return "Requests"


@dataclass
class Approved(LineAttributes):
    """Class for players when Approved a seat."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self) -> str:
        return "Approved"


@dataclass
class Joined(LineAttributes):
    """Class for players Joined the table."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self) -> str:
        return "Joined"


@dataclass
class MyCards(LineAttributes):
    """Class for users cards."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self) -> str:
        return "Player Cards"


@dataclass
class SmallBlind(LineAttributes):
    """Class for the Small Blind player."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self) -> str:
        return "Small Blind"


@dataclass
class BigBlind(LineAttributes):
    """Class for the Big Blind player."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self) -> str:
        return "Big Blind"


@dataclass
class Folds(LineAttributes):
    """Class for players that Fold."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self) -> str:
        return "Folds"


@dataclass
class Calls(LineAttributes):
    """Class for players that Call."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self) -> str:
        return "Calls"


@dataclass
class Raises(LineAttributes):
    """Class for players that Raise."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self) -> str:
        return "Raises"


@dataclass
class Checks(LineAttributes):
    """Class for players that Check."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self) -> str:
        return "Checks"


@dataclass
class Wins(LineAttributes):
    """Class for players that Win."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self) -> str:
        return "Wins"


@dataclass
class Shows(LineAttributes):
    """Class for players that Show their cards."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self) -> str:
        return "Shows"


@dataclass
class Quits(LineAttributes):
    """Class for players that Quit the table."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self) -> str:
        return "Quits"


@dataclass
class Flop(LineAttributes):
    """Class for Flop cards."""
    def __init__(self, text: Optional[str]):
        super().__init__(text)

    def __repr__(self) -> str:
        return "Flop Cards"


@dataclass
class Turn(LineAttributes):
    """Class for Turn card."""
    def __init__(self, text: Optional[str]):
        super().__init__(text)

    def __repr__(self) -> str:
        return "Turn Card"


@dataclass
class River(LineAttributes):
    """Class for River card."""
    def __init__(self, text: Optional[str]):
        super().__init__(text)

    def __repr__(self) -> str:
        return "River Card"


@dataclass
class Undealt(LineAttributes):
    """Class for Undealt cards."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self) -> str:
        return "Undealt"


@dataclass
class StandsUp(LineAttributes):
    """Class for players that Stand Up."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self) -> str:
        return "Stand Up"


@dataclass
class SitsIn(LineAttributes):
    """Class for players that Sit In."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self) -> str:
        return "Sits In"


@dataclass
class PlayerStacks(LineAttributes):
    """Class for getting players and their stacks at the beginning of a hand"""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self) -> str:
        return "Player Stacks"


def parser(lines: List[str], times: list, game_id: str) -> list:
    """This parses strings and converts to class objects"""
    n_lst, i_lst, v_lst, c_round = [], [], [], 0
    for line in lines:
        if 'starting hand' in line:
            c_round = int(line.split('starting hand #')[1].split(' (')[0])
        if 'Player stacks:' in line:
            for play in line.split('#')[1:]:
                n_lst.append(play.split('@')[0].split('"')[1].strip())
                i_lst.append(play.split('@')[1].split('"')[0].strip())
                v_lst.append(int(play.split('(')[1].split(')')[0]))

    if len(n_lst) == 0:
        for line in lines:
            if 'The admin approved' in line:
                n_lst.append(line.split('@')[0].split('"')[1].strip())
                i_lst.append(line.split('@')[1].split('"')[0].strip())
                v_lst.append(0)
    n_lst, i_lst, v_lst = tuple(n_lst), tuple(i_lst), tuple(v_lst)

    def first_pass(c):
        c = c(line)
        c.position, c.game_id, c.time, c.previous_time = pos, game_id, times[ind], p_time
        c.start_time, c.end_time, c.current_round, c.pot_size = s_time, e_time, c_round, pot
        c.starting_players, c.starting_chips, c.remaining_players = start_players, start_chips, players_left
        c.action_from_player, c.action_amount, c.current_chips = p_person, p_amount, current_chips
        c.win_stack, c.winner, c.winning_hand = win_stacks, winners, winning_hands
        return c

    lst = []
    s_time, e_time, p_time = times[0], times[-1], times[0]
    pot, players_left, pos = 0, i_lst, 'Pre Flop'
    p_person, p_amount = None, None
    start_chips, start_players, current_chips = dict(zip(i_lst, v_lst)), dict(zip(i_lst, n_lst)), dict(zip(i_lst, v_lst))
    winners, win_stacks, winning_hands = None, None, None
    for ind, line in enumerate(lines):
        if 'Flop:' in line or 'flop:' in line:
            pos = 'Post Flop'
        if 'Turn:' in line or 'turn:' in line:
            pos = 'Post Turn'
        if 'River:' in line or 'river:' in line:
            pos = 'Post River'

        if ind >= 1:
            p_time = times[ind - 1]

        if 'requested a seat' in line:
            lst.append(first_pass(Requests))
            continue
        elif 'The admin approved' in line:
            lst.append(first_pass(Approved))
            continue
        elif 'joined the game' in line:
            lst.append(first_pass(Joined))
            continue
        elif ' stand up with ' in line:
            n = first_pass(StandsUp)
            players_left = tuple([p for p in players_left if p != n.player_index])
            n.remaining_players = players_left
            lst.append(n)
            continue
        elif ' sit back with ' in line:
            lst.append(first_pass(SitsIn))
            continue
        elif 'Your hand' in line:
            n = first_pass(MyCards)
            new_cards = line.split(' hand is ')[1].split(',')
            n.cards = tuple([i.strip() for i in new_cards])
            lst.append(n)
            continue
        elif 'posts a small blind' in line:
            n = first_pass(SmallBlind)
            n.stack = int(line.split('of ')[1])
            pot += n.stack
            n.pot_size = pot
            current_chips[n.player_index] -= n.stack
            n.current_chips = current_chips
            p_person, p_amount = n.player_index, n.stack
            lst.append(n)
            continue
        elif 'posts a big blind' in line:
            n = first_pass(SmallBlind)
            n.stack = int(line.split('of ')[1])
            pot += n.stack
            n.pot_size = pot
            current_chips[n.player_index] -= n.stack
            n.current_chips = current_chips
            p_person, p_amount = n.player_index, n.stack
            lst.append(n)
            continue
        elif ' folds' in line:
            n = first_pass(Folds)
            players_left = tuple([p for p in players_left if p != n.player_index])
            n.remaining_players = players_left
            lst.append(n)
            continue
        elif ' calls ' in line:
            n = first_pass(Calls)
            new_stack = line.split(' calls ')[1]
            if ' and ' in new_stack:
                new_stack = int(new_stack.split(' and ')[0])
            else:
                new_stack = int(new_stack)
            n.stack = new_stack
            pot += n.stack
            n.pot_size = pot
            current_chips[n.player_index] -= n.stack
            n.current_chips = current_chips
            lst.append(n)
            continue
        elif ' bets ' in line or ' raises ' in line:
            n = first_pass(Raises)
            new_stack = 0
            if ' bets ' in line:
                new_stack = line.split(' bets ')[1]
            if ' raises to ' in line:
                new_stack = line.split(' raises to ')[1]
            if ' and ' in line:
                new_stack = new_stack.split(' and ')[0]
                n.all_in = True
            n.stack = int(new_stack)
            pot += n.stack
            n.pot_size = pot
            p_person, p_amount = n.player_index, n.stack
            current_chips[n.player_index] -= n.stack
            n.current_chips = current_chips
            lst.append(n)
            continue
        elif ' checks' in line:
            lst.append(first_pass(Checks))
            continue
        elif ' collected ' in line:
            n = first_pass(Wins)
            n.stack = int(line.split(' collected ')[1].split(' from ')[0])
            if ' from pot with ' in line:
                if ', ' in line.split(' from pot with ')[1].split(' (')[0]:
                    n.winning_hand = line.split(' from pot with ')[1].split(', ')[0]
                else:
                    n.winning_hand = line.split(' from pot with ')[1].split(' (')[0]
            if 'combination' in line:
                new_cards = line.split(': ')[1].split(')')[0].split(',')
                n.cards = tuple([i.strip() for i in new_cards])
            if winners is None:
                winners, win_stacks, winning_hands = n.player_index, n.stack, n.winning_hand
            for i in lst:
                i.winner, i.win_stack, i.winning_hand = winners, win_stacks, winning_hands
            current_chips[n.player_index] += n.stack
            n.current_chips = current_chips
            lst.append(n)
            continue
        elif ' shows a ' in line:
            n = first_pass(Shows)
            new_cards = line.split(' shows a ')[1].split('.')[0].split(',')
            n.cards = [i.strip() for i in new_cards]
            lst.append(n)
            continue
        elif ' quits the game ' in line:
            n = first_pass(Quits)
            players_left = tuple([p for p in players_left if p != n.player_index])
            n.remaining_players = players_left
            lst.append(n)
            continue
        elif 'Flop: ' in line or 'flop' in line:
            p_person, p_amount = None, None
            n = first_pass(Flop)
            n.position = 'Flop'
            new_cards = line.split(' [')[1].split(']')[0].split(',')
            n.cards = [i.strip() for i in new_cards]
            lst.append(n)
            continue
        elif 'Turn: ' in line or 'turn: ' in line:
            p_person, p_amount = None, None
            n = first_pass(Turn)
            n.position = 'Turn'
            n.cards = line.split(' [')[1].split(']')[0].strip()
            lst.append(n)
            continue
        elif 'River: ' in line or 'river: ' in line:
            p_person, p_amount = None, None
            n = first_pass(River)
            n.position = 'River'
            n.cards = line.split(' [')[1].split(']')[0].strip()
            lst.append(n)
            continue
        elif 'Undealt cards: ' in line:
            p_person, p_amount = None, None
            n = first_pass(Undealt)
            new_cards = line.split(' [')[1].split(']')[0].split(',')
            n.cards = [i.strip() for i in new_cards]
            if len(n.cards) == 1:
                n.position = 'Post Turn'
            elif len(n.cards) == 2:
                n.position = 'Post Flop'
            lst.append(n)
            continue
        elif 'Player stacks:' in line:
            n = first_pass(PlayerStacks)
            n.player_name, n.player_index = n_lst, i_lst
            n.stack = 0
            n.current_chips, n.starting_chips = current_chips, start_chips
            lst.append(n)
            continue
    return lst


class_object_lst = [Requests, Approved, Joined, MyCards, SmallBlind, BigBlind, Folds, Calls, Raises, Checks, Wins,
                    Shows, Quits, Flop, Turn, River, Undealt, StandsUp, SitsIn, PlayerStacks]
