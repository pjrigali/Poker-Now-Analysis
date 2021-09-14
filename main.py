import pandas as pd
import numpy as np
from os import walk
from poker.hand import Hand, Folds
from poker.base import Poker
from poker.analysis import whfc, streak, drsw, dealer_small_big, winning_cards, win_count
import time
pd.set_option('display.max_columns', None)


if __name__ == '__main__':

    repo = 'C:\\Users\\Peter\\Desktop\\Personal\\11_Repository\\Poker Related\\Data'

    start_timen = time.time()
    poker = Poker(repo_location=repo)
    start_timen = "--- %s seconds ---" % round((time.time() - start_timen), 2)
    # print(''), print('Poker Built'), print("--- %s seconds ---" % round((time.time() - start_timen), 2))

    poker

