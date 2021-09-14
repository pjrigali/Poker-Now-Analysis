from typing import List, Optional
import pandas as pd
import numpy as np
from collections import Counter


# Wining Hand Face Card or Not?
def whfc(data: pd.DataFrame):
    WHFCn = []
    for i in range(len(data)):
        temp = data.iloc[i]
        if len(temp['Turns Involved']) == 3:
            temp_lst = [j for j in ['J', 'Q', 'K', 'A'] if j in str(temp['Hand Winner Cards'])]
            if len(temp_lst) >= 1:
                WHFCn.append(temp_lst)
    return round(len(WHFCn) / len(data), 2) * 100


# Winning Streak
def streak(data: pd.DataFrame):
    dn = data[['Hand Winner']]
    player_lst = list(set(list([i[0] for i in dn['Hand Winner'] if len(i) > 1])))
    dic = {i: 0 for i in player_lst}

    for i in player_lst:
        conc_lst = []
        count = 0
        for j in range(len(dn)):
            temp = dn.iloc[j].item()
            if len(temp) > 0:
                if i == temp[0]:
                    count = count + 1
                    conc_lst.append(count)
                else:
                    count = 0

        dic[i] = max(conc_lst)

    df = pd.DataFrame(index=dic.keys())
    df['Win Streak'] = dic.values()
    return df


# Does raising signal winner?
def drsw(data: pd.DataFrame):
    dn = data[['Hand Winner', 'Pre Flop Raises', 'Post Flop Raises', 'Post Turn Raises', 'Post River Raises']]
    count_dic = {'Pre Flop Raises': 0, 'Post Flop Raises': 0, 'Post Turn Raises': 0, 'Post River Raises': 0}
    count_dic_occur = {'Pre Flop Raises': 0, 'Post Flop Raises': 0, 'Post Turn Raises': 0, 'Post River Raises': 0}
    for i in range(len(dn)):
        temp = dn.iloc[i]
        for j in ['Pre Flop Raises', 'Post Flop Raises', 'Post Turn Raises', 'Post River Raises']:
            if len(temp[j]) > 1:
                if temp['Hand Winner'][0] == temp[j][0]:
                    count_dic[j] += 1

                count_dic_occur[j] += 1

    final = {}
    for i in ['Pre Flop Raises', 'Post Flop Raises', 'Post Turn Raises', 'Post River Raises']:
        final[i + ' %'] = round(count_dic[i] / count_dic_occur[i], 2) * 100

    return final


# Dealer or big blind winning
def dealer_small_big(data: pd.DataFrame):
    dn = data[['Dealer', 'Small Blind', 'Big Blind', 'Hand Winner']]
    dic = {'Dealer': 0, 'Small Blind': 0, 'Big Blind': 0}
    d_lst = list(dn['Hand Winner'])

    for i, j in enumerate(d_lst):
        temp = dn.iloc[i]
        if len(j) > 1:
            for k in ['Dealer', 'Small Blind', 'Big Blind']:
                if len(temp[k]) > 1:
                    if k != 'Dealer':
                        if temp[3][0] == temp[k][0]:
                            dic[k] += 1

                    else:
                        if temp[3][0] == temp[k]:
                            dic[k] += 1

    vals = np.multiply(np.divide([*dic.values()], len(d_lst)), 100).astype(int)

    final = {}
    for i, j in enumerate(['Dealer', 'Small Blind', 'Big Blind']):
        final[j] = vals[i]

    return final


# Get the best cards
def winning_cards(data: pd.DataFrame, count=52):
    dn = data[['Hand Winner Cards', 'Flop Cards', 'Turn Card', 'River Card', 'Showed', 'Hand Winner', 'Turns Involved']]
    card_lst = []
    winner_lst = list(dn['Hand Winner'])
    for i, j in enumerate(winner_lst):
        if len(j) > 1:
            showed_lst = dn['Showed'].iloc[i]
            winner = j[0]
            winner_cards = dn['Hand Winner Cards'].iloc[i]

            if len(winner_cards) > 1:
                winner_cards = [card for card in winner_cards[2:][0].split(',')]
                winner_cards = [i.strip().split(" ")[0] + ' Spades' if 'Spades\xa0' in i else i.strip() for i in
                                winner_cards]

            table_cards_lst = list(dn['Flop Cards'].iloc[i])
            if type(dn['Turn Card']) != tuple:
                table_cards_lst.append(dn['Turn Card'].iloc[i])

            if type(dn['River Card']) != tuple:
                table_cards_lst.append(dn['River Card'].iloc[i])

            table_cards_lst = [i.split(" ")[0] + ' Spades' if 'Spades\xa0' in i else i for i in table_cards_lst]

            winner_cards_lst = []
            if len(winner_cards) > 1:
                for card in winner_cards:
                    if card not in table_cards_lst:
                        winner_cards_lst.append(card)

            if len(showed_lst) > 1:
                for player in showed_lst:
                    if winner in player:
                        player_cards = [card for card in player[1:][0].split(',')]
                        player_cards = [i.strip().split(" ")[0] + ' Spades' if 'Spades\xa0' in i else i.strip() for i in
                                        player_cards]
                        winner_cards_lst = player_cards
                        break

            card_lst.append(winner_cards_lst)

    c = Counter(sum(card_lst, []))
    df = pd.DataFrame(index=c.keys())
    df['Counts'] = c.values()
    dfn = df.sort_values('Counts', ascending=False)

    return dfn.nlargest(count, 'Counts')


def win_count(data: pd.DataFrame):
    players = []
    for i, j in enumerate(data['Hand Winner']):
        temp = data['Hand Winner'].iloc[i]
        if len(temp) > 1:
            players.append(temp[0])

    win_count = {i: 0 for i in set(players)}
    for i, j in enumerate(data['Hand Winner']):
        temp = data['Hand Winner'].iloc[i]
        if len(temp) > 1:
            win_count[temp[0]] += 1
    return win_count
