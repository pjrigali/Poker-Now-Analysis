from typing import List, Optional, Union
from dataclasses import dataclass
import datetime
from os import walk
import csv
from poker.classes.event import Event


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
        c = Event(line, c)
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
            lst.append(_fill('Requests'))
            continue
        elif 'The admin approved' in line:
            lst.append(_fill('Approved'))
            continue
        elif 'joined the game' in line:
            lst.append(_fill('Joined'))
            continue
        elif ' stand up with ' in line:
            n = _fill('StandsUp')
            players_left = tuple([p for p in players_left if p != n.player_index])
            n.remaining_players = players_left
            lst.append(n)
            continue
        elif ' sit back with ' in line:
            lst.append(_fill('SitsIn'))
            continue
        elif 'Your hand' in line:
            n = _fill('MyCards')
            new_cards = line.split(' hand is ')[1].split(',')
            n.cards = tuple([i.strip() for i in new_cards])
            lst.append(n)
            continue
        elif 'posts a small blind' in line:
            n = _fill('SmallBlind')
            n.stack = int(line.split('of ')[1])
            pot += n.stack
            n.pot_size = pot
            current_chips[n.player_index] -= n.stack
            n.current_chips = current_chips
            p_person, p_amount = n.player_index, n.stack
            lst.append(n)
            continue
        elif 'posts a big blind' in line:
            n = _fill('SmallBlind')
            n.stack = int(line.split('of ')[1])
            pot += n.stack
            n.pot_size = pot
            current_chips[n.player_index] -= n.stack
            n.current_chips = current_chips
            p_person, p_amount = n.player_index, n.stack
            lst.append(n)
            continue
        elif ' folds' in line:
            n = _fill('Folds')
            players_left = tuple([p for p in players_left if p != n.player_index])
            n.remaining_players = players_left
            lst.append(n)
            continue
        elif ' calls ' in line:
            n = _fill('Calls')
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
            n = _fill('Raises')
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
            lst.append(_fill('Checks'))
            continue
        elif ' collected ' in line:
            n = _fill('Wins')
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
            n = _fill('Shows')
            new_cards = line.split(' shows a ')[1].split('.')[0].split(',')
            n.cards = [i.strip() for i in new_cards]
            lst.append(n)
            continue
        elif ' quits the game ' in line:
            n = _fill('Quits')
            players_left = tuple([p for p in players_left if p != n.player_index])
            n.remaining_players = players_left
            lst.append(n)
            continue
        elif 'Flop: ' in line or 'flop' in line:
            p_person, p_amount = None, None
            n = _fill('Flop')
            n.position = 'Flop'
            new_cards = line.split(' [')[1].split(']')[0].split(',')
            n.cards = [i.strip() for i in new_cards]
            lst.append(n)
            continue
        elif 'Turn: ' in line or 'turn: ' in line:
            p_person, p_amount = None, None
            n = _fill('Turn')
            n.position = 'Turn'
            n.cards = line.split(' [')[1].split(']')[0].strip()
            lst.append(n)
            continue
        elif 'River: ' in line or 'river: ' in line:
            p_person, p_amount = None, None
            n = _fill('River')
            n.position = 'River'
            n.cards = line.split(' [')[1].split(']')[0].strip()
            lst.append(n)
            continue
        elif 'Undealt cards: ' in line:
            p_person, p_amount = None, None
            n = _fill('Undealt')
            new_cards = line.split(' [')[1].split(']')[0].split(',')
            n.cards = [i.strip() for i in new_cards]
            if len(n.cards) == 1:
                n.position = 'Post Turn'
            elif len(n.cards) == 2:
                n.position = 'Post Flop'
            lst.append(n)
            continue
        elif 'Player stacks:' in line:
            n = _fill('PlayerStacks')
            n.player_name, n.player_index = n_lst, i_lst
            n.stack = 0
            n.current_chips, n.starting_chips = current_chips, start_chips
            lst.append(n)
            continue
    return tuple(lst)


@dataclass
class Data:

    __slots__ = ('data', 'nothing')

    def __int__(self, repo_location: str):
        files = _poker_collect_data(repo_location=repo_location)
        event_lst = []
        for k, v in files.items():
            for i in v:
                hand_lst = parser(lines=i['lines'], times=i['times'], game_id=k)
                for event in hand_lst:
                    event_lst.append(event)
        self.data = tuple(event_lst)

    def __repr__(self):
        return 'PokerData'
