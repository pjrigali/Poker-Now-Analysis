from typing import List, Optional, Union
from dataclasses import dataclass
import numpy as np
import pandas as pd
from os import walk
from collections import Counter
from poker.analysis import whfc, streak, drsw, dealer_small_big, winning_cards, win_count
from poker.processor import Requests, Approved, Joined, MyCards, SmallBlind, BigBlind, Folds, Calls, Raises, Checks
from poker.processor import Wins, Shows, Quits, Flop, Turn, River, Undealt, StandsUp, SitsIn, PlayerStacks
from poker.processor import Classifier


def _convert_shapes(data: pd.DataFrame) -> pd.DataFrame:
    dn = np.array(data)
    for i, j in enumerate(dn):
        dn[i] = j.replace("â£", " Clubs").replace("â¦", " Diamonds").replace("â¥", " Hearts").replace("â",
                                                                                                         " Spades")
    return pd.DataFrame(dn)


def _get_hands(repo: str, file: str):
    # Load Data
    df = pd.read_csv(repo + file, encoding='latin1')['entry']
    df = df.reindex(index=df.index[::-1]).reset_index(drop=True)
    dfn = _convert_shapes(df)
    # Split into hands
    dfnn = np.array(dfn)
    hands = []
    hand_lst = []
    for i, j in enumerate(dfnn):
        if ' starting hand ' in j[0]:
            if ' hand #1 ' in j[0]:
                hands.append(hand_lst)
            hand_lst = []
            hand_lst.append(j[0])
            hands.append(hand_lst)
        else:
            hand_lst.append(j[0])
    return hands


@dataclass
class Hand:

    def __init__(self, hand: List[str]):
        self._hand = hand

        classifier = Classifier()
        self._parsed_hand = [line for line in classifier.parser(hand=self._hand)]

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
            if type(line) == BigBlind:
                self._big_blind = {line.player_name: line.stack}
                continue
            if type(line) == Wins:
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
            if type(line) == PlayerStacks:
                self._starting_players = dict(zip(line.player_name, line.player_index))
                self._starting_player_chips = dict(zip(line.player_name, line.stack))
                continue
            if type(line) == Flop:
                self._flop = line.cards
                continue
            if type(line) == Turn:
                self._turn = line.cards
                continue
            if type(line) == River:
                self._river = line.cards
                continue
            if type(line) == MyCards:
                self._my_cards = line.cards
                continue

    def __repr__(self):
        return "Hand " + str(self.parsed_hand[0].current_round)

    @property
    def parsed_hand(self) -> list:
        return self._parsed_hand

    @property
    def small_blind(self) -> Optional[dict]:
        return self._small_blind

    @property
    def big_blind(self) -> Optional[dict]:
        return self._big_blind

    @property
    def winner(self) -> Optional[dict]:
        return self._winner

    @property
    def winning_cards(self) -> Optional[tuple]:
        return self._winning_cards

    @property
    def winning_hand(self) -> Optional[str]:
        return self._winning_hand

    @property
    def starting_players(self) -> Optional[dict]:
        return self._starting_players

    @property
    def starting_players_chips(self) -> Optional[dict]:
        return self._starting_player_chips

    @property
    def flop_cards(self) -> Optional[tuple]:
        return self._flop

    @property
    def turn_card(self) -> Optional[str]:
        return self._turn

    @property
    def river_card(self) -> Optional[str]:
        return self._river

    @property
    def my_cards(self) -> tuple:
        return self._my_cards


@dataclass
class Player:

    def __init__(self, player_index: Union[str, List[str]], hands: List[Hand]):
        if type(player_index) == str:
            player_index = [player_index]
        self._player_index = player_index
        self._temp_ind = ['Pre Flop', 'Post Flop', 'Post Turn', 'Post River']

        # Winning Stats
        win_stack_lst, win_cards_lst, win_hand_lst, win_position_lst = [], [], [], []
        w_pre_flop_check_count, w_post_flop_check_count, w_post_turn_check_count, w_post_river_check_count = [], [], [], []
        w_pre_flop_call_count, w_post_flop_call_count, w_post_turn_call_count, w_post_river_call_count = [], [], [], []
        w_pre_flop_call_lst, w_post_flop_call_lst, w_post_turn_call_lst, w_post_river_call_lst = [], [], [], []
        w_pre_flop_raise_count, w_post_flop_raise_count, w_post_turn_raise_count, w_post_river_raise_count = [], [], [], []
        w_pre_flop_raise_lst, w_post_flop_raise_lst, w_post_turn_raise_lst, w_post_river_raise_lst = [], [], [], []
        # Normal Stats
        pre_flop_check_count, post_flop_check_count, post_turn_check_count, post_river_check_count = [], [], [], []
        pre_flop_fold_count, post_flop_fold_count, post_turn_fold_count, post_river_fold_count = [], [], [], []
        pre_flop_call_count, post_flop_call_count, post_turn_call_count, post_river_call_count = [], [], [], []
        pre_flop_call_lst, post_flop_call_lst, post_turn_call_lst, post_river_call_lst = [], [], [], []
        pre_flop_raise_count, post_flop_raise_count, post_turn_raise_count, post_river_raise_count = [], [], [], []
        pre_flop_raise_lst, post_flop_raise_lst, post_turn_raise_lst, post_river_raise_lst = [], [], [], []

        hand_count = 0
        for hand in hands:
            for line in hand.parsed_hand:
                # Count of hands the player is in.
                for p_ind in self._player_index:
                    if line.player_index is not None:
                        if p_ind in line.player_index:
                            if type(line) == PlayerStacks:
                                hand_count += 1

                if line.player_index in self._player_index:
                    # Player Win information.
                    if type(line) == Wins:
                        win_stack_lst.append(line.stack)
                        win_cards_lst.append(line.cards)
                        win_hand_lst.append(line.winning_hand)
                        win_position_lst.append(line.position)
                        for line in hand.parsed_hand:
                            if line.player_index in self._player_index:
                                self._check(line=line, cl=Checks, prfc=w_pre_flop_check_count,
                                            pofc=w_post_flop_check_count, potc=w_post_turn_check_count,
                                            porc=w_post_river_check_count)
                                self._check(line=line, cl=Calls, prfc=w_pre_flop_call_count,
                                            pofc=w_post_flop_call_count, potc=w_post_turn_call_count,
                                            porc=w_post_river_call_count, prfl=w_pre_flop_call_lst,
                                            pofl=w_post_flop_call_lst, potl=w_post_turn_call_lst,
                                            porl=w_post_river_call_lst)
                                self._check(line=line, cl=Raises, prfc=w_pre_flop_raise_count,
                                            pofc=w_post_flop_raise_count, potc=w_post_turn_raise_count,
                                            porc=w_post_river_raise_count, prfl=w_pre_flop_raise_lst,
                                            pofl=w_post_flop_raise_lst, potl=w_post_turn_raise_lst,
                                            porl=w_post_river_raise_lst)
                    # Checks, Folds, Calls, and Raises info
                    self._check(line=line, cl=Checks, prfc=pre_flop_check_count, pofc=post_flop_check_count,
                                potc=post_turn_check_count, porc=post_river_check_count)
                    self._check(line=line, cl=Folds, prfc=pre_flop_fold_count, pofc=post_flop_fold_count,
                                potc=post_turn_fold_count, porc=post_river_fold_count)
                    self._check(line=line, cl=Calls, prfc=pre_flop_call_count, pofc=post_flop_call_count,
                                potc=post_turn_call_count, porc=post_river_call_count, prfl=pre_flop_call_lst,
                                pofl=post_flop_call_lst, potl=post_turn_call_lst, porl=post_river_call_lst)
                    self._check(line=line, cl=Raises, prfc=pre_flop_raise_count, pofc=post_flop_raise_count,
                                potc=post_turn_raise_count, porc=post_river_raise_count, prfl=pre_flop_raise_lst,
                                pofl=post_flop_raise_lst, potl=post_turn_raise_lst, porl=post_river_raise_lst)

        win_df = pd.DataFrame([win_stack_lst, win_cards_lst, win_hand_lst, win_position_lst]).T
        win_df.columns = ['Win Stack', 'Win Cards', 'Win Hand', 'Win Position']
        self._win_df = win_df
        self._largest_win = np.max(win_df['Win Stack'])
        self._win_position_dist_df = pd.DataFrame.from_dict(dict(Counter(list(win_df['Win Position']))), orient='index',
                                                            columns=['Count'])
        self._win_position_dist_df_per = self._win_position_dist_df / len(win_df)
        self._win_hand_dist_df = pd.DataFrame.from_dict(dict(Counter(list(win_df['Win Hand']))), orient='index',
                                                        columns=['Count'])
        self._win_hand_dist_df_per = self._win_hand_dist_df / len(win_df)
        card_lst = list(win_df['Win Cards'].dropna())
        self._win_cards_dist_df = pd.DataFrame.from_dict(dict(Counter(sum([list(cards) for cards in card_lst], []))),
                                                         orient='index', columns=['Count'])
        # Winning Check df
        w_check_sum_df = self._make_df(keyword='Count', class_word='Check', prf=w_pre_flop_check_count,
                                       pof=w_post_flop_check_count, pot=w_post_turn_check_count,
                                       por=w_post_river_check_count)
        # Winning Call df
        w_call_mu_df = self._make_df(keyword='Average', class_word='Call', prf=w_pre_flop_call_lst,
                                     pof=w_post_flop_call_lst, pot=w_post_turn_call_lst, por=w_post_river_call_lst)
        w_call_mode_df = self._make_df(keyword='Mode', class_word='Call', prf=w_pre_flop_call_lst,
                                       pof=w_post_flop_call_lst, pot=w_post_turn_call_lst, por=w_post_river_call_lst)
        w_call_std_df = self._make_df(keyword='Std', class_word='Call', prf=w_pre_flop_call_lst,
                                      pof=w_post_flop_call_lst, pot=w_post_turn_call_lst, por=w_post_river_call_lst)
        w_call_sum_df = self._make_df(keyword='Count', class_word='Call', prf=w_pre_flop_call_count,
                                      pof=w_post_flop_call_count, pot=w_post_turn_call_count,
                                      por=w_post_river_call_count)
        # Winning Raise df
        w_raise_mu_df = self._make_df(keyword='Average', class_word='Raise', prf=w_pre_flop_raise_lst,
                                      pof=w_post_flop_raise_lst, pot=w_post_turn_raise_lst, por=w_post_river_raise_lst)
        w_raise_mode_df = self._make_df(keyword='Mode', class_word='Raise', prf=w_pre_flop_raise_lst,
                                        pof=w_post_flop_raise_lst, pot=w_post_turn_raise_lst,
                                        por=w_post_river_raise_lst)
        w_raise_std_df = self._make_df(keyword='Std', class_word='Raise', prf=w_pre_flop_raise_lst,
                                       pof=w_post_flop_raise_lst, pot=w_post_turn_raise_lst, por=w_post_river_raise_lst)
        w_raise_sum_df = self._make_df(keyword='Count', class_word='Raise', prf=w_pre_flop_raise_count,
                                       pof=w_post_flop_raise_count, pot=w_post_turn_raise_count,
                                       por=w_post_river_raise_count)

        self._winning_stats = pd.concat([w_check_sum_df, w_call_mu_df, w_call_mode_df, w_call_std_df, w_call_sum_df,
                                         w_raise_mu_df, w_raise_mode_df, w_raise_std_df, w_raise_sum_df], axis=1)

        l = len(self._win_df)
        for col in self._winning_stats.columns:
            if 'Count' in col:
                self._winning_stats[col+' Per'] = [round(item / l, 3) if item != 0 else 0 for item in self._winning_stats[col]]
        # Check df
        check_sum_df = self._make_df(keyword='Count', class_word='Check', prf=pre_flop_check_count,
                                     pof=post_flop_check_count, pot=post_turn_check_count, por=post_river_check_count)
        # Fold df
        fold_sum_df = self._make_df(keyword='Count', class_word='Fold', prf=pre_flop_fold_count,
                                    pof=post_flop_fold_count, pot=post_turn_fold_count, por=post_river_fold_count)
        # Call df
        call_mu_df = self._make_df(keyword='Average', class_word='Call', prf=pre_flop_call_lst,
                                   pof=post_flop_call_lst, pot=post_turn_call_lst, por=post_river_call_lst)
        call_mode_df = self._make_df(keyword='Mode', class_word='Call', prf=pre_flop_call_lst,
                                     pof=post_flop_call_lst, pot=post_turn_call_lst, por=post_river_call_lst)
        call_std_df = self._make_df(keyword='Std', class_word='Call', prf=pre_flop_call_lst,
                                    pof=post_flop_call_lst, pot=post_turn_call_lst, por=post_river_call_lst)
        call_sum_df = self._make_df(keyword='Count', class_word='Call', prf=pre_flop_call_count,
                                    pof=post_flop_call_count, pot=post_turn_call_count, por=post_river_call_count)
        # Raise df
        raise_mu_df = self._make_df(keyword='Average', class_word='Raise', prf=pre_flop_raise_lst,
                                    pof=post_flop_raise_lst, pot=post_turn_raise_lst, por=post_river_raise_lst)
        raise_mode_df = self._make_df(keyword='Mode', class_word='Raise', prf=pre_flop_raise_lst,
                                      pof=post_flop_raise_lst, pot=post_turn_raise_lst, por=post_river_raise_lst)
        raise_std_df = self._make_df(keyword='Std', class_word='Raise', prf=pre_flop_raise_lst,
                                     pof=post_flop_raise_lst, pot=post_turn_raise_lst, por=post_river_raise_lst)
        raise_sum_df = self._make_df(keyword='Count', class_word='Raise', prf=pre_flop_raise_count,
                                     pof=post_flop_raise_count, pot=post_turn_raise_count, por=post_river_raise_count)
        self._stats = pd.concat([check_sum_df, call_mu_df, call_mode_df, call_mode_df, call_std_df, call_sum_df,
                                 raise_mu_df, raise_mode_df, raise_std_df, raise_sum_df, fold_sum_df], axis=1)

        for col in self._stats.columns:
            if 'Count' in col:
                self._stats[col+' Per'] = [round(item / hand_count, 3) if item != 0 else 0 for item in self._stats[col]]

        if hand_count == 0:
            self._win_per = 0.0
        else:
            self._win_per = round(len(win_df) / hand_count, 2)

        if len(win_df) == 0:
            self._win_count = 0
        else:
            self._win_count = len(win_df)

    def __repr__(self):
        return self._player_index[0]

    def _check(self, line, cl, prfc: Optional[list] = None, pofc: Optional[list] = None, potc: Optional[list] = None,
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

    def _make_df(self, keyword: str, class_word: str, prf: list, pof: list, pot: list, por: list) -> pd.DataFrame:
        temp_lst = []
        for lst in [prf, pof, pot, por]:
            if keyword == 'Count':
                val = np.sum(lst)
            elif keyword == 'Median':
                val = np.median(lst)
            elif keyword == 'Std':
                val = np.std(lst, ddof=1)
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
        return pd.DataFrame(temp_lst,
                            index=['Pre Flop', 'Post Flop', 'Post Turn', 'Post River'],
                            columns=[class_word + ' ' + keyword]).fillna(0)

    @property
    def win_df(self) -> pd.DataFrame:
        return self._win_df

    @property
    def win_per(self) -> float:
        return self._win_per

    @property
    def win_count(self) -> int:
        return self._win_count

    @property
    def largest_win(self) -> int:
        return int(self._largest_win)

    @property
    def winning_habits(self) -> pd.DataFrame:
        return self._winning_stats

    @property
    def normal_habits(self) -> pd.DataFrame:
        return self._stats

    @property
    def win_position_distribution(self) -> pd.DataFrame:
        return self._win_position_dist_df.reindex(self._temp_ind )

    @property
    def win_position_distribution_per(self) -> pd.DataFrame:
        return self._win_position_dist_df_per.reindex(self._temp_ind )

    @property
    def win_hand_distribution(self) -> pd.DataFrame:
        return self._win_hand_dist_df

    @property
    def win_hand_distribution_per(self) -> pd.DataFrame:
        return self._win_hand_dist_df_per

    @property
    def win_card_distribution(self) -> pd.DataFrame:
        return self._win_cards_dist_df


@dataclass
class Game:

    def __init__(self, repo: str, file: str, grouped: list, money_multi: int):
        self._repo = repo
        self._file = file
        self._hands = _get_hands(repo=self._repo, file=self._file)
        self._class_lst = [Hand(hand=hand) for hand in self._hands]

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
                if type(line) == StandsUp:
                    if line.player_index in player_dic.keys():
                        player_dic[line.player_index]['player stands up'].append(line.stack)
                if type(line) == SitsIn:
                    if line.player_index in player_dic.keys():
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
        return self._file

    @property
    def hands_lst(self):
        return self._class_lst

    @property
    def players_info(self) -> pd.DataFrame:
        return self._player_dic_df

    @property
    def card_distribution(self) -> pd.DataFrame:
        return self._card_distribution

    @property
    def winning_hand_distribution(self) -> pd.DataFrame:
        return self._winning_hand_dist

    @property
    def players(self):
        return self._players


@dataclass
class Poker:

    def __init__(self, repo_location: str, grouped: Optional[list] = None, money_multi: Optional[int] = 100):
        self._repo_location = repo_location
        self._files = next(walk(self._repo_location))[2]

        self._grouped = None
        if grouped:
            self._grouped = grouped

        self._matches = [Game(repo=self._repo_location,
                              file=file,
                              grouped=self._grouped,
                              money_multi=money_multi) for file in self._files]

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
        final_df['Profit'] = final_df['Leave Table Amount'] - final_df['Buy in Total']

        if money_multi:
            final_df['Buy in Total'] = (final_df['Buy in Total'] / 100).astype(int)
            final_df['Leave Table Amount'] = (final_df['Leave Table Amount'] / 100).astype(int)
            final_df['Profit'] = (final_df['Profit'] / 100).astype(int)
        self._player_dic_df = final_df

        ind = set(sum([list(match.winning_hand_distribution.index) for match in self._matches], []))
        hand_dist = pd.DataFrame(index=ind, columns=['Count']).fillna(0)
        col_lst = ['Flop Count', 'Turn Count', 'River Count', 'Win Count', 'My Cards Count']
        card_dist = pd.DataFrame(index=self._matches[0].card_distribution.index, columns=col_lst).fillna(0)
        for match in self._matches:
            card_dist = card_dist + match.card_distribution
            hand_dist = hand_dist.add(match.winning_hand_distribution, fill_value=0)
        self._card_distribution = card_dist.dropna(subset=col_lst)
        self._winning_hand_dist = hand_dist.astype(int).sort_values('Count', ascending=False)

    def __repr__(self):
        return "Poker"

    @property
    def files(self) -> List[str]:
        return self._files

    @property
    def matches(self) -> List[Game]:
        return self._matches

    @property
    def player_info(self) -> pd.DataFrame:
        return self._player_dic_df.sort_values('Profit', ascending=False)

    @property
    def card_distribution(self) -> pd.DataFrame:
        return self._card_distribution

    @property
    def card_distribution_per(self) -> pd.DataFrame:
        return (self._card_distribution / self._card_distribution.sum()).round(3)

    @property
    def winning_hand_distribution(self) -> pd.DataFrame:
        return self._winning_hand_dist

    @property
    def winning_hand_distribution_per(self) -> pd.DataFrame:
        return (self._winning_hand_dist / self._winning_hand_dist.sum()).round(3)
