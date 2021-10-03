import pandas as pd
import numpy as np
from os import walk
import matplotlib.pyplot as plt
from poker.poker_class import Poker
from poker.game_class import Game
from poker.player_class import Player
from poker.hand_class import Hand
from poker.plot import Line, Scatter, Histogram
from poker.analysis import face_card_in_winning_cards, longest_streak, raise_signal_winning, small_or_big_blind_win
from poker.analysis import player_verse_player, bluff_study, tsanalysis, staticanalysis
from poker.base import normalize, running_mean, cumulative_mean, round_to, native_mean, native_mode, unique_values, running_std, calc_gini, search_dic_values, flatten, native_median
from poker.base import native_variance, native_std, native_sum, native_max
import time


if __name__ == '__main__':

    repo = 'C:\\Users\\Peter\\Desktop\\Personal\\11_Repository\\Poker Related\\Data\\'
    grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
               ['1_FRcDzJU-', 'ofZ3AjBJdl', 'yUaYOqMtWh', 'EIxKLHzvif'],
               ['3fuMmmzEQ-', 'LRdO6bTCRh', '9fNOKzXJkb'],
               ['FZayb4wOU1', '66rXA9g5yF', 'rM6qlbc77h', 'fy6-0HLhb_'],
               ['48QVRRsiae', 'u8_FUbXpAz'],
               ['Aeydg8fuEg', 'yoohsUunIZ'],
               ['mUwL4cyOAC', 'zGv-6DI_aJ'],
               ]

    start_timen = time.time()
    poker = Poker(repo_location=repo, grouped=grouped)
    start_timen = "--- %s seconds ---" % round((time.time() - start_timen), 2)
    print(start_timen)

    # full_dic = {}
    # for key, val in poker.players_history.items():
    #     full_dic[key] = pd.DataFrame(val.merged_moves['All'])
    #     full_dic[key]['Game_Id_Round'] = full_dic[key]['Game Id'] + '_splitpoint_' + [str(i) for i in full_dic[key]['Round']]
    #     old_df = full_dic[key].drop_duplicates('Game_Id_Round', keep='first').reset_index()
    #     new_df = full_dic[key].drop_duplicates('Game_Id_Round', keep='last').reset_index()
    #     unique_lst = unique_values(data=full_dic[key]['Game_Id_Round'])
    #
    #     second_dic = {}
    #     for id_rnd in unique_lst:
    #         t = (new_df[new_df['Game_Id_Round'] == id_rnd]['Time'] - old_df[old_df['Game_Id_Round'] == id_rnd][
    #             'Time']).tolist()[0].total_seconds()
    #         second_dic[id_rnd] = t
    #
    #     second_lst = []
    #     for i in full_dic[key]['Game_Id_Round']:
    #         second_lst.append(second_dic[i])
    #     full_dic[key]['Round Seconds'] = second_lst
    #     full_dic[key]['Move Seconds'] = [(row['Time'] - row['Previous Time']).total_seconds() for ind, row in full_dic[key].iterrows()]
    #     full_dic[key]['Win Number'] = [1.0 if i is True else 0.0 for i in full_dic[key]['Win']]
    #
    # for key, val in full_dic.items():
    #     Scatter(data=val,
    #             compare_two=['Round Seconds', 'Player Reserve'],
    #             normalize_x=['Round Seconds', 'Player Reserve'],
    #             color_lst=['tab:orange'],
    #             regression_line=['Player Reserve'],
    #             regression_line_color='tab:blue',
    #             title='Time per Hand vs Player Reserve (Player: ' + key + ')',
    #             ylabel='Player Chip Count',
    #             xlabel='Total Round Seconds')
    #     plt.show()
    #     Histogram(data=val,
    #               label_lst=['Move Seconds'],
    #               include_norm='Move Seconds',
    #               title='Move Second Histogram (Player: ' + key + ')')
    #     plt.show()
    #     Line(data=val[['Pot Size', 'Win Stack']],
    #          normalize_x=['Pot Size', 'Win Stack'],
    #          color_lst=['tab:orange', 'tab:blue'],
    #          title='Pot Size and Winning Stack Amount (Player: ' + key + ')',
    #          ylabel='Value',
    #          xlabel='Date',
    #          corr=['Pot Size', 'Win Stack'])
    #     plt.show()


    # ts_dic = {}
    # for person, val in poker.players_history.items():
    #     try:
    #         ts_dic[person] = tsanalysis(data=val.moves_dic)
    #     except:
    #         pass
    # temp_df = ts_dic['3fuMmmzEQ-'].reset_index()
    # t = pd.DataFrame()
    # for col in ['Running Std Values', 'Player Reserve']:
    #     t[col] = normalize(data=temp_df[col], keep_nan=True)
    # t.plot()
    # plt.show()

    # data_peter = poker.players_history['mQWfGaGPXE'].moves_dic
    # data_peter
    # data_flynn = poker.players_history['DZy-22KNBS'].moves_dic
    # data_henry = poker.players_history['HiZcYKvbcw'].moves_dic
    # data_mike = poker.players_history['yUaYOqMtWh'].moves_dic
    # a = player_habits_compared(data=data_peter)
    # b = player_habits_compared(data=data_flynn)
    # c = player_habits_compared(data=data_henry)
    # d = player_habits_compared(data=data_mike)
    # e = bluff_study(data=poker.players_history['mQWfGaGPXE'])
    # f = bluff_study(data=data_flynn)
    # g = bluff_study(data=data_henry)
    # h = bluff_study(data=data_mike)

    # ts = tsanalysis(data=data_peter)
    # ss = staticanalysis(data=data_peter)
    # fcwc1 = face_card_in_winning_cards(data=poker.players_history['mQWfGaGPXE'])
    # fcwc2 = face_card_in_winning_cards(data=poker.matches[0])
    # ls1 = longest_streak(data=poker.players_history['mQWfGaGPXE'])
    # ls2 = longest_streak(data=poker.matches[1])
    # rsw1 = raise_signal_winning(data=poker.players_history['mQWfGaGPXE'])
    # rsw2 = raise_signal_winning(data=poker.matches[1])
    # sb1 = small_or_big_blind_win(data=poker.players_history['mQWfGaGPXE'])
    # sb2 = small_or_big_blind_win(data=poker.matches[1])
    # pvp1 = player_verse_player(data=poker.players_history['mQWfGaGPXE'])
    # pvp2 = player_verse_player(data=poker.matches[1])
    poker

    # print(''), print('Poker Built'), print("--- %s seconds ---" % round((time.time() - start_timen), 2))

    # temp = poker.matches[9].players['YEtsj6CMK4'].reaction
    # calls = temp[temp['class'] == 'Calls']['stack']
    # folds = temp[temp['class'] == 'Folds']['stack']
    # data = pd.DataFrame(list(folds), columns=['folds'])
    # data['calls'] = list(calls) + [None] * (len(data) - len(calls))
    # Histogram(data=data,
    #           label_lst=['calls', 'folds'],
    #           include_norm='folds',
    #           title='Calls and Folds')
    # plt.show()

    # def calc_slope(x):
    #     slope = np.polyfit(range(len(x)), x, 1)[0]
    #     return slope
    #
    #
    # for key in poker.matches[9].players.keys():
    #     df = poker.matches[9].players[key].reaction
    #     # temp = poker.matches[9].players['YEtsj6CMK4'].reaction
    #     calls = df[df['class'] == 'Calls']['stack']
    #     folds = df[df['class'] == 'Folds']['stack']
    #     res = df['player reserve'].rolling(2).mean()
    #     a = calls.rolling(5).std()
    #     b = folds.rolling(5).std()
    #     try:
    #         c = int(np.median(a.dropna()))
    #         d = int(np.median(b.dropna()))
    #         e = df['player reserve'].rolling(25, min_periods=2).apply(calc_slope).dropna()
    #         a.plot(label='calls ' + str(int(c)))
    #         b.plot(label='folds ' + str(int(d)))
    #         res.plot(label='chips')
    #         # plt.title(str(e))
    #         plt.legend()
    #         plt.show()
    #     except:
    #         pass

    # temp = poker.matches[9].players['YEtsj6CMK4'].reaction.drop_duplicates(keep="first")

    # calls = temp[temp['class'] == 'Calls'].set_index('round')
    # folds = temp[temp['class'] == 'Folds'].set_index('round')
    # raises = temp[temp['class'] == 'Raises'].set_index('round')
    # res = temp['player reserve']
    # res_n1 = normalize(data=np.array(res))
    # r = raises.corr()
    # c = calls.corr()
    # f = folds.corr()
    # rr = raises.rolling(5).std().dropna().corr()
    # cc = calls.rolling(5).std().dropna().corr()
    # ff = folds.rolling(5).std().dropna().corr()

    # cr = (calls['stack'] / res)
    # fr = (folds['stack'] / res).bfill()
    # cr.plot(label='call / res')
    # fr.plot(label='fold / res')
    # res_n.plot(label='chips')
    # plt.xlim(0,200)
    # plt.legend()
    # plt.show()

    # fn = round_to(data=np.array(folds['stack']), val=50)
    # fn = round_to(data=list(cr), val=4, remainder=True)
    # t = round_to(data=[4.3, 5.6], val=4, remainder=False)

    # cw = calls[calls['win'] == True]
    # cl = calls[calls['win'] == False]
    #
    # cws = (cw['stack'] / res).dropna()
    # cls = (cl['stack'] / res).dropna()
    #
    # cws_mu = np.mean(cws[cws < 1])
    # cls_mu = np.mean(cls[cls < 1])
    # cws_std = np.std(cws[cws < 1])
    # cls_std = np.std(cls[cls < 1])
    # Histogram(data=pd.DataFrame(list(cws[cws < 1]), columns=['percent']),
    #           label_lst=['percent'],
    #           include_norm='percent',
    #           title='wins')
    # Histogram(data=pd.DataFrame(list(cls[cls < 1]), columns=['percent']),
    #           label_lst=['percent'],
    #           include_norm='percent',
    #           title='losses')
    # plt.show()

    # t = temp[temp['class'] == "Calls"]
    # tt = round_to(data=t['stack'], val=50, remainder=False)
    # Histogram(data=pd.DataFrame(list(tt[tt < 2000]), columns=['call amount']),
    #           label_lst=['call amount'],
    #           include_norm='call amount',
    #           title='Call Counts')
    # plt.show()

    # t = best_cards(data=poker.matches[9], player_index=['mQWfGaGPXE', '9fNOKzXJkb'])
    # tt = player_verse_player_reaction(data=poker.matches[9])

    # t = player_response(data=poker.players_history['mQWfGaGPXE'], player_reserve_chips=3000, percent_or_stack=False)

# data = poker.players_history['mQWfGaGPXE'].moves_dic
# awin_df = pd.DataFrame()
# aloss_df = pd.DataFrame()
# for key, val in data.items():
#     awin_df = pd.concat([awin_df, val[val['Win'] == True]])
#     aloss_df = pd.concat([aloss_df, val[val['Win'] == False]])
# awin_df = awin_df.reset_index(drop=True)
# aloss_df = aloss_df.reset_index(drop=True)

# compare_dic = {'Win': {'Pre Flop': {}, 'Post Flop': {}, 'Post Turn': {}, 'Post River': {}},
#                'Loss': {'Pre Flop': {}, 'Post Flop': {}, 'Post Turn': {}, 'Post River': {}}}
#
# for pos in ['Pre Flop', 'Post Flop', 'Post Turn', 'Post River']:
#     temp_df = awin_df[awin_df['Position'] == pos]
#     temp_dfn = aloss_df[aloss_df['Position'] == pos]
#     for cl in ['Checks', 'Raises', 'Calls']:
#         temp_lst = []
#         for row in temp_df['Round'].unique():
#             temp_lst.append(len(temp_df[(temp_df['Round'] == row) & (temp_df['Class'] == cl)]))
#         compare_dic['Win'][pos][cl] = temp_lst
#
#     for cl in ['Checks', 'Raises', 'Calls']:
#         temp_lst = []
#         for row in temp_dfn['Round'].unique():
#             temp_lst.append(len(temp_dfn[(temp_dfn['Round'] == row) & (temp_dfn['Class'] == cl)]))
#         compare_dic['Loss'][pos][cl] = temp_lst
#
# compare_dic_mean = {'Win': {'Pre Flop': {'Checks': 0, 'Raises': 0, 'Calls': 0},
#                             'Post Flop': {'Checks': 0, 'Raises': 0, 'Calls': 0},
#                             'Post Turn': {'Checks': 0, 'Raises': 0, 'Calls': 0},
#                             'Post River': {'Checks': 0, 'Raises': 0, 'Calls': 0}},
#                     'Loss': {'Pre Flop': {'Checks': 0, 'Raises': 0, 'Calls': 0},
#                              'Post Flop': {'Checks': 0, 'Raises': 0, 'Calls': 0},
#                              'Post Turn': {'Checks': 0, 'Raises': 0, 'Calls': 0},
#                              'Post River': {'Checks': 0, 'Raises': 0, 'Calls': 0}}}
# compare_dic_std = {'Win': {'Pre Flop': {'Checks': 0, 'Raises': 0, 'Calls': 0},
#                             'Post Flop': {'Checks': 0, 'Raises': 0, 'Calls': 0},
#                             'Post Turn': {'Checks': 0, 'Raises': 0, 'Calls': 0},
#                             'Post River': {'Checks': 0, 'Raises': 0, 'Calls': 0}},
#                     'Loss': {'Pre Flop': {'Checks': 0, 'Raises': 0, 'Calls': 0},
#                              'Post Flop': {'Checks': 0, 'Raises': 0, 'Calls': 0},
#                              'Post Turn': {'Checks': 0, 'Raises': 0, 'Calls': 0},
#                              'Post River': {'Checks': 0, 'Raises': 0, 'Calls': 0}}}
#
# for i in ['Win', 'Loss']:
#     for j in ['Pre Flop', 'Post Flop', 'Post Turn', 'Post River']:
#         for k in ['Checks', 'Raises', 'Calls']:
#             compare_dic_mean[i][j][k] = round(np.mean(compare_dic[i][j][k]), 2)
#             compare_dic_std[i][j][k] = round(np.std(compare_dic[i][j][k]), 2)