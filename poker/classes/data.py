from dataclasses import dataclass
import datetime
from os import walk
import csv
from poker.classes.event import Event
from poker.classes.hand import Hand
from poker.classes.match import Match
from poker.utils.class_functions import _str_nan
from poker.utils.base import calculate_hand, calc_gini


def _poker_collect_data(repo_location: str):
    """Open file, clean data and parse into Event/Hand and Match objects"""

    def _get_rows(file: str) -> dict:
        """Get rows of data"""

        def _convert(data: list, dic: dict):
            """Convert shapes to words and corrects timestamps"""
            dic['Event'].append(data[0].replace("â£", " Clubs").replace("â¦", " Diamonds").replace("â¥", " Hearts").replace("â", " Spades"))
            dic['Time'].append(datetime.datetime.strptime(data[1].replace('T', ' ').split('.')[0], '%Y-%m-%d %H:%M:%S'))

        def _rev(lst: list) -> list:
            """Reverse list"""
            lst.reverse()
            return lst

        dic = {'Event': [], 'Time': []}
        with open(file, 'r', encoding='latin1') as file:
            my_reader = csv.reader(file, delimiter=',')
            for ind, row in enumerate(my_reader):
                if ind > 0:
                    _convert(data=row, dic=dic)
        dic['Event'], dic['Time'] = _rev(dic['Event']), _rev(dic['Time'])
        return dic

    files, event_lst, matches = next(walk(repo_location))[2], [], {}
    for file in files:
        hands, v, t, d = [], [], [], _get_rows(file=repo_location + file)
        file = file.split('.')[0]
        for ind, val in enumerate(d['Event']):
            if ' starting hand ' in val:
                events = _parser(lines=v, times=t, game_id=file)
                hands.append(Hand(events=events))
                event_lst += [(e.time, e) for e in events]
                v, t = [val], [d['Time'][ind]]
            else:
                v.append(val), t.append(d['Time'][ind])
        events = _parser(lines=v, times=t, game_id=file)
        hands.append(Hand(events=events))
        event_lst += [(e.time, e) for e in events]
        matches[file] = Match(hands=tuple(hands))
    event_lst = sorted(event_lst, key=lambda x: x[0])
    return tuple(i[1] for i in event_lst), matches


def _parser(lines: list, times: list, game_id: str) -> tuple:
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
            continue
        elif 'Player stacks:' in line:
            for play in line.split('#')[1:]:
                n_lst.append(play.split('@')[0].split('"')[1].strip()), i_lst.append(play.split('@')[1].split('"')[0].strip()), v_lst.append(int(play.split('(')[1].split(')')[0]))
            break
    if len(n_lst) == 0:
        for line in lines:
            if 'The admin approved' in line:
                n_lst.append(line.split('@')[0].split('"')[1].strip()), i_lst.append(line.split('@')[1].split('"')[0].strip()), v_lst.append(0)
    n_lst, i_lst, v_lst = tuple(n_lst), tuple(i_lst), tuple(v_lst)

    def _fill(c):
        """applies values to the blank event class"""
        return Event(text=line, event=c, position=pos, winning_hand=winning_hands, current_round=c_round,
                     pot_size=pot, starting_players=start_players, remaining_players=players_left,
                     action_from_player=p_person, action_amount=p_amount, game_id=game_id,
                     starting_chips=start_chips, current_chips=current_chips, winner=winners, win_stack=win_stacks,
                     time=times[ind], previous_time=times[ind - 1], start_time=times[0], end_time=times[-1], gini=gini,
                     event_number=event_number)

    lst = []
    pot, players_left, pos, gini, event_number = 0, i_lst, 'Pre Flop', calc_gini(data=v_lst), -1
    start_chips, start_players, current_chips = dict(zip(i_lst, v_lst)), dict(zip(i_lst, n_lst)), dict(zip(i_lst, v_lst))
    p_person, p_amount, winners, win_stacks, winning_hands, cards, all_cards, shows = None, None, None, None, None, [], [], []
    for ind, line in enumerate(lines):
        if ' calls ' in line:
            event_number += 1
            n = _fill('Calls')._add_stack(line.split(' calls ')[1])
            if ' and ' in n.stack:
                n._add_stack(int(n.stack.split(' and ')[0]))._add_all_in()
            else:
                n._add_stack(int(n.stack))
            pot, current_chips = n._update_pot_curr(current_chips, '-')
            lst.append(n)
            continue
        elif ' checks' in line:
            event_number += 1
            lst.append(_fill('Checks'))
            continue
        elif ' folds' in line:
            event_number += 1
            n, players_left = _fill('Folds')._add_remaining(players_left, True)
            lst.append(n)
            continue
        elif ' bets ' in line or ' raises ' in line:
            event_number += 1
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
            event_number += 1
            n = _fill('Shows')._add_cards([i.strip() for i in line.split(' shows a ')[1].split('.')[0].split(',')])
            all_cards = n._get_cards_allcards(cards=None, all_cards=all_cards)
            lst.append(n), shows.append(n)
            continue
        elif ' collected ' in line:
            event_number += 1
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
            event_number += 1
            n = _fill('PlayerStacks')._add_stack(0)
            n.player_name, n.player_index, n.current_chips, n.starting_chips = n_lst, i_lst, current_chips, start_chips
            all_cards = n._get_cards_allcards(cards=None, all_cards=all_cards)
            lst.append(n)
            continue
        elif 'posts a big blind' in line:
            event_number += 1
            n, pot, current_chips = _fill('BigBlind')._add_stack(int(line.split('big blind of ')[1]))._update_pot_curr(current_chips, '-', True)
            p_person, p_amount = n.player_index, n.stack
            lst.append(n)
            continue
        elif 'posts a small blind' in line:
            event_number += 1
            n, pot, current_chips = _fill('SmallBlind')._add_stack(int(line.split('small blind of ')[1]))._update_pot_curr(current_chips, '-', True)
            p_person, p_amount = n.player_index, n.stack
            lst.append(n)
            continue
        elif 'Flop: ' in line or 'flop' in line:
            event_number += 1
            p_person, p_amount = None, None
            n = _fill('Flop')._add_cards([i.strip() for i in line.split(' [')[1].split(']')[0].split(',')])
            n.position, pos = 'Flop', 'Post Flop'
            cards, all_cards = n._get_cards_allcards(cards=n.cards, all_cards=all_cards)
            lst.append(n)
            continue
        elif 'Turn: ' in line or 'turn: ' in line:
            event_number += 1
            p_person, p_amount = None, None
            n = _fill('Turn')._add_cards([line.split(' [')[1].split(']')[0].strip()])
            cards, all_cards = n._get_cards_allcards(cards=n.cards, all_cards=all_cards)
            n.position, pos = 'Turn', 'Post Turn'
            lst.append(n)
            continue
        elif 'River: ' in line or 'river: ' in line:
            event_number += 1
            p_person, p_amount = None, None
            n = _fill('River')._add_cards([line.split(' [')[1].split(']')[0].strip()])
            n.position, pos = 'River', 'Post River'
            cards, all_cards = n._get_cards_allcards(cards=n.cards, all_cards=all_cards)
            lst.append(n)
            continue
        elif 'Your hand' in line:
            event_number += 1
            n = _fill('MyCards')._add_cards([i.strip() for i in line.split(' hand is ')[1].split(',')])
            all_cards = n._get_cards_allcards(cards=None, all_cards=all_cards)
            lst.append(n)
            continue
        elif 'joined the game' in line:
            event_number += 1
            lst.append(_fill('Joined'))
            continue
        elif 'requested a seat' in line:
            event_number += 1
            lst.append(_fill('Requests'))
            continue
        elif 'The admin approved' in line:
            event_number += 1
            lst.append(_fill('Approved'))
            continue
        elif ' quits the game ' in line:
            event_number += 1
            n, players_left = _fill('Quits')._add_remaining(players_left, True)
            lst.append(n)
            continue
        elif 'Undealt cards: ' in line:
            event_number += 1
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
            event_number += 1
            n, players_left = _fill('StandsUp')._add_remaining(players_left, True)
            lst.append(n)
            continue
        elif ' sit back with ' in line:
            event_number += 1
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


@dataclass
class Data:

    __slots__ = ('events', 'matches')

    def __init__(self, repo_location: str):
        self.events, self.matches = _poker_collect_data(repo_location=repo_location)

    def __repr__(self):
        return 'PokerData'

    def grouped_names(self) -> dict:
        """Get grouped dict of names and indexes"""
        id_d, id_c = {}, {}
        for i in self.events:
            if _str_nan(i.player_index) and i.player_index in id_c:
                if i.player_name not in id_d[i.player_index]:
                    id_d[i.player_index].append(i.player_name)
            elif _str_nan(i.player_index) and i.player_index not in id_c:
                id_d[i.player_index], id_c[i.player_index] = [i.player_name], True
        return {k: tuple(v) for k, v in id_d.items()}

    def unique_ids(self) -> tuple:
        """Get unique player indexes"""
        return tuple(set([i.player_index for i in self.events if _str_nan(i.player_index)]))

    def unique_names(self) -> tuple:
        """Get unique player names"""
        return tuple(set([i.player_name for i in self.events if _str_nan(i.player_name)]))

    def unique_games(self) -> tuple:
        """Get unique match names"""
        return tuple(set([i.game_id for i in self.events if _str_nan(i.game_id)]))

    def items(self):
        """Returns event and match attributes"""
        return self.events, self.matches
