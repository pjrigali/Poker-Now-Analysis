from typing import Union
import pandas as pd
import numpy as np
from poker.processor import Wins
from poker.classes import Game, Player
from poker.base import round_to, flatten, unique_values, running_mean, running_std, native_std, native_mean
# from poker.base import normalize
# import matplotlib.pyplot as plt


# Wining Hand Face Card or Not?
def face_card_in_winning_cards(data: Union[Game, Player]) -> dict:
    """

    Find what percent of the time a face card is used to win.

    :param data: Input data.
    :type data: Union[Game or Player]
    :return: A dict of file_id and face card in winning hand percent.
    :rtype: dict
    :example: *None*
    :note: Percent of all Winning Cards = Total all cards and get percent that include a face card.
        Percent one face in Winning Cards = Percent of all wins hand at least a single face card.

    """
    if type(data) == Player:
        datan = data.line_dic
        player = data.player_index
    elif type(data) == Game:
        datan = {data.file_name: flatten(data=[i.parsed_hand for i in data.hands_lst], type_used='class objects')}
        player = [None]
    else:
        raise AttributeError('Pass Game or Player Object in for data.')

    final_dic = {}
    for key, val in datan.items():
        final_dic[key] = {'Percent of all Winning Cards': 0.0, 'Percent one face in Winning Cards': 0.0}
        win_tally, win_face_tally, win_face_one_count, win_nonface_tally = 0, 0, 0, 0
        for line in val:
            if type(line) == Wins:
                if type(data) == Player:
                    for winner in line.winner:
                        if winner in player:
                            win_tally += 1
                            break
                else:
                    win_tally += 1

                if line.cards is not None:
                    for card in line.cards:
                        if card.split(' ')[0] in ['J', 'Q', 'K', 'A']:
                            win_face_tally += 1
                        else:
                            win_nonface_tally += 1
                    for card in line.cards:
                        if card.split(' ')[0] in ['J', 'Q', 'K', 'A']:
                            win_face_one_count += 1
                            break

        if win_face_tally != 0:
            temp_tally = win_nonface_tally + win_face_tally
            final_dic[key]['Percent of all Winning Cards'] = round_to(data=win_face_tally / temp_tally, val=1000,
                                                                      remainder=True)
        if win_tally != 0:
            final_dic[key]['Percent one face in Winning Cards'] = round_to(data=win_face_one_count / win_tally,
                                                                           val=1000, remainder=True)
    return final_dic


# Winning Streak
def longest_streak(data: Union[Game, Player]) -> dict:
    """

    Find the longest winning streak.

    :param data: Input data.
    :type data: Union[Game, Player]
    :return: Longest streak.
    :rtype: dict
    :example: *None*
    :note: *None*

    """
    if type(data) == Player:
        datan = {}
        for key, val in data.moves_dic.items():
            datan[key] = {}
            for play in data.player_index:
                datan[key][play] = val
    elif type(data) == Game:
        datan = {data.file_name: {}}
        for ind, player in data.players_data.items():
            for key, val in player.moves_dic.items():
                if key == data.file_name:
                    datan[key][player.player_index[0]] = val
    else:
        raise AttributeError('Pass Game or Player Object in for data.')

    final_dic = {}
    for key, val in datan.items():
        final_dic[key] = {}
        for key1, val1 in val.items():
            temp_df = val1.drop_duplicates('Round', keep='last').reset_index(drop=True)
            count, temp_count = [], 0
            for ind, row in temp_df.iterrows():
                if ind >= 1:
                    prev = temp_df.iloc[ind - 1]['Winner']
                    temp_val = False
                    for winner in row['Winner']:
                        if winner in prev:
                            temp_val = True
                            break
                    if temp_val is True:
                        temp_count += 1
                    else:
                        count.append(temp_count)
                        temp_count = 0
            final_dic[key][key1] = max(count)
    return final_dic


# Does raising signal winner?
def raise_signal_winning(data: Union[Game, Player]) -> pd.DataFrame:
    """

    When a player raises, does that mean they are going to win(?).

    :param data: Input data.
    :type data: Union[Game, Player]
    :return: A pd.DataFrame with the percent related to each position.
    :rtype: pd.DataFrame
    :example: *None*
    :note: *None*

    """
    if type(data) == Player:
        datan = {}
        for key, val in data.moves_dic.items():
            datan[key] = {}
            for play in data.player_index:
                datan[key][play] = val
    elif type(data) == Game:
        datan = {data.file_name: {}}
        for ind, player in data.players_data.items():
            for key, val in player.moves_dic.items():
                if key == data.file_name:
                    datan[key][player.player_index[0]] = val
    else:
        raise AttributeError('Pass Game or Player Object in for data.')

    pos_lst = ['Pre Flop', 'Post Flop', 'Post Turn', 'Post River']
    dic = {}
    for key, val in datan.items():
        for key1, val1 in val.items():
            if key1 not in dic.keys():
                dic[key1] = []
            dic[key1].append(val1)

    final_dic = {key: pd.concat(val, axis=0).reset_index(drop=True) for key, val in dic.items()}
    result_dic = {}
    for key, val in final_dic.items():
        val['Win Temp'] = ['Win' if i is True else 'Loss' for i in val['Win']]
        temp_lst = val['Win Temp'] + '_splitpoint_' + val['Position'] + '_splitpoint_' + val['Class']
        temp_dic = {wl: {pos: [] for pos in pos_lst} for wl in ['Win', 'Loss']}
        for ind, item in enumerate(temp_lst):
            for wl in ['Win', 'Loss']:
                for pos in pos_lst:
                    if wl in item and pos in item and 'Raises' in item:
                        temp_dic[wl][pos].append(1)

        person_dic = {}
        for pos in pos_lst:
            if len(temp_dic['Win'][pos]) >= 1:
                temp_val = sum(temp_dic['Win'][pos]) / (sum(temp_dic['Win'][pos]) + sum(temp_dic['Loss'][pos]))
            else:
                temp_val = 0.0
            person_dic[pos] = round_to(data=temp_val, val=1000, remainder=True)
        result_dic[key] = person_dic
    return pd.DataFrame.from_dict(result_dic)


# Dealer or big blind winning
def small_or_big_blind_win(data: Union[Game, Player]) -> pd.DataFrame:
    """

    When a player is small or big blind, does that mean they are going to win(?).

    :param data: Input data.
    :type data: Union[Game, Player]
    :return: A pd.DataFrame with the percent related to each blind.
    :rtype: pd.DataFrame
    :example: *None*
    :note: *None*

    """
    if type(data) == Player:
        datan = {}
        for key, val in data.moves_dic.items():
            datan[key] = {}
            for play in data.player_index:
                datan[key][play] = val
    elif type(data) == Game:
        datan = {data.file_name: {}}
        for ind, player in data.players_data.items():
            for key, val in player.moves_dic.items():
                if key == data.file_name:
                    datan[key][player.player_index[0]] = val
    else:
        raise AttributeError('Pass Game or Player Object in for data.')

    mov_lst = ['Small Blind', 'Big Blind']
    dic = {}
    for key, val in datan.items():
        for key1, val1 in val.items():
            if key1 not in dic.keys():
                dic[key1] = []
            dic[key1].append(val1)

    final_dic = {key: pd.concat(val, axis=0).reset_index(drop=True) for key, val in dic.items()}
    result_dic = {}
    for key, val in final_dic.items():
        val['Win Temp'] = ['Win' if i is True else 'Loss' for i in val['Win']]
        temp_lst = val['Win Temp'] + '_splitpoint_' + val['Class']
        temp_dic = {wl: {mov: [] for mov in mov_lst} for wl in ['Win', 'Loss']}
        for ind, item in enumerate(temp_lst):
            for wl in ['Win', 'Loss']:
                for mov in mov_lst:
                    if wl in item and mov in item:
                        temp_dic[wl][mov].append(1)

        person_dic = {}
        for mov in mov_lst:
            if len(temp_dic['Win'][mov]) >= 1:
                temp_val = sum(temp_dic['Win'][mov]) / (sum(temp_dic['Win'][mov]) + sum(temp_dic['Loss'][mov]))
            else:
                temp_val = 0.0
            person_dic[mov] = round_to(data=temp_val, val=1000, remainder=True)
        result_dic[key] = person_dic
    return pd.DataFrame.from_dict(result_dic)


def player_verse_player(data: Union[Game, Player]) -> dict:
    """

    Find how many times and what value a player called or folded related all other players.

    :param data: Input data.
    :type data: Union[Game, Player]
    :return: A dict of counts and values for each 'Calls', 'Raises', 'Checks', and 'Folds'.
    :rtype: dict
    :example: *None*
    :note: *None*

    """
    if type(data) == Player:
        datan = {}
        for key, val in data.moves_dic.items():
            datan[key] = {}
            for play in data.player_index:
                datan[key][play] = val
    elif type(data) == Game:
        datan = {data.file_name: {}}
        for ind, player in data.players_data.items():
            for key, val in player.moves_dic.items():
                if key == data.file_name:
                    datan[key][player.player_index[0]] = val
    else:
        raise AttributeError('Pass Game or Player Object in for data.')

    mov_lst = ['Calls', 'Raises', 'Checks', 'Folds']
    dic = {}
    for key, val in datan.items():
        for key1, val1 in val.items():
            if key1 not in dic.keys():
                dic[key1] = []
            dic[key1].append(val1)

    final_dic = {key: pd.concat(val, axis=0).reset_index(drop=True) for key, val in dic.items()}
    result_dic = {}
    for key, val in final_dic.items():
        names_lst = unique_values(data=val['From Person'].dropna())
        val['Temp Bet Amount'] = [str(i) if type(i) == int else '0' for i in val['Bet Amount']]
        val['Temp From Person'] = [str(i) if i == i else '0' for i in val['From Person'] if i == i]
        temp_lst = val['Temp From Person'] + '_splitpoint_' + val['Class'] + '_splitpoint_' + val['Temp Bet Amount']
        temp_dic = {nam: {mov: [] for mov in mov_lst} for nam in names_lst}
        for ind, item in enumerate(temp_lst):
            for nam in names_lst:
                for mov in mov_lst:
                    if nam in item and mov in item:
                        temp_dic[nam][mov].append(int(item.split('_splitpoint_')[2]))

        person_dic = {name: {mov: {'Count': 0, 'Values': []} for mov in mov_lst} for name in names_lst}
        for nam in names_lst:
            for mov in mov_lst:
                if len(temp_dic[nam][mov]) >= 1:
                    person_dic[nam][mov]['Count'] = len(temp_dic[nam][mov])
                    person_dic[nam][mov]['Values'] = int(round_to(data=native_mean(data=temp_dic[nam][mov]), val=10))
                else:
                    person_dic[nam][mov]['Count'] = 0
                    person_dic[nam][mov]['Values'] = 0
        col_lst = flatten(data=[[person + ' Count', person + ' Value'] for person in person_dic.keys()],
                          type_used='str')
        temp_df = pd.DataFrame(index=mov_lst, columns=col_lst)
        for key1, val1 in person_dic.items():
            for key2, val2 in val1.items():
                temp_df.loc[key2][key1 + ' Count'] = val2['Count']
                temp_df.loc[key2][key1 + ' Value'] = val2['Values']
        result_dic[key] = temp_df
    return result_dic


def bluff_study(data: Player) -> dict:
    """

    Compare betting habits when a player is bluffing.

    :param data: Input data.
    :type data: Player
    :return: A dict of counts and values for each position.
    :rtype: dict
    :example: *None*
    :note: Bluff Count Raises and Calls = Average and std count per position when bluffing.
        Bluff Stack = Average and std value per position when bluffing.
        Bluff Stack Raises and Calls = Average and std value for Raises and Calls when bluffing.
        Both = Average and std when they win and loss.
        Loss = Average and std when they loss.
        Win = Average and std when they Win.

    """
    data = data.moves_dic
    pos_lst = ['Pre Flop', 'Post Flop', 'Post Turn', 'Post River']
    awin_dic, aloss_dic, aboth_dic = {}, {}, {}
    for key, val in data.items():
        for key1, val1 in val[val['Win'] == True].to_dict(orient='list').items():
            if key1 in awin_dic.keys():
                awin_dic[key1] += val1
            else:
                awin_dic[key1] = val1

        for key1, val1 in val[val['Win'] == False].to_dict(orient='list').items():
            if key1 in aloss_dic.keys():
                aloss_dic[key1] += val1
            else:
                aloss_dic[key1] = val1

        for key1, val1 in val.to_dict(orient='list').items():
            if key1 in aboth_dic.keys():
                aboth_dic[key1] += val1
            else:
                aboth_dic[key1] = val1

    win_loss_dic = {'Win': pd.DataFrame.from_dict(awin_dic),
                    'Loss': pd.DataFrame.from_dict(aloss_dic),
                    'Both': pd.DataFrame.from_dict(aboth_dic)}

    for key, val in win_loss_dic.items():
        win_loss_dic[key]['Game_Round_ID'] = val['Game Id'] + '_splitpoint_' + [str(i) for i in val['Round']]

    # Win, Loss, and Both
    result_dic = {}
    for key in win_loss_dic.keys():
        middle = win_loss_dic[key]
        temp_middle = middle[(middle['All In'] == False) & (middle['Class'] == 'Calls') | (middle['Class'] == 'Raises')]
        middle_result_dic = {j: [] for j in pos_lst}
        middle_mean_dic = {j: 0 for j in pos_lst}
        middle_std_dic = {j: 0 for j in pos_lst}
        for position in pos_lst:
            temp_df = temp_middle[temp_middle['Position'] == position]
            temp_lst = temp_df['Game_Round_ID'].unique()
            for row in temp_lst:
                t = temp_df[temp_df['Game_Round_ID'] == row]['Bet Amount']
                middle_result_dic[position].append(np.sum(np.nan_to_num(list(t))))

        for j in pos_lst:
            middle_mean_dic[j] = round_to(data=int(np.mean(middle_result_dic[j])), val=25)
            middle_std_dic[j] = round_to(data=int(np.std(middle_result_dic[j])), val=25)

        result_dic[key] = {'Mu': middle_mean_dic, 'Std': middle_std_dic, 'Result': middle_result_dic}

    # Cancel Bluff
    loss = win_loss_dic['Loss']
    temp_loss = loss[(loss['Position'] == 'Post River') & (loss['Class'] == 'Folds')]
    both = win_loss_dic['Both']
    both_temp = both[(both['Class'] == 'Calls') | (both['Class'] == 'Raises')]
    row_lst = [temp_loss.iloc[i]['Game_Round_ID'] for i, j in enumerate(temp_loss['Bet Amount'])]

    class_lst = ['Raises', 'Calls']
    pos_lst = ['Pre Flop', 'Post Flop', 'Post Turn', 'Post River']
    compare_dic = {j: [] for j in pos_lst}
    compare_dic_mean = {j: 0 for j in pos_lst}
    compare_dic_std = {j: 0 for j in pos_lst}
    for position in pos_lst:
        temp_df = both_temp[both_temp['Position'] == position]
        for row in row_lst:
            t = temp_df[temp_df['Game_Round_ID'] == row]['Bet Amount']
            compare_dic[position].append(np.sum(np.nan_to_num(list(t))))

    for j in pos_lst:
        compare_dic_mean[j] = round_to(data=int(np.mean(compare_dic[j])), val=25)
        compare_dic_std[j] = round_to(data=int(np.std(compare_dic[j])), val=25)

    result_dic['Bluff Stack'] = {'Mu': compare_dic_mean, 'Std': compare_dic_std, 'Result': compare_dic}

    compare_dic = {j: {k: [] for k in class_lst} for j in pos_lst}
    compare_dic_mean = {j: {k: [] for k in class_lst} for j in pos_lst}
    compare_dic_std = {j: {k: [] for k in class_lst} for j in pos_lst}
    for pos in pos_lst:
        temp_df = both_temp[both_temp['Position'] == pos]
        for cl in class_lst:
            temp_lst = []
            temp_df2 = temp_df[temp_df['Class'] == cl]
            for row in row_lst:
                temp_lst += list(temp_df2[temp_df2['Game_Round_ID'] == row]['Bet Amount'])
            compare_dic[pos][cl] = temp_lst

    for j in pos_lst:
        for k in class_lst:
            if len(compare_dic[j][k]) > 0.0:
                compare_dic_mean[j][k] = round_to(data=int(np.mean(np.nan_to_num(compare_dic[j][k]))), val=25)
                compare_dic_std[j][k] = round_to(data=int(np.std(np.nan_to_num(compare_dic[j][k]))), val=25)
            else:
                compare_dic_mean[j][k] = 0
                compare_dic_std[j][k] = 0

    result_dic['Bluff Stack Raises and Calls'] = {'Mu': compare_dic_mean, 'Std': compare_dic_std, 'Result': compare_dic}

    compare_dic = {j: {k: [] for k in class_lst} for j in pos_lst}
    compare_dic_mean = {j: {k: [] for k in class_lst} for j in pos_lst}
    compare_dic_std = {j: {k: [] for k in class_lst} for j in pos_lst}
    for pos in pos_lst:
        temp_df = both_temp[both_temp['Position'] == pos]
        for cl in class_lst:
            temp_lst = []
            temp_df2 = temp_df[temp_df['Class'] == cl]
            for row in row_lst:
                temp_lst.append(len(temp_df2[temp_df2['Game_Round_ID'] == row]))
            compare_dic[pos][cl] = temp_lst

    for j in pos_lst:
        for k in class_lst:
            compare_dic_mean[j][k] = round_to(data=float(np.mean(np.nan_to_num(compare_dic[j][k]))), val=1000,
                                              remainder=True)
            compare_dic_std[j][k] = round_to(data=float(np.std(np.nan_to_num(compare_dic[j][k]))), val=1000,
                                             remainder=True)

    result_dic['Bluff Count Raises and Calls'] = {'Mu': compare_dic_mean, 'Std': compare_dic_std, 'Result': compare_dic}
    return result_dic
    # import matplotlib.pyplot as plt
    # import pandas as pd
    #
    # for j in pos_lst:
    #     fig, ax = plt.subplots(figsize=(10, 7))
    #     m = np.array(middle_result_dic[j])[np.where(np.array(middle_result_dic[j]) > 50)]
    #     w = np.array(win_result_dic[j])[np.where(np.array(win_result_dic[j]) > 50)]
    #     l = np.array(loss_result_dic[j])[np.where(np.array(loss_result_dic[j]) > 50)]
    #     plt.title(j, fontsize='xx-large')
    #     plt.hist(m, label=j + ' Middle', alpha=.5, color='tab:blue')
    #     plt.hist(w, label=j + ' Win', alpha=.5, color='tab:orange')
    #     plt.hist(l, label=j + ' Loss', alpha=.5, color='tab:green')
    #     plt.vlines(np.mean(m), 0, 175, label='Middle Mu', color='tab:blue')
    #     plt.vlines(np.mean(w), 0, 175, label='Win Mu', color='tab:orange')
    #     plt.vlines(np.mean(l), 0, 175, label='loss Mu', color='tab:green')
    #     plt.vlines(np.median(m), 0, 175, label='Middle Median', color='tab:blue', linestyles=':')
    #     plt.vlines(np.median(w), 0, 175, label='Win Median', color='tab:orange', linestyles=':')
    #     plt.vlines(np.median(l), 0, 175, label='loss Median', color='tab:green', linestyles=':')
    #     plt.vlines(mode(round_to(m, 50)), 0, 175, label='Middle Mode', color='tab:blue', linestyles='--')
    #     plt.vlines(mode(round_to(w, 50)), 0, 175, label='Win Mode', color='tab:orange', linestyles='--')
    #     plt.vlines(mode(round_to(l, 50)), 0, 175, label='loss Mode', color='tab:green', linestyles='--')
    #     plt.legend()
    #     plt.show()


def staticanalysis(data: Union[Player, dict]) -> pd.DataFrame:
    """

    Build a static analysis DataFrame.

    :param data: A Player class object.
    :type data: Player or Dict
    :return: A DataFrame of mean and std values.
    :rtype: pd.DataFrame
    :example: *None*
    :note: If a dict is passed it is intended to be Player.move_dic.

    """
    if type(data) == Player:
        data = data.moves_dic
    elif type(data) == dict:
        pass
    else:
        raise AttributeError("Input needs to be a Player object or a Player.mov_dic")

    pos_lst = ['Pre Flop', 'Post Flop', 'Post Turn', 'Post River']
    mov_lst = ['Raises', 'Calls', 'Folds']
    group_lst = ['Win', 'Loss', 'Both']
    dic = {}
    for key, val in data.items():
        for key1, val1 in val.to_dict(orient='list').items():
            if key1 in dic.keys():
                dic[key1] += val1
            else:
                dic[key1] = val1

    ss_data = pd.DataFrame.from_dict(dic)
    ind_dic = {wlb: {pos: {mov: [] for mov in mov_lst} for pos in pos_lst} for wlb in group_lst}
    ss_data['Win String'] = ['Win' if i is True else 'Loss' for i in ss_data['Win']]
    win_lst = (ss_data['Win String']+'_splitpoint_'+ss_data['Position']+'_splitpoint_'+ss_data['Class']).tolist()
    for i, j in enumerate(win_lst):
        for gro in group_lst[:2]:
            for pos in pos_lst:
                for mov in mov_lst:
                    if mov in j and gro in j and pos in j:
                        ind_dic[j.split('_splitpoint_')[0]][j.split('_splitpoint_')[1]][j.split('_splitpoint_')[2]].append(i)
                        ind_dic['Both'][j.split('_splitpoint_')[1]][j.split('_splitpoint_')[2]].append(i)
                        break

    final_dic = {}
    for gro in group_lst:
        temp_dic = {}
        for pos in pos_lst:
            temp_dic[pos] = {}
            for mov in mov_lst:
                temp_dic[pos][mov] = {'Values': [], 'Seconds': []}
        final_dic[gro] = temp_dic

    for gro in group_lst:
        for pos in pos_lst:
            for mov in mov_lst:
                temp_df = ss_data.iloc[ind_dic[gro][pos][mov]]
                new_val = final_dic[gro][pos][mov]
                if temp_df.empty is False:
                    for ind, row in temp_df.iterrows():
                        new_val['Values'].append(row['Bet Amount'])
                        new_val['Seconds'].append((row['Time'] - row['Previous Time']).total_seconds())

    final_lst = []
    for key, val in final_dic.items():
        temp_df = pd.DataFrame(index=[key])
        for pos in pos_lst:
            for mov in mov_lst:
                for item in ['Values', 'Seconds']:
                    vals = val[pos][mov][item]
                    if len(vals) > 1:
                        temp_df[pos + ' ' + mov + ' ' + item + ' mean'] = round_to(data=native_mean(data=vals), val=1)
                        temp_df[pos + ' ' + mov + ' ' + item + ' std'] = round_to(data=native_std(data=vals), val=1)
                    else:
                        temp_df[pos + ' ' + mov + ' ' + item + ' mean'] = 0
                        temp_df[pos + ' ' + mov + ' ' + item + ' std'] = 0
        final_lst.append(temp_df)
    return pd.concat(final_lst).fillna(0)


def tsanalysis(data: Union[Player, dict]) -> pd.DataFrame:
    """

    Build a Time Series DataFrame.

    :param data: A Player class object.
    :type data: Player or Dict
    :return: A DataFrame of various moves over time.
    :rtype: pd.DataFrame
    :example: *None*
    :note: If a dict is passed it is intended to be Player.move_dic.

    """
    if type(data) == Player:
        data = data.moves_dic
    elif type(data) == dict:
        pass
    else:
        raise AttributeError("Input needs to be a Player object or a Player.mov_dic")

    pos_lst = ['Pre Flop', 'Post Flop', 'Post Turn', 'Post River']
    mov_lst = ['Checks', 'Raises', 'Calls', 'Folds']
    dic = {}
    for key, val in data.items():
        for key1, val1 in val.to_dict(orient='list').items():
            if key1 in dic.keys():
                dic[key1] += val1
            else:
                dic[key1] = val1

    ts_data = pd.DataFrame.from_dict(dic)
    ts_data['Game_Round_ID'] = ts_data['Game Id'] + '_splitpoint_' + [str(i) for i in ts_data['Round']]

    final_dic = {}
    for pos in pos_lst:
        temp_dic = {}
        for mov in mov_lst:
            temp_dic[mov] = {'Times': [], 'Values': [], 'Seconds': [], 'Player Reserve': [], 'Game Id': [],
                             'Pot Size': [], 'Win': [], 'Position': [], 'Class': []}
        final_dic[pos] = temp_dic

    ind_dic = {pos: {mov: [] for mov in mov_lst} for pos in pos_lst}
    class_lst = (ts_data['Position'] + '_splitpoint_' + ts_data['Class']).tolist()
    for i, j in enumerate(class_lst):
        for mov in mov_lst:
            if mov in j:
                ind_dic[j.split('_splitpoint_')[0]][j.split('_splitpoint_')[1]].append(i)
                break

    for pos in pos_lst:
        for mov in mov_lst:
            temp_df = ts_data.iloc[ind_dic[pos][mov]]
            new_val = final_dic[pos][mov]
            if temp_df.empty is False:
                for ind, row in temp_df.iterrows():
                    new_val['Values'].append(row['Bet Amount'])
                    new_val['Times'].append(row['Time'])
                    new_val['Seconds'].append((row['Time'] - row['Previous Time']).total_seconds())
                    new_val['Player Reserve'].append(row['Player Reserve'])
                    new_val['Game Id'].append(row['Game Id'])
                    new_val['Pot Size'].append(row['Pot Size'])
                    new_val['Win'].append(row['Win'])
                    new_val['Position'].append(row['Position'])
                    new_val['Class'].append(row['Class'])

    df_lst = []
    for pos in pos_lst:
        for mov in mov_lst:
            temp_df = pd.DataFrame(final_dic[pos][mov]).set_index('Times').sort_index(ascending=True)
            if temp_df.empty is False:
                temp_df['Running Mean Values'] = round_to(data=running_mean(data=temp_df['Values'], num=10), val=1,
                                                          remainder=False)
                temp_df['Running Std Values'] = round_to(data=running_std(data=temp_df['Values'], num=10), val=1,
                                                         remainder=False)
                temp_df['Running Mean Seconds'] = round_to(data=running_mean(data=temp_df['Seconds'], num=10), val=1,
                                                           remainder=False)
                temp_df['Running Std Seconds'] = round_to(data=running_std(data=temp_df['Seconds'], num=10), val=1,
                                                          remainder=False)
                df_lst.append(temp_df)

    final_df = pd.concat(df_lst, axis=0).sort_index(ascending=True)
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
