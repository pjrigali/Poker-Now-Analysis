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
from poker.analysis import player_verse_player, bluff_study, ts_analysis, static_analysis, pressure_or_hold
from poker.base import normalize, running_mean, cumulative_mean, round_to, native_mean, native_mode, unique_values
from poker.base import running_std, calc_gini, search_dic_values, flatten, native_median, standardize
from poker.base import native_variance, native_std, native_sum, native_max
from poker.document_filter_class import DocumentFilter
from poker.time_series_class import TSanalysis
import time
pd.set_option('use_inf_as_na', True)


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

    # doc_filter = DocumentFilter(data=poker, player_index_lst=['DZy-22KNBS', 'mQWfGaGPXE'])
    # fcw = face_card_in_winning_cards(data=DocumentFilter(data=poker, class_lst=['Player Stacks', 'Wins']))
    # ls = longest_streak(data=DocumentFilter(data=poker, class_lst=['Wins']))
    # rsw = raise_signal_winning(data=DocumentFilter(data=poker, class_lst=['Raises']))
    # sbw = small_or_big_blind_win(data=DocumentFilter(data=poker, class_lst=['Small Blind', 'Big Blind']))
    # pvp = player_verse_player(data=DocumentFilter(data=poker, class_lst=['Calls', 'Raises', 'Checks', 'Folds']))
    # bs = bluff_study(data=DocumentFilter(data=poker, player_index_lst=['DZy-22KNBS']), position_lst=['Post Turn', 'Post River'])
    # sa = static_analysis(data=DocumentFilter(data=poker, player_index_lst=['DZy-22KNBS']))
    # ph = pressure_or_hold(data=DocumentFilter(data=poker, player_index_lst=['DZy-22KNBS']), bet=500, position='Pre Flop')
    # ts = ts_analysis(data=DocumentFilter(data=poker, player_index_lst=['DZy-22KNBS']))
    # ts = TSanalysis(data=DocumentFilter(data=poker, player_index_lst=['DZy-22KNBS']))

    # player_index_lst = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'], ['mQWfGaGPXE'], ['HiZcYKvbcw']]
    # temp = NNClassifier(poker=poker, player_index_lst=player_index_lst, y_variable='win', random_selection=False)

    poker

    # flynn_data = DocumentFilter(data=poker, player_index_lst=['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'])
    # peter_data = DocumentFilter(data=poker, player_index_lst=['mQWfGaGPXE'])
    # henry_data = DocumentFilter(data=poker, player_index_lst=['HiZcYKvbcw'])
    #
    # ts_flynn = TSanalysis(data=flynn_data)
    # ts_peter = TSanalysis(data=peter_data)
    # ts_henry = TSanalysis(data=henry_data)
    #
    # flynn_lst = [ts_flynn.ts_class_median, ts_flynn.ts_class_lower_quantile, ts_flynn.ts_class_upper_quantile,
    #              ts_flynn.ts_position_median, ts_flynn.ts_position_lower_quantile, ts_flynn.ts_position_upper_quantile]
    # flynn_df = pd.DataFrame()
    # for item in flynn_lst:
    #     for col in item.columns:
    #         if col not in ['Game Id', 'index', 'Start Time', 'Win', 'Fold Next']:
    #             flynn_df[col] = standardize(data=item[col])
    #
    # peter_lst = [ts_peter.ts_class_median, ts_peter.ts_class_lower_quantile, ts_peter.ts_class_upper_quantile,
    #              ts_peter.ts_position_median, ts_peter.ts_position_lower_quantile, ts_peter.ts_position_upper_quantile]
    # peter_df = pd.DataFrame()
    # for item in peter_lst:
    #     for col in item.columns:
    #         if col not in ['Game Id', 'index', 'Start Time', 'Win', 'Fold Next']:
    #             peter_df[col] = standardize(data=item[col])
    #
    # henry_lst = [ts_henry.ts_class_median, ts_henry.ts_class_lower_quantile, ts_henry.ts_class_upper_quantile,
    #              ts_henry.ts_position_median, ts_henry.ts_position_lower_quantile, ts_henry.ts_position_upper_quantile]
    # henry_df = pd.DataFrame()
    # for item in henry_lst:
    #     for col in item.columns:
    #         if col not in ['Game Id', 'index', 'Start Time', 'Win', 'Fold Next']:
    #             henry_df[col] = standardize(data=item[col])

    # Randomly select
    # import secrets
    #
    # p_len = len(peter_df)
    # f_len = len(flynn_df)
    # h_len = len(henry_df)
    # min_len = min([p_len, f_len, h_len])
    #
    # if f_len != min_len:
    #     choice_dic = {}
    #     count = 0
    #     while count < min_len:
    #         val = secrets.choice(range(f_len))
    #         if val not in choice_dic:
    #             choice_dic[val] = True
    #             count += 1
    # uv_ind = unique_values(data=list(choice_dic.keys()), count=True)

    # p_len = len(peter_df)
    # f_len = len(flynn_df)
    # h_len = len(henry_df)
    # min_len = min([p_len, f_len, h_len])
    # whole_df = pd.concat([flynn_df[:min_len], peter_df[:min_len], henry_df[:min_len]])
    # whole_df = pd.concat([flynn_df, peter_df, henry_df]).reset_index(drop=True)
    # y_lst = ts_flynn.ts_class_median['Win'].tolist()[:min_len] + ts_peter.ts_class_median['Win'].tolist()[:min_len] + ts_henry.ts_class_median['Win'].tolist()[:min_len]
    # y_lst = ts_flynn.ts_class_median['Win'].tolist() + ts_peter.ts_class_median['Win'].tolist() + ts_henry.ts_class_median['Win'].tolist()
    # y_lst = ts_flynn.ts_class_median['Fold Next'].tolist() + ts_peter.ts_class_median['Fold Next'].tolist() + ts_henry.ts_class_median['Fold Next'].tolist()
    # y_lst = [0.0] * min_len + [1.0] * min_len + [2.0] * min_len

    # from sklearn.neural_network import MLPClassifier
    # from sklearn.model_selection import train_test_split
    #
    # x_train, x_test, y_train, y_test = train_test_split(whole_df, y_lst, test_size=0.20, random_state=1)
    # clf = MLPClassifier(solver='adam', alpha=0.01, hidden_layer_sizes=(52,), random_state=1, activation='logistic',
    #                     learning_rate='adaptive', max_iter=1000, batch_size=50, learning_rate_init=.001)
    #
    # clf.fit(x_train, y_train)
    # pred_act = clf.predict(x_test)
    # pred_prob = clf.predict_proba(x_test)
    # acc_df = pd.DataFrame(pred_act, columns=['Predicted'])
    # acc_df['Actual'] = y_test
    # acc_df['Predicted Loss Prob'] = pred_prob[:, 0]
    # acc_df['Predicted Win Prob'] = pred_prob[:, 1]
    # acc = clf.score(x_test, y_test)
    # t = [whole_df.columns[22]] + [whole_df.columns[27]] + [whole_df.columns[28]] + [whole_df.columns[29]] + [
    #     whole_df.columns[35]] + [whole_df.columns[41]] + [whole_df.columns[42]]

    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch.utils.data import Dataset, DataLoader
    from sklearn.metrics import accuracy_score, classification_report
    torch.manual_seed(1)
    np.random.seed(1)
    peter_data = DocumentFilter(data=poker, player_index_lst=['mQWfGaGPXE'])
    ts_peter = TSanalysis(data=peter_data)
    peter_lst = [ts_peter.ts_class_median, ts_peter.ts_class_lower_quantile, ts_peter.ts_class_upper_quantile,
                 ts_peter.ts_position_median, ts_peter.ts_position_lower_quantile, ts_peter.ts_position_upper_quantile]
    peter_df = pd.DataFrame()
    for item in peter_lst:
        for col in item.columns:
            if col not in ['Game Id', 'index', 'Start Time', 'Win', 'Fold Next']:
                # peter_df[col] = standardize(data=item[col], keep_nan=0.0)
                peter_df[col] = item[col]

    from sklearn.model_selection import train_test_split
    y_lst = ts_peter.ts_class_median['Win'].tolist()
    x_train, x_test, y_train, y_test = train_test_split(np.array(peter_df), np.array(y_lst), test_size=0.20, random_state=1)

    X_train = torch.from_numpy(x_train.to_numpy()).float()
    y_train = torch.squeeze(torch.from_numpy(y_train.to_numpy()).float())
    X_test = torch.from_numpy(x_test.to_numpy()).float()
    y_test = torch.squeeze(torch.from_numpy(y_test.to_numpy()).float())
    # x_train = x_train.reshape(-1, x_train.shape[1]).astype('float32')
    # x_test = x_test.reshape(-1, x_test.shape[1]).astype('float32')
    # x_train.shape, y_train.shape, x_test.shape, y_test.shape
    # x_test = torch.from_numpy(x_test)
    # y_test = torch.from_numpy(y_test)

    class Data(Dataset):
        def __init__(self, x_data, y_data):
            self.x = torch.tensor(x_data, dtype=torch.float32)
            self.y = torch.tensor(y_data, dtype=torch.float32)
            self.len = self.x.shape[0]

        def __getitem__(self, index):
            return self.x[index], self.y[index]

        def __len__(self):
            return self.len

    train_set = Data(x_data=x_train, y_data=y_train)
    test_set = Data(x_data=x_test, y_data=y_test)
    trainloader = DataLoader(dataset=train_set, batch_size=50, shuffle=False)
    testloader = DataLoader(dataset=test_set, batch_size=50)

    input_dim = x_train.shape[1]  # how many Variables are in the dataset
    hidden_dim = 3  # hidden layers
    output_dim = 2

    class Net(torch.nn.Module):
        def __init__(self, input_shape):
            super().__init__()
            self.hid1 = torch.nn.Linear(input_shape, input_shape * 2)
            self.hid2 = torch.nn.Linear(input_shape * 2, input_shape * 2)
            self.oupt = torch.nn.Linear(input_shape * 2, 1)

            torch.nn.init.xavier_uniform_(self.hid1.weight)
            torch.nn.init.zeros_(self.hid1.bias)
            torch.nn.init.xavier_uniform_(self.hid2.weight)
            torch.nn.init.zeros_(self.hid2.bias)
            torch.nn.init.xavier_uniform_(self.oupt.weight)
            torch.nn.init.zeros_(self.oupt.bias)

        def forward(self, x):
            z = torch.relu(self.hid1(x))
            z = torch.relu(self.hid2(z))
            z = torch.sigmoid(self.oupt(z))
            return z

    # torch.cuda.get_device_name(0)
    # device = torch.device("cuda")
    # net = Net().to(device)
    net = Net(input_shape=input_dim)
    # criterion = nn.CrossEntropyLoss()
    n_epochs = 100
    learning_rate = 0.01
    criterion = nn.BCELoss()
    # optimizer = torch.optim.Adam(net.parameters(), lr=learning_rate)
    optimizer = torch.optim.SGD(net.parameters(), lr=learning_rate)


