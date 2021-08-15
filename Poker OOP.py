# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 14:27:18 2020

@author: Peter
"""

# import time
import matplotlib.pyplot as plt
from numpy import array
import numpy as np
import pandas as pd
from pandas import DataFrame, read_csv, concat
pd.set_option('display.max_columns', None)
from collections import Counter
from collections import namedtuple
from os import walk

from hand import hand, request, approved, joined, my_cards, small_blind, big_blind, folds, calls, raises, checks, wins, \
    shows, quits, flop, turn, river, undealt, stand_up, sit_in, player_stacks


class Poker:
    def __init__(self):
        self.files = next(walk('C:\\Users\\Peter\\Desktop\\Personal\\11_Repository\\Poker Related\\Data'))[2]
        
    def convert_Shapes(self, d):
        
        dn = array(d)
        for i,j in enumerate(dn):
            dn[i] = j.replace("â£"," Clubs").replace("â¦"," Diamonds").replace("â¥"," Hearts").replace("â"," Spades")
        return DataFrame(dn)

    def players_in_hand(self, lst):
        
        sub_string = ["folds","calls","raises","checks"]
        players = list(set(j.split('@')[0].replace('"','').strip() for j in lst if any(x in j for x in sub_string)))
        return tuple(players)

    def turns_in_hand(self, lst):
        
        turns = []
        sub_string = ["Player stacks","collected","starting hand"]
        for j in lst:
            if ":" in j:
                if not any(x in j for x in sub_string):
                    turns.append(j.split(':')[0])
        return tuple(turns)

    def moves_in_hand(self, lst):
        
        if len(lst) == 0:
            return [(),(),(),()]
        else:
            checks, raises, calls, folds = (), (), (), ()
            for j in lst[0]:
                if "folds" in j:
                    folds = folds + tuple((j.split('@')[0].replace('"','').strip(),))
                if "calls" in j:
                    calls = calls + (j.split('@')[0].replace('"','').strip(), j.split('calls ')[1])
                if "raises" in j:
                    raises = raises + (j.split('@')[0].replace('"','').strip(), j.split('raises to')[1])
                if "checks" in j:
                    checks = checks + tuple((j.split('@')[0].replace('"','').strip(),))    
            return [tuple(checks), tuple(raises), tuple(calls), tuple(folds)]
        
    def getHands(self, file):
        
        #Load Data
        df = read_csv('C:\\Users\\Peter\\Desktop\\Personal\\11_Repository\\Poker Related\\Data\\'+file, encoding='latin1')['entry']
        df = df.reindex(index=df.index[::-1]).reset_index(drop=True)    
        dfn = self.convert_Shapes(df)   
        #Split into hands
        dfnn = array(dfn)
        hands = []
        hand_lst = []
        for i,j in enumerate(dfnn):
            if ' starting hand ' in j[0]:
                if ' hand #1 ' in j[0]:
                    hands.append(hand_lst)
                hand_lst = []
                hand_lst.append(j[0])
                hands.append(hand_lst)
            else:
                hand_lst.append(j[0])
        return hands
        
    def getPlayers(self, hands):
        
        lst = []
        for i in hands:
            for j in i:
                if ' @ ' in j:
                    lst.append(j.split('@')[0].split('"')[1].strip()) 
                    
        return list(set(lst)) 
    
    def getPlayerIds(self, hands):

        ids = list(([j.split('@')[0].split('"')[1].strip(),j.split('@')[1].split('"')[0].strip()] for i in hands for j in i if ' @ ' in j))
        ids_lst = list(set((j[1] for i,j in enumerate(ids))))
        id_dict = {}
        for j,k in enumerate(ids):
            for first_item in set([k[1]]).intersection(ids_lst): break
            try:
                id_dict[first_item] = list(set(id_dict[first_item] + [k[0]]))
            except:
                id_dict[first_item] = [k[0]]        
                
        return id_dict

    def calcs(self, hands):
        
        result = DataFrame()
        result = []
        for i in hands:      
            
            players_in = self.players_in_hand(i)
            turns_in = self.turns_in_hand(i)
            small_blind = ()
            big_blind = ()
            hand_winner = []
            hand_winner_cards = []
            shows = []
            flop_cards = ()
            turn_card = ()
            river_card = ()
            hand_number = ()
            dealer = ()
            stands_up = []
            pre_flop = []
            post_flop = []
            post_turn = []
            post_river = []
            items = []       
            loses = []
            sit = []
            approved = []
            joined = []
            end = []
    
            for j in i:
                items.append(j)
                if " was changed " in j:
                    continue
        
                else:
                    if "posts a small blind" in j:
                        small_blind = (j.split(' @ ')[0].split('"')[1], int(j.split(' of ')[1].strip()))
                        continue
        
                    if "posts a big blind" in j:
                        big_blind = (j.split(' @ ')[0].replace('"','').strip(), int(j.split(' of ')[1].strip()))
                        continue
            
                    if " collected " in j:
                        hand_winner.append((j.split(' @ ')[0].split('"')[1], int(j.split('collected')[1].split('from')[0].strip())))
                        
                        if " with " in j:
                            hand_winner_cards.append((j.split(' with ')[1].split(', ')[0], j.split(', ')[1].split('(')[0], j.split(':')[1].split(')')[0]))
            
                    if " shows " in j:
                        shows.append((j.split('@')[0].split('"')[1].strip(), j.split(" a ")[1].split('.')[0]))
                        continue
            
                    if any(x in j for x in ["Flop:","flop:"]):
                        if "Flop:" in j:
                            flop = j.replace('Flop: ','').replace('[','').replace(']','').split(',')
                        else:    
                            flop = j.replace('flop: ','').replace('[','').replace(']','').split(',')
                    
                        flop_cards = (flop[0].lstrip(), flop[1].lstrip(), flop[2].lstrip())
                        pre_flop.append(items)
                        items = []
                        continue
            
                    if any(x in j for x in ["Turn:","turn:"]):
                        turn_card = (j.split('[')[1].replace(']','').strip())
                        post_flop.append(items)
                        items = []
                        continue
                    
                    if any(x in j for x in ["River:","river:"]):    
                        river_card = (j.split('[')[1].replace(']','').strip())
                        post_turn.append(items)
                        items = []
                        continue
                    
                    if "dealer" in j:
                        hand_number = (int(j.split('#')[1].split(' ')[0]))
                        dealer = (j.split('dealer')[1].split('@')[0].split('"')[1].strip()) 
                        continue
                
                    if "stand up" in j:
                        stands_up.append((j.split('@')[0].split('"')[1].strip(), int(j.split('stack of')[1].split('.')[0])))
                        continue
            
                    if " collected " in j:
                        post_river.append(items)
                        items = []
                        continue
                    
                    if " quits the game " in j:
                        loses.append((j.split('@')[0].split('"')[1].strip(), int(j.split('stack of')[1].split('.')[0].strip())))
                        continue
                
                    if "approved" in j:
                        approved.append((j.split('@')[0].split('"')[1].strip(), int(j.split('stack of')[1].split('.')[0].strip())))
                        continue
                
                    if "joined" in j:
                        joined.append((j.split('@')[0].split('"')[1].strip(), int(j.split('stack of')[1].split('.')[0].strip())))
                        continue

                    if "sit back" in j:
                        sit.append((j.split('@')[0].split('"')[1].strip(), int(j.split('stack of')[1].split('.')[0].strip())))
                        continue
        
                    if 'Player stacks:' in j:
                        for l in range(1,len(j.split("#"))):
                            end.append((j.split("#")[l].split('@')[0].split('"')[1].strip(), j.split("#")[l].split('@')[1].split('(')[1].split(')')[0]))  
                        continue
                    
            players = self.getPlayers(hands)
            oh = [(i,0) for i in players if i not in (i[0] for i in end)]
            end_n = [(i,int(j[1])) for i in players for j in end if i == j[0]]
            
            Pre_Flop_Checks, Pre_Flop_Raises, Pre_Flop_Calls, Pre_Flop_Folds = self.moves_in_hand(pre_flop)
            Post_Flop_Checks, Post_Flop_Raises, Post_Flop_Calls, Post_Flop_Folds = self.moves_in_hand(post_flop)
            Post_Turn_Checks, Post_Turn_Raises, Post_Turn_Calls, Post_Turn_Folds = self.moves_in_hand(post_turn)
            Post_River_Checks, Post_River_Raises, Post_River_Calls, Post_River_Folds = self.moves_in_hand(post_river)
            
            roundn = [
                players_in, turns_in, small_blind, big_blind,
                hand_winner, hand_winner_cards, shows,
                flop_cards, turn_card, river_card,
                hand_number, dealer,
                stands_up, loses, sit, joined, approved, 
                end_n + oh,
                Pre_Flop_Checks, Pre_Flop_Raises, Pre_Flop_Calls, Pre_Flop_Folds,
                Post_Flop_Checks, Post_Flop_Raises, Post_Flop_Calls, Post_Flop_Folds,
                Post_Turn_Checks, Post_Turn_Raises, Post_Turn_Calls, Post_Turn_Folds,
                Post_River_Checks, Post_River_Raises, Post_River_Calls, Post_River_Folds,
                  ]
            
            result.append(roundn)

        cols = ['Players Involved', 'Turns Involved', 'Small Blind', 'Big Blind', 
                'Hand Winner', 'Hand Winner Cards', 'Showed', 
                'Flop Cards', 'Turn Card', 'River Card', 
                'Hand Number', 'Dealer',
                'Stood Up', 'Loses', 'Sits In', 'Joined', 'Approved',
                'Round Amounts', 
                'Pre Flop Checks', 'Pre Flop Raises', 'Pre Flop Calls', 'Pre Flop Folds',
                'Post Flop Checks', 'Post Flop Raises', 'Post Flop Calls', 'Post Flop Folds',
                'Post Turn Checks', 'Post Turn Raises', 'Post Turn Calls', 'Post Turn Folds',
                'Post River Checks', 'Post River Raises', 'Post River Calls', 'Post River Folds',
                ]
        
        result_df = DataFrame(result, columns = cols)

        return result_df

    def getWinnings(self, r, pdn):
        
        players = list(set(sum([pdn[i] for i in pdn.keys()],[])))
        rn = r[['Round Amounts','Sits In', 'Joined','Stood Up','Loses', 'Approved']]
        
        lst = {i:[0] for i in players}
        am_in = {i:0 for i in players}
        am_past = {i:0 for i in players}
        for i in rn['Round Amounts']:
            for j in i:
                if am_past[j[0]] == 0:
                    am_in[j[0]] += j[1]
                am_past[j[0]] = j[1]
                lst[j[0]] = lst[j[0]] + [j[1]]

        # plt.plot(DataFrame(lst))
        
        lstn = {i:[0] for i in players}
        for i in players:
            for j,k in enumerate(lst[i]):
                if lst[i][j] != 0:
                    if lst[i][j-1] == 0:
                        lstn[i].append(lst[i][j]) 
        # print(DataFrame(lst)['Mac'].tolist())
        al = {i:{'Joined':[], 'Stood Up': [], 'Sits In': [], 'Approved': []} for i in players}
        bi = {i:0 for i in players}
        su = {i:0 for i in players}
        for i in players:
            su_temp = [0]
            j_temp = [0]
            si_temp = [0]
            a_temp = [0]
            for j in range(len(rn)):
                jj = rn['Joined'].iloc[j]
                jn = rn['Stood Up'].iloc[j]
                nn = rn['Sits In'].iloc[j]
                nj = rn['Approved'].iloc[j]
                
                if len(jn) > 0:
                    for k in range(len(jn)):
                        if jn[k][0] == i:
                            su_temp.append(int(jn[k][1]))
    
                if len(jj) > 0:
                    for k in range(len(jj)):
                        if jj[k][0] == i:
                            j_temp.append(int(jj[k][1]))

                if len(nn) > 0:
                    for k in range(len(nn)):
                        if nn[k][0] == i:
                            si_temp.append(int(nn[k][1]))

                if len(nj) > 0:
                    for k in range(len(nj)):
                        if nj[k][0] == i:
                            a_temp.append(int(nj[k][1]))
            
            al[i]['Joined'] = sum(j_temp)
            al[i]['Stood Up'] = sum(su_temp)
            al[i]['Sits In'] = sum(si_temp)
            al[i]['Approved'] = sum(a_temp)
            # print(i, a_temp, j_temp, su_temp, si_temp, sum(j_temp) - sum(si_temp))
            # print(i, sum(su_temp)- sum(j_temp))
            # print(i,j_temp, su_temp, si_temp)
            
            # buy_in = sum(j_temp) - abs(sum(lstn[i]) - sum(su_temp)- sum(j_temp) +sum(l_temp))
            # if buy_in <= 0:
            #     buy_in = sum(j_temp) 
            # elif str(buy_in)[-2:] != '00':
            #     buy_in = sum([i for i in j_temp if str(i)[-2:] == '00']) 
                
            bi[i] = sum(j_temp) - sum(si_temp)
            su[i] = [i for i in su_temp if i not in j_temp]
            # bi[i] = sum([i for i in j_temp if i not in su_temp])
            # print(su,bi)
        ju = su.copy()
        for i in players:
            if len(su[i]) == 0:
                jjj = rn['Round Amounts'].iloc[-1]
                for j in jjj:
                    if j[0] == i:
                        ju[i] = j[1]
            else:
                ju[i] = su[i][0]
    
        names, id_name, b_in, b_out  = [], [], [], []
        for i in pdn.keys():
            namesn, b_inn, b_outn = [], [], []
            id_name.append(i)
            for j in pdn[i]:
                namesn.append(j), b_inn.append(bi[j]), b_outn.append(ju[j])
            names.append(namesn), b_in.append(sum(b_inn)), b_out.append(sum(b_outn))
        
        wl = DataFrame()     
        wl['Index'] = id_name
        wl['Names'] = names
        wl['Buy-In Amount'] = b_in
        wl['Leave Table Amount'] = b_out
    
        return (wl,al)

    def getRunningTotalWinnings(self, savedf):
        
        gw_temp = []
        for i in self.files:
            hands = self.getHands(i)
            gw_temp.append(self.getWinnings(self.calcs(hands), self.getPlayerIds(hands))[0])
        
        ind = list(set(sum([list(i['Index']) for i in gw_temp],[])))
        names = []
        id_name = []
        b_in = []
        b_out = []
        games = []
        for i in ind:
            namesn = []
            buy_inn = []
            buy_outn = []
            gamesn = 0
            for j in gw_temp:
                if i in list(j['Index']):
                    j_i = j[j['Index'] == i]
                    namesn.append(j_i['Names'].values[0])
                    buy_inn.append(j_i['Buy-In Amount'].values[0])
                    buy_outn.append(j_i['Leave Table Amount'].values[0])
                    gamesn = gamesn + 1
            names.append(list(set(sum(namesn,[]))))
            id_name.append(i)
            b_in.append(sum(buy_inn))
            b_out.append(sum(buy_outn))
            games.append(gamesn)
        
        wl = pd.DataFrame()     
        wl['Index'] = id_name
        wl['Names'] = names
        wl['Games Played'] = games
        wl['Buy-In Amount'] = b_in
        wl['Leave Table Amount'] = b_out
        wl['Total Amount'] = wl['Leave Table Amount'] - wl['Buy-In Amount']
        wl['Percent Change'] = round(((wl['Leave Table Amount'] - wl['Buy-In Amount'])/wl['Buy-In Amount'])*100,1)
        wl = wl.drop_duplicates(['Buy-In Amount','Leave Table Amount']).sort_values('Total Amount',ascending=False).reset_index(drop=True)
        # wl = wl[wl['Games Played'] >= 2].reset_index(drop=True)
        
        grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
                   ['1_FRcDzJU-', 'ofZ3AjBJdl', 'yUaYOqMtWh', 'EIxKLHzvif'],
                   ['3fuMmmzEQ-', 'LRdO6bTCRh'],
                   ['FZayb4wOU1', '66rXA9g5yF'],
                   # ['48QVRRsiae', 'u8_FUbXpAz'],
                   ]
    
        h2 = wl.copy()
        for i in grouped:
            index = []
            names = []
            games_played = 0
            buy_in = 0
            leave_amount = 0
            total_amount = 0
            for j in i:
                temp = h2[h2['Index'] == j]
                h2 = h2.drop(temp.index, axis='index')

                for name in list(temp['Names'])[0]:
                    if name not in names:
                        names.append(name)
                    
                temp.columns
                games_played += list(temp['Games Played'])[0]
                buy_in += list(temp['Buy-In Amount'])[0]
                leave_amount += list(temp['Leave Table Amount'])[0]
                total_amount += list(temp['Total Amount'])[0]
                index.append(list(temp['Index'])[0])
            per_change = round(((leave_amount - buy_in) / buy_in) * 100, 1)
            h2 = pd.concat([h2, pd.DataFrame([[index, names, games_played, buy_in, leave_amount, total_amount, per_change]], columns=list(h2.columns))])
        h2 = h2.sort_values('Percent Change', ascending=False).reset_index()
        
        if savedf == 1:
            h2.to_csv('C:\\Users\\Peter\\Desktop\\Personal\\11_Repository\\Poker Related\\Running Total.csv', header = True)
        return h2

    #Wining Hand Face Card or Not?
    def WHFC(self, d):
        WHFCn = []
        for i in range(len(d)):
            temp = d.iloc[i]
            if len(temp['Turns Involved']) == 3:
                temp_lst = [j for j in ['J','Q','K','A'] if j in str(temp['Hand Winner Cards'])]
                if len(temp_lst) >= 1:
                    WHFCn.append(temp_lst)
        return round(len(WHFCn)/len(d),2) * 100

    #Winning Streak
    def streak(self, d):
        dn = d[['Hand Winner']]
        player_lst = list(set(list([i[0] for i in dn['Hand Winner'] if len(i) > 1])))
        dic = {i:0 for i in player_lst}

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

    #Does raising signal winner?
    def DRSW(self, d):
        dn = d[['Hand Winner', 'Pre Flop Raises','Post Flop Raises', 'Post Turn Raises','Post River Raises']]
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
            final[i + ' %'] = round(count_dic[i]/count_dic_occur[i], 2) * 100
    
        return final

    #Dealer or big blind winning
    def Dealer_Small_Big(self, d):
        dn = d[['Dealer', 'Small Blind', 'Big Blind', 'Hand Winner']]
        dic = {'Dealer': 0, 'Small Blind': 0, 'Big Blind': 0}
        d_lst = list(dn['Hand Winner'])
    
        for i,j in enumerate(d_lst):
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
                            
        vals = np.multiply(np.divide([*dic.values()],len(d_lst)),100).astype(int)
    
        final = {}
        for i,j in enumerate(['Dealer', 'Small Blind', 'Big Blind']):
            final[j] = vals[i]
        
        return final

    #Get the best cards
    def Winning_Cards(self, d, count=52):        
        dn = d[['Hand Winner Cards', 'Flop Cards', 'Turn Card', 'River Card', 'Showed', 'Hand Winner', 'Turns Involved']]
        card_lst = []
        winner_lst = list(dn['Hand Winner'])
        for i, j in enumerate(winner_lst):
            if len(j) > 1:
                showed_lst = dn['Showed'].iloc[i]
                winner = j[0]
                winner_cards = dn['Hand Winner Cards'].iloc[i]
            
                if len(winner_cards) > 1:            
                    winner_cards = [card for card in winner_cards[2:][0].split(',')]            
                    winner_cards = [i.strip().split(" ")[0]+' Spades' if 'Spades\xa0' in i else i.strip() for i in winner_cards]
            
                table_cards_lst = list(dn['Flop Cards'].iloc[i])
                if type(dn['Turn Card']) != tuple:
                    table_cards_lst.append(dn['Turn Card'].iloc[i])
            
                if type(dn['River Card']) != tuple:
                    table_cards_lst.append(dn['River Card'].iloc[i])           

                table_cards_lst = [i.split(" ")[0]+' Spades' if 'Spades\xa0' in i else i for i in table_cards_lst]
            
                winner_cards_lst = []
                if len(winner_cards) > 1:
                    for card in winner_cards:
                        if card not in table_cards_lst:
                            winner_cards_lst.append(card)
                        
                if len(showed_lst) > 1:
                    for player in showed_lst:
                        if winner in player:
                            player_cards = [card for card in player[1:][0].split(',')]            
                            player_cards = [i.strip().split(" ")[0]+' Spades' if 'Spades\xa0' in i else i.strip() for i in player_cards]  
                            winner_cards_lst = player_cards
                            break
                
                card_lst.append(winner_cards_lst)
                
        c = Counter(sum(card_lst, []))
        df = pd.DataFrame(index=c.keys())
        df['Counts'] = c.values()
        dfn = df.sort_values('Counts', ascending=False)
    
        return dfn.nlargest(count,'Counts')

    def winCount(self, d):
        players = []
        for i,j in enumerate(d['Hand Winner']):
            temp = d['Hand Winner'].iloc[i]
            if len(temp) > 1:
                players.append(temp[0])
    
        win_count = {i: 0 for i in set(players)}
        for i,j in enumerate(d['Hand Winner']):
            temp = d['Hand Winner'].iloc[i]
            if len(temp) > 1:
                win_count[temp[0]] += 1
        
        return win_count


if __name__ == '__main__':
    poker = Poker()
    hands = poker.getHands(poker.files[9])
    h = poker.calcs(hands)

    oop = hand()
    
    n_lst = []
    for i in hands:
        n = oop.parser(i)
        for j in n:
            n_lst.append(j)
    
    n_df = pd.DataFrame(n_lst)
    
    nn_lst = []
    for i in n_lst:
        if type(i) == folds:
            nn_lst.append(i)
    nn_lst
    
    
    
    #
    # players = poker.getPlayerIds(hands)
    #
    # player_results = []
    # for player_index in players.keys():
    #     player_names = players[player_index]
    #
    #     setup_dict = []
    #     calls = []
    #     folds = []
    #     raises = []
    #     winner = []
    #     for player_name in player_names:
    #         count = 0
    #         amount = 0
    #         for col in ['Small Blind', 'Big Blind', 'Dealer']:
    #             for row in h[col]:
    #                 if player_name in row:
    #                     count += 1
    #                     if col != 'Dealer':
    #                         amount += row[1]
    #             if col != 'Dealer':
    #                 setup_dict.append({col: [count, amount]})
    #             else:
    #                 setup_dict.append({col: [count]})
    #
    #         call_person = []
    #         call_amount = []
    #         alt_cols = {'Pre Flop Calls': 'Pre Flop Raises', 'Post Flop Calls': 'Post Flop Raises', 'Post Turn Calls': 'Post Turn Raises', 'Post River Calls': 'Post River Raises'}
    #         for col in alt_cols.keys():
    #             for index, row in enumerate(h[col]):
    #                 if player_name in row:
    #                     call_amount.append(row[row.index(player_name) + 1])
    #                     temp = list(h.loc[index, alt_cols[col]])[::2]
    #                     if len(temp) > 1:
    #                         for person in temp:
    #                             call_person.append(person)
    #         calls.append({'Call Amount': call_amount, 'Call Person': call_person})
    #
    #         fold_person = []
    #         fold_amount = []
    #         alt_cols = {'Pre Flop Folds': 'Pre Flop Raises', 'Post Flop Folds': 'Post Flop Raises', 'Post Turn Folds': 'Post Turn Raises', 'Post River Folds': 'Post River Raises'}
    #         for col in alt_cols.keys():
    #             for index, row in enumerate(h[col]):
    #                 if player_name in row:
    #                     temp = list(h.loc[index, alt_cols[col]])
    #                     if len(temp) > 1:
    #                         for person in temp[::2]:
    #                             fold_person.append(person)
    #                         for amount in temp[1::2]:
    #                             fold_amount.append(amount)
    #         folds.append({'Fold Amount': fold_amount, 'Fold Person': fold_person})
    #
    #         raise_person = []
    #         raise_amount = []
    #         alt_cols = {'Pre Flop Raises': ['Pre Flop Folds', 'Pre Flop Calls'], 'Post Flop Raises': ['Post Flop Folds', 'Post Flop Calls'], 'Post Turn Raises': ['Post Turn Folds', 'Post Turn Calls'], 'Post River Raises': ['Post River Folds', 'Post River Calls']}
    #         for col in alt_cols.keys():
    #             for index, row in enumerate(h[col]):
    #                 if player_name in row:
    #                     raise_amount.append(row[row.index(player_name) + 1])
    #                     for reaction in alt_cols[col]:
    #                         temp = list(h.loc[index, reaction])
    #                         if len(temp) > 1:
    #                             if 'Folds' in reaction:
    #                                 for person in temp:
    #                                     raise_person.append(person)
    #                             else:
    #                                 for person in temp[::2]:
    #                                     raise_person.append(person)
    #         raises.append({'Raise Amount': raise_amount, 'Raise Person': raise_person})
    #
    #         winner_amount = []
    #         winner_hands = []
    #         alt_cols = {'Hand Winner': 'Hand Winner Cards'}
    #         for index, row in enumerate(h['Hand Winner']):
    #             if len(row) == 1:
    #                 if player_name in row:
    #                     winner_amount.append(row[0][1])
    #                     winner_hands.append(h.loc[index, alt_cols['Hand Winner']][0][0])
    #             if len(row) > 1:
    #                 for ind, person in enumerate(row):
    #                     if player_name in person:
    #                         winner_amount.append(person[1])
    #                         winner_hands.append(h.loc[index, alt_cols['Hand Winner']][ind][0])
    #         winner.append({'Win Amount': winner_amount, 'Wining Hands': winner_hands})
    #
    #         player_results.append([player_index, player_name, setup_dict, calls, folds, raises, winner])
    #
    
    
    # hh, hhh = poker.getWinnings(h, poker.getPlayerIds(hands))
    
    # print(hh['Buy-In Amount'].sum()-hh['Leave Table Amount'].sum())
    # hhhh = DataFrame.from_dict(hhh)
    # print(hhhh)
    # (hhhh.loc['Joined']-hhhh.loc['Sits In']).sum()
    # (hhhh.loc['Stood Up']-hhhh.loc['Joined']).sum()
    # hhhh.loc['Approved'].sum()
    # print(DataFrame.from_dict(hhh))
    # h = poker.getWinnings(poker.calcs(hands), poker.getPlayerIds(hands))    
    
    # for i in poker.files:
    #     hands = poker.getHands(i)
    #     h = poker.getWinnings(poker.calcs(hands), poker.getPlayerIds(hands))[0]
    #     print(h)
    #     print(h['Buy-In Amount'].sum()-h['Leave Table Amount'].sum())
    #     print()
    
    # h1 = poker.getRunningTotalWinnings(0)
    # print(h1)
    

# p_dict = {i: [] for i in grtw['Index'].to_list()}
# for i in filenames:
#     result, players_dict, players = create_df(i)
#     ind = range(1,[int(i) for i in result['Hand Number'].to_list()][-1]+1)
#     result['Hand Number'] = ind
#     temp = pd.DataFrame(index=ind, columns=players)
#     for play in players:
#         temp_lst = []
#         for j,k in enumerate(result['Round Amounts']):
#             for l in k:
#                 if l[0] == play:
#                     temp_lst.append(int(l[1]))
#         temp[play] = temp_lst
    
#     for j in players:
#         plt.plot(temp[j], label=j)
#     plt.plot(ind, [3000]*len(ind), linestyle='dashed', color = 'black')
#     plt.title('Game '+i)
#     plt.ylabel('Dollar')
#     plt.xlabel('Hand')
#     plt.legend(framealpha=.5)
#     plt.show()



    #
    # poker.WHFC(h)
    #
    # poker.streak(h)
    #
    # poker.DRSW(h)
    #
    # poker.Dealer_Small_Big(h)
    #
    # poker.Winning_Cards(h)
    #
    # lst = []
    # for i,j in enumerate(h['Hand Winner']):
    #     temp = h['Hand Winner'].iloc[i]
    #     if len(temp) > 1:
    #         if 'Peter' in temp[0]:
    #             lst.append(i)
    #
    # poker.Winning_Cards(h.iloc[lst])
    #
    #
    # poker.winCount(h)
    #
    #
    #
    #
    # move_lst = ['Small Blind', 'Big Blind',
    #             'Pre Flop Raises', 'Pre Flop Calls',
    #             'Post Flop Raises', 'Post Flop Calls',
    #             'Post Turn Raises', 'Post Turn Calls',
    #             'Post River Raises', 'Post River Calls']
    #
    # for i,j in enumerate(h['Hand Winner']):
    #     temp = h.iloc[i]
    #     pot = 0
    #     for k in move_lst:
    #         temp_n = temp[k]
    #         if len(temp_n) > 1:
    #             for value in temp_n[::-2]:
    #                 if type(value) != int:
    #                     if 'and' in value:
    #                         value = int(value.strip().split(' and')[0])
    #                     else:
    #                         value = int(value.strip())
    #                 print(round(pot/value, 2))
    #                 pot += value
    #
    #
    #
    #
    #
    # #Pre Flop Stats
    # move_lst = ['Pre Flop Checks', 'Pre Flop Raises', 'Pre Flop Folds', 'Pre Flop Calls']
    #
    # players = []
    # for i,j in enumerate(h['Players Involved']):
    #     temp = h['Players Involved'].iloc[i]
    #     if len(temp) > 1:
    #         players.append(temp)
    #
    # player_dict = {i: {'Pre Flop Checks': 0, 'Pre Flop Raises': 0, 'Pre Flop Folds': 0, 'Pre Flop Calls': 0, 'Players Involved': 0} for i in set(sum(players, ()))}
    #
    # for i,j in enumerate(h['Hand Winner']):
    #     temp = h.iloc[i]
    #
    #     for move in move_lst:
    #         if move != 'Pre Flop Checks':
    #             for player in temp[move][::2]:
    #                 player_dict[player][move] += 1
    #         else:
    #             for player in temp[move]:
    #                 player_dict[player][move] += 1
    #
    #     for player in temp['Players Involved']:
    #         player_dict[player]['Players Involved'] += 1
    #
    # player_dict_percent = player_dict.copy()
    # for i in player_dict_percent.keys():
    #     for move in move_lst:
    #         player_dict_percent[i][move] = round(player_dict_percent[i][move] / player_dict_percent[i]['Players Involved'], 2) * 100
    #
    # pd.DataFrame.from_dict(player_dict_percent, orient='index')[['Pre Flop Checks', 'Pre Flop Raises', 'Pre Flop Folds', 'Pre Flop Calls']]
    #
    #
    




#What Amount triggers people to fold?
# def FoldStats(d):
#     dn = h[['Players Involved','Pre Flop Raises','Pre Flop Folds', 'Post Flop Raises', 'Post Flop Folds', 'Post Turn Raises', 'Post Turn Folds', 'Post River Raises', 'Post River Folds']]
#     fold_amount = []
#     for i in range(len(dn)):
#         temp = dn.iloc[i]
#         for j,k in [['Pre Flop Raises','Pre Flop Folds'], ['Post Flop Raises', 'Post Flop Folds'], ['Post Turn Raises', 'Post Turn Folds'],['Post River Raises', 'Post River Folds']]:
#             if len(temp[j]) >= 1:
#                 if len(temp[k]) >= 1:
#                     if ' and ' in temp[j][1]:
#                         fold_amount.append([int(temp[j][1].split(' and ')[0].strip()), round(len(temp[k])/(len(temp['Players Involved'])-1), 2)])
#                     else:
#                         fold_amount.append([int(temp[j][1]), round(len(temp[k])/(len(temp['Players Involved'])-1),2)])
#
#     amounts = list(set([fold_amount[i][0] for i in range(len(fold_amount))]))
#     dic = {i : [] for i in amounts}
#
#     for i in range(len(fold_amount)):
#         dic[fold_amount[i][0]].append(fold_amount[i][1])
#
#     for i in dic.keys():
#         dic[i] = round(sum(dic[i])/len(dic[i]),2)
#
#     df = pd.DataFrame()
#     df['Value'], df['Fold Perc'] = dic.keys(), dic.values()
#
#     n_lst = [amounts[i] for i in range(len(amounts)) if amounts[i] == round(amounts[i],-(len(str(amounts[i]))-2))]
#     dfn = df.sort_values('Value').reset_index(drop=True)
#     non_shuv = dfn[dfn['Value'].isin(n_lst)].copy()
#     non_shuv['Fold Perc'] = list((non_shuv['Fold Perc']*100).astype(int))
#     shuv = int(dfn[~dfn['Value'].isin(n_lst)]['Fold Perc'].mean()*100)
#     res = pd.concat([non_shuv,pd.DataFrame([['Shuv', shuv]],columns=['Value', 'Fold Perc'])]).reset_index(drop=True)
#     return res
#
# FoldStats(h)















#Individual Player Stats
# def player_betting(data, p):
#     def pbw_calcs(datan, lst, play):
#         lstnn = []
#         d = datan[lst]
#         for j in range(len(d)):
#             dd = d.iloc[j]
#             if len(dd) > 0:
#                 for k in range(len(dd)):
#                     if play in dd[k][0]:
#                         lstnn.append([sum(dd,[]), lst])
#         return lstnn
#
#     def pbw_per(datan, lstn, adn, playn):
#         dw = datan[datan['Hand Winner'] == playn]
#         dl = datan[datan['Hand Winner'] != playn]
#         l = len(pbw_calcs(dl, lstn+adn, playn))
#         w = len(pbw_calcs(dw, lstn+adn, playn))
#         if l+w == 0:
#             return 0
#         else:
#             return w/(l+w)
#
#     col_lst = ['Pre Flop', 'Post Flop', 'Post Turn', 'Post River']
#     col_lst_adds = [' Raises', ' Checks', ' Calls']
#
#     df_lst = []
#     for k in p:
#         dfn = []
#         for i in col_lst:
#             for j in col_lst_adds:
#                 dfn.append(pbw_per(data, i, j, k))
#         df_lst.append(dfn)
#
#     df = pd.DataFrame(index=[i+j for j in col_lst_adds for i in col_lst])
#     for i in range(len(df_lst)):
#         df[p[i]] = df_lst[i]
#
#     return round(df*100,0)
#
# player_betting(result, players)
     
# def fold_reaction(r, p):
#     # r = result
#     # p = players
#     # col = 'Hand Winner'
#     # pi = person
#     def reaction_calcs(r, pi, col, move, shuv):
#         if move == 'no':
#             c = 0
#             for i in range(len(r[col])):
#                 if type(r[col].iloc[i]) == list:
#                     if pi in r[col].iloc[i]:
#                         c = c + 1
#                 elif type(r[col].iloc[i]) == str:
#                     if pi in r[col].iloc[i]:
#                         c = c + 1
#             return [c, 0]
#         else:
#             c = 0
#             bet = []
#             for i in range(len(r[col])):
#                 if len(r.iloc[i][col]) >= 1:
#                     for j in range(len(r.iloc[i][col])):
#                         if pi in r.iloc[i][col][j]:
#                             c = c + 1
#                             if 'and' in r.iloc[i][col][j][1].strip():
#                                 if shuv == 'yes':
#                                     bet.append(r.iloc[i][col][j][1].strip().split(' '))
#                                 else:
#                                     pass
#                             else:
#                                 bet.append(int(r.iloc[i][col][j][1].strip()))
#
#             return [c,bet]
#
#     col_lst = ['Pre Flop', 'Post Flop', 'Post Turn', 'Post River']
#     col_lst_adds = [' Raises', ' Checks', ' Calls']
#     cols = [i+j for j in col_lst_adds for i in col_lst]
#
#     df_lst = []
#     for person in p:
#         c1 = reaction_calcs(r, person, 'Players Involved', 'no', 'no')
#         c2 = reaction_calcs(r, person, 'Pre Flop Folds', 'no', 'no')
#         c3 = reaction_calcs(r, person, 'Hand Winner', 'no', 'no')
#
#         #Likehood to call
#         c9 = []
#         #Likehood to preflop call
#         c11 = []
#         #Percent win when raising
#         c7 = []
#         #Likehood to preflop raise
#         c15 = []
#         #Average Bet
#         c4 = []
#         #Percentage Check
#         c8 = []
#         #Call Shuv
#         c13 = 0
#         #Fold Shuv
#         c14 = 0
#         #Percentage Raise
#         c21 = []
#
#         for i in cols:
#             if 'Calls' in i:
#                 c10 = reaction_calcs(r, person, i, 'yes', 'no')
#                 try:
#                     c9.append([(c10[0]/c1[0])*100, '% '+i])
#                 except:
#                     c9.append([0, i])
#
#                 if 'Pre' in i:
#                     c12 = reaction_calcs(r, person, i, 'yes', 'no')
#                     try:
#                         c11.append([len(c12[1]), '% '+i])
#                     except:
#                         c11.append([0, '% '+i])
#
#             if 'Raises' in i:
#                 c6 = reaction_calcs(r, person, i, 'yes', 'no')
#                 try:
#                     c66 = [(c6[0]/c3[0])*100,i]
#                 except:
#                     c66 = [c3[0],'never '+i]
#                 c7.append(c66)
#
#                 c20 = reaction_calcs(r, person, i, 'yes', 'no')
#                 try:
#                     c21.append([(c20[0]/c1[0])*100, '% '+i])
#                 except:
#                     c21.append([0, i])
#
#                 if 'Pre' in i:
#                     c16 = reaction_calcs(r, person, i, 'yes', 'no')
#                     try:
#                         c15.append([len(c16[1]), '% '+i])
#                     except:
#                         c15.append([0, '% '+i])
#
#                 for j in range(len(r[i])):
#                     if len(r.iloc[j][i]) >= 1:
#                         for k in range(len(r.iloc[j][i])):
#                             if 'and' in r.iloc[j][i][k][1].strip():
#                                 for l in range(len(r.iloc[j][i.split(' ')[0]+' '+i.split(' ')[1]+' Calls'])):
#                                     if person in r.iloc[j][i.split(' ')[0]+' '+i.split(' ')[1]+' Calls'][l]:
#                                         c13 = c13 + 1
#                                     elif person in r.iloc[j][i.split(' ')[0]+' '+i.split(' ')[1]+' Folds']:
#                                         c14 = c14 + 1
#
#             if 'Checks' in i:
#                 c5 = reaction_calcs(r, person, i, 'no', 'no')
#                 try:
#                     c8.append([(c5[0]/c1[0])*100, '% '+i])
#                 except:
#                     c8.append([0, i])
#             else:
#                 c5 = reaction_calcs(r, person, i, 'yes', 'no')
#                 if c5[0] != 0:
#                     ave = sum(c5[1])/c5[0]
#                 else:
#                     ave = 0
#                 c4.append([ave,i])
#
#
#         try:
#             call_shuv = (c13/(c13+c14))*100
#         except:
#             call_shuv = 0
#
#         if c1[0] == 0:
#             c1[0] = 1
#
#         pre_flop_fold_per = round((c2[0]/c1[0])*100,1)
#         pre_flop_call = round(((c11[0][0])/c1[0])*100,1)
#         pre_flop_raise = round(((c15[0][0])/c1[0])*100,1)
#         per_call = [[round(c9[i][0],1), c9[i][1]] for i in range(len(c9))]
#         per_raise = [[round(c21[i][0],1), c21[i][1]] for i in range(len(c21))]
#         per_check = [[round(c8[i][0],1), c8[i][1]] for i in range(len(c8))]
#         ave_bet = [[round(c4[i][0],1), c4[i][1]] for i in range(len(c4))]
#         winning_per = round((c3[0]/c1[0])*100,1)
#         win_after_raise = [[round(c7[i][0],1), c7[i][1]] for i in range(len(c7))]
#
#         df_lst.append([pre_flop_fold_per, pre_flop_call, pre_flop_raise, per_call[0][0], per_call[1][0], per_call[2][0], per_call[3][0], per_raise[0][0], per_raise[1][0], per_raise[2][0], per_raise[3][0], per_check[0][0], per_check[1][0], per_check[2][0], per_check[3][0], ave_bet[0][0], ave_bet[1][0], ave_bet[2][0], ave_bet[3][0], ave_bet[4][0], ave_bet[5][0], ave_bet[6][0], ave_bet[7][0], win_after_raise[0][0], win_after_raise[1][0], win_after_raise[2][0], win_after_raise[3][0], winning_per, round(call_shuv,1)])
#
#     pcall = ['% Pre Flop Calls', '% Post Flop Calls', '% Post Turn Calls', '% Post River Calls'] + ['% Pre Flop Raises', '% Post Flop Raises', '% Post Turn Raises', '% Post River Raises']
#     pcheck = ['% Pre Flop Checks','% Post Flop Checks','% Post Turn Checks','% Post River Checks']
#     pbr = ['Pre Flop Raises', 'Post Flop Raises', 'Post Turn Raises', 'Post River Raises', 'Pre Flop Calls', 'Post Flop Calls', 'Post Turn Calls', 'Post River Calls']
#     w = ['Pre Flop Raises', 'Post Flop Raises', 'Post Turn Raises', 'Post River Raises']
#     ind = ['Pre flop fold per','Pre flop call', 'Pre flop raise'] + pcall + pcheck + pbr + w + ['Win per', 'Shuv call per']
#
#     df = pd.DataFrame(index=ind)
#     for i in range(len(df_lst)):
#         df[p[i]] = df_lst[i]
#
#     return df
 
# start_timen = time.time()       
# fold_reaction(result, players)
# print(''), print('Fold Reaction'), print("--- %s seconds ---" % round((time.time() - start_timen),2)) 


#
# def PrintPlots(file):
#     file = filenames
#
#     idn = []
#     whfcn = [] #Done
#     drswn = [] #Done
#     dsbn = [] #Done
#     fn = [] #Done
#     gwn = []
#     owcn = [] #Done
#     twcn = [] #Done
#     thwcn = [] #Done
#
#     final_temp = []
#     for i in file:
#         idn.append(i)
#         result, players_dict, players = create_df(i)
#         gwn.append(GetWinnings(result, players_dict,0))
#         whfcn.append(WHFC(result,0)) #Face Card in Winning Hand
#         drswn.append(DRSW(result,0)) #Raising Signals Winning
#         fn.append(FoldStats(result)) #Amount to bet to make fold
#         dsbn.append(list(Dealer_Small_Big(result)['Percents'])) #Dealer stats
#         one, two, three = Winning_Cards(result, 25, 1) #Card counts, Number Counts, Suit Count
#         owcn.append(one)
#         twcn.append(two)
#         thwcn.append(three)
#
#     plt.plot(range(len(idn)),whfcn)
#     plt.title('Face Card in Winning Hand % mu='+str(sum(whfcn)/len(whfcn)))
#     plt.xticks(range(len(drswn)))
#     plt.ylabel('Percent')
#     plt.xlabel('Game')
#     plt.show()
#
#     plt.plot(range(len(idn)),drswn)
#     plt.title('Does Raising Signal Winning % mu='+str(sum(drswn)/len(drswn)))
#     plt.xticks(range(len(drswn)))
#     plt.ylabel('Percent')
#     plt.xlabel('Game')
#     plt.show()
#
#     d_mu = np.mean(np.array(dsbn)[:,0])
#     sb_mu = np.mean(np.array(dsbn)[:,1])
#     bb_mu = np.mean(np.array(dsbn)[:,2])
#     for i in range(len(dsbn)):
#         plt.plot(['Dealer', 'Small Blind',' Big Blind'],dsbn[i],label=i)
#     plt.title('Does Dealer or Blinds Win % mu='+str([d_mu, sb_mu, bb_mu]))
#     plt.ylabel('Percent')
#     plt.xlabel('Position')
#     plt.xticks(['Dealer', 'Small Blind',' Big Blind'])
#     plt.legend()
#     plt.show()
#
#     owcn_temp = [list(i['Counts']) for i in owcn]
#     if len([i for i in [list(i.index) for i in owcn] if len(i) == 53]) > 1:
#         ind = [i for i in [list(i.index) for i in owcn] if len(i) == 53][0]
#     else:
#         ind = [i for i in [list(i.index) for i in owcn] if len(i) == 53]
#
#     owcn_df = pd.DataFrame(index=ind)
#     for i in range(len(owcn_temp)):
#         if len(owcn_temp[i]) == 53:
#             owcn_df[i] = owcn_temp[i]
#         elif len(owcn_temp[i]) == 52:
#             owcn_df[i] = owcn_temp[i]+[0]
#
#     for i in owcn_df:
#         plt.plot(ind,owcn_df[i])
#     plt.xticks(ind, rotation='vertical')
#     plt.title('Count Each Card Came up')
#     plt.xlabel('Card Type')
#     plt.ylabel('Count')
#     plt.show()
#
#     ind = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2', '1']
#     twcn_df = pd.DataFrame(columns=list(range(len(twcn))),index=ind)
#     for i in range(len(twcn)):
#         for j in ind:
#             if j in list(twcn[i].keys()):
#                 twcn_df.loc[j,i] = twcn[i][j]
#             else:
#                 twcn_df.loc[j,i] = 0
#
#     for i in twcn_df:
#         plt.plot(ind,twcn_df[i])
#     plt.xticks(ind, rotation='vertical')
#     plt.title('Count Each Card Type Came up')
#     plt.xlabel('Card Type')
#     plt.ylabel('Count')
#     plt.show()
#
#     def norma(lst):
#         return [round((lst[i] - min(lst))/(max(lst) - min(lst)),2) for i in range(len(lst))]
#
#     ind = ['Spades', 'Clubs', 'Hearts', 'Diamonds']
#     thwcn_df = pd.DataFrame(columns=list(range(len(thwcn))),index=ind)
#     for i in range(len(thwcn)):
#         for j in ind:
#             if j in list(thwcn[i].keys()):
#                 thwcn_df.loc[j,i] = thwcn[i][j]
#             else:
#                 thwcn_df.loc[j,i] = 0
#
#     for i in thwcn_df:
#         thwcn_df[i] = norma(list(thwcn_df[i]))
#
#     for i in thwcn_df:
#         plt.scatter(ind,thwcn_df[i])
#     plt.xticks(ind, rotation='vertical')
#     plt.title('Percent Each Suite Came up')
#     plt.xlabel('Suite')
#     plt.ylabel('Percent')
#     plt.show()
#
#     fn_ind = list(set(sum([list(i['Value']) for i in fn],[])))
#     fn_ind.remove('Shuv')
#     fn_ind.sort()
#     fn_ind = fn_ind + ['Shuv']
#
#     fn_df = pd.DataFrame(columns=list(range(len(fn))),index=fn_ind)
#     for i in range(len(fn)):
#         for j in fn_ind:
#             if j in list(fn[i]['Value']):
#                 fn_df.loc[j,i] = fn[i][fn[i]['Value'] == j]['Fold Perc'].values[0]
#             else:
#                 fn_df.loc[j,i] = 0
#
#     fn_ind[-1] = 0
#     fn_df.index = fn_ind
#     fn_df = fn_df[fn_df.index < 3000]
#
#     for i in fn_df:
#         plt.scatter(fn_df.index,fn_df[i])
#     plt.title('Percent Fold Associated with a Bet Amount')
#     plt.xticks(fn_df.index, rotation='vertical')
#     plt.xlabel('0 means Shuv')
#     plt.ylabel('Percent')
#     plt.show()
#
#     return [idn, whfcn, drswn, dsbn, fn, gwn, owcn, twcn, thwcn]
#
# PrintPlots(filenames)

