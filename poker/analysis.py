from typing import List, Union, Optional
import pandas as pd
import numpy as np
from collections import Counter
from poker.processor import Wins, Raises, SmallBlind, BigBlind
from poker.base import Hand, Game, Player


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


# Dealer or big blind winning
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
    unique_card_lst = list(set(sum(unique_cards, [])))
    person_stack_dic = {person + ' stack': {card: 0 for card in unique_card_lst} for person in player_dic.keys()}

    for hand in data.hands_lst:
        for line in hand.parsed_hand:
            if type(line) == Wins and line.cards is not None and line.player_index in player_dic.keys():
                player_dic[line.player_index].append(list(line.cards))
                for card in line.cards:
                    person_stack_dic[line.player_index + ' stack'][card] += line.stack
                break

    card_lst = [dict(Counter(list(sum(player_dic[key], [])))) for key in player_dic.keys()]
    temp_df = pd.DataFrame(card_lst, index=player_dic.keys()).T
    final_df = pd.concat([temp_df, pd.DataFrame.from_dict(person_stack_dic)], axis=1).fillna(0)
    return final_df
