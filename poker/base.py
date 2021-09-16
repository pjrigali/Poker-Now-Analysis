from typing import List, Optional, Union
from dataclasses import dataclass
import numpy as np
import pandas as pd
from os import walk
from collections import Counter
from poker.analysis import whfc, streak, drsw, dealer_small_big, winning_cards, win_count
from poker.processor import Requests, Approved, Joined, MyCards, SmallBlind, BigBlind, Folds, Calls, Raises, Checks
from poker.processor import Wins, Shows, Quits, Flop, Turn, River, Undealt, StandsUp, SitsIn, PlayerStacks
from poker.processor import parser


def normalize(arr: np.ndarray, multi: Optional[bool] = None) -> np.ndarray:
    """

    Normalize an Array.

    :param arr: Input array.
    :type arr: np.ndarray
    :param multi: If array has multiple columns, default is None.
    :type multi: bool
    :return: Normalized array.
    :rtype: np.ndarray
    :example: *None*
    :note: Set *multi* to True, if multiple columns.

    """
    if multi:
        return np.array([(arr[:, i] - np.min(arr[:, i])) / (np.max(arr[:, i]) - np.min(arr[:, i])) for i in
                         range(arr.shape[1])]).T
    else:
        return np.around((arr - np.min(arr)) / (np.max(arr) - np.min(arr)).T, 3)


def running_mean(arr: np.ndarray, num: int) -> np.ndarray:
    """

    Calculate the running mean on *num* interval

    :param arr: Input array.
    :type arr: np.ndarray
    :param num: Input int, default is 50.
    :type num: int
    :return: Running mean for a given array.
    :rtype: np.ndarray
    :example: *None*
    :note: *None*

    """
    cum_sum = np.cumsum(np.insert(arr=arr, values=[np.mean(arr)] * num, obj=0))
    return (cum_sum[num:] - cum_sum[:-num]) / float(num)


def cumulative_mean(arr: np.ndarray) -> np.ndarray:
    """

    Calculate the cumulative mean.

    :param arr: Input array.
    :type arr: np.ndarray
    :return: Cumulative mean for a given array.
    :rtype: np.ndarray
    :example: *None*
    :note: *None*

    """
    cum_sum = np.cumsum(arr, axis=0)
    for i in range(cum_sum.shape[0]):
        cum_sum[i] = cum_sum[i] / (i + 1)
    return cum_sum


def _convert_shapes(data: List[str]) -> List[str]:
    return [row.replace("â£", " Clubs").replace("â¦", " Diamonds").replace("â¥", " Hearts").replace("â", " Spades") for row in data]


def _get_hands(repo: str, file: str) -> List[str]:
    df = pd.read_csv(repo + file, encoding='latin1')['entry']
    lst = _convert_shapes(list(df.reindex(index=df.index[::-1]).reset_index(drop=True)))
    hands, hand_lst = [], []
    for item in lst:
        if ' starting hand ' in item:
            if ' hand #1 ' in item:
                hands.append(hand_lst)
            hand_lst = []
            hand_lst.append(item)
            hands.append(hand_lst)
        else:
            hand_lst.append(item)
    return hands


@dataclass
class Hand:
    """

    Calculate stats for a Hand.

    :param hand: A list of strings associated with a hand.
    :type hand: List[str]
    :example: *None*
    :note: This class is intended to be used internally.

    """
    def __init__(self, hand: List[str]):
        self._hand = hand
        self._parsed_hand = [line for line in parser(hand=self._hand)]

        self._small_blind = None
        self._big_blind = None
        self._winner = None
        self._winning_cards = None
        self._winning_hand = None
        self._starting_players = None
        self._starting_player_chips = None
        self._flop = None
        self._turn = None
        self._river = None
        self._my_cards = None
        for line in self._parsed_hand:
            if type(line) == SmallBlind:
                self._small_blind = {line.player_name: line.stack}
                continue
            elif type(line) == BigBlind:
                self._big_blind = {line.player_name: line.stack}
                continue
            elif type(line) == Wins:
                lst = []
                if self._flop is not None:
                    lst += self._flop
                if self._turn is not None:
                    lst.append(self._turn)
                if self._river is not None:
                    lst.append(self._river)
                if line.cards is not None:
                    self._winning_cards = line.cards
                if line.player_name is not None:
                    self._winner = {line.player_name: line.stack}

                if self._winner is not None:
                    if self._winning_cards is None:
                        for temp_line in self._parsed_hand:
                            if type(temp_line) == Shows:
                                if temp_line.player_name == self._winner:
                                    self._winning_cards = temp_line.cards
                                    break

                if self._winning_cards is not None:
                    temp = []
                    for card in self._winning_cards:
                        if card not in lst:
                            temp.append(card)
                    self._winning_cards = tuple(temp)

                if line.winning_hand is not None:
                    self._winning_hand = line.winning_hand
                continue
            elif type(line) == PlayerStacks:
                self._starting_players = dict(zip(line.player_name, line.player_index))
                self._starting_player_chips = dict(zip(line.player_name, line.stack))
                continue
            elif type(line) == Flop:
                self._flop = line.cards
                continue
            elif type(line) == Turn:
                self._turn = line.cards
                continue
            elif type(line) == River:
                self._river = line.cards
                continue
            elif type(line) == MyCards:
                self._my_cards = line.cards

    def __repr__(self):
        return "Hand " + str(self.parsed_hand[0].current_round)

    @property
    def parsed_hand(self) -> list:
        """Returns a list of actions as objects"""
        return self._parsed_hand

    @property
    def small_blind(self) -> Optional[dict]:
        """Returns small blind person and amount"""
        return self._small_blind

    @property
    def big_blind(self) -> Optional[dict]:
        """Returns big blind person and amount"""
        return self._big_blind

    @property
    def winner(self) -> Optional[dict]:
        """Returns winner name and amount won"""
        return self._winner

    @property
    def winning_cards(self) -> Optional[tuple]:
        """Return winning cards, if they are shown"""
        return self._winning_cards

    @property
    def winning_hand(self) -> Optional[str]:
        """Returns winning hand"""
        return self._winning_hand

    @property
    def starting_players(self) -> Optional[dict]:
        """Returns dict of name and ID for each player that was present at the hand start"""
        return self._starting_players

    @property
    def starting_players_chips(self) -> Optional[dict]:
        """Returns dict of name and stack amount for each player that was present at the hand start"""
        return self._starting_player_chips

    @property
    def flop_cards(self) -> Optional[tuple]:
        """Returns flop cards"""
        return self._flop

    @property
    def turn_card(self) -> Optional[str]:
        """Returns turn card"""
        return self._turn

    @property
    def river_card(self) -> Optional[str]:
        """Returns river card"""
        return self._river

    @property
    def my_cards(self) -> Optional[tuple]:
        """Returns player cards"""
        return self._my_cards


def _check(line, cl, prfc: Optional[list] = None, pofc: Optional[list] = None, potc: Optional[list] = None,
           porc: Optional[list] = None, prfl: Optional[list] = None, pofl: Optional[list] = None, potl: Optional[list] = None,
           porl: Optional[list] = None) -> None:
    if type(line) == cl:
        if line.position == 'Pre Flop':
            if prfc is not None:
                prfc.append(1)
            if prfl is not None:
                prfl.append(line.stack)
            return
        if line.position == 'Post Flop':
            if pofc is not None:
                pofc.append(1)
            if pofl is not None:
                pofl.append(line.stack)
            return
        if line.position == 'Post Turn':
            if potc is not None:
                potc.append(1)
            if potl is not None:
                potl.append(line.stack)
            return
        if line.position == 'Post River':
            if porc is not None:
                porc.append(1)
            if porl is not None:
                porl.append(line.stack)
            return


def _make_dict(keyword: str, class_word: str, prf: list, pof: list, pot: list, por: list) -> dict:
    temp_lst = []
    for lst in [prf, pof, pot, por]:
        if keyword == 'Count':
            val = np.sum(lst)
        elif keyword == 'Median':
            val = np.median(lst)
        elif keyword == 'Std':
            val = np.std(lst)
        elif keyword == 'Mode':
            vals, counts = np.unique(lst, return_counts=True)
            try:
                val = vals[np.argmax(counts)]
            except:
                val = np.median(lst)
        elif keyword == 'Average':
            val = np.mean(lst)
        else:
            raise AttributeError('Keyword needs to be {Count, Median, Std, Mode, Average}')
        temp_lst.append(val)
    return {class_word + ' ' + keyword: np.nan_to_num(temp_lst)}


def _make_df(lst: List[dict], length: int) -> pd.DataFrame:
    dic_lst = [_make_dict(keyword=dic['keyword'], class_word=dic['class word'], prf=dic['lists'][0],
                               pof=dic['lists'][1], pot=dic['lists'][2], por=dic['lists'][3]) for dic in lst]
    temp_df = pd.DataFrame({k: v for d in dic_lst for k, v in d.items()},
                           index=['Pre Flop', 'Post Flop', 'Post Turn', 'Post River'])
    for col in temp_df.columns:
        if 'Count' in col:
            temp_df[col.replace("Count", "Percent")] = [round(item / length, 3) if item != 0 else 0 for item in temp_df[col]]
    return temp_df


@dataclass
class Player:
    """

    Calculate stats for a player. Stats are for a single match.

    :param player_index: A unique player ID.
    :type player_index: str
    :param hands: list of Hand objects related to a game.
    :type hands: List[Hand]
    :example: *None*
    :note: This class is intended to be used internally.

    """
    def __init__(self, player_index: str, hands: List[Hand]):
        self._player_index = player_index
        self._temp_ind = ['Pre Flop', 'Post Flop', 'Post Turn', 'Post River']

        win_stack_lst, win_cards_lst, win_hand_lst, win_position_lst = [], [], [], []
        # Winning Stats
        wprf_check_count, wpof_check_count, wpot_check_count, wpor_check_count = [], [], [], []
        wprf_call_count, wpof_call_count, wpot_call_count, wpor_call_count = [], [], [], []
        wprf_call_lst, wpof_call_lst, wpot_call_lst, wpor_call_lst = [], [], [], []
        wprf_raise_count, wpof_raise_count, wpot_raise_count, wpor_raise_count = [], [], [], []
        wprf_raise_lst, wpof_raise_lst, wpot_raise_lst, wpor_raise_lst = [], [], [], []
        # Normal Stats
        prf_check_count, pofl_check_count, pot_check_count, por_check_count = [], [], [], []
        prf_fold_count, pof_fold_count, pot_fold_count, por_fold_count = [], [], [], []
        prf_call_count, pof_call_count, pot_call_count, por_call_count = [], [], [], []
        prf_call_lst, pof_call_lst, pot_call_lst, por_call_lst = [], [], [], []
        prf_raise_count, pof_raise_count, pot_raise_count, por_raise_count = [], [], [], []
        prf_raise_lst, pof_raise_lst, pot_raise_lst, por_raise_lst = [], [], [], []

        hand_count = 0
        for hand in hands:
            for line in hand.parsed_hand:
                if line.player_index is not None:
                    if line.player_index == self._player_index or self._player_index in line.player_index:
                        # Count of hands the player is in.
                        if type(line) == PlayerStacks:
                            hand_count += 1
                        # Player Win information.
                        if type(line) == Wins:
                            win_stack_lst.append(line.stack)
                            win_cards_lst.append(line.cards)
                            win_hand_lst.append(line.winning_hand)
                            win_position_lst.append(line.position)
                            for line in hand.parsed_hand:
                                if line.player_index == self._player_index:
                                    _check(line=line, cl=Checks, prfc=wprf_check_count, pofc=wpof_check_count,
                                           potc=wpot_check_count, porc=wpor_check_count)
                                    _check(line=line, cl=Calls, prfc=wprf_call_count, pofc=wpof_call_count,
                                           potc=wpot_call_count, porc=wpor_call_count, prfl=wprf_call_lst,
                                           pofl=wpof_call_lst, potl=wpot_call_lst, porl=wpor_call_lst)
                                    _check(line=line, cl=Raises, prfc=wprf_raise_count, pofc=wpof_raise_count,
                                           potc=wpot_raise_count, porc=wpor_raise_count, prfl=wprf_raise_lst,
                                           pofl=wpof_raise_lst, potl=wpot_raise_lst, porl=wpor_raise_lst)
                        # Checks, Folds, Calls, and Raises info
                        _check(line=line, cl=Checks, prfc=prf_check_count, pofc=pofl_check_count,
                               potc=pot_check_count, porc=por_check_count)
                        _check(line=line, cl=Folds, prfc=prf_fold_count, pofc=pof_fold_count,
                               potc=pot_fold_count, porc=por_fold_count)
                        _check(line=line, cl=Calls, prfc=prf_call_count, pofc=pof_call_count,
                               potc=pot_call_count, porc=por_call_count, prfl=prf_call_lst,
                               pofl=pof_call_lst, potl=pot_call_lst, porl=por_call_lst)
                        _check(line=line, cl=Raises, prfc=prf_raise_count, pofc=pof_raise_count,
                               potc=pot_raise_count, porc=por_raise_count, prfl=prf_raise_lst,
                               pofl=pof_raise_lst, potl=pot_raise_lst, porl=por_raise_lst)

        win_df = pd.DataFrame([win_stack_lst, win_cards_lst, win_hand_lst, win_position_lst]).T
        win_df.columns = ['Win Stack', 'Win Cards', 'Win Hand', 'Win Position']
        if len(win_df) > 1:
            self._win_df = win_df
            self._largest_win = np.max(win_df['Win Stack'])
            self._win_position_dist_df = pd.DataFrame.from_dict(dict(Counter(list(win_df['Win Position']))), orient='index',
                                                                columns=['Count'])
            self._win_position_dist_df['Percent'] = self._win_position_dist_df / len(win_df)
            self._win_hand_dist_df = pd.DataFrame.from_dict(dict(Counter(list(win_df['Win Hand']))), orient='index',
                                                            columns=['Count'])
            self._win_hand_dist_df['Percent'] = self._win_hand_dist_df / len(win_df)
            card_lst = list(win_df['Win Cards'].dropna())
            self._win_cards_dist_df = pd.DataFrame.from_dict(dict(Counter(sum([list(cards) for cards in card_lst], []))),
                                                             orient='index', columns=['Count'])

            lst = [{'keyword': 'Count', 'class word': 'Check',
                    'lists': [wprf_check_count, wpof_check_count, wpot_check_count, wpor_check_count]},
                   {'keyword': 'Average', 'class word': 'Call',
                    'lists': [wprf_call_lst, wpof_call_lst, wpot_call_lst, wpor_call_lst]},
                   {'keyword': 'Mode', 'class word': 'Call',
                    'lists': [wprf_call_lst, wpof_call_lst, wpot_call_lst, wpor_call_lst]},
                   {'keyword': 'Std', 'class word': 'Call',
                    'lists': [wprf_call_lst, wpof_call_lst, wpot_call_lst, wpor_call_lst]},
                   {'keyword': 'Count', 'class word': 'Call',
                    'lists': [wprf_call_count, wpof_call_count, wpot_call_count, wpor_call_count]},
                   {'keyword': 'Average', 'class word': 'Raise',
                    'lists': [wprf_raise_lst, wpof_raise_lst, wpot_raise_lst, wpor_raise_lst]},
                   {'keyword': 'Mode', 'class word': 'Raise',
                    'lists': [wprf_raise_lst, wpof_raise_lst, wpot_raise_lst, wpor_raise_lst]},
                   {'keyword': 'Std', 'class word': 'Raise',
                    'lists': [wprf_raise_lst, wpof_raise_lst, wpot_raise_lst, wpor_raise_lst]},
                   {'keyword': 'Count', 'class word': 'Raise',
                    'lists': [wprf_raise_count, wpof_raise_count, wpot_raise_count, wpor_raise_count]},
                   ]
            self._winning_stats = _make_df(lst=lst, length=len(self._win_df))

            lst = [{'keyword': 'Count', 'class word': 'Check',
                    'lists': [prf_check_count, pofl_check_count, pot_check_count, por_check_count]},
                   {'keyword': 'Count', 'class word': 'Fold',
                    'lists': [prf_fold_count, pof_fold_count, pot_fold_count, por_fold_count]},
                   {'keyword': 'Average', 'class word': 'Call',
                    'lists': [prf_call_lst, pof_call_lst, pot_call_lst, por_call_lst]},
                   {'keyword': 'Mode', 'class word': 'Call',
                    'lists': [prf_call_lst, pof_call_lst, pot_call_lst, por_call_lst]},
                   {'keyword': 'Std', 'class word': 'Call',
                    'lists': [prf_call_lst, pof_call_lst, pot_call_lst, por_call_lst]},
                   {'keyword': 'Count', 'class word': 'Call',
                    'lists': [prf_call_count, pof_call_count, pot_call_count, por_call_count]},
                   {'keyword': 'Average', 'class word': 'Raise',
                    'lists': [prf_raise_lst, pof_raise_lst, pot_raise_lst, por_raise_lst]},
                   {'keyword': 'Mode', 'class word': 'Raise',
                    'lists': [prf_raise_lst, pof_raise_lst, pot_raise_lst, por_raise_lst]},
                   {'keyword': 'Std', 'class word': 'Raise',
                    'lists': [prf_raise_lst, pof_raise_lst, pot_raise_lst, por_raise_lst]},
                   {'keyword': 'Count', 'class word': 'Raise',
                    'lists': [prf_raise_count, pof_raise_count, pot_raise_count, por_raise_count]},
                   ]
            self._stats = _make_df(lst=lst, length=hand_count)

        else:
            self._win_df = None
            self._largest_win = None
            self._win_position_dist_df = None
            self._win_hand_dist_df = None
            self._win_cards_dist_df = None
            self._winning_stats = None
            self._stats = None

        if hand_count == 0:
            self._win_per = 0.0
        else:
            self._win_per = round(len(win_df) / hand_count, 2)

        if len(win_df) == 0:
            self._win_count = 0
        else:
            self._win_count = len(win_df)

        hand_lst = []
        for hand in hands:
            for line in hand.parsed_hand:
                if type(line) == PlayerStacks and self._player_index in line.player_index:
                    hand_lst.append(hand)
                    break

        reaction_lst = []
        for hand in hand_lst:
            temp_stack, temp_position, temp_person, temp_round, temp_player_stack = None, None, None, None, None
            temp_win, temp_win_stack = False, 0
            for line in hand.parsed_hand:
                if type(line) == Wins and line.player_index == self._player_index:
                    temp_win, temp_win_stack = True, line.stack
                    break
            for line in hand.parsed_hand:
                if type(line) == PlayerStacks:
                    temp_player_stack = line.stack[line.player_index.index(self._player_index)]
                if type(line) == Raises and line.player_index != self._player_index:
                    temp_stack, temp_position, temp_person, temp_round = line.stack, line.position, line.player_index, line.current_round
                if type(line) == Calls or type(line) == Folds:
                    if line.player_index == self._player_index and temp_person is not None:
                        cl = 'Folds'
                        if type(line) == Calls:
                            cl = 'Calls'
                        reaction_lst.append({'person': temp_person, 'stack': temp_stack, 'position': temp_position,
                                             'round': temp_round, 'player reserve': temp_player_stack, 'class': cl,
                                             'win': temp_win, 'win_stack': temp_win_stack})
                        if type(line) == Folds:
                            break
        self._player_reaction = pd.DataFrame(reaction_lst)

        if 'player reserve' in self._player_reaction.columns:
            previous, max_loss = 0, 0
            for val in self._player_reaction['player reserve']:
                if val - previous < max_loss:
                    max_loss = val - previous
                previous = val
            self._largest_loss = max_loss
        else:
            self._largest_loss = 0

    def __repr__(self):
        return self._player_index

    @property
    def win_df(self) -> pd.DataFrame:
        """Returns info detailing all of the players wins"""
        return self._win_df

    @property
    def win_per(self) -> float:
        """Returns player win percent"""
        return self._win_per

    @property
    def win_count(self) -> int:
        """Returns player win count"""
        return self._win_count

    @property
    def largest_win(self) -> int:
        """Returns players largest win"""
        return int(self._largest_win)

    @property
    def largest_loss(self) -> int:
        """Returns players largest loss"""
        return self._largest_loss

    @property
    def winning_habits(self) -> pd.DataFrame:
        """Returns player betting habits when they did win"""
        return self._winning_stats

    @property
    def normal_habits(self) -> pd.DataFrame:
        """Returns player betting habits when they didnt win"""
        return self._stats

    @property
    def win_position_distribution(self) -> pd.DataFrame:
        """Returns count and percentage of player win locations"""
        return self._win_position_dist_df.reindex(self._temp_ind)

    @property
    def win_hand_distribution(self) -> pd.DataFrame:
        """Returns count for each card that a player won with"""
        return self._win_hand_dist_df

    @property
    def win_card_distribution(self) -> pd.DataFrame:
        """Returns count and percentage of player winning hands"""
        return self._win_cards_dist_df

    @property
    def reaction(self) -> pd.DataFrame:
        """Returns player info related to when they called or folded"""
        return self._player_reaction


@dataclass
class Game:
    """

    Calculate stats for a game.

    :param repo_location: Location of data folder.
    :type repo_location: str
    :param file: Name of file.
    :type file: str
    :example: *None*
    :note: This class is intended to be used internally.

    """
    def __init__(self, repo_location: str, file: str):
        self._repo = repo_location
        self._file = file
        hands = _get_hands(repo=self._repo, file=self._file)
        self._class_lst = [Hand(hand=hand) for hand in hands]

        player_dic = {}
        for hand in self._class_lst:
            for line in hand.parsed_hand:
                if type(line) == Approved:
                    if line.player_index in player_dic.keys():
                        if line.player_name not in player_dic[line.player_index]['Player Names']:
                            player_dic[line.player_index]['Player Names'].append(line.player_name)
                        player_dic[line.player_index]['player stack'].append(line.stack)
                    else:
                        player_dic[line.player_index] = {'Player Names': [line.player_name],
                                                         'player stack': [line.stack],
                                                         'player quits': [],
                                                         'player stands up': [],
                                                         'player sits in': []}

        for hand in self._class_lst:
            for line in hand.parsed_hand:
                if type(line) == Quits:
                    player_dic[line.player_index]['player quits'].append(line.stack)
                if type(line) == StandsUp and line.player_index in player_dic.keys():
                    player_dic[line.player_index]['player stands up'].append(line.stack)
                if type(line) == SitsIn and line.player_index in player_dic.keys():
                    player_dic[line.player_index]['player sits in'].append(line.stack)
        self._player_dic = player_dic

        temp_df = pd.DataFrame.from_dict(self._player_dic, orient='index')
        buy_in_sum, player_loses, player_stands_up_sum, player_sits_in_sum = [], [], [], []
        for ind in list(temp_df.index):
            buy_in_sum.append(np.sum(temp_df.loc[ind]['player stack']))
            player_loses.append(len(temp_df.loc[ind]['player quits']))
            player_stands_up_sum.append(np.sum(temp_df.loc[ind]['player stands up']))
            player_sits_in_sum.append(np.sum(temp_df.loc[ind]['player sits in']))

        temp_df['Buy in Total'] = buy_in_sum
        temp_df['Loss Count'] = player_loses
        temp_df['player stands up sum'] = player_stands_up_sum
        temp_df['player sits in sum'] = player_sits_in_sum
        temp_df['Leave Table Amount'] = temp_df['player stands up sum'] - temp_df['player sits in sum']
        self._player_dic_df = temp_df[['Player Names', 'Buy in Total', 'Loss Count', 'Leave Table Amount']]

        flop, turn, river, win, my_cards = [], [], [], [], []
        for hand in self._class_lst:
            if hand.flop_cards is not None:
                flop.append(list(hand.flop_cards))
            if hand.turn_card is not None:
                turn.append(hand.turn_card)
            if hand.river_card is not None:
                river.append(hand.river_card)
            if hand.winning_cards is not None:
                win.append(list(hand.winning_cards))
            if hand.my_cards is not None:
                my_cards.append(list(hand.my_cards))

        dist_df = pd.DataFrame([dict(Counter(sum(flop, []))), dict(Counter(turn)), dict(Counter(river)),
                                dict(Counter(sum(win, []))), dict(Counter(sum(my_cards, [])))]).T
        dist_df.columns = ['Flop Count', 'Turn Count', 'River Count', 'Win Count', 'My Cards Count']
        self._card_distribution = dist_df.fillna(0)
        self._winning_hand_dist = pd.DataFrame.from_dict(dict(Counter([hand.winning_hand for hand in self._class_lst])),
                                                         orient='index',
                                                         columns=['Count']).sort_values('Count', ascending=False)
        self._players = {plyr: Player(player_index=plyr, hands=self._class_lst) for plyr in self._player_dic.keys()}

    def __repr__(self):
        val = self._file
        if "." in val:
            val = self._file.split(".")[0]
        return val

    @property
    def file_name(self) -> str:
        """Returns name of data file"""
        return self._file

    @property
    def hands_lst(self) -> List[Hand]:
        """Returns list of hands in the game"""
        return self._class_lst

    @property
    def players_info(self) -> pd.DataFrame:
        """Returns player total buy-in, loss count and leave table amount"""
        return self._player_dic_df

    @property
    def card_distribution(self) -> pd.DataFrame:
        """Returns count of each card that showed up"""
        return self._card_distribution

    @property
    def winning_hand_distribution(self) -> pd.DataFrame:
        """Returns count of winning hands"""
        return self._winning_hand_dist

    @property
    def players(self) -> dict:
        """Returns Player objects for players across games"""
        return self._players


@dataclass
class Poker:
    """

    Calculate stats for all games and players.

    :param repo_location: Location of data folder.
    :type repo_location: str
    :param grouped: List of lists, filled with unique player Ids that are related to the same person. *Optional*
    :type grouped: str
    :param money_multi: Multiple to divide the money amounts to translate them to dollars *Optional*
    :type money_multi: int
    :example:
        >>> from poker.base import Poker
        >>> repo = 'location of your previous game'
        >>> grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
        >>>             ['48QVRRsiae', 'u8_FUbXpAz']]
        >>> poker = Poker(repo_location=repo, grouped=grouped)
    :note: *None*

    """
    def __init__(self, repo_location: str, grouped: Optional[list] = None, money_multi: Optional[int] = 100):
        self._repo_location = repo_location
        self._files = next(walk(self._repo_location))[2]

        self._grouped = None
        if grouped:
            self._grouped = grouped

        self._matches = [Game(repo_location=self._repo_location, file=file) for file in self._files]

        player_dic = {}
        for match in self._matches:
            temp_df = match.players_info
            for ind in list(temp_df.index):
                if ind in player_dic.keys():
                    player_dic[ind]['Player Names'] = list(set(player_dic[ind]['Player Names'] + temp_df.loc[ind]['Player Names']))

                    if ind not in player_dic[ind]['Player Ids']:
                        player_dic[ind]['Player Ids'].append(ind)

                    player_dic[ind]['Buy in Total'] = player_dic[ind]['Buy in Total'] + temp_df.loc[ind]['Buy in Total']
                    player_dic[ind]['Loss Count'] = player_dic[ind]['Loss Count'] + temp_df.loc[ind]['Loss Count']
                    player_dic[ind]['Leave Table Amount'] = player_dic[ind]['Leave Table Amount'] + temp_df.loc[ind]['Leave Table Amount']
                    player_dic[ind]['Game Count'] += 1
                else:
                    player_dic[ind] = {'Player Names': temp_df.loc[ind]['Player Names'],
                                       'Player Ids': [ind],
                                       'Buy in Total': temp_df.loc[ind]['Buy in Total'],
                                       'Loss Count': temp_df.loc[ind]['Loss Count'],
                                       'Leave Table Amount': temp_df.loc[ind]['Leave Table Amount'],
                                       'Game Count': 1}
        self._player_dic = player_dic
        result_df = pd.DataFrame.from_dict(self._player_dic, orient='index')

        if self._grouped is not None:
            final_df = pd.DataFrame()
            for ind_group in self._grouped:
                temp = pd.DataFrame(index=[ind_group[0]], columns=result_df.columns)
                for col in result_df.columns:
                    val = []
                    for ind in ind_group:
                        val.append(result_df.loc[ind][col])
                    if col == 'Player Names' or col == 'Player Ids':
                        temp[col] = [list(set(sum(val, [])))]
                    else:
                        temp[col] = np.sum(val)
                final_df = pd.concat([final_df, temp])

            grouped_lst = sum(self._grouped, [])
            for ind in list(result_df.index):
                if ind not in grouped_lst:
                    final_df.loc[ind] = result_df.loc[ind]
        else:
            final_df = result_df

        final_df['Profit'] = final_df['Leave Table Amount'] - final_df['Buy in Total']

        if money_multi:
            final_df['Buy in Total'] = (final_df['Buy in Total'] / 100).astype(int)
            final_df['Leave Table Amount'] = (final_df['Leave Table Amount'] / 100).astype(int)
            final_df['Profit'] = (final_df['Profit'] / 100).astype(int)
            # final_df['Buy in Total'] = [int(val / 100) if val != 0 else 0 for val in final_df['Buy in Total']]
            # final_df['Leave Table Amount'] = [int(val / 100) if val != 0 else 0 for val in final_df['Leave Table Amount']]
            # final_df['Profit'] = [int(val / 100) if val != 0 else 0 for val in final_df['Profit']]

        self._player_dic_df = final_df
        ind = set(sum([list(match.winning_hand_distribution.index) for match in self._matches], []))
        hand_dist = pd.DataFrame(index=ind, columns=['Count']).fillna(0)
        col_lst = ['Flop Count', 'Turn Count', 'River Count', 'Win Count', 'My Cards Count']
        card_dist = pd.DataFrame(index=self._matches[0].card_distribution.index, columns=col_lst).fillna(0)
        for match in self._matches:
            card_dist = card_dist + match.card_distribution
            hand_dist = hand_dist.add(match.winning_hand_distribution, fill_value=0)
        self._card_distribution = card_dist.dropna(subset=col_lst)
        for col in self._card_distribution.columns:
            s = np.sum(self._card_distribution[col])
            arr = np.around([val / s if val != 0 else 0 for val in self._card_distribution[col]], 3)
            # self._card_distribution[col.replace("Count", "Percent")] = (self._card_distribution[col] / s).round(3)
            self._card_distribution[col.replace("Count", "Percent")] = list(arr)

        self._winning_hand_dist = hand_dist.astype(int).sort_values('Count', ascending=False)
        self._winning_hand_dist['Percent'] = (self._winning_hand_dist / self._winning_hand_dist.sum()).round(3)

    def __repr__(self):
        return "Poker"

    @property
    def files(self) -> List[str]:
        """Returns list of data files"""
        return self._files

    @property
    def matches(self) -> List[Game]:
        """Returns list of games"""
        return self._matches

    @property
    def players_info(self) -> pd.DataFrame:
        """Returns summary info for each player across games"""
        return self._player_dic_df.sort_values('Profit', ascending=False)

    @property
    def card_distribution(self) -> pd.DataFrame:
        """Returns count and percent for each card that showed up across games"""
        return self._card_distribution

    @property
    def winning_hand_distribution(self) -> pd.DataFrame:
        """Returns count and percent of each type of winning hand across games"""
        return self._winning_hand_dist
