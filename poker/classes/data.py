from typing import List
from dataclasses import dataclass
import datetime
from os import walk
import csv
from poker.classes.event import Event
from poker.utils.class_functions import _str_nan
from poker.utils.base import calculate_hand, calc_gini


def _convert(data: List[str], dic: dict):
    dic['Event'].append(data[0].replace("â£", " Clubs").replace("â¦", " Diamonds").replace("â¥", " Hearts").replace("â", " Spades"))
    dic['Time'].append(datetime.datetime.strptime(data[1].replace('T', ' ').split('.')[0], '%Y-%m-%d %H:%M:%S'))


def rev(lst: list) -> list:
    lst.reverse()
    return lst


def _get_rows(file: str) -> dict:
    dic = {'Event': [], 'Time': []}
    with open(file, 'r', encoding='latin1') as file:
        my_reader = csv.reader(file, delimiter=',')
        for ind, row in enumerate(my_reader):
            if ind > 0:
                _convert(data=row, dic=dic)
    dic['Event'], dic['Time'] = rev(dic['Event']), rev(dic['Time'])
    return dic


def _poker_collect_data(repo_location: str) -> dict:
    """Open file, clean data and return a dict"""
    files, file_dic = next(walk(repo_location))[2], {}
    for file in files:
        temp, v, t, d = [], [], [], _get_rows(file=repo_location + file)
        for ind, val in enumerate(d['Event']):
            if ' starting hand ' in val:
                if ' hand #1 ' in val:
                    temp.append({'lines': v, 'times': t})
                v, t = [val], [d['Time'][ind]]
                temp.append({'lines': v, 'times': t})
            else:
                v.append(val), t.append(d['Time'][ind])
        file_dic[file.split(".")[0]] = temp
    return file_dic


def parser(lines: List[str], times: list, game_id: str) -> tuple:
    """
    Takes a hand and the times associated with each event in that hand. Returns a list of Event Class objects.

    :param lines: List of str's
    :param times: List of Datetime objects
    :param game_id: str corresponding to a unique match
    :return: tuple of Event Objects
    :rtype: tuple
    :note: Conceptually, this is processing one hand of events at a time.
    """
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

    def _fill(c):
        """applies values to the blank event class"""
        return Event(text=line, event=c, position=pos, winning_hand=winning_hands, current_round=c_round,
                     pot_size=pot, starting_players=start_players, remaining_players=players_left,
                     action_from_player=p_person, action_amount=p_amount, game_id=game_id,
                     starting_chips=start_chips, current_chips=current_chips, winner=winners, win_stack=win_stacks,
                     time=times[ind], previous_time=times[ind - 1], start_time=times[0], end_time=times[-1], gini=gini)

    lst = []
    pot, players_left, pos, gini = 0, i_lst, 'Pre Flop', calc_gini(data=v_lst)
    p_person, p_amount = None, None
    start_chips, start_players, current_chips = dict(zip(i_lst, v_lst)), dict(zip(i_lst, n_lst)), dict(zip(i_lst, v_lst))
    winners, win_stacks, winning_hands, cards, all_cards, shows = None, None, None, [], [], []
    for ind, line in enumerate(lines):
        if ' calls ' in line:
            n = _fill('Calls')._add_stack(line.split(' calls ')[1])
            if ' and ' in n.stack:
                n._add_stack(int(n.stack.split(' and ')[0]))._add_all_in()
            else:
                n._add_stack(int(n.stack))
            pot, current_chips = n._update_pot_curr(current_chips, '-')
            lst.append(n)
            continue
        elif ' checks' in line:
            lst.append(_fill('Checks'))
            continue
        elif ' folds' in line:
            n, players_left = _fill('Folds')._add_remaining(players_left, True)
            lst.append(n)
            continue
        elif ' bets ' in line or ' raises ' in line:
            n = _fill('Bets')
            if ' and ' in line:
                n._add_all_in()
                new_stack = line.split(' and ')[0]
            else:
                new_stack = line
            if ' raises to ' in line:
                new_stack = int(new_stack.split(' raises to ')[1])
                n._add_raise(new_stack)
            else:
                new_stack = int(new_stack.split(' bets ')[1])
            pot, current_chips = n._add_stack(new_stack)._update_pot_curr(current_chips, '-')
            p_person, p_amount = n.player_index, n.stack
            lst.append(n)
            continue
        elif ' shows a ' in line:
            n = _fill('Shows')._add_cards([i.strip() for i in line.split(' shows a ')[1].split('.')[0].split(',')])
            all_cards = n._get_cards_allcards(cards=None, all_cards=all_cards)
            lst.append(n), shows.append(n)
            continue
        elif ' collected ' in line:
            n = _fill('Wins')._add_stack(int(line.split(' collected ')[1].split(' from ')[0]))
            if ' from pot with ' in line:
                if ', ' in line.split(' from pot with ')[1].split(' (')[0]:
                    n.winning_hand = line.split(' from pot with ')[1].split(', ')[0]
                else:
                    n.winning_hand = line.split(' from pot with ')[1].split(' (')[0]
            if 'combination' in line:
                n._add_cards([i.strip() for i in line.split(': ')[1].split(')')[0].split(',')], True)
            if winners is None:
                winners, win_stacks, winning_hands = n.player_index, n.stack, n.winning_hand
            elif isinstance(winners, str):
                winners = [winners, n.player_index]
            else:
                winners.append(n.player_index)
            current_chips = n._add_chips(current_chips, '+')
            all_cards = n._get_cards_allcards(cards=None, all_cards=all_cards)
            lst.append(n)
            continue
        elif 'Player stacks:' in line:
            n = _fill('PlayerStacks')._add_stack(0)
            n.player_name, n.player_index, n.current_chips, n.starting_chips = n_lst, i_lst, current_chips, start_chips
            all_cards = n._get_cards_allcards(cards=None, all_cards=all_cards)
            lst.append(n)
            continue
        elif 'posts a big blind' in line:
            n, pot, current_chips = _fill('BigBlind')._add_stack(int(line.split('of ')[1]))._update_pot_curr(current_chips, '-', True)
            p_person, p_amount = n.player_index, n.stack
            lst.append(n)
            continue
        elif 'posts a small blind' in line:
            n, pot, current_chips = _fill('SmallBlind')._add_stack(int(line.split('of ')[1]))._update_pot_curr(current_chips, '-', True)
            p_person, p_amount = n.player_index, n.stack
            lst.append(n)
            continue
        elif 'Flop: ' in line or 'flop' in line:
            p_person, p_amount = None, None
            n = _fill('Flop')._add_cards([i.strip() for i in line.split(' [')[1].split(']')[0].split(',')])
            n.position, pos = 'Flop', 'Post Flop'
            cards, all_cards = n._get_cards_allcards(cards=n.cards, all_cards=all_cards)
            lst.append(n)
            continue
        elif 'Turn: ' in line or 'turn: ' in line:
            p_person, p_amount = None, None
            n = _fill('Turn')._add_cards([line.split(' [')[1].split(']')[0].strip()])
            cards, all_cards = n._get_cards_allcards(cards=n.cards, all_cards=all_cards)
            n.position, pos = 'Turn', 'Post Turn'
            lst.append(n)
            continue
        elif 'River: ' in line or 'river: ' in line:
            p_person, p_amount = None, None
            n = _fill('River')._add_cards([line.split(' [')[1].split(']')[0].strip()])
            n.position, pos = 'River', 'Post River'
            cards, all_cards = n._get_cards_allcards(cards=n.cards, all_cards=all_cards)
            lst.append(n)
            continue
        elif 'Your hand' in line:
            n = _fill('MyCards')._add_cards([i.strip() for i in line.split(' hand is ')[1].split(',')])
            all_cards = n._get_cards_allcards(cards=None, all_cards=all_cards)
            lst.append(n)
            continue
        elif 'joined the game' in line:
            lst.append(_fill('Joined'))
            continue
        elif 'requested a seat' in line:
            lst.append(_fill('Requests'))
            continue
        elif 'The admin approved' in line:
            lst.append(_fill('Approved'))
            continue
        elif ' quits the game ' in line:
            n, players_left = _fill('Quits')._add_remaining(players_left, True)
            lst.append(n)
            continue
        elif 'Undealt cards: ' in line:
            p_person, p_amount = None, None
            n = _fill('Undealt')._add_cards([i.strip() for i in line.split(' [')[1].split(']')[0].split(',')])
            if len(n.cards) == 1:
                n.position = 'Post Turn'
            elif len(n.cards) == 2:
                n.position = 'Post Flop'
            cards, all_cards = n._get_cards_allcards(cards=cards, all_cards=all_cards)
            lst.append(n)
            continue
        elif ' stand up with ' in line:
            n, players_left = _fill('StandsUp')._add_remaining(players_left, True)
            lst.append(n)
            continue
        elif ' sit back with ' in line:
            lst.append(_fill('SitsIn'))
            continue

    if isinstance(winners, str):
        winners = [winners]

    for i in lst:
        if i.event == 'PlayerStacks':
            i.cards = tuple(set(all_cards))
        elif i.event == 'Wins' and len(shows) > 0:
            for k in shows:
                if k.player_index == i.player_index and i.cards is None:
                    i._add_cards(cards + list(k.cards), True)
                    if winning_hands is None and len(i.cards) >= 5:
                        winning_hands = calculate_hand(cards=i.cards)
                        i.winning_hand = winning_hands
        if winners is not None:
            i.winner, i.win_stack, i.winning_hand = tuple(winners), win_stacks, winning_hands
            if _str_nan(i.player_index) and i.player_index in winners:
                i.wins = True
        if i.cards is None:
            continue
        else:
            if isinstance(i.cards, str):
                i.cards = (i.cards,)
            elif isinstance(i.cards, list):
                i.cards = tuple(i.cards)
    return tuple(lst)


def _get_events_matches(repo_location: str) -> tuple:
    files = _poker_collect_data(repo_location=repo_location)
    event_lst, matches, players, p_check = [], {}, {}, {}
    for k, v in files.items():
        matches[k] = []
        for i in v:
            hand_lst = parser(lines=i['lines'], times=i['times'], game_id=k)
            for event in hand_lst:
                event_lst.append((event.start_time, event)), matches[k].append(event)
    event_lst = sorted(event_lst, key=lambda x: x[0])
    event_lst = tuple(i[1] for i in event_lst)
    return event_lst, {k: tuple(v) for k, v in matches.items()}


@dataclass
class Data:

    __slots__ = ('events', 'matches')

    def __init__(self, repo_location: str):
        self.events, self.matches = _get_events_matches(repo_location=repo_location)

    def __repr__(self):
        return 'PokerData'

    def grouped_names(self) -> dict:
        id_d, id_c = {}, {}
        for i in self.events:
            if _str_nan(i.player_index) and i.player_index in id_c:
                if i.player_name not in id_d[i.player_index]:
                    id_d[i.player_index].append(i.player_name)
            elif _str_nan(i.player_index) and i.player_index not in id_c:
                id_d[i.player_index], id_c[i.player_index] = [i.player_name], True
        return {k: tuple(v) for k, v in id_d.items()}

    def unique_ids(self) -> tuple:
        return tuple(set([i.player_index for i in self.events if _str_nan(i.player_index)]))

    def unique_names(self) -> tuple:
        return tuple(set([i.player_name for i in self.events if _str_nan(i.player_name)]))
