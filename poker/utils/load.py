"""
Functions for loading in csv files.
"""
from typing import List
import datetime
from os import walk
import csv


def _convert(data: List[str], dic: dict):
    """convert symbols to words and time strings to Datetime objects"""
    dic['Event'].append(data[0].replace("â£", " Clubs").replace("â¦", " Diamonds").replace("â¥", " Hearts").replace("â", " Spades"))
    dic['Time'].append(datetime.datetime.strptime(data[1].replace('T', ' ').split('.')[0], '%Y-%m-%d %H:%M:%S'))


def _rev(lst: list) -> list:
    """reverse a list"""
    lst.reverse()
    return lst


def _get_rows(file: str) -> dict:
    dic = {'Event': [], 'Time': []}
    with open(file, 'r', encoding='latin1') as file:
        my_reader = csv.reader(file, delimiter=',')
        for ind, row in enumerate(my_reader):
            if ind > 0:
                _convert(data=row, dic=dic)
    dic['Event'], dic['Time'] = _rev(dic['Event']), _rev(dic['Time'])
    return dic


def collect_data(repo_location: str) -> dict:
    """Open file, clean data and return a dict"""
    files, file_dic = next(walk(repo_location))[2], {}
    for file in files:
        temp, v, t, d = [], [], [], _get_rows(file=repo_location + file)
        for ind, val in enumerate(d['Event']):
            if ' starting hand ' in val:
                if ' hand #1 ' in val:
                    temp.append({'lines': v, 'times': t})
                v, t = [val], [d['Time'][ind]]
                temp.append({'lines': v, 'times': t})
            else:
                v.append(val), t.append(d['Time'][ind])
        file_dic[file.split(".")[0]] = temp
    return file_dic
