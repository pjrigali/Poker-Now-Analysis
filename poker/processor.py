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
    def __init__(self, text: Union[str, None]):
        self._text = None
        self._player_name = None
        self._player_index = None
        self._stack = None
        if text is not None:
            self.text = text
            self._player_name = _player_name(self.text)
            self._player_index = _player_index(self.text)
            self._stack = _stack(self.text)
        self._position = None
        self._winning_hand = None
        self._cards = None
        self._current_round = None
        self._pot_size = 0
        self._remaining_players = None
        self._action_from_player = None
        self._action_amount = None
        self._all_in = False
        self._game_id = None
        self._start_chips = None
        self._current_chips = None
        self._winner = None
        self._win_stack = None
        self._time = None
        self._previous_time = None

    @property
    def text(self) -> Union[str, None]:
        """Text input"""
        return self._text

    @text.setter
    def text(self, val):
        self._text = val

    @property
    def player_name(self) -> Union[str, None]:
        """Player Name"""
        return self._player_name

    @player_name.setter
    def player_name(self, val):
        self._player_name = val

    @property
    def player_index(self) -> Union[str, None]:
        """Player Id"""
        return self._player_index

    @player_index.setter
    def player_index(self, val):
        self._player_index = val

    @property
    def stack(self) -> Union[int, None]:
        """Amount offered to the table"""
        return self._stack

    @stack.setter
    def stack(self, val):
        self._stack = val

    @property
    def position(self) -> Union[str, None]:
        """Position of move in relation to table cards being drawn"""
        return self._position

    @position.setter
    def position(self, val):
        self._position = val

    @property
    def winning_hand(self) -> Union[str, None]:
        """Winning hand"""
        return self._winning_hand

    @winning_hand.setter
    def winning_hand(self, val):
        self._winning_hand = val

    @property
    def cards(self) -> Union[str, tuple, None]:
        """Card or cards"""
        return self._cards

    @cards.setter
    def cards(self, val):
        self._cards = val

    @property
    def current_round(self) -> Union[int, None]:
        """Round number within the game"""
        return self._current_round

    @current_round.setter
    def current_round(self, val):
        self._current_round = val

    @property
    def pot_size(self) -> Union[int, None]:
        """Size of pot when move happens"""
        return self._pot_size

    @pot_size.setter
    def pot_size(self, val):
        self._pot_size = val

    @property
    def remaining_players(self) -> Union[List[str], None]:
        """Players left in hand"""
        return self._remaining_players

    @remaining_players.setter
    def remaining_players(self, val):
        self._remaining_players = val

    @property
    def action_from_player(self) -> Union[str, None]:
        """Who bet previously"""
        return self._action_from_player

    @action_from_player.setter
    def action_from_player(self, val):
        self._action_from_player = val

    @property
    def action_amount(self) -> Union[int, None]:
        """Previous bet amount"""
        return self._action_amount

    @action_amount.setter
    def action_amount(self, val):
        self._action_amount = val

    @property
    def all_in(self) -> Union[bool, None]:
        """Notes if player when all-in"""
        return self._all_in

    @all_in.setter
    def all_in(self, val):
        self._all_in = val

    @property
    def game_id(self) -> Union[str, None]:
        """File name"""
        return self._game_id

    @game_id.setter
    def game_id(self, val):
        self._game_id = val

    @property
    def starting_chips(self) -> Union[int, None]:
        """Player's chip count at start of hand"""
        return self._start_chips

    @starting_chips.setter
    def starting_chips(self, val):
        self._start_chips = val

    @property
    def current_chips(self) -> Union[int, None]:
        """Player's chip count at start of hand"""
        return self._current_chips

    @current_chips.setter
    def current_chips(self, val):
        self._current_chips = val

    @property
    def winner(self) -> Union[str, None]:
        """Player Name who wins the hand"""
        return self._winner

    @winner.setter
    def winner(self, val):
        self._winner = val

    @property
    def win_stack(self) -> Union[int, None]:
        """Amount won at end of hand"""
        return self._win_stack

    @win_stack.setter
    def win_stack(self, val):
        self._win_stack = val

    @property
    def time(self):
        """Timestamp of action"""
        return self._time

    @time.setter
    def time(self, val):
        self._time = val

    @property
    def previous_time(self):
        """Timestamp of previous action"""
        return self._previous_time

    @previous_time.setter
    def previous_time(self, val):
        self._previous_time = val


@dataclass
class Requests(LineAttributes):
    """Class for players Requesting a seat."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return "Requests"


@dataclass
class Approved(LineAttributes):
    """Class for players when Approved a seat."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return "Approved"


@dataclass
class Joined(LineAttributes):
    """Class for players Joined the table."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return "Joined"


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
        return "Small Blind"


@dataclass
class BigBlind(LineAttributes):
    """Class for the Big Blind player."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return "Big Blind"


@dataclass
class Folds(LineAttributes):
    """Class for players that Fold."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return "Folds"


@dataclass
class Calls(LineAttributes):
    """Class for players that Call."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return "Calls"


@dataclass
class Raises(LineAttributes):
    """Class for players that Raise."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return "Raises"


@dataclass
class Checks(LineAttributes):
    """Class for players that Check."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return "Checks"


@dataclass
class Wins(LineAttributes):
    """Class for players that Win."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return "Wins"


@dataclass
class Shows(LineAttributes):
    """Class for players that Show their cards."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return "Shows"


@dataclass
class Quits(LineAttributes):
    """Class for players that Quit the table."""
    def __init__(self, text: str):
        super().__init__(text)

    def __repr__(self):
        return "Quits"


@dataclass
class Flop(LineAttributes):
    """Class for Flop cards."""
    def __init__(self, text: Union[str, None]):
        super().__init__(text)

    def __repr__(self):
        return "Flop Cards"


@dataclass
class Turn(LineAttributes):
    """Class for Turn card."""
    def __init__(self, text: Union[str, None]):
        super().__init__(text)

    def __repr__(self):
        return "Turn Card"


@dataclass
class River(LineAttributes):
    """Class for River card."""
    def __init__(self, text: Union[str, None]):
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


def parser(lines: List[str], times: list, game_id: str) -> list:
    """This parses strings and converts to class objects"""
    hand_position = []
    start_position = 'Pre Flop'
    for line in lines:
        if 'Flop:' in line or 'flop:' in line:
            start_position = 'Post Flop'
        if 'Turn:' in line or 'turn:' in line:
            start_position = 'Post Turn'
        if 'River:' in line or 'river:' in line:
            start_position = 'Post River'
        hand_position.append(start_position)

    curr_round = 0
    for line in lines:
        if 'starting hand' in line:
            curr_round = int(line.split('starting hand #')[1].split(' (')[0])
            break

    player_name_lst, player_index_lst, player_value_lst = [], [], []
    for line in lines:
        if _player_stacks(line=line) is not None:
            for play in line.split('#')[1:]:
                player_name_lst.append(play.split('@')[0].split('"')[1].strip())
                player_index_lst.append(play.split('@')[1].split('"')[0].strip())
                player_value_lst.append(int(play.split('(')[1].split(')')[0]))

    check_players_name_lst = False
    if len(player_name_lst) > 0:
        starting_chip_values = dict(zip(player_index_lst, player_value_lst))
        current_chip_values = dict(zip(player_index_lst, player_value_lst))
        check_players_name_lst = True

    pot_size = 0
    lst = []
    previous_time = None
    pressor = 'None'
    pressor_amount = 0
    players_left = player_index_lst
    for ind, line in enumerate(lines):

        if ind >= 1:
            previous_time = times[ind - 1]

        if _request(line) is not None:
            new = Requests(line)
            new.game_id = game_id
            new.current_round = curr_round
            new.pot_size = pot_size
            new.time = times[ind]
            new.previous_time = previous_time
            new.action_from_player = 'None'
            new.action_amount = 0
            new.starting_chips = 0
            new.current_chips = 0

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _approved(line) is not None:
            new = Approved(line)
            new.game_id = game_id
            new.current_round = curr_round
            new.pot_size = pot_size
            new.time = times[ind]
            new.previous_time = previous_time
            new.action_from_player = 'None'
            new.action_amount = 0
            new.starting_chips = 0
            new.current_chips = 0

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _joined(line) is not None:
            new = Joined(line)
            new.game_id = game_id
            new.current_round = curr_round
            new.pot_size = pot_size
            new.time = times[ind]
            new.previous_time = previous_time
            new.action_from_player = 'None'
            new.action_amount = 0
            new.starting_chips = 0
            new.current_chips = 0

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _stand_up(line) is not None:
            new = StandsUp(line)
            new.game_id = game_id
            new.current_round = curr_round
            new.pot_size = pot_size
            new.time = times[ind]
            new.previous_time = previous_time
            new.action_from_player = 'None'
            new.action_amount = 0
            players_left = [player for player in players_left if player != new.player_index]
            new.remaining_players = players_left

            if check_players_name_lst is True:
                new.starting_chips = starting_chip_values[new.player_index]
                new.current_chips = current_chip_values[new.player_index]

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _sit_in(line) is not None:
            new = SitsIn(line)
            new.game_id = game_id
            new.current_round = curr_round
            new.pot_size = pot_size
            new.time = times[ind]
            new.previous_time = previous_time
            new.action_from_player = 'None'
            new.action_amount = 0
            if check_players_name_lst is True:
                new.starting_chips = new.stack
                new.current_chips = new.stack

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _my_cards(line) is not None:
            new = MyCards(line)
            new.game_id = game_id
            new.current_round = curr_round
            new.pot_size = pot_size
            new.time = times[ind]
            new.previous_time = previous_time

            if new.cards is None:
                new_cards = line.split(' hand is ')[1].split(',')
                new.cards = tuple([i.strip() for i in new_cards])

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _small_blind(line) is not None:
            new = SmallBlind(line)
            new.game_id = game_id
            new.current_round = curr_round
            new.time = times[ind]
            new.previous_time = previous_time
            new.action_from_player = 'None'
            new.action_amount = pressor_amount
            new.remaining_players = players_left

            if new.stack is None:
                new.stack = int(line.split('of ')[1])

            pot_size += new.stack
            new.pot_size = pot_size
            pressor = new.player_index
            pressor_amount = new.stack

            if check_players_name_lst is True:
                current_chip_values[new.player_index] -= new.stack
                new.current_chips = current_chip_values[new.player_index]
                new.starting_chips = starting_chip_values[new.player_index]

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _big_blind(line) is not None:
            new = BigBlind(line)
            new.game_id = game_id
            new.current_round = curr_round
            new.time = times[ind]
            new.previous_time = previous_time
            new.action_from_player = pressor
            new.action_amount = pressor_amount
            new.remaining_players = players_left

            if new.stack is None:
                new.stack = int(line.split('of ')[1])

            pot_size += new.stack
            new.pot_size = pot_size
            pressor = new.player_index
            pressor_amount = new.stack
            if check_players_name_lst is True:
                current_chip_values[new.player_index] -= new.stack
                new.current_chips = current_chip_values[new.player_index]
                new.starting_chips = starting_chip_values[new.player_index]

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _folds(line) is not None:
            new = Folds(line)
            new.game_id = game_id
            new.current_round = curr_round
            new.pot_size = pot_size
            new.time = times[ind]
            new.previous_time = previous_time
            new.action_from_player = pressor
            new.action_amount = pressor_amount
            players_left = [player for player in players_left if player != new.player_index]
            new.remaining_players = players_left
            if check_players_name_lst is True:
                new.current_chips = current_chip_values[new.player_index]
                new.starting_chips = starting_chip_values[new.player_index]

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _calls(line) is not None:
            new = Calls(line)
            new.game_id = game_id
            new.current_round = curr_round
            new.time = times[ind]
            new.previous_time = previous_time
            new.remaining_players = players_left

            if new.stack is None:
                new_stack = line.split(' calls ')[1]
                if ' and ' in new_stack:
                    new_stack = int(new_stack.split(' and ')[0])
                else:
                    new_stack = int(new_stack)
                new.stack = new_stack

            pot_size += new.stack
            new.pot_size = pot_size
            new.action_from_player = pressor
            new.action_amount = pressor_amount
            if check_players_name_lst is True:
                current_chip_values[new.player_index] -= new.stack
                new.current_chips = current_chip_values[new.player_index]
                new.starting_chips = starting_chip_values[new.player_index]

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _raises(line) is not None:
            new = Raises(line)
            new.game_id = game_id
            new.current_round = curr_round
            new.time = times[ind]
            new.previous_time = previous_time
            new.remaining_players = players_left

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
            new.action_from_player = pressor
            new.action_amount = pressor_amount
            pressor = new.player_index
            pressor_amount = new.stack
            if check_players_name_lst is True:
                current_chip_values[new.player_index] -= new.stack
                new.current_chips = current_chip_values[new.player_index]
                new.starting_chips = starting_chip_values[new.player_index]

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _checks(line) is not None:
            new = Checks(line)
            new.game_id = game_id
            new.current_round = curr_round
            new.pot_size = pot_size
            new.time = times[ind]
            new.previous_time = previous_time
            new.action_from_player = pressor
            new.action_amount = 0
            new.remaining_players = players_left
            if check_players_name_lst is True:
                new.current_chips = current_chip_values[new.player_index]
                new.starting_chips = starting_chip_values[new.player_index]

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _wins(line) is not None:
            new = Wins(line)
            new.game_id = game_id
            new.current_round = curr_round
            new.pot_size = pot_size
            new.time = times[ind]
            new.previous_time = previous_time
            new.remaining_players = players_left

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

            if check_players_name_lst is True:
                current_chip_values[new.player_index] += new.stack
                new.current_chips = current_chip_values[new.player_index]
                new.starting_chips = starting_chip_values[new.player_index]
            lst.append(new)
            continue

        if _shows(line) is not None:
            new = Shows(line)
            new.game_id = game_id
            new.current_round = curr_round
            new.pot_size = pot_size
            new.time = times[ind]
            new.previous_time = previous_time
            new.action_from_player = 'None'
            new.action_amount = 0
            new.remaining_players = players_left
            new.stack = 0
            if check_players_name_lst is True:
                new.current_chips = current_chip_values[new.player_index]
                new.starting_chips = starting_chip_values[new.player_index]

            if new.cards is None:
                new_cards = line.split(' shows a ')[1].split('.')[0].split(',')
                new.cards = tuple([i.strip() for i in new_cards])

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _quits(line) is not None:
            new = Quits(line)
            new.game_id = game_id
            new.current_round = curr_round
            new.pot_size = pot_size
            new.time = times[ind]
            new.previous_time = previous_time
            new.action_from_player = 'None'
            new.action_amount = 0
            players_left = [player for player in players_left if player != new.player_index]
            new.remaining_players = players_left
            if check_players_name_lst is True:
                if new.player_index in starting_chip_values:
                    new.current_chips = current_chip_values[new.player_index]
                    new.starting_chips = starting_chip_values[new.player_index]

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

        if _flop(line) is not None:
            pressor = 'None'
            pressor_amount = 0
            new = Flop(line)
            new.game_id = game_id
            new.current_round = curr_round
            new.pot_size = pot_size
            new.time = times[ind]
            new.previous_time = previous_time
            new.action_from_player = pressor
            new.action_amount = pressor_amount
            new.remaining_players = players_left
            new.current_chips = 0
            new.starting_chips = 0

            if new.cards is None:
                new_cards = line.split(' [')[1].split(']')[0].split(',')
                new.cards = tuple([i.strip() for i in new_cards])

            if new.position is None:
                new.position = 'Flop'
            lst.append(new)
            continue

        if _turn(line) is not None:
            pressor = 'None'
            pressor_amount = 0
            new = Turn(line)
            new.game_id = game_id
            new.current_round = curr_round
            new.pot_size = pot_size
            new.time = times[ind]
            new.previous_time = previous_time
            new.action_from_player = pressor
            new.action_amount = pressor_amount
            new.remaining_players = players_left
            new.current_chips = 0
            new.starting_chips = 0

            if new.cards is None:
                new.cards = line.split(' [')[1].split(']')[0].strip()

            if new.position is None:
                new.position = 'Turn'
            lst.append(new)
            continue

        if _river(line) is not None:
            pressor = 'None'
            pressor_amount = 0
            new = River(line)
            new.game_id = game_id
            new.current_round = curr_round
            new.pot_size = pot_size
            new.time = times[ind]
            new.previous_time = previous_time
            new.action_from_player = pressor
            new.action_amount = pressor_amount
            new.remaining_players = players_left
            new.current_chips = 0
            new.starting_chips = 0

            if new.cards is None:
                new.cards = line.split(' [')[1].split(']')[0].strip()

            if new.position is None:
                new.position = 'River'
            lst.append(new)
            continue

        if _undealt(line) is not None:
            pressor = 'None'
            pressor_amount = 0
            new = Undealt(line)
            new.game_id = game_id
            new.current_round = curr_round
            new.pot_size = pot_size
            new.time = times[ind]
            new.previous_time = previous_time
            new.action_from_player = pressor
            new.action_amount = pressor_amount
            new.remaining_players = players_left
            new.current_chips = 0
            new.starting_chips = 0
            new.stack = 0

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
            new.game_id = game_id
            new.current_round = curr_round
            new.pot_size = pot_size
            new.time = times[ind]
            new.previous_time = previous_time
            new.action_from_player = 'None'
            new.action_amount = 0
            new.player_name = player_name_lst
            new.player_index = player_index_lst
            new.stack = 0
            new.remaining_players = players_left
            if check_players_name_lst is True:
                new.current_chips = player_value_lst
                new.starting_chips = player_value_lst

            if new.position is None:
                new.position = hand_position[ind]
            lst.append(new)
            continue

    return lst


class_object_lst = [Requests, Approved, Joined, MyCards, SmallBlind, BigBlind, Folds, Calls, Raises, Checks, Wins,
                    Shows, Quits, Flop, Turn, River, Undealt, StandsUp, SitsIn, PlayerStacks]
