from typing import Union, Optional, List
import pandas as pd
import numpy as np
from poker.base import round_to, flatten, unique_values, running_mean, running_std, native_std, native_mean, native_max, native_sum, native_median, native_percentile
from poker.document_filter_class import DocumentFilter
# import matplotlib.pyplot as plt
pd.set_option('use_inf_as_na', True)


# Wining Hand Face Card or Not?
def face_card_in_winning_cards(data: DocumentFilter) -> dict:
    """

    Find what percent of the time a face card is used to win.

    :param data: Input data.
    :type data: DocumentFilter
    :return: A dict of file_id and face card in winning hand percent.
    :rtype: dict
    :example:
        >>> # This function requires Player Stacks and Wins to be included in the DocumentFilter.
        >>> from poker.poker_class import Poker
        >>> from poker.analysis import face_card_in_winning_cards
        >>> from poker.document_filter_class import DocumentFilter
        >>> repo = 'location of your previous game'
        >>> grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
        >>>             ['48QVRRsiae', 'u8_FUbXpAz']]
        >>> poker = Poker(repo_location=repo, grouped=grouped)
        >>> face_card_in_winning_cards(data=DocumentFilter(data=poker, class_lst=['Player Stacks', 'Wins']))
    :note: Percent of all Winning Cards = Total all cards and get percent that include a face card.
        Percent one face in Winning Cards = Percent of all wins hand at least a single face card.

    """
    df = data.df.drop_duplicates('Start Time', keep='last').sort_values('Start Time',
                                                                        ascending=True).reset_index(drop=True)
    card_lst = ['None' if item is None else str('_'.join(item)) for item in df['Cards'].tolist()]
    card_dic_lst = []
    for cards in card_lst:
        if cards != 'None':
            card_dic_lst.append({card.split(' ')[0]: True for card in cards.split('_')})
        else:
            card_dic_lst.append({'None': True})

    win_tally, win_face_tally, win_face_one_count, win_nonface_tally = 0, 0, 0, 0
    for dic in card_dic_lst:
        if 'None' not in dic:
            win_tally += 1
            one_face_card = False
            for letter in dic.keys():
                if letter in {'J': True, 'Q': True, 'K': True, 'A': True}:
                    one_face_card = True
                    win_face_tally += 1
                else:
                    win_nonface_tally += 1
            if one_face_card is True:
                win_face_one_count += 1

    final_dic = {'Percent of all Winning Cards': 0.0, 'Percent one face in Winning Cards': 0.0}
    if win_face_tally != 0:
        temp_tally = win_nonface_tally + win_face_tally
        final_dic['Percent of all Winning Cards'] = round_to(data=win_face_tally / temp_tally, val=1000, remainder=True)
    if win_tally != 0:
        final_dic['Percent one face in Winning Cards'] = round_to(data=win_face_one_count / win_tally, val=1000,
                                                                  remainder=True)
    return final_dic


# Winning Streak
def longest_streak(data: DocumentFilter) -> pd.DataFrame:
    """

    Find the longest winning streak.

    :param data: Input data.
    :type data: DocumentFilter
    :return: Longest streak.
    :rtype: pd.DataFrame
    :example:
        >>> # This function requires Wins to be included in the DocumentFilter.
        >>> from poker.poker_class import Poker
        >>> from poker.analysis import longest_streak
        >>> from poker.document_filter_class import DocumentFilter
        >>> repo = 'location of your previous game'
        >>> grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
        >>>            ['48QVRRsiae', 'u8_FUbXpAz']]
        >>> poker = Poker(repo_location=repo, grouped=grouped)
        >>> longest_streak(data=DocumentFilter(data=poker, class_lst=['Wins']))
    :note: DocumentFilter requires class_lst=['Wins']

    """
    df = data.df.drop_duplicates('Start Time', keep='last').sort_values('Start Time',
                                                                        ascending=True).reset_index(drop=True)
    winner_lst = [{item: True for item in item_lst} for item_lst in df['Winner'].tolist()]
    unique_players = unique_values(data=df['Player Index'])
    final_dic = {player: 0 for player in unique_players}
    for player in unique_players:
        count, temp_count = [], 0
        for ind, winner in enumerate(winner_lst):
            if ind > 0:
                prev = winner_lst[ind - 1]
                if player in winner and player in prev:
                    temp_count += 1
                else:
                    count.append(temp_count)
                    temp_count = 0
        final_dic[player] = native_max(data=count)
    return pd.DataFrame.from_dict(final_dic, orient='index')


# Does raising signal winner?
def raise_signal_winning(data: DocumentFilter) -> pd.DataFrame:
    """

    When a player raises, does that mean they are going to win(?).

    :param data: Input data.
    :type data: DocumentFilter
    :return: A pd.DataFrame with the percent related to each position.
    :rtype: pd.DataFrame
    :example:
        >>> # This function requires Raises to be included in the DocumentFilter.
        >>> from poker.poker_class import Poker
        >>> from poker.analysis import raise_signal_winning
        >>> from poker.document_filter_class import DocumentFilter
        >>> repo = 'location of your previous game'
        >>> grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
        >>>            ['48QVRRsiae', 'u8_FUbXpAz']]
        >>> poker = Poker(repo_location=repo, grouped=grouped)
        >>> raise_signal_winning(data=DocumentFilter(data=poker, class_lst=['Raises']))
    :note: *None*

    """
    df = data.df
    winner_lst = [{item: True for item in item_lst} for item_lst in df['Winner'].tolist()]
    player_lst = df['Player Index'].tolist()
    position_lst = df['Position'].tolist()
    ran = range(len(position_lst))
    temp_lst = [{'Winner': winner_lst[ind], 'Player': player_lst[ind], 'Position': position_lst[ind]} for ind in ran]
    unique_players = unique_values(data=player_lst)
    temp_dic = {p: {'Pre Flop': {'Win': 0, 'Count': 0}, 'Post Flop': {'Win': 0, 'Count': 0}, 'Post Turn': {'Win': 0, 'Count': 0}, 'Post River': {'Win': 0, 'Count': 0}} for p in unique_players}
    for player in unique_players:
        for item in temp_lst:
            pos = item['Position']
            if player == item['Player'] and player in item['Winner']:
                temp_dic[player][pos]['Count'] += 1
                temp_dic[player][pos]['Win'] += 1
                continue
            elif player == item['Player'] and player not in item['Winner']:
                temp_dic[player][pos]['Count'] += 1

    final_dic = {p: {'Pre Flop': 0.0, 'Post Flop': 0.0, 'Post Turn': 0.0, 'Post River': 0.0} for p in unique_players}
    pos_lst = ['Pre Flop', 'Post Flop', 'Post Turn', 'Post River']
    for player in unique_players:
        for pos in pos_lst:
            val = temp_dic[player][pos]
            if val['Win'] != 0:
                final_dic[player][pos] = round_to(data=val['Win'] / val['Count'], val=1000, remainder=True)
            else:
                final_dic[player][pos] = 0.0
    return pd.DataFrame.from_dict(final_dic, orient='index')


# Dealer or big blind winning
def small_or_big_blind_win(data: DocumentFilter) -> pd.DataFrame:
    """

    When a player is small or big blind, does that mean they are going to win(?).

    :param data: Input data.
    :type data: DocumentFilter
    :return: A pd.DataFrame with the percent related to each blind.
    :rtype: pd.DataFrame
    :example:
        >>> # This function requires Small Blind and Big Blind to be included in the DocumentFilter.
        >>> from poker.poker_class import Poker
        >>> from poker.analysis import small_or_big_blind_win
        >>> from poker.document_filter_class import DocumentFilter
        >>> repo = 'location of your previous game'
        >>> grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
        >>>            ['48QVRRsiae', 'u8_FUbXpAz']]
        >>> poker = Poker(repo_location=repo, grouped=grouped)
        >>> small_or_big_blind_win(data=DocumentFilter(data=poker, class_lst=['Small Blind', 'Big Blind']))
    :note: *None*

    """
    df = data.df
    winner_lst = [{item: True for item in item_lst} for item_lst in df['Winner'].tolist()]
    player_lst = df['Player Index'].tolist()
    class_lst = df['Class'].tolist()
    ran = range(len(class_lst))
    temp_lst = [{'Winner': winner_lst[ind], 'Player': player_lst[ind], 'Class': class_lst[ind]} for ind in ran]
    unique_players = unique_values(data=player_lst)
    temp_dic = {p: {'Small Blind': {'Win': 0, 'Count': 0}, 'Big Blind': {'Win': 0, 'Count': 0}} for p in unique_players}
    for player in unique_players:
        for item in temp_lst:
            class_item = item['Class']
            if player == item['Player'] and player in item['Winner']:
                temp_dic[player][class_item]['Count'] += 1
                temp_dic[player][class_item]['Win'] += 1
                continue
            elif player == item['Player'] and player not in item['Winner']:
                temp_dic[player][class_item]['Count'] += 1

    final_dic = {player: {'Small Blind': 0.0, 'Big Blind': 0.0} for player in unique_players}
    move_lst = ['Small Blind', 'Big Blind']
    for player in unique_players:
        for mov in move_lst:
            val = temp_dic[player][mov]
            if val['Win'] != 0:
                final_dic[player][mov] = round_to(data=val['Win'] / val['Count'], val=1000, remainder=True)
            else:
                final_dic[player][mov] = 0.0
    return pd.DataFrame.from_dict(final_dic, orient='index')


def player_verse_player(data: DocumentFilter) -> dict:
    """

    Find how many times and what value a player called or folded related all other players.

    :param data: Input data.
    :type data: DocumentFilter
    :return: A dict of counts and values for each 'Calls', 'Raises', 'Checks', and 'Folds'.
    :rtype: dict
    :example:
        >>> # This function requires 'Calls', 'Raises', 'Checks', and 'Folds' to be included in the DocumentFilter.
        >>> from poker.poker_class import Poker
        >>> from poker.analysis import player_verse_player
        >>> from poker.document_filter_class import DocumentFilter
        >>> repo = 'location of your previous game'
        >>> grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
        >>>            ['48QVRRsiae', 'u8_FUbXpAz']]
        >>> poker = Poker(repo_location=repo, grouped=grouped)
        >>> player_verse_player(data=DocumentFilter(data=poker, class_lst=['Calls', 'Raises', 'Checks', 'Folds']))
    :note: *None*

    """
    df = data.df
    player_lst = df['Player Index'].tolist()
    class_lst = df['Class'].tolist()
    bet_lst = df['Bet Amount'].tolist()
    from_player_lst = df['From Person'].tolist()
    unique_players = unique_values(data=player_lst)
    ran = range(len(class_lst))
    temp_lst = [{'From Player': from_player_lst[ind], 'Bet Amount': bet_lst[ind], 'Player': player_lst[ind],
                 'Class': class_lst[ind]} for ind in ran]
    mov_lst = ['Calls', 'Raises', 'Checks', 'Folds']
    temp_dic = {}
    for player1 in unique_players:
        temp_dic[player1] = {}
        for player2 in unique_players[::-1]:
            if player1 != player2:
                temp_dic[player1][player2] = {mov: {'Count': 0, 'Values': []} for mov in mov_lst}

    for item in temp_lst:
        if item['From Player'] != 'None' and item['From Player'] in temp_dic[item['Player']].keys():
            temp_dic[item['Player']][item['From Player']][item['Class']]['Count'] += 1
            temp_dic[item['Player']][item['From Player']][item['Class']]['Values'] += [item['Bet Amount']]

    for player1 in unique_players:
        for player2 in unique_players[::-1]:
            if player1 != player2:
                for mov in mov_lst:
                    if native_sum(data=temp_dic[player1][player2][mov]['Values']) != 0:
                        temp_dic[player1][player2][mov]['Values'] = round_to(data=native_mean(temp_dic[player1][player2][mov]['Values']), val=1)
                    else:
                        temp_dic[player1][player2][mov]['Values'] = 0.0
    return temp_dic


def bluff_study(data: DocumentFilter, position_lst: Union[List[str], str] = None) -> pd.DataFrame:
    """

    Compare betting habits when a player is bluffing.

    :param data: Input data.
    :type data: DocumentFilter
    :param position_lst: Position in the hand to analyze, default is None. *Optional
    :type position_lst: Union[List[str], str]
    :return: A pd.DataFrame of counts and values for each position.
    :rtype: pd.DataFrame
    :example:
        >>> # This function requires a single player_index to be included in the DocumentFilter.
        >>> from poker.poker_class import Poker
        >>> from poker.analysis import bluff_study
        >>> from poker.document_filter_class import DocumentFilter
        >>> repo = 'location of your previous game'
        >>> grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
        >>>            ['48QVRRsiae', 'u8_FUbXpAz']]
        >>> poker = Poker(repo_location=repo, grouped=grouped)
        >>> bluff_study(data=DocumentFilter(data=poker, player_index_lst=['DZy-22KNBS']))
    :note: This function requires a single player_index to be included in the DocumentFilter.

    """
    if position_lst is None:
        position_lst = ['Post Flop', 'Post Turn', 'Post River', 'Wins']
    elif type(position_lst) == list:
        position_lst = position_lst
    else:
        position_lst = [position_lst]
    df = data.df
    col_lst = ['Position', 'Class', 'Player Starting Chips', 'Player Current Chips', 'Bet Amount', 'Pot Size', 'Time',
               'Previous Time', 'Remaining Players', 'Start Time']
    col_data = {col: df[col].tolist() for col in col_lst}
    ran = range(len(col_data['Class']))

    final_dic = {}
    for pos in position_lst:
        if pos != 'Wins':
            ind_dic = {col_data['Start Time'][ind]: True for ind in ran if col_data['Position'][ind] == pos and col_data['Class'][ind] == 'Folds'}
            key_value = 'Bluff'
        else:
            ind_dic = {col_data['Start Time'][ind]: True for ind in ran if col_data['Class'][ind] == 'Wins'}
            key_value = 'Win'

        bluff_lst, other_lst = [], []
        for ind in ran:
            temp = {col: col_data[col][ind] for col in col_lst}
            if col_data['Class'][ind] in ['Calls', 'Raises']:
                if col_data['Start Time'][ind] in ind_dic:
                    bluff_lst.append(temp)
                else:
                    other_lst.append(temp)

        bluff_df = pd.DataFrame(bluff_lst)
        other_df = pd.DataFrame(other_lst)

        temp_dic = {key_value: {}, 'Other': {}}
        for item in [bluff_df, other_df]:
            bet_lst = item['Bet Amount'].tolist()
            pot_lst = item['Pot Size'].tolist()
            curr_lst = item['Player Current Chips'].tolist()
            time_lst = item['Time'].tolist()
            prev_lst = item['Previous Time'].tolist()
            if len(item) == len(bluff_df):
                val = key_value
            else:
                val = 'Other'
            temp_dic[val]['Pot Per'] = []
            for i, j in enumerate(bet_lst):
                temp_val = pot_lst[i] - j
                if j > 0 and temp_val > 0:
                    temp_dic[val]['Pot Per'].append(j / temp_val)
                else:
                    temp_dic[val]['Pot Per'].append(0.0)

            temp_dic[val]['Curr Per'] = []
            for i, j in enumerate(bet_lst):
                temp_val = curr_lst[i] + j
                if j > 0 and temp_val > 0:
                    temp_dic[val]['Curr Per'].append(j / temp_val)
                else:
                    temp_dic[val]['Curr Per'].append(0.0)

            temp_dic[val]['Seconds'] = []
            for i, j in enumerate(time_lst):
                temp_dic[val]['Seconds'].append((j - prev_lst[i]).total_seconds())

            temp_dic[val]['Pot Per'] = round_to(temp_dic[val]['Pot Per'], 1000, True)
            temp_dic[val]['Curr Per'] = round_to(temp_dic[val]['Curr Per'], 1000, True)

        mu_dic = {}
        std_dic = {}
        median_dic = {}
        for key, val in temp_dic.items():
            mu_dic[key] = {}
            std_dic[key] = {}
            median_dic[key] = {}
            for key1, val1 in temp_dic[key].items():
                mu_dic[key][key1] = round_to(native_mean(data=val1), 1000, True)
                std_dic[key][key1] = round_to(native_std(data=val1, ddof=1), 1000, True)
                median_dic[key][key1] = round_to(native_median(data=val1), 1000, True)
        final_dic[pos] = {'Mean': mu_dic, 'Std': std_dic, 'Median': median_dic}

    result_dic = {}
    for key in final_dic.keys():
        for key1 in final_dic[key].keys():
            for key2 in final_dic[key][key1].keys():
                result_dic[key1 + ' ' + key + ' ' + key2] = final_dic[key][key1][key2]

    return pd.DataFrame.from_dict(result_dic, orient='index').sort_index()


def static_analysis(data: DocumentFilter) -> dict:
    """

    Build a static analysis DataFrame.

    :param data: Input data.
    :type data: DocumentFilter
    :return: A dict of stats.
    :rtype: dict
    :example:
        >>> # This function requires a single player_index to be included in the DocumentFilter.
        >>> from poker.poker_class import Poker
        >>> from poker.analysis import static_analysis
        >>> from poker.document_filter_class import DocumentFilter
        >>> repo = 'location of your previous game'
        >>> grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
        >>>            ['48QVRRsiae', 'u8_FUbXpAz']]
        >>> poker = Poker(repo_location=repo, grouped=grouped)
        >>> static_analysis(data=DocumentFilter(data=poker, player_index_lst=['DZy-22KNBS']))
    :note: This function requires a single player_index to be included in the DocumentFilter.

    """
    df = data.df
    temp_dic = {'Win': {'Mean': {}, 'Std': {}}, 'Loss': {'Mean': {}, 'Std': {}}}
    for wl in [True, False]:
        val = temp_dic['Loss']
        if wl is True:
            val = temp_dic['Win']

        temp_df = df[df['Win'] == wl]
        key_dic = {'Per Hand': 'Start Time', 'Per Position': 'Position', 'Per Class': 'Class'}
        for key1, val1 in key_dic.items():
            if key1 == 'Per Hand':
                aph_bet_lst = temp_df.groupby(val1)['Bet Amount'].mean()
                aph_sec_lst = temp_df.groupby(val1)['Seconds'].mean()
                aph_pot_lst = temp_df.groupby(val1)['Pot Size'].mean()
                aph_chips_lst = temp_df.groupby(val1)['Player Current Chips'].mean()
                aph_per_pot_lst = (aph_bet_lst / (aph_pot_lst - aph_bet_lst)).fillna(0.0)
                aph_per_curr_lst = (aph_bet_lst / (aph_bet_lst + aph_chips_lst)).fillna(0.0)
                times_seconds = [(row['End Time'] - row['Start Time']).total_seconds() for i, row in temp_df.iterrows()]

                val['Mean'][key1] = {}
                val['Mean'][key1]['Bet Amount'] = native_mean(data=aph_bet_lst)
                val['Mean'][key1]['Seconds'] = native_mean(data=aph_sec_lst)
                val['Mean'][key1]['Bet Percent of Pot'] = native_mean(data=aph_per_pot_lst)
                val['Mean'][key1]['Bet Percent of Chips'] = native_mean(data=aph_per_curr_lst)
                val['Mean']['Time'] = native_mean(data=times_seconds)

                val['Std'][key1] = {}
                val['Std'][key1]['Bet Amount'] = native_std(data=aph_bet_lst)
                val['Std'][key1]['Seconds'] = native_std(data=aph_sec_lst)
                val['Std'][key1]['Bet Percent of Pot'] = native_std(data=aph_per_pot_lst)
                val['Std'][key1]['Bet Percent of Chips'] = native_std(data=aph_per_curr_lst)
                val['Std']['Time'] = native_std(data=times_seconds)
            else:
                app_bet_lst_mu = temp_df.groupby(val1)['Bet Amount'].mean()
                app_sec_lst_mu = temp_df.groupby(val1)['Seconds'].mean()
                app_pot_lst_mu = temp_df.groupby(val1)['Pot Size'].mean()
                app_chips_lst_mu = temp_df.groupby(val1)['Player Current Chips'].mean()
                app_per_pot_lst_mu = (app_bet_lst_mu / (app_pot_lst_mu - app_bet_lst_mu)).fillna(0.0)
                app_per_curr_lst_mu = (app_bet_lst_mu / (app_bet_lst_mu + app_chips_lst_mu)).fillna(0.0)

                app_bet_lst_std = temp_df.groupby(val1)['Bet Amount'].std()
                app_sec_lst_std = temp_df.groupby(val1)['Seconds'].std()
                app_pot_lst_std = temp_df.groupby(val1)['Pot Size'].std()
                app_chips_lst_std = temp_df.groupby(val1)['Player Current Chips'].std()
                app_per_pot_lst_std = (app_bet_lst_std / (app_pot_lst_std - app_bet_lst_std)).fillna(0.0)
                app_per_curr_lst_std = (app_bet_lst_std / (app_bet_lst_std + app_chips_lst_std)).fillna(0.0)

                val['Mean'][key1] = {}
                val['Mean'][key1]['Bet Amount'] = app_bet_lst_mu.to_dict()
                val['Mean'][key1]['Seconds'] = app_sec_lst_mu.to_dict()
                val['Mean'][key1]['Bet Percent of Pot'] = app_per_pot_lst_mu.to_dict()
                val['Mean'][key1]['Bet Percent of Chips'] = app_per_curr_lst_mu.to_dict()

                val['Std'][key1] = {}
                val['Std'][key1]['Bet Amount'] = app_bet_lst_std.to_dict()
                val['Std'][key1]['Seconds'] = app_sec_lst_std.to_dict()
                val['Std'][key1]['Bet Percent of Pot'] = app_per_pot_lst_std.to_dict()
                val['Std'][key1]['Bet Percent of Chips'] = app_per_curr_lst_std.to_dict()
    return temp_dic


def pressure_or_hold(data: DocumentFilter, bet: int, position: Optional[str] = None):
    """

    Check how a player has responded to a bet in the past.

    :param data: Input data.
    :type data: DocumentFilter
    :paran bet: Proposed bet amount.
    :type bet: int
    :param position: Location in the hand, default is None. *Optional*
    :type position: str
    :return: A dict of Call Counts, Fold Counts, Total Count, and Call Percent.
    :rtype: dict
    :example:
        >>> # This function requires a single player_index to be included in the DocumentFilter.
        >>> from poker.poker_class import Poker
        >>> from poker.analysis import pressure_or_hold
        >>> from poker.document_filter_class import DocumentFilter
        >>> repo = 'location of your previous game'
        >>> grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
        >>>            ['48QVRRsiae', 'u8_FUbXpAz']]
        >>> poker = Poker(repo_location=repo, grouped=grouped)
        >>> pressure_or_hold(data=DocumentFilter(data=poker, player_index_lst=['DZy-22KNBS']),
        >>>                  bet=500, position='Pre Flop')
    :note: *None*

    """
    a = [bet]
    df = data.df
    if position is not None:
        if position not in {'Pre Flop': True, 'Post Flop': True, 'Post Turn': True, 'Post River': True}:
            raise AttributeError('position must be {Pre Flop, Post Flop, Post Turn, Post River, or None}')

        call_fold = df[(df['Class'] == 'Calls') | (df['Class'] == 'Folds') & (df['Position'] == position)]
        call = df[(df['Class'] == 'Calls') & (df['Position'] == position)]['Bet Amount'].tolist()
        fold = df[(df['Class'] == 'Folds') & (df['Position'] == position)]['Bet Amount'].tolist()
    else:
        call_fold = df[(df['Class'] == 'Calls') | (df['Class'] == 'Folds') & (df['Position'] == position)]
        call = df[df['Class'] == 'Calls']['Bet Amount'].tolist()
        fold = df[df['Class'] == 'Folds']['Bet Amount'].tolist()

    both = call_fold['Bet Amount'].tolist()
    qu_lst = [native_percentile(data=both, q=i) for i in [.023, .159, .500, .841, .977]]
    c_lst, f_lst, b_lst, t_lst = [], [], [], []
    for key1, val1 in {'Call': [c_lst, call], 'Fold': [f_lst, fold], 'Both': [b_lst, both], 'Test': [t_lst, a]}.items():
        for i in val1[1]:
            if i > qu_lst[-1]:
                val = round_to(data=i, val=1000)
            elif i < qu_lst[0]:
                val = round_to(data=i, val=25)
            else:
                val = round_to(data=i, val=50)
            val1[0].append(val)

    uv = unique_values(data=b_lst)
    temp_dic = {}
    for i in uv:
        c, f, p = c_lst.count(i), f_lst.count(i), 0.0
        if c > 0:
            p = round_to(data=c / (c + f), val=1000, remainder=True)
        temp_dic[i] = {'Call Count': c, 'Fold Count': f, 'Total Count': c + f, 'Percent': p}

    if bet in temp_dic.keys():
        return temp_dic[bet]
    else:
        print('No direct match, one below and above returned')
        key_lst = list(temp_dic.keys())
        one_smaller = 0
        one_larger = native_max(data=key_lst)
        for item in key_lst:
            if item < bet:
                if item - bet > one_smaller - bet:
                    one_smaller = item
            else:
                if bet - item > bet - one_larger:
                    one_larger = item
        if one_smaller == native_max(data=key_lst) or one_larger == 0:
            raise AttributeError('No results found')
        else:
            return {one_smaller: temp_dic[one_smaller], one_larger: temp_dic[one_larger]}


def ts_analysis(data: DocumentFilter, window: Optional[int] = 5) -> pd.DataFrame:
    """

    Build a Time Series DataFrame.

    :param data: A Player class object.
    :type data: DocumentFilter
    :param window: Rolling window value, default is 5. *Optional*
    :type window: int
    :return: A DataFrame of various moves over time.
    :rtype: pd.DataFrame
    :example:
        >>> # This function requires a single player_index to be included in the DocumentFilter.
        >>> from poker.poker_class import Poker
        >>> from poker.analysis import ts_analysis
        >>> from poker.document_filter_class import DocumentFilter
        >>> repo = 'location of your previous game'
        >>> grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
        >>>            ['48QVRRsiae', 'u8_FUbXpAz']]
        >>> poker = Poker(repo_location=repo, grouped=grouped)
        >>> ts_analysis(data=DocumentFilter(data=poker, player_index_lst=['DZy-22KNBS']))
        :note: This is a function version of the TSanalysis class.

    """
    df = data.df
    pos_dic = {'Pre Flop': 0.25, 'Post Flop': 0.50, 'Post Turn': 0.75, 'Post River': 1.0}

    # Game Id
    g_i_df = pd.DataFrame(df.groupby('Start Time')['Game Id'].last())
    g_i_df.columns = ['']

    # Time in Hand
    t_h_df = pd.DataFrame(df.groupby('Start Time')['Seconds into Hand'].last())
    t_h_df.columns = ['']

    # Last Position
    last_position = df.groupby('Start Time')['Position'].last().tolist()
    l_p_df = pd.DataFrame([pos_dic[item] for item in last_position], index=t_h_df.index, columns=[''])

    # Win
    r_w_p = df.groupby('Start Time')['Win'].last().tolist()
    r_w_p = [1 if item is True else 0 for item in r_w_p]
    r_w_p_df = pd.DataFrame(running_mean(data=r_w_p, num=window), index=t_h_df.index, columns=[''])

    # Bet, Count, and Time Per Position
    temp_df = df[(df['Class'] == 'Calls') | (df['Class'] == 'Raises') | (df['Class'] == 'Checks')]
    temp_df = temp_df.sort_values('Time', ascending=True).reset_index(drop=True)
    ind_lst = unique_values(data=temp_df['Start Time'].tolist(), order=True)
    pos_lst = ['Pre Flop', 'Post Flop', 'Post Turn', 'Post River']
    class_lst, short_class_lst = ['Checks', 'Calls', 'Raises'], ['Calls', 'Raises']

    p_bet = {'Pre Flop': [], 'Post Flop': [], 'Post Turn': [], 'Post River': []}
    c_count = {item1 + ' ' + item: [] for item in class_lst for item1 in pos_lst}
    c_seconds = {item1 + ' ' + item: [] for item in class_lst for item1 in pos_lst}
    c_bet = {item1 + ' ' + item: [] for item in short_class_lst for item1 in pos_lst}
    c_bet_per_pot = {item1 + ' ' + item: [] for item in short_class_lst for item1 in pos_lst}
    c_bet_per_chips = {item1 + ' ' + item: [] for item in short_class_lst for item1 in pos_lst}

    t_p_bet = {'Pre Flop': 0, 'Post Flop': 0, 'Post Turn': 0, 'Post River': 0}
    t_c_count = {item1 + ' ' + item: 0 for item in class_lst for item1 in pos_lst}
    t_c_seconds = {item1 + ' ' + item: None for item in class_lst for item1 in pos_lst}
    t_c_bet = {item1 + ' ' + item: None for item in short_class_lst for item1 in pos_lst}
    t_c_bet_per_pot = {item1 + ' ' + item: None for item in short_class_lst for item1 in pos_lst}
    t_c_bet_per_chips = {item1 + ' ' + item: None for item in short_class_lst for item1 in pos_lst}

    prev_ind, len_temp_df = temp_df['Start Time'].iloc[0], len(temp_df)
    for ind, row in temp_df.iterrows():
        if row['Start Time'] != prev_ind:
            prev_ind = row['Start Time']
            for key, val in t_p_bet.items():
                p_bet[key].append(val)

            for item in class_lst:
                for item1 in pos_lst:
                    c_count[item1 + ' ' + item].append(t_c_count[item1 + ' ' + item])
                    c_seconds[item1 + ' ' + item].append(t_c_seconds[item1 + ' ' + item])
                    if item != 'Checks':
                        c_bet[item1 + ' ' + item].append(t_c_bet[item1 + ' ' + item])
                        c_bet_per_pot[item1 + ' ' + item].append(t_c_bet_per_pot[item1 + ' ' + item])
                        c_bet_per_chips[item1 + ' ' + item].append(t_c_bet_per_chips[item1 + ' ' + item])

            t_p_bet = {'Pre Flop': 0, 'Post Flop': 0, 'Post Turn': 0, 'Post River': 0}
            t_c_count = {item1 + ' ' + item: 0 for item in class_lst for item1 in pos_lst}
            t_c_seconds = {item1 + ' ' + item: None for item in class_lst for item1 in pos_lst}
            t_c_bet = {item1 + ' ' + item: None for item in short_class_lst for item1 in pos_lst}
            t_c_bet_per_pot = {item1 + ' ' + item: None for item in short_class_lst for item1 in pos_lst}
            t_c_bet_per_chips = {item1 + ' ' + item: None for item in short_class_lst for item1 in pos_lst}

        t_pos, t_bet, t_class, t_second = row['Position'], row['Bet Amount'], row['Class'], row['Seconds']
        t_key = t_pos + ' ' + t_class

        t_p_bet[t_pos] += t_bet
        t_c_count[t_key] += 1
        if t_c_seconds[t_key] is not None:
            t_c_seconds[t_key] = native_mean(data=[t_c_seconds[t_key]] + [t_second])
        else:
            t_c_seconds[t_key] = t_second

        if t_class != 'Checks':
            if t_c_bet[t_key] is not None:
                t_c_bet[t_key] = native_mean(data=[t_c_bet[t_key]] + [t_bet])
            else:
                t_c_bet[t_key] = t_bet

            bet_pot_per = t_bet / (row['Pot Size'] - t_bet)
            if t_c_bet_per_pot[t_key] is not None:
                t_c_bet_per_pot[t_key] = native_mean(data=[t_c_bet_per_pot[t_key]] + [bet_pot_per])
            else:
                t_c_bet_per_pot[t_key] = bet_pot_per

            bet_chip_per = t_bet / (row['Player Current Chips'] + t_bet)
            if t_c_bet_per_chips[t_key] is not None:
                t_c_bet_per_chips[t_key] = native_mean(data=[t_c_bet_per_chips[t_key]] + [bet_chip_per])
            else:
                t_c_bet_per_chips[t_key] = bet_chip_per

        if ind == len_temp_df:
            for key, val in t_p_bet.items():
                p_bet[key].append(val)

            for item in class_lst:
                for item1 in pos_lst:
                    c_count[item1 + ' ' + item].append(t_c_count[item1 + ' ' + item])
                    c_seconds[item1 + ' ' + item].append(t_c_seconds[item1 + ' ' + item])
                    if item != 'Checks':
                        c_bet[item1 + ' ' + item].append(t_c_bet[item1 + ' ' + item])
                        c_bet_per_pot[item1 + ' ' + item].append(t_c_bet_per_pot[item1 + ' ' + item])
                        c_bet_per_chips[item1 + ' ' + item].append(t_c_bet_per_chips[item1 + ' ' + item])

    lst_dic = {'Position Bet': p_bet, 'Class Count': c_count, 'Class Seconds': c_seconds, 'Class Bet': c_bet,
               'Class Bet Percent of Pot': c_bet_per_pot, 'Class Bet Percent of Chips': c_bet_per_chips,
               'Seconds per Hand': t_h_df, 'Last Position in Hand': l_p_df, 'Rolling Win Percent': r_w_p_df,
               'Game Id': g_i_df}
    lst_df = []
    for key, val in lst_dic.items():
        if type(val) != pd.DataFrame:
            val = pd.DataFrame(val, index=ind_lst)
            val.columns = [key + ' ' + col for col in val.columns]
        else:
            val.columns = [key]
        lst_df.append(val)
    final_df = pd.concat(lst_df, axis=1).reset_index()
    return final_df

    # Plot Specific
    # t = pd.DataFrame(final_dic['Post Flop']['Calls']).set_index('Times').sort_index(ascending=True)
    # t['Temp Index'] = range(len(t))
    # tt = t.set_index('Temp Index')
    #
    # lst = []
    # prev = ' '
    # for i in tt['Game Id']:
    #     if prev != i:
    #         prev = i
    #     lst.append(prev)
    #
    # ttt = pd.DataFrame()
    # for col in tt.columns:
    #     if col not in ['Game Id']:
    #         ttt[col] = normalize(data=tt[col], keep_nan=True)
    #     elif col == 'Game Id':
    #         ttt[col] = lst
    # ttt = ttt.dropna(subset=['Counts', 'Values']).reset_index(drop=True)
    #
    # lst = []
    # prev = ' '
    # for i in ttt['Game Id']:
    #     if prev != i:
    #         prev = i
    #         lst.append(1)
    #     else:
    #         lst.append(np.nan)
    # tttt = ttt['Game Id'].drop_duplicates(keep='last')
    #
    # plt.figure(figsize=(10, 7))
    # ttt[['Counts', 'Player Reserve', 'Seconds', 'Values']].plot()
    # plot_lim_dic = {}
    # count = 0
    # ind_lst = list(tttt.index)
    # for i, j in enumerate(tttt):
    #     plt.vlines(x=ind_lst[i], ymin=0, ymax=1, color='black', linestyle='--')
    #     if i != 0:
    #         plot_lim_dic[str(count)] = [ind_lst[i - 1], ind_lst[i]]
    #     else:
    #         plot_lim_dic[str(count)] = [0, ind_lst[i]]
    #     count += 1
    # plt.xlim(plot_lim_dic['0'][0], plot_lim_dic['0'][1])
    # plt.legend(loc='upper right')
    # plt.show()
