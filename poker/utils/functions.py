import os
import csv
import datetime
from poker.classes.hand import Hand


def group_names(d: dict = None) -> dict:
    dct = {'other': ''}
    if d:
        for k, v in d.items():
            for i in v:
                dct[i] = k
    return dct


def player_id_name(s: str):
    s = s.split('"')[1]
    return s, s.split('@')[1].strip(), s.split('@')[0].strip()


def read_csv(folder: str, file_name: str) -> list:
    rows = []
    with open(os.path.join(folder, file_name), 'r', encoding='latin1') as f: # , encoding='utf-8-sig'
        rows.extend(csv.DictReader(f, delimiter=','))
    return rows


def parser(repo: str, file_name: str, me: str, player_dct: dict = None):
    lst, keep, player_names, hand_cnt, start_end, chips, player_dct, raw = [], False, set(), 1, {}, {}, group_names(player_dct), read_csv(repo, file_name)[::-1]
    for i in raw:
        i['game_id'] = file_name
        i['at'] = datetime.datetime.strptime(i['at'].split('.')[0].replace('T', ' '), '%Y-%m-%d %H:%M:%S')
        i['entry'] = i['entry'].strip()\
            .replace("â£", " Clubs")\
            .replace("â¦", " Diamonds")\
            .replace("â¥", " Hearts")\
            .replace("â", " Spades")
        del i['order']

        if not keep:
            if i['entry'].startswith('-- starting hand #1'):
                start_end[hand_cnt] = {'startTs': i['at'], 'endTs': None}
                keep = True
            else:
                continue
        else:
            if i['entry'].startswith('-- starting hand #'):
                hand_cnt = int(i['entry'].replace('-- starting hand #', '').split('(')[0].strip())
                start_end[hand_cnt] = {'startTs': i['at'], 'endTs': None}
                chips = {}
            elif i['entry'].startswith('-- ending hand #'):
                start_end[hand_cnt]['endTs'] = i['at']
            elif i['entry'].startswith('Player stacks:'):
                s = i['entry'].replace('Player stacks: ', '').split(' | ')
                for j in s:
                    j = j.split('"')
                    if j[1] not in player_names:
                        player_names.add(j[1])
                    chips[j[1]] = float(j[2].replace(' (', '').replace(')', ''))
                i['move'], i['value'] = 'Player Stacks', 0.0
            i['hand'] = {'number': hand_cnt}
            i['starting_chips'] = dict(chips)
            if not i['entry'].startswith('-- starting hand #')\
                    and not i['entry'].startswith('-- ending hand #')\
                    and i['entry'] not in ('Dead Small Blind', 'Dead Big Blind'):
                lst.append(i)

    # Hand Related
    hand_dct, hand_lst = {'win_cards': [], 'event_lst': [], 'event_dct': {}}, []

    # Event Related
    prev_dct = {'hand_cnt': 1,
                'pot': 0.0,
                'starting_chips': {},
                'current_chips': {},
                'time': lst[0]['at'],
                'player': None,
                'amount': None,
                'position': 'Pre Flop',
                'event': None,
                'winner': {'players': []},
                'table_cards': {'winner': []},
                'joined': []}

    for i in lst:
        i['hand'] = {**i['hand'], **start_end[i['hand']['number']]}
        if i.get('hand') and i['hand']['number'] != prev_dct['hand_cnt']:
            # Save old information
            hand_dct['game_id'] = prev_dct['event']['game_id']
            hand_dct['start_time'] = prev_dct['event']['hand_startTs']
            hand_dct['end_time'] = prev_dct['event']['hand_endTs']
            hand_dct['hand_time'] = hand_dct['end_time'] - hand_dct['start_time']
            hand_dct['hand_number'] = prev_dct['hand_cnt']
            hand_dct['starting_chips'] = dict(prev_dct['starting_chips'])
            hand_dct['ending_chips'] = dict(prev_dct['current_chips'])
            hand_dct['total_chips'] = sum(list(hand_dct['ending_chips'].values()))
            hand_dct['position'] = prev_dct['position']
            hand_dct['all_cards'] = list(set(sum(list(prev_dct['table_cards'].values()), [])))
            hand_dct['table_cards'] = prev_dct['table_cards']
            hand_dct['pot_size'] = prev_dct['pot']
            hand_dct['joined'] = prev_dct['joined']
            hand_dct['winner'] = prev_dct['winner']['players']
            hand_dct['win_stack'] = prev_dct['winner']['value']
            hand_dct['win_hand'] = prev_dct['winner'].get('with')
            hand_dct['win_cards'] = prev_dct['table_cards']['winner']
            for j in prev_dct['winner']['players']:
                if j in prev_dct['table_cards']:
                    hand_dct['win_cards'].extend(prev_dct['table_cards'][j])
            hand_dct['win_cards'] = list(set(hand_dct['win_cards']))
            hand_lst.append(Hand(hand_dct))
            hand_dct = {'win_cards': [], 'event_lst': [], 'event_dct': {}}

            # Reset prev_dct
            prev_dct = {'hand_cnt': i['hand']['number'],
                        'pot': 0.0,
                        'starting_chips': dict(i['starting_chips']),
                        'current_chips': dict(i['starting_chips']),
                        'time': i['at'],
                        'player': None,
                        'amount': None,
                        'position': 'Pre Flop',
                        'event': None,
                        'winner': {'players': []},
                        'table_cards': {'winner': []},
                        'joined': []}

        if i['entry'].endswith(' and go all in'):
            i['allIn'] = True

        if ' calls ' in i['entry']:
            i['move'], i['value'] = 'Call', i['entry'].split(' calls ')[1]
            if i.get('allIn', False):
                i['value'] = i['value'].replace(' and go all in', '')
            i['value'] = float(i['value'])
        elif i['entry'].endswith('checks'):
            i['move'] = 'Checks'
        elif i['entry'].endswith('folds'):
            i['move'] = 'Fold'
        elif ' bets ' in i['entry']:
            i['move'], i['value'] = 'Bet', i['entry'].split(' bets ')[1]
            if i.get('allIn', False):
                i['value'] = i['value'].replace(' and go all in', '')
            i['value'] = float(i['value'])
        elif ' shows ' in i['entry']:
            i['move'], i['cards'] = 'Show', i['entry'].split(' shows a ')[1].replace('.', '').split(',')
            i['cards'] = [j.strip() for j in i['cards']]
            prev_dct['player'], prev_dct['amount'], prev_dct['table_cards'][i['entry'].split('"')[1]] = None, None, i['cards']
        elif ' collected ' in i['entry']:
            i['move'], i['value'] = 'Win', float(i['entry'].split(' collected ')[1].split(' from ')[0])
            if i['entry'].endswith(')'):
                i['winWith'] = i['entry'].split(' pot with ')[1].replace(' (combination: ', ', [').replace(')', ']')
                i['cards'] = i['winWith'].split('[')[1].replace(']', '').split(',')
                i['cards'] = [j.strip() for j in i['cards']]
                prev_dct['winner']['with'] = i['winWith'].split(', [')[0]
                prev_dct['table_cards']['winner'].extend(i['cards'])
            prev_dct['winner']['players'].append(i['entry'].split('"')[1])
            prev_dct['winner']['value'] = i['value']
        elif i['entry'].startswith('Player stacks: '):
            prev_dct['starting_chips'] = dict(i['starting_chips'])
        elif ' big blind of ' in i['entry']:
            i['move'], i['value'] = 'Big Blind', i['entry'].split(' big blind of ')[1]
            if i.get('allIn', False):
                i['value'] = i['value'].replace(' and go all in', '')
            i['value'] = float(i['value'])
        elif ' raises to ' in i['entry']:
            i['move'], i['value'] = 'Raise', i['entry'].split(' raises to ')[1]
            if i.get('allIn', False):
                i['value'] = i['value'].replace(' and go all in', '')
            i['value'] = float(i['value'])
        elif ' small blind of ' in i['entry']:
            i['move'], i['value'] = 'Small Blind', i['entry'].split(' small blind of ')[1]
            if i.get('allIn', False):
                i['value'] = i['value'].replace(' and go all in', '')
            i['value'] = float(i['value'])
        elif i['entry'].startswith('Your hand is'):
            i['player'], i['move'], i['cards'] = me, 'Your Hand', i['entry'].replace('Your hand is ', '').split(',')
            i['cards'] = [j.strip() for j in i['cards']]
            prev_dct['table_cards']['your_cards'] = i['cards']
        elif i['entry'].startswith('Flop') or i['entry'].startswith('flop'):
            i['move'], i['cards'] = 'Flop', i['entry'].split('[')[1].replace(']', '').split(',')
            i['cards'] = [j.strip() for j in i['cards']]
            prev_dct['player'], prev_dct['amount'], prev_dct['position'], prev_dct['table_cards']['flop'] = None, None, 'Post Flop', i['cards']
        elif i['entry'].startswith('Turn') or i['entry'].startswith('turn'):
            i['move'], i['cards'] = 'Turn', i['entry'].split('[')[1].replace(']', '').split(',')
            i['cards'] = [j.strip() for j in i['cards']]
            prev_dct['player'], prev_dct['amount'], prev_dct['position'], prev_dct['table_cards']['turn'] = None, None, 'Post Turn', i['cards']
        elif i['entry'].startswith('River') or i['entry'].startswith('river'):
            i['move'], i['cards'] = 'River', i['entry'].split('[')[1].replace(']', '').split(',')
            i['cards'] = [j.strip() for j in i['cards']]
            prev_dct['player'], prev_dct['amount'], prev_dct['position'], prev_dct['table_cards']['river'] = None, None, 'Post River', i['cards']
        elif i['entry'].startswith('Undealt cards') or i['entry'].startswith('undealt cards'):
            i['move'], i['cards'] = 'Undealt Cards', i['entry'].split('[')[1].replace(']', '').split(',')
            i['cards'] = [j.strip() for j in i['cards']]
            prev_dct['player'], prev_dct['amount'], prev_dct['table_cards']['undealt'] = None, None, i['cards']
        elif i['entry'].startswith('Uncalled bet '):
            i['move'], i['value'] = 'Uncalled Bet', float(i['entry'].replace('Uncalled bet of ', '').split(' returned to')[0])
            prev_dct['player'], prev_dct['amount'] = None, None
        elif ' joined the game with ' in i['entry']:
            i['move'] = 'Joined'
            prev_dct['joined'].append(i['entry'].split('"')[1])
        elif i['entry'].endswith('requested a seat.'):
            i['move'] = 'Request'
        elif i['entry'].startswith('The admin approved the '):
            i['move'] = 'Approved'
        elif 'stand up with ' in i['entry']:
            i['move'] = 'Stands'
        elif ' sit back with ' in i['entry']:
            i['move'] = 'Sits'
        elif ' quits the game with ' in i['entry']:
            i['move'] = 'Quits'
        elif i['entry'].startswith('The game')\
                or 'run it twice' in i['entry']\
                or i['entry'].startswith('WARNING:')\
                or i['entry'].startswith('The admin ')\
                or i['entry'].startswith('Remaining players ')\
                or i['entry'].endswith('canceled the seat request.')\
                or ' passed the room ownership ' in i['entry']:
            i['move'] = 'Game'

        if i['move'] not in ('Player Stacks', 'Your Hand', 'Flop', 'Turn', 'River', 'Game', 'Undealt Cards'):
            i['player'], i['playerId'], i['playerName'] = player_id_name(i['entry'])
            i['playerGroup'] = player_dct.get(i['playerId'], 'other')

            if i['move'] in ('Bet', 'Raise', 'Small Blind', 'Big Blind'):
                if i['move'] in ('Raise', 'Big Blind'):
                    i['actionFrom'], i['actionAmount'] = prev_dct['player'], prev_dct['amount']
                prev_dct['player'], prev_dct['amount'] = i['player'], i['value']
            elif prev_dct['player']:
                i['actionFrom'], i['actionAmount'] = prev_dct['player'], prev_dct['amount']

            if i.get('move') != 'Win':
                if i.get('move') != 'Uncalled Bet':
                    prev_dct['pot'] += i.get('value', 0.0)
                    if i.get('player') in prev_dct['current_chips']:
                        prev_dct['current_chips'][i['player']] -= i.get('value', 0.0)
        i['current_chips'] = dict(prev_dct['current_chips'])
        i['pot'] = prev_dct['pot']
        i['decisionTime'] = prev_dct['time']
        i['position'] = prev_dct['position']
        prev_dct['time'] = i['at']
        prev_dct['starting_chips'] = dict(i['starting_chips']) if i['starting_chips'] != prev_dct['starting_chips'] else prev_dct['starting_chips']
        for j in ('starting_chips', 'current_chips', 'hand'):
            if j in i:
                if i[j]:
                    for k, v in i[j].items():
                        i[f"{j}_{k}"] = v
                del i[j]
        hand_dct['event_lst'].append(i)
        if not hand_dct['event_dct'].get(i['move']):
            hand_dct['event_dct'][i['move']] = [i]
        else:
            hand_dct['event_dct'][i['move']].append(i)
        prev_dct['event'] = i
    return lst, hand_lst


def parse_games(repo: str, me: str, grouped: dict = None):
    files = next(os.walk(repo))[2]
    lst, hands = [], []
    for f in files:
        l, h = parser(repo, f, me, grouped)
        lst.extend(l), hands.extend(h)
    return lst, hands
