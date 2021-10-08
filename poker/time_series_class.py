from typing import Optional
from dataclasses import dataclass
import pandas as pd
from poker.base import unique_values,  native_mean, running_mean, running_std, running_median, running_percentile
from poker.document_filter_class import DocumentFilter
pd.set_option('use_inf_as_na', True)


def _ts_concat(dic: dict, index_lst: list) -> pd.DataFrame:
    """Concat a dict of dicts or pd.DataFrames"""
    lst_df = []
    for key, val in dic.items():
        if type(val) != pd.DataFrame:
            val = pd.DataFrame(val, index=index_lst)
            val.columns = [key + ' ' + col if col != '' else key for col in val.columns]
        else:
            val.columns = [key]
        lst_df.append(val)
    final_df = pd.concat(lst_df, axis=1).reset_index()
    return final_df


def _ts_hand(data: pd.DataFrame) -> pd.DataFrame:
    """Build Hand related data"""
    pos_dic = {'Pre Flop': 0.25, 'Post Flop': 0.50, 'Post Turn': 0.75, 'Post River': 1.0}
    # Game Id
    g_i_df = pd.DataFrame(data.groupby('Start Time')['Game Id'].last())
    g_i_df.columns = ['']
    # Time in Hand
    t_h_df = pd.DataFrame(data.groupby('Start Time')['Seconds into Hand'].last())
    t_h_df.columns = ['']
    # Last Position
    last_position = data.groupby('Start Time')['Position'].last().tolist()
    l_p_df = pd.DataFrame([pos_dic[item] for item in last_position], index=t_h_df.index, columns=[''])
    # Win
    r_w_p = data.groupby('Start Time')['Win'].last().tolist()
    r_w_p = [1 if item is True else 0 for item in r_w_p]
    r_w_p_df = pd.DataFrame(running_mean(data=r_w_p, num=5), index=t_h_df.index, columns=[''])
    ind_lst = data.groupby('Start Time').last().index.tolist()
    lst_dic = {'Seconds per Hand': t_h_df, 'Last Position in Hand': l_p_df, 'Rolling Win Percent': r_w_p_df,
               'Game Id': g_i_df}
    return _ts_concat(dic=lst_dic, index_lst=ind_lst)


def _ts_position(data: pd.DataFrame) -> pd.DataFrame:
    """Build position related data"""
    temp_df = data[(data['Class'] == 'Calls') | (data['Class'] == 'Raises') | (data['Class'] == 'Checks')]
    p_bet = {'Pre Flop': [], 'Post Flop': [], 'Post Turn': [], 'Post River': []}
    t_p_bet = {'Pre Flop': 0, 'Post Flop': 0, 'Post Turn': 0, 'Post River': 0}
    prev_ind, len_temp_df, game_id_lst = temp_df['Start Time'].iloc[0], len(temp_df), []
    for ind, row in temp_df.iterrows():
        if row['Start Time'] != prev_ind:
            prev_ind = row['Start Time']
            game_id_lst.append(row['Game Id'])
            for key, val in t_p_bet.items():
                p_bet[key].append(val)
            t_p_bet = {'Pre Flop': 0, 'Post Flop': 0, 'Post Turn': 0, 'Post River': 0}
        t_p_bet[row['Position']] += row['Bet Amount']
        if ind == len_temp_df:
            game_id_lst.append(row['Game Id'])
            for key, val in t_p_bet.items():
                p_bet[key].append(val)
    ind_lst = unique_values(data=temp_df['Start Time'].tolist())
    lst_dic = {'Position Bet': p_bet, 'Game Id': {'': game_id_lst}}
    return _ts_concat(dic=lst_dic, index_lst=ind_lst)


def _ts_class_counts_seconds(data: pd.DataFrame) -> pd.DataFrame:
    """Build class, counts, and seconds data"""
    # Bet, Count, and Time Per Position
    temp_df = data[(data['Class'] == 'Calls') | (data['Class'] == 'Raises') | (data['Class'] == 'Checks')]
    pos_lst = ['Pre Flop', 'Post Flop', 'Post Turn', 'Post River']
    class_lst, short_class_lst = ['Checks', 'Calls', 'Raises'], ['Calls', 'Raises']
    c_count = {item1 + ' ' + item: [] for item in class_lst for item1 in pos_lst}
    c_seconds = {item1 + ' ' + item: [] for item in class_lst for item1 in pos_lst}
    c_bet = {item1 + ' ' + item: [] for item in short_class_lst for item1 in pos_lst}
    c_bet_per_pot = {item1 + ' ' + item: [] for item in short_class_lst for item1 in pos_lst}
    c_bet_per_chips = {item1 + ' ' + item: [] for item in short_class_lst for item1 in pos_lst}
    t_c_count = {item1 + ' ' + item: 0 for item in class_lst for item1 in pos_lst}
    t_c_seconds = {item1 + ' ' + item: None for item in class_lst for item1 in pos_lst}
    t_c_bet = {item1 + ' ' + item: None for item in short_class_lst for item1 in pos_lst}
    t_c_bet_per_pot = {item1 + ' ' + item: None for item in short_class_lst for item1 in pos_lst}
    t_c_bet_per_chips = {item1 + ' ' + item: None for item in short_class_lst for item1 in pos_lst}

    prev_ind, len_temp_df, game_id_lst = temp_df['Start Time'].iloc[0], len(temp_df), []
    for ind, row in temp_df.iterrows():
        if row['Start Time'] != prev_ind:
            prev_ind = row['Start Time']
            game_id_lst.append(row['Game Id'])
            for item in class_lst:
                for item1 in pos_lst:
                    c_count[item1 + ' ' + item].append(t_c_count[item1 + ' ' + item])
                    c_seconds[item1 + ' ' + item].append(t_c_seconds[item1 + ' ' + item])
                    if item != 'Checks':
                        c_bet[item1 + ' ' + item].append(t_c_bet[item1 + ' ' + item])
                        c_bet_per_pot[item1 + ' ' + item].append(t_c_bet_per_pot[item1 + ' ' + item])
                        c_bet_per_chips[item1 + ' ' + item].append(t_c_bet_per_chips[item1 + ' ' + item])

            t_c_count = {item1 + ' ' + item: 0 for item in class_lst for item1 in pos_lst}
            t_c_seconds = {item1 + ' ' + item: None for item in class_lst for item1 in pos_lst}
            t_c_bet = {item1 + ' ' + item: None for item in short_class_lst for item1 in pos_lst}
            t_c_bet_per_pot = {item1 + ' ' + item: None for item in short_class_lst for item1 in pos_lst}
            t_c_bet_per_chips = {item1 + ' ' + item: None for item in short_class_lst for item1 in pos_lst}

        t_pos, t_bet, t_class, t_second = row['Position'], row['Bet Amount'], row['Class'], row['Seconds']
        t_key = t_pos + ' ' + t_class

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
            game_id_lst.append(row['Game Id'])
            for item in class_lst:
                for item1 in pos_lst:
                    c_count[item1 + ' ' + item].append(t_c_count[item1 + ' ' + item])
                    c_seconds[item1 + ' ' + item].append(t_c_seconds[item1 + ' ' + item])
                    if item != 'Checks':
                        c_bet[item1 + ' ' + item].append(t_c_bet[item1 + ' ' + item])
                        c_bet_per_pot[item1 + ' ' + item].append(t_c_bet_per_pot[item1 + ' ' + item])
                        c_bet_per_chips[item1 + ' ' + item].append(t_c_bet_per_chips[item1 + ' ' + item])
    ind_lst = unique_values(data=temp_df['Start Time'].tolist())
    lst_dic = {'Class Count': c_count, 'Class Seconds': c_seconds, 'Class Bet': c_bet,
               'Class Bet Percent of Pot': c_bet_per_pot, 'Class Bet Percent of Chips': c_bet_per_chips,
               'Game Id': {'': game_id_lst}}
    return _ts_concat(dic=lst_dic, index_lst=ind_lst)


@dataclass
class TSanalysis:
    """

    Calculate Time Series stats for a player.

    :param data: Input DocumentFilter.
    :type data: DocumentFilter
    :param upper_q: Upper Quantile percent, default is 0.841. *Optional*
    :type upper_q: float
    :param lower_q: Lower Quantile percent, default is 0.159. *Optional*
    :type lower_q: float
    :param window: Rolling window, default is 5. *Optional*
    :type window: int
    :example:
        >>> from poker.time_series_class import TSanalysis
        >>> docu_filter = DocumentFilter(data=poker, player_index_lst=['DZy-22KNBS'])
        >>> TSanalysis(data=docu_filter)
    :note: This class expects a DocumentFilter with only one player_index used.

    """
    def __init__(self, data: DocumentFilter, upper_q: Optional[float] = 0.841, lower_q: Optional[float] = 0.159,
                 window: Optional[int] = 5):
        self._docu_filter = data
        self._window = window
        self._upper_q = upper_q
        self._lower_q = lower_q
        self._df = data.df
        hand_df = _ts_hand(data=self._df)
        self._hand = hand_df.copy()
        position_df = _ts_position(data=self._df)
        self._position = position_df.copy()
        class_df = _ts_class_counts_seconds(data=self._df)
        self._class = class_df.copy()

        hand_cols, hand_ind = hand_df.columns, hand_df.index
        self._hand_mean = pd.DataFrame(columns=hand_cols, index=hand_ind)
        self._hand_std = pd.DataFrame(columns=hand_cols, index=hand_ind)
        self._hand_median = pd.DataFrame(columns=hand_cols, index=hand_ind)
        self._hand_upper_q = pd.DataFrame(columns=hand_cols, index=hand_ind)
        self._hand_lower_q = pd.DataFrame(columns=hand_cols, index=hand_ind)
        for col in hand_cols:
            if col not in ['Game Id', 'index', 'Start Time']:
                self._hand_mean[col] = running_mean(data=hand_df[col], num=self._window)
                self._hand_std[col] = running_std(data=hand_df[col], num=self._window)
                self._hand_median[col] = running_median(data=hand_df[col], num=self._window)
                self._hand_upper_q[col] = running_percentile(data=hand_df[col], num=self._window, q=upper_q)
                self._hand_lower_q[col] = running_percentile(data=hand_df[col], num=self._window, q=lower_q)

        pos_cols, pos_ind = position_df.columns, position_df.index
        self._position_mean = pd.DataFrame(columns=pos_cols, index=pos_ind)
        self._position_std = pd.DataFrame(columns=pos_cols, index=pos_ind)
        self._position_median = pd.DataFrame(columns=pos_cols, index=pos_ind)
        self._position_upper_q = pd.DataFrame(columns=pos_cols, index=pos_ind)
        self._position_lower_q = pd.DataFrame(columns=pos_cols, index=pos_ind)
        for col in pos_cols:
            if col not in ['Game Id', 'index', 'Start Time']:
                self._position_mean[col] = running_mean(data=position_df[col], num=self._window)
                self._position_std[col] = running_std(data=position_df[col], num=self._window)
                self._position_median[col] = running_median(data=position_df[col], num=self._window)
                self._position_upper_q[col] = running_percentile(data=position_df[col], num=self._window, q=upper_q)
                self._position_lower_q[col] = running_percentile(data=position_df[col], num=self._window, q=lower_q)

        class_cols, class_ind = class_df.columns, class_df.index
        self._class_mean = pd.DataFrame(columns=class_cols, index=class_ind)
        self._class_std = pd.DataFrame(columns=class_cols, index=class_ind)
        self._class_median = pd.DataFrame(columns=class_cols, index=class_ind)
        self._class_upper_q = pd.DataFrame(columns=class_cols, index=class_ind)
        self._class_lower_q = pd.DataFrame(columns=class_cols, index=class_ind)
        for col in class_cols:
            if col not in ['Game Id', 'index', 'Start Time']:
                self._class_mean[col] = running_mean(data=class_df[col], num=self._window)
                self._class_std[col] = running_std(data=class_df[col], num=self._window)
                self._class_median[col] = running_median(data=class_df[col], num=self._window)
                self._class_upper_q[col] = running_percentile(data=class_df[col], num=self._window, q=upper_q)
                self._class_lower_q[col] = running_percentile(data=class_df[col], num=self._window, q=lower_q)

    def __repr__(self):
        return 'TSanalysis'

    @property
    def ts_hand(self) -> pd.DataFrame:
        """Hand Related base data"""
        return self._hand

    @property
    def ts_hand_mean(self) -> pd.DataFrame:
        """Hand Related mean data"""
        return self._hand_mean

    @property
    def ts_hand_std(self) -> pd.DataFrame:
        """Hand Related std data"""
        return self._hand_std

    @property
    def ts_hand_median(self) -> pd.DataFrame:
        """Hand Related median data"""
        return self._hand_median

    @property
    def ts_hand_upper_quantile(self) -> pd.DataFrame:
        """Hand Related upper quantile data"""
        return self._hand_upper_q

    @property
    def ts_hand_lower_quantile(self) -> pd.DataFrame:
        """Hand Related lower quantile data"""
        return self._hand_lower_q

    @property
    def ts_position(self) -> pd.DataFrame:
        """Position Related base data"""
        return self._position

    @property
    def ts_position_mean(self) -> pd.DataFrame:
        """Position Related mean data"""
        return self._position_mean

    @property
    def ts_position_std(self) -> pd.DataFrame:
        """Position Related std data"""
        return self._position_std

    @property
    def ts_position_median(self) -> pd.DataFrame:
        """Position Related median data"""
        return self._position_median

    @property
    def ts_position_upper_quantile(self) -> pd.DataFrame:
        """Position Related upper quantile data"""
        return self._position_upper_q

    @property
    def ts_position_lower_quantile(self) -> pd.DataFrame:
        """Position Related lower quantile data"""
        return self._position_lower_q

    @property
    def ts_class(self) -> pd.DataFrame:
        """Class Related base data"""
        return self._class

    @property
    def ts_class_mean(self) -> pd.DataFrame:
        """Class Related mean data"""
        return self._class_mean

    @property
    def ts_class_std(self) -> pd.DataFrame:
        """Class Related std data"""
        return self._class_std

    @property
    def ts_class_median(self) -> pd.DataFrame:
        """Class Related median data"""
        return self._class_median

    @property
    def ts_class_upper_quantile(self) -> pd.DataFrame:
        """Class Related upper quantile data"""
        return self._class_upper_q

    @property
    def ts_class_lower_quantile(self) -> pd.DataFrame:
        """Class Related lower quantile data"""
        return self._class_lower_q
