import pandas as pd
import numpy as np
from os import walk
import matplotlib.pyplot as plt
from poker.classes import Poker
from poker.plot import Line, Scatter, Histogram
from poker.analysis import face_card_in_winning_cards, longest_streak, raise_signal_winning, small_or_big_blind_win, best_cards, player_verse_player_reaction
from poker.base import normalize, running_mean, cumulative_mean, round_to
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

    poker
