from typing import List, Optional
from dataclasses import dataclass
import numpy as np
import pandas as pd
from os import walk
from poker.analysis import whfc, streak, drsw, dealer_small_big, winning_cards, win_count
from poker.hand import Hand
pd.set_option('display.max_columns', None)


def _convert_shapes(data: pd.DataFrame) -> pd.DataFrame:
    dn = np.array(data)
    for i, j in enumerate(dn):
        dn[i] = j.replace("â£", " Clubs").replace("â¦", " Diamonds").replace("â¥", " Hearts").replace("â",
                                                                                                         " Spades")
    return pd.DataFrame(dn)


def _players_in_hand(lst) -> tuple:
    sub_string = ["folds", "calls", "raises", "checks"]
    players = list(set(j.split('@')[0].replace('"', '').strip() for j in lst if any(x in j for x in sub_string)))
    return tuple(players)


def _turns_in_hand(lst) -> tuple:
    turns = []
    sub_string = ["Player stacks", "collected", "starting hand"]
    for j in lst:
        if ":" in j:
            if not any(x in j for x in sub_string):
                turns.append(j.split(':')[0])
    return tuple(turns)


def _moves_in_hand(lst):
    if len(lst) == 0:
        return [(), (), (), ()]
    else:
        checks, raises, calls, folds = (), (), (), ()
        for j in lst[0]:
            if "folds" in j:
                folds = folds + tuple((j.split('@')[0].replace('"', '').strip(),))
            if "calls" in j:
                calls = calls + (j.split('@')[0].replace('"', '').strip(), j.split('calls ')[1])
            if "raises" in j:
                raises = raises + (j.split('@')[0].replace('"', '').strip(), j.split('raises to')[1])
            if "checks" in j:
                checks = checks + tuple((j.split('@')[0].replace('"', '').strip(),))
        return [tuple(checks), tuple(raises), tuple(calls), tuple(folds)]


def _get_hands(file):
    # Load Data
    df = \
    pd.read_csv('C:\\Users\\Peter\\Desktop\\Personal\\11_Repository\\Poker Related\\Data\\' + file, encoding='latin1')[
        'entry']
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


def _get_players(hands):
    lst = []
    for i in hands:
        for j in i:
            if ' @ ' in j:
                lst.append(j.split('@')[0].split('"')[1].strip())

    return list(set(lst))


def _get_player_ids(hands):
    ids = list(
        ([j.split('@')[0].split('"')[1].strip(), j.split('@')[1].split('"')[0].strip()] for i in hands for j in i if
         ' @ ' in j))
    ids_lst = list(set((j[1] for i, j in enumerate(ids))))
    id_dict = {}
    for j, k in enumerate(ids):
        for first_item in set([k[1]]).intersection(ids_lst): break
        try:
            id_dict[first_item] = list(set(id_dict[first_item] + [k[0]]))
        except:
            id_dict[first_item] = [k[0]]
    return id_dict


def _calcs(hands):
    result = []
    for i in hands:
        players_in = _players_in_hand(i)
        turns_in = _turns_in_hand(i)
        small_blind = ()
        big_blind = ()
        hand_winner = []
        hand_winner_cards = []
        shows = []
        flop_cards = ()
        turn_card = ()
        river_card = ()
        hand_number = ()
        dealer = ()
        stands_up = []
        pre_flop = []
        post_flop = []
        post_turn = []
        post_river = []
        items = []
        loses = []
        sit = []
        approved = []
        joined = []
        end = []

        for j in i:
            items.append(j)
            if " was changed " in j:
                continue

            else:
                if "posts a small blind" in j:
                    small_blind = (j.split(' @ ')[0].split('"')[1], int(j.split(' of ')[1].strip()))
                    continue

                if "posts a big blind" in j:
                    big_blind = (j.split(' @ ')[0].replace('"', '').strip(), int(j.split(' of ')[1].strip()))
                    continue

                if " collected " in j:
                    hand_winner.append(
                        (j.split(' @ ')[0].split('"')[1], int(j.split('collected')[1].split('from')[0].strip())))

                    if " with " in j:
                        hand_winner_cards.append((j.split(' with ')[1].split(', ')[0],
                                                  j.split(', ')[1].split('(')[0], j.split(':')[1].split(')')[0]))

                if " shows " in j:
                    shows.append((j.split('@')[0].split('"')[1].strip(), j.split(" a ")[1].split('.')[0]))
                    continue

                if any(x in j for x in ["Flop:", "flop:"]):
                    if "Flop:" in j:
                        flop = j.replace('Flop: ', '').replace('[', '').replace(']', '').split(',')
                    else:
                        flop = j.replace('flop: ', '').replace('[', '').replace(']', '').split(',')

                    flop_cards = (flop[0].lstrip(), flop[1].lstrip(), flop[2].lstrip())
                    pre_flop.append(items)
                    items = []
                    continue

                if any(x in j for x in ["Turn:", "turn:"]):
                    turn_card = (j.split('[')[1].replace(']', '').strip())
                    post_flop.append(items)
                    items = []
                    continue

                if any(x in j for x in ["River:", "river:"]):
                    river_card = (j.split('[')[1].replace(']', '').strip())
                    post_turn.append(items)
                    items = []
                    continue

                if "dealer" in j:
                    hand_number = (int(j.split('#')[1].split(' ')[0]))
                    dealer = (j.split('dealer')[1].split('@')[0].split('"')[1].strip())
                    continue

                if "stand up" in j:
                    stands_up.append(
                        (j.split('@')[0].split('"')[1].strip(), int(j.split('stack of')[1].split('.')[0])))
                    continue

                if " collected " in j:
                    post_river.append(items)
                    items = []
                    continue

                if " quits the game " in j:
                    loses.append(
                        (j.split('@')[0].split('"')[1].strip(), int(j.split('stack of')[1].split('.')[0].strip())))
                    continue

                if "approved" in j:
                    approved.append(
                        (j.split('@')[0].split('"')[1].strip(), int(j.split('stack of')[1].split('.')[0].strip())))
                    continue

                if "joined" in j:
                    joined.append(
                        (j.split('@')[0].split('"')[1].strip(), int(j.split('stack of')[1].split('.')[0].strip())))
                    continue

                if "sit back" in j:
                    sit.append(
                        (j.split('@')[0].split('"')[1].strip(), int(j.split('stack of')[1].split('.')[0].strip())))
                    continue

                if 'Player stacks:' in j:
                    for l in range(1, len(j.split("#"))):
                        end.append((j.split("#")[l].split('@')[0].split('"')[1].strip(),
                                    j.split("#")[l].split('@')[1].split('(')[1].split(')')[0]))
                    continue

        players = _get_players(hands)
        oh = [(i, 0) for i in players if i not in (i[0] for i in end)]
        end_n = [(i, int(j[1])) for i in players for j in end if i == j[0]]

        Pre_Flop_Checks, Pre_Flop_Raises, Pre_Flop_Calls, Pre_Flop_Folds = _moves_in_hand(pre_flop)
        Post_Flop_Checks, Post_Flop_Raises, Post_Flop_Calls, Post_Flop_Folds = _moves_in_hand(post_flop)
        Post_Turn_Checks, Post_Turn_Raises, Post_Turn_Calls, Post_Turn_Folds = _moves_in_hand(post_turn)
        Post_River_Checks, Post_River_Raises, Post_River_Calls, Post_River_Folds = _moves_in_hand(post_river)

        roundn = [
            players_in, turns_in, small_blind, big_blind,
            hand_winner, hand_winner_cards, shows,
            flop_cards, turn_card, river_card,
            hand_number, dealer,
            stands_up, loses, sit, joined, approved,
            end_n + oh,
            Pre_Flop_Checks, Pre_Flop_Raises, Pre_Flop_Calls, Pre_Flop_Folds,
            Post_Flop_Checks, Post_Flop_Raises, Post_Flop_Calls, Post_Flop_Folds,
            Post_Turn_Checks, Post_Turn_Raises, Post_Turn_Calls, Post_Turn_Folds,
            Post_River_Checks, Post_River_Raises, Post_River_Calls, Post_River_Folds,
        ]

        result.append(roundn)

    cols = ['Players Involved', 'Turns Involved', 'Small Blind', 'Big Blind',
            'Hand Winner', 'Hand Winner Cards', 'Showed',
            'Flop Cards', 'Turn Card', 'River Card',
            'Hand Number', 'Dealer',
            'Stood Up', 'Loses', 'Sits In', 'Joined', 'Approved',
            'Round Amounts',
            'Pre Flop Checks', 'Pre Flop Raises', 'Pre Flop Calls', 'Pre Flop Folds',
            'Post Flop Checks', 'Post Flop Raises', 'Post Flop Calls', 'Post Flop Folds',
            'Post Turn Checks', 'Post Turn Raises', 'Post Turn Calls', 'Post Turn Folds',
            'Post River Checks', 'Post River Raises', 'Post River Calls', 'Post River Folds',
            ]

    result_df = pd.DataFrame(result, columns=cols)

    return result_df


def getWinnings(r, pdn):
    players = list(set(sum([pdn[i] for i in pdn.keys()], [])))
    rn = r[['Round Amounts', 'Sits In', 'Joined', 'Stood Up', 'Loses', 'Approved']]

    lst = {i: [0] for i in players}
    am_in = {i: 0 for i in players}
    am_past = {i: 0 for i in players}
    for i in rn['Round Amounts']:
        for j in i:
            if am_past[j[0]] == 0:
                am_in[j[0]] += j[1]
            am_past[j[0]] = j[1]
            lst[j[0]] = lst[j[0]] + [j[1]]

    # plt.plot(DataFrame(lst))

    lstn = {i: [0] for i in players}
    for i in players:
        for j, k in enumerate(lst[i]):
            if lst[i][j] != 0:
                if lst[i][j - 1] == 0:
                    lstn[i].append(lst[i][j])
                    # print(DataFrame(lst)['Mac'].tolist())
    al = {i: {'Joined': [], 'Stood Up': [], 'Sits In': [], 'Approved': []} for i in players}
    bi = {i: 0 for i in players}
    su = {i: 0 for i in players}
    for i in players:
        su_temp = [0]
        j_temp = [0]
        si_temp = [0]
        a_temp = [0]
        for j in range(len(rn)):
            jj = rn['Joined'].iloc[j]
            jn = rn['Stood Up'].iloc[j]
            nn = rn['Sits In'].iloc[j]
            nj = rn['Approved'].iloc[j]

            if len(jn) > 0:
                for k in range(len(jn)):
                    if jn[k][0] == i:
                        su_temp.append(int(jn[k][1]))

            if len(jj) > 0:
                for k in range(len(jj)):
                    if jj[k][0] == i:
                        j_temp.append(int(jj[k][1]))

            if len(nn) > 0:
                for k in range(len(nn)):
                    if nn[k][0] == i:
                        si_temp.append(int(nn[k][1]))

            if len(nj) > 0:
                for k in range(len(nj)):
                    if nj[k][0] == i:
                        a_temp.append(int(nj[k][1]))

        al[i]['Joined'] = sum(j_temp)
        al[i]['Stood Up'] = sum(su_temp)
        al[i]['Sits In'] = sum(si_temp)
        al[i]['Approved'] = sum(a_temp)
        # print(i, a_temp, j_temp, su_temp, si_temp, sum(j_temp) - sum(si_temp))
        # print(i, sum(su_temp)- sum(j_temp))
        # print(i,j_temp, su_temp, si_temp)

        # buy_in = sum(j_temp) - abs(sum(lstn[i]) - sum(su_temp)- sum(j_temp) +sum(l_temp))
        # if buy_in <= 0:
        #     buy_in = sum(j_temp)
        # elif str(buy_in)[-2:] != '00':
        #     buy_in = sum([i for i in j_temp if str(i)[-2:] == '00'])

        bi[i] = sum(j_temp) - sum(si_temp)
        su[i] = [i for i in su_temp if i not in j_temp]
        # bi[i] = sum([i for i in j_temp if i not in su_temp])
        # print(su,bi)
    ju = su.copy()
    for i in players:
        if len(su[i]) == 0:
            jjj = rn['Round Amounts'].iloc[-1]
            for j in jjj:
                if j[0] == i:
                    ju[i] = j[1]
        else:
            ju[i] = su[i][0]

    names, id_name, b_in, b_out = [], [], [], []
    for i in pdn.keys():
        namesn, b_inn, b_outn = [], [], []
        id_name.append(i)
        for j in pdn[i]:
            namesn.append(j), b_inn.append(bi[j]), b_outn.append(ju[j])
        names.append(namesn), b_in.append(sum(b_inn)), b_out.append(sum(b_outn))

    wl = pd.DataFrame()
    wl['Index'] = id_name
    wl['Names'] = names
    wl['Buy-In Amount'] = b_in
    wl['Leave Table Amount'] = b_out
    return (wl, al)


def _running_total_winnings(files: List[str], savedf: Optional[bool] = False) -> pd.DataFrame:
    gw_temp = []
    for file in files:
        hands = _get_hands(file)
        gw_temp.append(getWinnings(_calcs(hands), _get_player_ids(hands))[0])

    ind = list(set(sum([list(i['Index']) for i in gw_temp], [])))
    names = []
    id_name = []
    b_in = []
    b_out = []
    games = []
    for i in ind:
        namesn = []
        buy_inn = []
        buy_outn = []
        gamesn = 0
        for j in gw_temp:
            if i in list(j['Index']):
                j_i = j[j['Index'] == i]
                namesn.append(j_i['Names'].values[0])
                buy_inn.append(j_i['Buy-In Amount'].values[0])
                buy_outn.append(j_i['Leave Table Amount'].values[0])
                gamesn = gamesn + 1
        names.append(list(set(sum(namesn, []))))
        id_name.append(i)
        b_in.append(sum(buy_inn))
        b_out.append(sum(buy_outn))
        games.append(gamesn)

    wl = pd.DataFrame()
    wl['Index'] = id_name
    wl['Names'] = names
    wl['Games Played'] = games
    wl['Buy-In Amount'] = b_in
    wl['Leave Table Amount'] = b_out
    wl['Total Amount'] = wl['Leave Table Amount'] - wl['Buy-In Amount']
    wl['Percent Change'] = round(((wl['Leave Table Amount'] - wl['Buy-In Amount']) / wl['Buy-In Amount']) * 100, 1)
    wl = wl.drop_duplicates(['Buy-In Amount', 'Leave Table Amount']).sort_values('Total Amount',
                                                                                 ascending=False).reset_index(
        drop=True)
    # wl = wl[wl['Games Played'] >= 2].reset_index(drop=True)

    grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
               ['1_FRcDzJU-', 'ofZ3AjBJdl', 'yUaYOqMtWh', 'EIxKLHzvif'],
               ['3fuMmmzEQ-', 'LRdO6bTCRh'],
               ['FZayb4wOU1', '66rXA9g5yF'],
               # ['48QVRRsiae', 'u8_FUbXpAz'],
               ]

    h2 = wl.copy()
    for i in grouped:
        index = []
        names = []
        games_played = 0
        buy_in = 0
        leave_amount = 0
        total_amount = 0
        for j in i:
            temp = h2[h2['Index'] == j]
            h2 = h2.drop(temp.index, axis='index')

            for name in list(temp['Names'])[0]:
                if name not in names:
                    names.append(name)

            games_played += list(temp['Games Played'])[0]
            buy_in += list(temp['Buy-In Amount'])[0]
            leave_amount += list(temp['Leave Table Amount'])[0]
            total_amount += list(temp['Total Amount'])[0]
            index.append(list(temp['Index'])[0])
        per_change = round(((leave_amount - buy_in) / buy_in) * 100, 1)
        h2 = pd.concat([h2,
                        pd.DataFrame([[index, names, games_played, buy_in, leave_amount, total_amount, per_change]],
                                     columns=list(h2.columns))])
    h2 = h2.sort_values('Percent Change', ascending=False).reset_index(drop=True)

    if savedf == 1:
        h2.to_csv('C:\\Users\\Peter\\Desktop\\Personal\\11_Repository\\Poker Related\\Running Total.csv',
                  header=True)
    return h2


@dataclass
class Game:

    def __init__(self, file: str):
        self._file = file
        self._hands = _get_hands(file=self._file)
        self._calculated_hands = _calcs(hands=self._hands)
        # self._whfc = whfc(data=self._calculated_hands)
        # self._streak = streak(data=self._calculated_hands)
        # self._drsw = drsw(data=self._calculated_hands)
        # self._dealer_small_big = dealer_small_big(data=self._calculated_hands)
        # self._winning_cards = winning_cards(data=self._calculated_hands)
        # self._win_count = win_count(data=self._calculated_hands)

        oop = Hand()
        self._class_lst = [line for hand in self._hands for line in oop.parser(hand=hand)]

    def __repr__(self):
        val = self._file
        if "." in val:
            val = self._file.split(".")[0]
        return val

    @property
    def file_name(self) -> str:
        return self._file

    # @property
    # def hands_lst(self) -> List[list]:
    #     return self._hands

    @property
    def hands_df(self) -> pd.DataFrame:
        return self._calculated_hands

    @property
    def hands_lst(self):
        return self._class_lst


@dataclass
class Poker:

    def __init__(self, repo_location: str):
        self._repo_location = repo_location
        self._files = next(walk(self._repo_location))[2]
        self._running_total = _running_total_winnings(files=self._files, savedf=False)

        self._matches = []
        for file in self._files:
            self._matches.append(Game(file=file))

    def __repr__(self):
        return "Poker"

    @property
    def files(self) -> List[str]:
        return self._files

    @property
    def running_total_winning(self) -> pd.DataFrame:
        return self._running_total

    @property
    def matches(self) -> List[Game]:
        return self._matches
