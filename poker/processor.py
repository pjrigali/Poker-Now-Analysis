"""
Created on Sat Aug 15 14:27:18 2021

@author: Peter
"""
from dataclasses import dataclass
from typing import Optional, Union, List


def _player_name(text: str) -> Optional[str]:
    if ' @ ' in text:
        return text.split('"')[1].split('@')[0].strip()
    else:
        return None


def _player_index(text: str) -> Optional[str]:
    if ' @ ' in text:
        return text.split('@')[1].split('"')[0].strip()
    else:
        return None


def _stack(text: str) -> Optional[int]:
    if 'stack of ' in text:
        return int(text.split('stack of ')[1].split('.')[0])
    else:
        return 0


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
                 'end_time')

    def __init__(self, text: str = None):
        if text is not None:
            self.text = text
            self.player_name = _player_name(self.text)
            self.player_index = _player_index(self.text)
            self.stack = _stack(self.text)
        else:
            self.text = None
            self.player_name = None
            self.player_index = None
            self.stack = 0
        self.position = None
        self.winning_hand = None
        self.cards = None
        self.current_round = None
        self.pot_size = 0
        self.remaining_players = None
        self.action_from_player = 'None'
        self.action_amount = 0
        self.all_in = False
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
    def __init__(self, text: Union[str, None]):
        super().__init__(text)

    def __repr__(self) -> str:
        return "Flop Cards"


@dataclass
class Turn(LineAttributes):
    """Class for Turn card."""
    def __init__(self, text: Union[str, None]):
        super().__init__(text)

    def __repr__(self) -> str:
        return "Turn Card"


@dataclass
class River(LineAttributes):
    """Class for River card."""
    def __init__(self, text: Union[str, None]):
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
    player_name_lst, player_index_lst, player_value_lst, curr_round = [], [], [], 0
    for line in lines:
        if 'starting hand' in line:
            curr_round = int(line.split('starting hand #')[1].split(' (')[0])
        if 'Player stacks:' in line:
            for play in line.split('#')[1:]:
                player_name_lst.append(play.split('@')[0].split('"')[1].strip())
                player_index_lst.append(play.split('@')[1].split('"')[0].strip())
                player_value_lst.append(int(play.split('(')[1].split(')')[0]))

    if len(player_name_lst) == 0:
        for line in lines:
            if 'The admin approved' in line:
                player_name_lst.append(line.split('@')[0].split('"')[1].strip())
                player_index_lst.append(line.split('@')[1].split('"')[0].strip())
                player_value_lst.append(0)

    def _build_class(l: str, c, players_left, pot_size):
        c = c(l)
        if isinstance(c, Raises):
            if c.stack is None:
                n_s = 0
                if ' bets ' in l:
                    n_s = l.split(' bets ')[1]
                if ' raises to ' in l:
                    n_s = l.split(' raises to ')[1]
                if ' and ' in l:
                    n_s = n_s.split(' and ')[0]
                    c.all_in = True
                c.stack = int(n_s)
        if isinstance(c, (SmallBlind, BigBlind, Calls, Raises)):
            current_chip_values[c.player_index] -= c.stack
        elif isinstance(c, Wins):
            current_chip_values[c.player_index] += c.stack
        if isinstance(c, (StandsUp, Folds, Quits)):
            players_left = [player for player in players_left if player != c.player_index]
        c.game_id, c.current_round, c.pot_size, c.time = game_id, curr_round, pot_size, line_time_val
        c.previous_time, c.start_time, c.end_time, c.position = previous_time, start_time_val, end_time_val, start_position
        c.remaining_players, c.action_from_player, c.action_amount = players_left, pressor, pressor_amount
        if isinstance(c.player_index, str):
            if c.player_index in starting_chip_values:
                c.starting_chips, c.current_chips = starting_chip_values[c.player_index], current_chip_values[c.player_index]
        else:
            c.starting_chips, c.current_chips = starting_chip_values, current_chip_values
        if isinstance(c, SitsIn):
            c.starting_chips, c.current_chips = c.stack, c.stack
        return c

    start_time_val = times[0]
    end_time_val = times[-1]
    pot_size = 0
    lst = []
    previous_time = None
    pressor = None
    pressor_amount = 0
    players_left = player_index_lst
    small_blind, big_blind, flop, turn, river, undealt = False, False, False, False, False, False
    start_position = 'Pre Flop'
    starting_chip_values = dict(zip(player_index_lst, player_value_lst))
    current_chip_values = dict(zip(player_index_lst, player_value_lst))
    for ind, line in enumerate(lines):
        if 'Flop:' in line or 'flop:' in line:
            start_position = 'Post Flop'
        if 'Turn:' in line or 'turn:' in line:
            start_position = 'Post Turn'
        if 'River:' in line or 'river:' in line:
            start_position = 'Post River'
        line_time_val = times[ind]

        if ind >= 1:
            previous_time = times[ind - 1]

        if 'requested a seat' in line:
            lst.append(_build_class(line, Requests, players_left, pot_size))
            continue

        if 'The admin approved' in line:
            lst.append(_build_class(line, Approved, players_left, pot_size))
            continue

        if 'joined the game' in line:
            lst.append(_build_class(line, Joined, players_left, pot_size))
            continue

        if ' stand up with ' in line:
            lst.append(_build_class(line, StandsUp, players_left, pot_size))
            continue

        if ' sit back with ' in line:
            lst.append(_build_class(line, SitsIn, players_left, pot_size))
            continue

        if 'Your hand' in line:
            n = _build_class(line, MyCards, players_left, pot_size)
            if n.cards is None:
                new_cards = line.split(' hand is ')[1].split(',')
                n.cards = tuple([i.strip() for i in new_cards])
            lst.append(n)
            continue

        if small_blind is False:
            if 'posts a small blind' in line:
                n = _build_class(line, SmallBlind, players_left, pot_size)
                if n.stack is None:
                    n.stack = int(line.split('of ')[1])
                pot_size += n.stack
                n.pot_size = pot_size
                pressor = n.player_index
                pressor_amount = n.stack
                lst.append(n)
                small_blind = True
                continue

        if big_blind is False:
            if 'posts a big blind' in line:
                n = _build_class(line, BigBlind, players_left, pot_size)
                if n.stack is None:
                    n.stack = int(line.split('of ')[1])
                pot_size += n.stack
                n.pot_size = pot_size
                pressor = n.player_index
                pressor_amount = n.stack
                lst.append(n)
                big_blind = True
                continue

        if ' folds' in line:
            lst.append(_build_class(line, Folds, players_left, pot_size))
            continue

        if ' calls ' in line:
            n = _build_class(line, Calls, players_left, pot_size)
            if n.stack is None:
                new_stack = line.split(' calls ')[1]
                if ' and ' in new_stack:
                    new_stack = int(new_stack.split(' and ')[0])
                else:
                    new_stack = int(new_stack)
                n.stack = new_stack
            pot_size += n.stack
            n.pot_size = pot_size
            lst.append(n)
            continue

        if ' bets ' in line or ' raises ' in line:
            n = _build_class(line, Raises, players_left, pot_size)
            if n.stack is None:
                new_stack = 0
                if ' bets ' in line:
                    new_stack = line.split(' bets ')[1]
                if ' raises to ' in line:
                    new_stack = line.split(' raises to ')[1]
                if ' and ' in line:
                    new_stack = new_stack.split(' and ')[0]
                    n.all_in = True
                n.stack = int(new_stack)
            pot_size += n.stack
            n.pot_size = pot_size
            pressor = n.player_index
            pressor_amount = n.stack
            lst.append(n)
            continue

        if ' checks' in line:
            lst.append(_build_class(line, Checks, players_left, pot_size))
            continue

        if ' collected ' in line:
            n = _build_class(line, Wins, players_left, pot_size)
            if n.stack is None:
                n.stack = int(line.split(' collected ')[1].split(' from ')[0])
            if n.winning_hand is None:
                if ' from pot with ' in line:
                    if ', ' in line.split(' from pot with ')[1].split(' (')[0]:
                        n.winning_hand = line.split(' from pot with ')[1].split(', ')[0]
                    else:
                        n.winning_hand = line.split(' from pot with ')[1].split(' (')[0]
            if n.cards is None:
                if 'combination' in line:
                    new_cards = line.split(': ')[1].split(')')[0].split(',')
                    n.cards = tuple([i.strip() for i in new_cards])
            lst.append(n)
            continue

        if ' shows a ' in line:
            n = _build_class(line, Shows, players_left, pot_size)
            if n.cards is None:
                new_cards = line.split(' shows a ')[1].split('.')[0].split(',')
                n.cards = [i.strip() for i in new_cards]
            lst.append(n)
            continue

        if ' quits the game ' in line:
            lst.append(_build_class(line, Quits, players_left, pot_size))
            continue

        if flop is False:
            if 'Flop: ' in line or 'flop' in line:
                pressor = None
                pressor_amount = 0
                n = _build_class(line, Flop, players_left, pot_size)
                n.position = 'Flop'
                if n.cards is None:
                    new_cards = line.split(' [')[1].split(']')[0].split(',')
                    n.cards = [i.strip() for i in new_cards]
                lst.append(n)
                flop = True
                continue

        if turn is False:
            if 'Turn: ' in line or 'turn: ' in line:
                pressor = None
                pressor_amount = 0
                n = _build_class(line, Turn, players_left, pot_size)
                n.position = 'Turn'
                if n.cards is None:
                    n.cards = line.split(' [')[1].split(']')[0].strip()
                lst.append(n)
                turn = True
                continue

        if river is False:
            if 'River: ' in line or 'river: ' in line:
                pressor = None
                pressor_amount = 0
                n = _build_class(line, River, players_left, pot_size)
                n.position = 'River'
                if n.cards is None:
                    n.cards = line.split(' [')[1].split(']')[0].strip()
                lst.append(n)
                river = True
                continue

        if undealt is False:
            if 'Undealt cards: ' in line:
                pressor = None
                pressor_amount = 0
                n = _build_class(line, Undealt, players_left, pot_size)
                if n.cards is None:
                    new_cards = line.split(' [')[1].split(']')[0].split(',')
                    n.cards = [i.strip() for i in new_cards]
                if len(n.cards) == 1:
                    n.position = 'Post Turn'
                elif len(n.cards) == 2:
                    n.position = 'Post Flop'
                lst.append(n)
                undealt = True
                continue

        if 'Player stacks:' in line:
            n = _build_class(line, PlayerStacks, players_left, pot_size)
            n.player_name = player_name_lst
            n.player_index = player_index_lst
            n.stack = 0
            n.current_chips = player_value_lst
            n.starting_chips = player_value_lst
            lst.append(n)
            continue

    return lst


class_object_lst = [Requests, Approved, Joined, MyCards, SmallBlind, BigBlind, Folds, Calls, Raises, Checks, Wins,
                    Shows, Quits, Flop, Turn, River, Undealt, StandsUp, SitsIn, PlayerStacks]
