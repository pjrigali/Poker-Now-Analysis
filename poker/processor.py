"""
Created on Sat Aug 15 14:27:18 2021

@author: Peter
"""
from dataclasses import dataclass
from typing import Optional


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
        return None


@dataclass
class LineAttributes:
    """

    Applies attributes to a Class.

    :param text: A line of text from the data.
    :type text: str
    :example: *None*
    :note: This class is intended to be used internally.

    """
    def __init__(self, text: str):
        self.text = text
        self.player_name = _player_name(self.text)
        self.player_index = _player_index(self.text)
        self.stack = _stack(self.text)
        self.position = None
        self.winning_hand = None
        self.cards = None
        self.current_round = None
        self.pot_size = 0
        self.remaining_players = None
        self.action_from_player = None
        self.action_amount = None
        self.all_in = False


@dataclass
class Requests(LineAttributes):
    """Class for players Requesting a seat."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return self.player_name + " Requests"


@dataclass
class Approved(LineAttributes):
    """Class for players when Approved a seat."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return self.player_name + " Approved"


@dataclass
class Joined(LineAttributes):
    """Class for players Joined the table."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return self.player_name + " Joined"


@dataclass
class MyCards(LineAttributes):
    """Class for users cards."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return "Player Cards"


@dataclass
class SmallBlind(LineAttributes):
    """Class for the Small Blind player."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return self.player_name + " Small Blind"


@dataclass
class BigBlind(LineAttributes):
    """Class for the Big Blind player."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return self.player_name + " Big Blind"


@dataclass
class Folds(LineAttributes):
    """Class for players that Fold."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return self.player_name + " Folds"


@dataclass
class Calls(LineAttributes):
    """Class for players that Call."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return self.player_name + " Calls"


@dataclass
class Raises(LineAttributes):
    """Class for players that Raise."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return self.player_name + " Raises"


@dataclass
class Checks(LineAttributes):
    """Class for players that Check."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return self.player_name + " Checks"


@dataclass
class Wins(LineAttributes):
    """Class for players that Win."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return self.player_name + " Wins"


@dataclass
class Shows(LineAttributes):
    """Class for players that Show their cards."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return self.player_name + " Shows"


@dataclass
class Quits(LineAttributes):
    """Class for players that Quit the table."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return self.player_name + " Quits"


@dataclass
class Flop(LineAttributes):
    """Class for Flop cards."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return "Flop Cards"


@dataclass
class Turn(LineAttributes):
    """Class for Turn card."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return "Turn Card"


@dataclass
class River(LineAttributes):
    """Class for River card."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return "River Card"


@dataclass
class Undealt(LineAttributes):
    """Class for Undealt cards."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return "Undealt"


@dataclass
class StandsUp(LineAttributes):
    """Class for players that Stand Up."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return "Stand Up"


@dataclass
class SitsIn(LineAttributes):
    """Class for players that Sit In."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return "Sits In"


@dataclass
class PlayerStacks(LineAttributes):
    """Class for getting players and their stacks at the beginning of a hand"""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return "Player Stacks"


def _request(line: str) -> Optional[Requests]:

    if 'requested a seat' in line:
        return Requests(line)
    else:
        return None


def _approved(line: str) -> Optional[Approved]:

    if 'The admin approved' in line:
        return Approved(line)
    else:
        return None


def _joined(line: str) -> Optional[Joined]:

    if 'joined the game' in line:
        return Joined(line)
    else:
        return None


def _my_cards(line: str) -> Optional[MyCards]:

    if 'Your hand' in line:
        return MyCards(line)
    else:
        return None


def _small_blind(line: str) -> Optional[SmallBlind]:

    if 'posts a small blind' in line:
        return SmallBlind(line)
    else:
        return None


def _big_blind(line: str) -> Optional[BigBlind]:

    if 'posts a big blind' in line:
        return BigBlind(line)
    else:
        return None


def _folds(line: str) -> Optional[Folds]:

    if ' folds' in line:
        return Folds(line)
    else:
        return None


def _calls(line: str) -> Optional[Calls]:

    if ' calls ' in line:
        return Calls(line)
    else:
        return None


def _raises(line: str) -> Optional[Raises]:

    if ' bets ' in line or ' raises ' in line:
        return Raises(line)
    else:
        return None


def _checks(line: str) -> Optional[Checks]:

    if ' checks' in line:
        return Checks(line)
    else:
        return None


def _wins(line: str) -> Optional[Wins]:

    if ' collected ' in line:
        return Wins(line)
    else:
        return None


def _shows(line: str) -> Optional[Shows]:

    if ' shows a ' in line:
        return Shows(line)
    else:
        return None


def _quits(line: str) -> Optional[Quits]:

    if ' quits the game ' in line:
        return Quits(line)
    else:
        return None


def _flop(line: str) -> Optional[Flop]:

    if 'Flop: ' in line or 'flop' in line:
        return Flop(line)
    else:
        return None


def _turn(line: str) -> Optional[Turn]:

    if 'Turn: ' in line or 'turn: ' in line:
        return Turn(line)
    else:
        return None


def _river(line: str) -> Optional[River]:

    if 'River: ' in line or 'river: ' in line:
        return River(line)
    else:
        return None


def _undealt(line: str) -> Optional[Undealt]:

    if 'Undealt cards: ' in line:
        return Undealt(line)
    else:
        return None


def _stand_up(line: str) -> Optional[StandsUp]:

    if ' stand up with ' in line:
        return StandsUp(line)
    else:
        return None


def _sit_in(line: str) -> Optional[SitsIn]:

    if ' sit back with ' in line:
        return SitsIn(line)
    else:
        return None


def _player_stacks(line: str) -> Optional[PlayerStacks]:

    if 'Player stacks:' in line:
        return PlayerStacks(line)
    else:
        return None


def parser(hand) -> list:
    hand_position = []
    start_position = 'Pre Flop'
    for line in hand:
        if 'Flop:' in line or 'flop:' in line:
            start_position = 'Post Flop'
        if 'Turn:' in line or 'turn:' in line:
            start_position = 'Post Turn'
        if 'River:' in line or 'river:' in line:
            start_position = 'Post River'
        hand_position.append(start_position)

    curr_round = 0
    for line in hand:
        if 'starting hand' in line:
            curr_round = int(line.split('starting hand #')[1].split(' (')[0])
            break

    pot_size = 0
    lst = []
    for ind, line in enumerate(hand):

        if _request(line) is not None:
            new = Requests(line)
            new.current_round = curr_round
            new.pot_size = pot_size

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _approved(line) is not None:
            new = Approved(line)
            new.current_round = curr_round
            new.pot_size = pot_size

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _joined(line) is not None:
            new = Joined(line)
            new.current_round = curr_round
            new.pot_size = pot_size

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _stand_up(line) is not None:
            new = StandsUp(line)
            new.current_round = curr_round
            new.pot_size = pot_size

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _sit_in(line) is not None:
            new = SitsIn(line)
            new.current_round = curr_round
            new.pot_size = pot_size

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _my_cards(line) is not None:
            new = MyCards(line)
            new.current_round = curr_round
            new.pot_size = pot_size

            if new.cards is None:
                new_cards = line.split(' hand is ')[1].split(',')
                new.cards = tuple([i.strip() for i in new_cards])

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _small_blind(line) is not None:
            new = SmallBlind(line)
            new.current_round = curr_round

            if new.stack is None:
                new.stack = int(line.split('of ')[1])

            pot_size += new.stack
            new.pot_size = pot_size

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _big_blind(line) is not None:
            new = BigBlind(line)
            new.current_round = curr_round

            if new.stack is None:
                new.stack = int(line.split('of ')[1])

            pot_size += new.stack
            new.pot_size = pot_size

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _folds(line) is not None:
            new = Folds(line)
            new.current_round = curr_round
            new.pot_size = pot_size

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _calls(line) is not None:
            new = Calls(line)
            new.current_round = curr_round

            if new.stack is None:
                new_stack = line.split(' calls ')[1]
                if ' and ' in new_stack:
                    new_stack = int(new_stack.split(' and ')[0])
                else:
                    new_stack = int(new_stack)
                new.stack = new_stack

            pot_size += new.stack
            new.pot_size = pot_size

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _raises(line) is not None:
            new = Raises(line)
            new.current_round = curr_round

            if new.stack is None:
                new_stack = 0
                if ' bets ' in line:
                    new_stack = line.split(' bets ')[1]
                if ' raises to ' in line:
                    new_stack = line.split(' raises to ')[1]
                if ' and ' in line:
                    new_stack = new_stack.split(' and ')[0]
                    new.all_in = True
                new.stack = int(new_stack)

            pot_size += new.stack
            new.pot_size = pot_size

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _checks(line) is not None:
            new = Checks(line)
            new.current_round = curr_round
            new.pot_size = pot_size

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _wins(line) is not None:
            new = Wins(line)
            new.current_round = curr_round
            new.pot_size = pot_size

            if new.stack is None:
                new.stack = int(line.split(' collected ')[1].split(' from ')[0])

            if new.winning_hand is None:
                if ' from pot with ' in line:
                    if ', ' in line.split(' from pot with ')[1].split(' (')[0]:
                        new.winning_hand = line.split(' from pot with ')[1].split(', ')[0]
                    else:
                        new.winning_hand = line.split(' from pot with ')[1].split(' (')[0]

            if new.cards is None:
                if 'combination' in line:
                    new_cards = line.split(': ')[1].split(')')[0].split(',')
                    new.cards = tuple([i.strip() for i in new_cards])

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _shows(line) is not None:
            new = Shows(line)
            new.current_round = curr_round
            new.pot_size = pot_size

            if new.cards is None:
                new_cards = line.split(' shows a ')[1].split('.')[0].split(',')
                new.cards = tuple([i.strip() for i in new_cards])

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _quits(line) is not None:
            new = Quits(line)
            new.current_round = curr_round
            new.pot_size = pot_size

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _flop(line) is not None:
            new = Flop(line)
            new.current_round = curr_round
            new.pot_size = pot_size

            if new.cards is None:
                new_cards = line.split(' [')[1].split(']')[0].split(',')
                new.cards = tuple([i.strip() for i in new_cards])

            if new.position is None:
                new.position = 'Flop'
            lst.append(new)
            continue

        if _turn(line) is not None:
            new = Turn(line)
            new.current_round = curr_round
            new.pot_size = pot_size

            if new.cards is None:
                new.cards = line.split(' [')[1].split(']')[0].strip()

            if new.position is None:
                new.position = 'Turn'
            lst.append(new)
            continue

        if _river(line) is not None:
            new = River(line)
            new.current_round = curr_round
            new.pot_size = pot_size

            if new.cards is None:
                new.cards = line.split(' [')[1].split(']')[0].strip()

            if new.position is None:
                new.position = 'River'
            lst.append(new)
            continue

        if _undealt(line) is not None:
            new = Undealt(line)
            new.current_round = curr_round
            new.pot_size = pot_size

            if new.cards is None:
                new_cards = line.split(' [')[1].split(']')[0].split(',')
                new.cards = tuple([i.strip() for i in new_cards])

            if new.position is None:
                if len(new.cards) == 1:
                    new.position = 'Post Turn'
                elif len(new.cards) == 2:
                    new.position = 'Post Flop'
            lst.append(new)
            continue

        if _player_stacks(line) is not None:
            new = PlayerStacks(line)
            new.current_round = curr_round
            new.pot_size = pot_size

            p_name_lst = []
            p_index_lst = []
            p_value_lst = []
            for play in line.split('#')[1:]:
                p_name = play.split('@')[0].split('"')[1].strip()
                p_index = play.split('@')[1].split('"')[0].strip()
                p_value = int(play.split('(')[1].split(')')[0])
                p_name_lst.append(p_name)
                p_index_lst.append(p_index)
                p_value_lst.append(p_value)

            new.player_name = p_name_lst
            new.player_index = p_index_lst
            new.stack = p_value_lst

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

    return lst
