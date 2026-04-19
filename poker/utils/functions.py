"""
Functions used in the parsing of Poker Now logs.
"""
# pylint: disable=E0401
# pylint: disable=E0611
import os
import re
import csv
import datetime
from poker.classes.hand import Hand


def group_names(d: dict = None) -> dict:
    group_dict = {'other': ''}
    if d:
        for key, values in d.items():
            for value in values:
                group_dict[value] = key
    return group_dict


def get_player_id(s: str) -> str:
    if s:
        return s.split('@')[1].strip()
    else:
        return None


def get_player_name(s: str) -> str:
    if s:
        return s.split('@')[0].strip()
    else:
        return None


def player_id_name(s: str):
    s = s.split('"')[1]
    return s, get_player_id(s), get_player_name(s)


def read_csv(folder: str, file_name: str) -> list:
    rows = []
    with open(os.path.join(folder, file_name), 'r', encoding='latin1') as f:
        rows.extend(csv.DictReader(f, delimiter=','))
        f.close()
    return rows


def get_player_lookup(path: str, grouped: dict = None) -> dict:
    """Read poker log CSVs and return a mapping of player IDs to known names.

    Parameters
    ----------
    path : str
        Either a path to a single CSV file **or** a folder containing CSV files.
        When a folder is provided every ``.csv`` file in the folder is scanned.
    grouped : dict, optional
        A canonical guide mapping real names to their known IDs, e.g.
        ``{'Peter': ('mQWfGaGPXE', 'hOG9_DzBzN'), ...}``.
        When provided the return shape changes — see below.

    Returns
    -------
    dict
        **Without** ``grouped``:
            ``{player_id: [name1, name2, ...]}`` – raw ID → display-name lookup.

        **With** ``grouped``:
            ``{canonical_name: {'ids': [...], 'names': [...]}}`` where ``ids``
            are taken from ``grouped`` and ``names`` is the deduplicated union
            of every display name seen in the data for those IDs.
    """
    # Decide whether path is a file or directory and build file list
    if os.path.isfile(path):
        folder, files = os.path.dirname(path), [os.path.basename(path)]
    else:
        folder = path
        files = [f for f in os.listdir(path) if f.endswith('.csv')]

    # Pattern captures the "Name @ ID" tokens wrapped in quotes within entries
    pattern = re.compile(r'"([^"]+?)\s*@\s*([^"]+)"')

    # Build raw id -> [display names] lookup from every CSV row
    raw_lookup: dict[str, list[str]] = {}
    for file in files:
        rows = read_csv(folder, file)
        for row in rows:
            entry = row.get('entry', '')
            for name, pid in pattern.findall(entry):
                name = name.strip()
                pid = pid.strip()
                if pid not in raw_lookup:
                    raw_lookup[pid] = []
                if name not in raw_lookup[pid]:
                    raw_lookup[pid].append(name)

    if grouped is None:
        return raw_lookup

    # Collect all IDs claimed by the guide
    grouped_ids = {pid for ids in grouped.values() for pid in ids}

    # Merge with the canonical guide
    merged: dict[str, dict] = {}
    for canonical_name, ids in grouped.items():
        all_names = []
        for pid in ids:
            for display_name in raw_lookup.get(pid, []):
                if display_name not in all_names:
                    all_names.append(display_name)
        merged[canonical_name] = {'ids': list(ids), 'names': all_names}

    # Add any IDs found in the data that aren't covered by the guide
    for pid, names in raw_lookup.items():
        if pid not in grouped_ids:
            merged[pid] = {'ids': [pid], 'names': names}

    return merged


def rename_logs(path: str, dry_run: bool = False) -> list:
    """Rename Poker Now CSV log files to a standard ``YYYY_MM_DD_Poker Log`` format.

    The game date is determined by reading the earliest ``at`` timestamp found
    inside each CSV.  Files that already match the target naming scheme are
    skipped.  When more than one file maps to the same calendar date the first
    file keeps the plain name and each subsequent collision receives a numeric
    suffix (``_02``, ``_03``, …).

    Parameters
    ----------
    path : str
        Path to a folder containing Poker Now CSV log files.
    dry_run : bool, optional
        When ``True`` the function prints what would be renamed without
        actually writing anything to disk.  Useful for previewing changes
        before committing.  Defaults to ``False``.

    Returns
    -------
    list of dict
        One entry per file that was (or would be) renamed, each with the
        keys ``'old'`` and ``'new'`` containing the original and target
        file names respectively.
    """
    target_pattern = re.compile(r'^\d{4}_\d{2}_\d{2}_Poker Log(_\d{2})?\.csv$')

    files = [f for f in os.listdir(path) if f.endswith('.csv')]

    # --- pass 1: resolve the game date for every file that needs renaming ---
    pending = []   # list of (old_name, date_obj)
    for file in files:
        if target_pattern.match(file):
            continue  # already correctly named — skip

        rows = read_csv(path, file)
        if not rows:
            continue

        # Find the earliest timestamp in the file to get the true game date
        dates = []
        for row in rows:
            at_raw = row.get('at', '')
            if at_raw:
                try:
                    dt = datetime.datetime.strptime(at_raw.split('.')[0], '%Y-%m-%dT%H:%M:%S')
                    dates.append(dt.date())
                except ValueError:
                    pass

        if not dates:
            continue

        game_date = min(dates)
        pending.append((file, game_date))

    # --- pass 2: sort by (date, original name) for deterministic ordering ---
    pending.sort(key=lambda x: (x[1], x[0]))

    # Count how many files already exist for each date (from already-renamed files)
    date_counts: dict = {}
    for existing in files:
        m = target_pattern.match(existing)
        if m:
            try:
                d = datetime.date(int(existing[:4]), int(existing[5:7]), int(existing[8:10]))
                date_counts[d] = date_counts.get(d, 0) + 1
            except ValueError:
                pass

    # --- pass 3: assign new names and rename ---
    renames = []
    for old_name, game_date in pending:
        count = date_counts.get(game_date, 0)

        if count == 0:
            new_name = game_date.strftime('%Y_%m_%d') + '_Poker Log.csv'
        else:
            new_name = game_date.strftime('%Y_%m_%d') + f'_Poker Log_{count + 1:02d}.csv'

        date_counts[game_date] = count + 1
        renames.append({'old': old_name, 'new': new_name})

        if dry_run:
            print(f'[dry-run] {old_name!r}  ->  {new_name!r}')
        else:
            src = os.path.join(path, old_name)
            dst = os.path.join(path, new_name)
            os.rename(src, dst)
            print(f'Renamed: {old_name!r}  ->  {new_name!r}')

    return renames


def parser(repo: str, file_name: str, me: str, player_dct: dict = None):
    lst, keep, player_names, hand_cnt, start_end, chips, player_dct, raw = [], False, set(), 1, {}, {}, group_names(player_dct), read_csv(repo, file_name)[::-1]
    for i in raw:
        i['game_id'] = file_name
        i['at'] = datetime.datetime.strptime(i['at'].split('.')[0].replace('T', ' '), '%Y-%m-%d %H:%M:%S')
        i['entry'] = i['entry'].strip()\
            .replace("â£", " Clubs")\
            .replace("â¦", " Diamonds")\
            .replace("â¥", " Hearts")\
            .replace("â", " Spades")\
            .replace('1 Clubs', 'A Clubs')\
            .replace('1 Diamonds', 'A Diamonds')\
            .replace('1 Hearts', 'A Hearts')\
            .replace('1 Spades', 'A Spades')
        if i.get('oder'):
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
                'joined': [],
                'remaining_players': []}

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
            hand_dct['ending_players'] = prev_dct['remaining_players']
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
                        'joined': [],
                        'remaining_players': []}

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
                prev_dct['table_cards']['winner'] = i['cards']
            prev_dct['winner']['players'].append(i['entry'].split('"')[1])
            prev_dct['winner']['value'] = i['value']
        elif i['entry'].startswith('Player stacks: '):
            prev_dct['starting_chips'] = dict(i['starting_chips'])
            prev_dct['remaining_players'] = list(prev_dct['starting_chips'].keys())
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
            i['value'] = float(i['entry'].split('with a stack of ')[1].replace('.', ''))
        elif i['entry'].endswith('requested a seat.'):
            i['move'] = 'Request'
        elif i['entry'].startswith('The admin approved the '):
            i['move'] = 'Approved'
            i['value'] = float(i['entry'].split('with a stack of ')[1].replace('.', ''))
        elif 'stand up with ' in i['entry']:
            i['move'] = 'Stands'
            i['value'] = float(i['entry'].split('with the stack of ')[1].replace('.', ''))
        elif ' sit back with ' in i['entry']:
            i['move'] = 'Sits'
            i['value'] = float(i['entry'].split('with the stack of ')[1].replace('.', ''))
        elif ' quits the game with ' in i['entry']:
            i['move'] = 'Quits'
            i['value'] = float(i['entry'].split('with a stack of ')[1].replace('.', ''))
        elif i['entry'].startswith('The game')\
                or 'run it twice' in i['entry']\
                or i['entry'].startswith('WARNING:')\
                or i['entry'].startswith('The admin ')\
                or i['entry'].startswith('Remaining players ')\
                or i['entry'].endswith('canceled the seat request.')\
                or ' passed the room ownership ' in i['entry']:
            i['move'] = 'Game'

        if i.get('move') and i['move'] not in ('Player Stacks', 'Your Hand', 'Flop', 'Turn', 'River', 'Game', 'Undealt Cards'):
            i['player'], i['playerId'], i['playerName'] = player_id_name(i['entry'])
            i['playerGroup'] = player_dct.get(i['playerId'], 'other')

            if i['move'] in ('Bet', 'Raise', 'Small Blind', 'Big Blind'):
                if i['move'] in ('Raise', 'Big Blind'):
                    i['actionFrom'], i['actionAmount'] = prev_dct['player'], prev_dct['amount']
                prev_dct['player'], prev_dct['amount'] = i['player'], i['value']
            elif prev_dct['player']:
                i['actionFrom'], i['actionAmount'] = prev_dct['player'], prev_dct['amount']

            if i.get('move') not in ('Win', 'Uncalled Bet', 'Joined', 'Request', 'Approved', 'Stands', 'Sits', 'Quits'):
                prev_dct['pot'] += i.get('value', 0.0)
                if i.get('player') in prev_dct['current_chips']:
                    prev_dct['current_chips'][i['player']] -= i.get('value', 0.0)
            if i.get('move') in ('Fold', 'Quits', 'Stands'):
                if i['player'] in prev_dct['remaining_players']:
                    prev_dct['remaining_players'].remove(i['player'])
        i['current_chips'] = dict(prev_dct['current_chips'])
        i['pot'] = prev_dct['pot']
        i['decisionTime'] = prev_dct['time']
        i['position'] = prev_dct['position']
        i['remaining_players'] = prev_dct['remaining_players'].copy()
        prev_dct['time'] = i['at']
        prev_dct['starting_chips'] = dict(i['starting_chips']) if i['starting_chips'] != prev_dct['starting_chips'] else prev_dct['starting_chips']
        for j in ('starting_chips', 'current_chips', 'hand'):
            if j in i:
                if i[j]:
                    for key, value in i[j].items():
                        i[f"{j}_{key}"] = value
                del i[j]
        hand_dct['event_lst'].append(i)
        if i.get('move'):
            if not hand_dct['event_dct'].get(i['move']):
                hand_dct['event_dct'][i['move']] = [i]
            else:
                hand_dct['event_dct'][i['move']].append(i)
            prev_dct['event'] = i
    return lst, hand_lst


def parse_games(repo: str, user_name: str, grouped: dict = None):
    """This function grabs files within a given repo and parses the log file."""
    lst, hands, files = [], [], next(os.walk(repo))[2]
    for file in files:
        if file.endswith('.csv'):
            event_lst, hand_lst = parser(repo, file, user_name, grouped)
            lst.extend(event_lst)
            hands.extend(hand_lst)
    return lst, hands
