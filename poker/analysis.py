from typing import List, Union, Optional
import pandas as pd
import numpy as np
from collections import Counter
from poker.processor import Wins, Raises, SmallBlind, BigBlind, Folds, Calls
from poker.classes import Hand, Game, Player
from poker.base import round_to, flatten


# Wining Hand Face Card or Not?
def face_card_in_winning_cards(hands: Union[List[Hand], Game]) -> float:
    """

    Find what percent of the time a face card is used to win.

    :param hands: Input data.
    :type hands: List[Hand] or Game
    :return: A percent.
    :rtype: float
    :example: *None*
    :note: *None*

    """
    win_tally = 0
    win_face_tally = 0
    for hand in hands:
        for line in hand.parsed_hand:
            if type(line) == Wins:
                win_tally += 1
                if line.cards is not None:
                    for card in line.cards:
                        if card.split(' ')[0] in ['J', 'Q', 'K', 'A']:
                            win_face_tally += 1
                            break
                break
    if win_face_tally != 0:
        return round(win_face_tally / win_tally, 2)
    else:
        return 0.0


# Winning Streak
def longest_streak(data: Union[Player, pd.DataFrame, pd.Series, np.ndarray]) -> int:
    """

    Find the longest winning streak.

    :param data: Input data.
    :type data: Player, pd.DataFrame, pd.Series, or np.ndarray
    :return: Longest streak.
    :rtype: int
    :example: *None*
    :note: *None*

    """
    if type(data) == Player:
        if 'Win Round' not in data.win_df.columns:
            raise AttributeError('No Win Round column in win_df')
        else:
            lst = list(data.win_df['Win Round'])
    elif type(data) == pd.DataFrame:
        if 'Win Round' not in data.columns:
            raise AttributeError('No Win Round column in win_df')
        else:
            lst = list(data['Win Round'])
    elif type(data) == pd.Series or type(data) == np.ndarray:
        lst = list(data)
    elif type(data) == list:
        lst = data
    else:
        raise AttributeError('Incorrect dtype for data')

    count, temp_count = [], 0
    for ind, item in enumerate(lst):
        previous = lst[ind - 1]
        if item - 1 == previous:
            temp_count += 1
        else:
            count.append(temp_count)
            temp_count = 0
    return max(count)


# Does raising signal winner?
def raise_signal_winning(data: Game, player_index: Optional[str] = None) -> pd.DataFrame:
    """

    When a player raises, does that mean they are going to win(?).

    :param data: Input data.
    :type data: Game
    :param player_index: ID of a specific player, default is None. *Optional*
    :type player_index: str
    :return: A pd.DataFrame with the count and percent related to each position.
    :rtype: pd.DataFrame
    :example: *None*
    :note: *None*

    """
    if player_index is not None:
        temp_id = player_index

    total_win_count = 0
    raise_dic = {"Pre Flop": 0, 'Post Flop': 0, 'Post Turn': 0, 'Post River': 0}

    for hand in data.hands_lst:
        for line in hand.parsed_hand:
            if type(line) == Wins:
                if player_index is None:
                    temp_id = line.player_index
                    total_win_count += 1
                else:
                    if line.player_index == player_index:
                        total_win_count += 1
                        break
        for line in hand.parsed_hand:
            if type(line) == Raises and line.player_index == temp_id:
                raise_dic[line.position] += 1
    temp_df = pd.DataFrame.from_dict(raise_dic, orient='index', columns=['Count'])
    temp_df['Percent'] = [round(val / total_win_count, 2) if val != 0 else 0 for val in raise_dic.values()]
    return temp_df


# Dealer or big blind winning
def small_or_big_blind_win(data: Game, player_index: Optional[str] = None) -> pd.DataFrame:
    """

    When a player is small or big blind, does that mean they are going to win(?).

    :param data: Input data.
    :type data: Game
    :param player_index: ID of a specific player, default is None. *Optional*
    :type player_index: str
    :return: A pd.DataFrame with the count and percent related to each blind.
    :rtype: pd.DataFrame
    :example: *None*
    :note: *None*

    """
    if player_index is not None:
        temp_id = player_index

    total_win_count = 0
    blind_dic = {'Small Blind': 0, 'Big Blind': 0}
    for hand in data.hands_lst:
        for line in hand.parsed_hand:
            if type(line) == Wins:
                if player_index is None:
                    temp_id = line.player_index
                    total_win_count += 1
                else:
                    if line.player_index == player_index:
                        total_win_count += 1
                        break
        count = 0
        for line in hand.parsed_hand:
            if type(line) == SmallBlind and line.player_index == temp_id:
                blind_dic['Small Blind'] += 1
                break
            elif type(line) == SmallBlind and line.player_index != temp_id:
                count += 1
            elif type(line) == BigBlind and line.player_index == temp_id:
                blind_dic['Big Blind'] += 1
                break
            elif type(line) == BigBlind and line.player_index != temp_id:
                count += 1
            elif count == 2:
                break

    temp_df = pd.DataFrame.from_dict(blind_dic, orient='index', columns=['Count'])
    temp_df['Percent'] = [round(val / total_win_count, 2) if val != 0 else 0 for val in blind_dic.values()]
    return temp_df


# Cards used in wins
def best_cards(data: Game, player_index: Optional[Union[str, List[str]]] = None) -> pd.DataFrame:
    """

    Find the most common winning cards and respective money earned.

    :param data: Input data.
    :type data: Game
    :param player_index: ID of a specific player or players, default is None. *Optional*
    :type player_index: str or List[str]
    :return: A pd.DataFrame with the count and money earned related to each blind.
    :rtype: pd.DataFrame
    :example: *None*
    :note: *None*

    """
    if player_index is not None:
        if type(player_index) == str:
            player_dic = {player_index: []}
        else:
            player_dic = {id: [] for id in player_index}
    else:
        players = list(data.players_info.index)
        player_dic = {id: [] for id in players}

    unique_cards = []
    for person in data.players.values():
        if person.win_df is not None:
            for row in person.win_df['Win Cards']:
                if row is not None:
                    unique_cards.append(list(row))
    unique_card_lst = flatten(data=unique_cards, return_unique=True)
    person_stack_dic = {person + ' stack': {card: 0 for card in unique_card_lst} for person in player_dic.keys()}

    for hand in data.hands_lst:
        for line in hand.parsed_hand:
            if type(line) == Wins and line.cards is not None and line.player_index in player_dic.keys():
                player_dic[line.player_index].append(list(line.cards))
                for card in line.cards:
                    person_stack_dic[line.player_index + ' stack'][card] += line.stack
                break

    card_lst = [dict(Counter(flatten(data=player_dic[key]))) for key in player_dic.keys()]
    temp_df = pd.DataFrame(card_lst, index=player_dic.keys()).T
    final_df = pd.concat([temp_df, pd.DataFrame.from_dict(person_stack_dic)], axis=1).fillna(0)
    return final_df


def player_verse_player_reaction(data: Game) -> dict:
    """

    Find how many times and what value a player called or folded related to each player.

    :param data: Input data.
    :type data: Game
    :return: A dict of counts and values for each call and fold.
    :rtype: dict
    :example: *None*
    :note: *None*

    """
    hands = data.hands_lst
    player_lst = list(data.players.keys())
    player_dic = {}
    for player_1 in player_lst:
        temp_dic = {}
        for player_2 in player_lst:
            if player_2 != player_1:
                temp_dic[player_2] = {'Call Count': 0, 'Fold Count': 0, 'Call Lst': [], 'Fold Lst': []}
        player_dic[player_1] = temp_dic

    for hand in hands:
        for line in hand.parsed_hand:
            if type(line) == Calls:
                if line.player_index is not None and line.action_from_player is not None:
                    player_dic[line.player_index][line.action_from_player]['Call Count'] += 1
                    if line.action_amount is None:
                        player_dic[line.player_index][line.action_from_player]['Call Lst'].append(0)
                    else:
                        player_dic[line.player_index][line.action_from_player]['Call Lst'].append(line.action_amount)

            elif type(line) == Folds:
                if line.player_index is not None and line.action_from_player is not None:
                    player_dic[line.player_index][line.action_from_player]['Fold Count'] += 1
                    if line.action_amount is None:
                        player_dic[line.player_index][line.action_from_player]['Fold Lst'].append(0)
                    else:
                        player_dic[line.player_index][line.action_from_player]['Fold Lst'].append(line.action_amount)

    return player_dic


def player_response(data: Player, player_reserve_chips: int, percent_or_stack: Optional[bool] = False) -> pd.DataFrame:
    """

    Find what value to bet to make a player call or fold.

    :param data: Input Player data.
    :type data: Player
    :param player_reserve_chips: Amount of chips the player has.
    :type player_reserve_chips: int
    :param percent_or_stack: If True, will use percent of bet related to players reserve chips.
        If False, will use bet amount, default is False. *Optional*
    :type percent_or_stack: bool
    :return: A DataFrame with an index representing percent of players stack.
    :rtype: pd.DataFrame
    :example: *None*
    :note: The Percent columns represent an int value of a percent.
        The Mu Stack columns represent an int value of the betting amount.
        If percent_or_stack is True, The Bet Value, represents the value to achieve a respective percent.

    """
    data_n = data.reaction
    if percent_or_stack:
        data_n['Percent of Reserve'] = data_n['Bet Amount'] / data_n['Player Reserve']

    for col in ['Bet Amount', 'Player Reserve']:
        data_n[col] = round_to(data=data_n[col], val=50, remainder=False)

    if percent_or_stack:
        data_n['Percent of Reserve'] = round_to(data=data_n['Percent of Reserve'], val=20, remainder=True)

    call_per_dic = {}
    fold_per_dic = {}
    call_mu_dic = {}
    fold_mu_dic = {}
    call_std_dic = {}
    fold_std_dic = {}

    if percent_or_stack:
        item = 'Percent of Reserve'
    else:
        item = 'Bet Amount'

    for i in data_n[item].unique():
        temp_calls = data_n[(data_n[item] == i) & (data_n['Class'] == 'Calls')]
        temp_folds = data_n[(data_n[item] == i) & (data_n['Class'] == 'Folds')]
        call_mu_dic[i] = np.median(temp_calls['Bet Amount'])
        fold_mu_dic[i] = np.median(temp_folds['Bet Amount'])

        if percent_or_stack:
            call_std_dic[i] = np.std(temp_calls['Bet Amount'], ddof=1)
            fold_std_dic[i] = np.std(temp_folds['Bet Amount'], ddof=1)
        else:
            call_std_dic[i] = len(temp_calls)
            fold_std_dic[i] = len(temp_folds)

        if len(temp_calls) != 0:
            call_per_dic[i] = round((len(temp_calls) / (len(temp_calls) + len(temp_folds))) * 100, 2)
        else:
            call_per_dic[i] = 0.0

        if len(temp_folds) != 0:
            fold_per_dic[i] = round((len(temp_folds) / (len(temp_calls) + len(temp_folds))) * 100, 2)
        else:
            fold_per_dic[i] = 0.0

    if percent_or_stack:
        dic = {'Call Percent': call_per_dic, 'Call Mu Stack': call_mu_dic, 'Call Std Stack': call_std_dic,
               'Fold Percent': fold_per_dic, 'Fold Mu Stack': fold_mu_dic, 'Fold Std Stack': fold_std_dic}
    else:
        dic = {'Call Percent': call_per_dic, 'Call Mu Stack': call_mu_dic, 'Call Count': call_std_dic,
               'Fold Percent': fold_per_dic, 'Fold Mu Stack': fold_mu_dic, 'Fold Count': fold_std_dic}

    df = pd.DataFrame.from_dict(dic).fillna(0.0).sort_index(ascending=True).astype(int)

    if percent_or_stack:
        df['Bet Value'] = [i * player_reserve_chips for i in list(df.index)]

    return df
