from typing import List, Optional, Union
from dataclasses import dataclass
import pandas as pd
from poker.poker_class import Poker
from poker.base import flatten
pd.set_option('use_inf_as_na', True)


def _df_convert_list(data: Union[List[str], str, None]) -> Union[List[str], None]:
    """Converts str to List[str] and raises error"""
    if type(data) == list:
        return data
    elif data is None:
        return None
    elif type(data) == str:
        return [data]
    else:
        raise AttributeError('Incorrect input type used')


@dataclass
class DocumentFilter:
    """

    Get a selection from the Poker Object.
    Uses a set of filters to return a desired set of data to be used in later analysis.

    :param data: Input Poker object to be filtered.
    :type data: Poker
    :param game_id_lst: Game Id filter, default is None. *Optional*
    :type game_id_lst: Union[List[str], str, None]
    :param player_index_lst: Player Index filter, default is None. *Optional*
    :type player_index_lst: Union[List[str], str, None]
    :param player_name_lst: Player Name filter, default is None. *Optional*
    :type player_name_lst: Union[List[str], str, None]
    :param class_lst: Filter by class objects, default is None. *Optional*
    :type class_lst: Union[List[str], str, None]
    :param position_lst: Filter by position, default is None. *Optional*
    :type position_lst: Union[List[str], str, None]
    :param win_loss_all: Filter by Win, Loss or All, default is None. *Optional*
    :type win_loss_all: Union[str, None]
    :param column_lst: Filter by column name, default is None. *Optional*
    :type column_lst: Union[List[str], str, None]
    :example: *None*
    :note: All inputs, except data, are *Optional* and defaults are set to None.

    """
    def __init__(self, data: Poker,
                 game_id_lst: Optional[Union[List[str], str, None]] = None,
                 player_index_lst: Optional[Union[List[str], str, None]] = None,
                 player_name_lst: Optional[Union[List[str], str, None]] = None,
                 class_lst: Optional[Union[List[str], str, None]] = None,
                 position_lst: Optional[Union[List[str], str, None]] = None,
                 win_loss_all: Optional[str] = None,
                 column_lst: Optional[Union[List[str], str, None]] = None):
        self._data = data
        self._game_id_lst = _df_convert_list(data=game_id_lst)
        self._player_index_lst = _df_convert_list(data=player_index_lst)
        self._player_name_lst = _df_convert_list(data=player_name_lst)
        self._class_lst = _df_convert_list(data=class_lst)
        self._position_lst = _df_convert_list(data=position_lst)
        self._win_loss_all = win_loss_all
        self._column_lst = _df_convert_list(data=column_lst)

        if self._win_loss_all is None:
            self._win_loss_all = 'All'
        elif self._win_loss_all in ['Win', 'Loss', 'All']:
            pass
        else:
            raise AttributeError('Incorrect win_loss_all str used')

        dic = {}
        for key, val in self._data.players_history.items():
            for key1, val1 in val.merged_moves[self._win_loss_all].items():
                if self._column_lst is None:
                    if key1 in dic.keys():
                        dic[key1] += val1
                    else:
                        dic[key1] = val1
                elif self._column_lst is not None and key1 in self._column_lst:
                    if key1 in dic.keys():
                        dic[key1] += val1
                    else:
                        dic[key1] = val1
                elif self._column_lst is not None and key1 not in self._column_lst:
                    raise AttributeError('Column not in the dictionary')

        col_lst = []
        item_dic = {}
        if self._game_id_lst is not None:
            col_lst.append('Game Id')
            for item in self._game_id_lst:
                item_dic[item] = True
        if self._player_index_lst is not None:
            col_lst.append('Player Index')
            for item in self._player_index_lst:
                item_dic[item] = True
        if self._player_name_lst is not None:
            col_lst.append('Player Name')
            for item in self._player_name_lst:
                item_dic[item] = True
        if self._position_lst is not None:
            col_lst.append('Position')
            for item in self._position_lst:
                item_dic[item] = True
        if self._class_lst is not None:
            col_lst.append('Class')
            for item in self._class_lst:
                item_dic[item] = True

        col_lst_len = len(col_lst)
        if len(col_lst) > 0:
            ind_set = None
            temp_ind_dic = {col: {} for col in col_lst}
            for col in col_lst:
                if col not in ['Player Name', 'Player Index']:
                    temp_ind_dic[col] = {ind: True for ind, item in enumerate(dic[col]) if item in item_dic}
                else:
                    temp_values = [item if type(item) == list else [item] for item in dic[col]]
                    temp = [[item for item in flatten(item_lst, 'str')] for item_lst in temp_values]
                    for ind, item_lst in enumerate(temp):
                        for item in item_lst:
                            if item in item_dic:
                                temp_ind_dic[col][ind] = True
                                break
                if ind_set is None:
                    ind_set = set(temp_ind_dic[col].keys())
                else:
                    (ind_set.add(item) for item in temp_ind_dic[col].keys())

            final_ind = []
            for ind in ind_set:
                count = 0
                for col in col_lst:
                    if ind in temp_ind_dic[col]:
                        count += 1
                if count == col_lst_len:
                    final_ind.append(ind)
            final_ind.sort()

            for key, val in dic.items():
                dic[key] = [val[ind] for ind in final_ind]

        final_df = pd.DataFrame(dic).drop_duplicates('Time', keep='first').sort_values('Time', ascending=True).reset_index(drop=True)
        if 'Player Index' in final_df.columns:
            psc, pcc = [], []
            for ind, row in final_df.iterrows():
                if ind == 0:
                    if type(row['Player Index']) == str:
                        prev = row['Player Index']

                if row['Class'] != 'Player Stacks':
                    psc.append(row['Player Starting Chips'])
                    pcc.append(row['Player Current Chips'])
                else:
                    val = row['Player Index'].index(prev)
                    psc.append(row['Player Starting Chips'][val])
                    pcc.append(row['Player Current Chips'][val])

                if type(row['Player Index']) == str:
                    prev = row['Player Index']

            final_df['Player Starting Chips'], final_df['Player Current Chips'] = psc, pcc
        final_df['Seconds'] = [(row['Time'] - row['Previous Time']).total_seconds() for ind, row in final_df.iterrows()]
        final_df['Seconds into Hand'] = [(row['Time'] - row['Start Time']).total_seconds() for ind, row in final_df.iterrows()]
        self._df = final_df
        # self._df = pd.DataFrame(dic).drop_duplicates('Time', keep='first').sort_values('Time', ascending=True).reset_index(drop=True)

    def __repr__(self):
        return "DocumentFilter"

    @property
    def df(self) -> pd.DataFrame:
        """Returns a DataFrame of requested items"""
        return self._df

    @property
    def game_id_lst(self) -> Union[List[str], None]:
        """Returns game id input"""
        return self._game_id_lst

    @property
    def player_index_lst(self) -> Union[List[str], None]:
        """Returns player index input"""
        return self._player_index_lst

    @property
    def player_name_lst(self) -> Union[List[str], None]:
        """Returns player name input"""
        return self._player_name_lst

    @property
    def class_lst(self) -> Union[List[str], None]:
        """Returns class input"""
        return self._class_lst

    @property
    def position_lst(self) -> Union[List[str], None]:
        """Returns position input"""
        return self._position_lst

    @property
    def win_loss_all(self) -> Union[str, None]:
        """Returns win loss or all input"""
        return self._win_loss_all

    @property
    def column_lst(self) -> Union[List[str], None]:
        """Returns column input"""
        return self._column_lst
