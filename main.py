import pandas as pd
import numpy as np
from os import walk
from poker.processor import Classifier
from poker.base import Poker
from poker.analysis import whfc, streak, drsw, dealer_small_big, winning_cards, win_count
import time
pd.set_option('display.max_columns', None)


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

    poker

