
class player_index:
    def _player_index(self, text) -> str:
        if ' @ ' in self.text:
            return text.split('@')[1].split('"')[0].strip()
        else:
            return None
        
class player_name:
    def _player_name(self, text) -> str:
        if ' @ ' in self.text:
            return text.split('"')[1].split('@')[0].strip()
        else:
            return None

class stack:
    def _stack(self, text = None) -> int:
        if 'stack of ' in self.text:
            return int(text.split('stack of ')[1].split('.')[0])
        else:
            return None
        
class position:
    def _position(self):
        return None

class winning_hand:
    def _winning_hand(self):
        return None

class cards:
    def _cards(self) -> list:
        return None

class current_round:
    def _current_round(self):
            return None

class line_attributes(player_index, player_name, stack, position, winning_hand, cards, current_round):

    def __init__(self, text):
        self.text = text
        self.player_name = self._player_name(self.text)
        self.player_index = self._player_index(self.text)
        self.stack = self._stack(self.text)
        self.position = self._position()
        self.winning_hand = self._winning_hand()
        self.cards = self._cards()
        self.current_round = self._current_round()

class request(line_attributes):
        def _line_attributes(self, text):
            return self._line_attributes(self.text)
    
class approved(line_attributes):
    def _line_attributes(self, text):
        return self._line_attributes(self.text)

class joined(line_attributes):
    def _line_attributes(self, text):
        return self._line_attributes(self.text)
    
class my_cards(line_attributes):
    def _line_attributes(self, text):
        return self._line_attributes(self.text)
    
class small_blind(line_attributes):
    def _line_attributes(self, text):
        return self._line_attributes(self.text)
    
class big_blind(line_attributes):
    def _line_attributes(self, text):
        return self._line_attributes(self.text)
 
class folds(line_attributes):
     def _line_attributes(self, text):
        return self._line_attributes(self.text)

class calls(line_attributes):
     def _line_attributes(self, text):
        return self._line_attributes(self.text)

class raises(line_attributes):
     def _line_attributes(self, text):
        return self._line_attributes(self.text)

class checks(line_attributes):
     def _line_attributes(self, text):
        return self._line_attributes(self.text)

class wins(line_attributes):
    def _line_attributes(self, text):
        return self._line_attributes(self.text)

class shows(line_attributes):
    def _line_attributes(self, text):
        return self._line_attributes(self.text)

class quits(line_attributes):
    def _line_attributes(self, text):
        return self._line_attributes(self.text)

class flop(line_attributes):
    def _line_attributes(self, text):
        return self._line_attributes(self.text)

class turn(line_attributes):
    def _line_attributes(self, text):
        return self._line_attributes(self.text)

class river(line_attributes):
    def _line_attributes(self, text):
        return self._line_attributes(self.text)

class undealt(line_attributes):
    def _line_attributes(self, text):
        return self._line_attributes(self.text)

class stand_up(line_attributes):
    def _line_attributes(self, text):
        return self._line_attributes(self.text)

class sit_in(line_attributes):
    def _line_attributes(self, text):
        return self._line_attributes(self.text)

class player_stacks(line_attributes):
    def _line_attributes(self, text):
        return self._line_attributes(self.text)

class hand(request, approved, joined, my_cards, small_blind, big_blind, folds, calls, raises, checks, wins, shows, quits,
           flop, turn, river, undealt, stand_up, sit_in, player_stacks):

    def __init__(self):
        pass
    
    def _request(self, line: str) -> request:
        
        if 'requested a seat' in line:
            return request(line)
        else:
            return None

    def _approved(self, line: str) -> approved:
        
        if 'The admin approved' in line:
            return approved(line)
        else:
            return None

    def _joined(self, line: str) -> joined:
    
        if 'joined the game' in line:
            return joined(line)
        else:
            return None
        
    def _my_cards(self, line: str) -> my_cards:
        
        if 'Your hand' in line:
            return my_cards(line)
        else:
            return None
        
    def _small_blind(self, line: str) -> small_blind:

        if 'posts a small blind' in line:
            return small_blind(line)
        else:
            return None

    def _big_blind(self, line: str) -> big_blind:

        if 'posts a big blind' in line:
            return big_blind(line)
        else:
            return None
        
    def _folds(self, line: str) -> folds:
        
        if ' folds' in line:
            return folds(line)
        else:
            return None
        
    def _calls(self, line: str) -> calls:

        if ' calls ' in line:
            return calls(line)
        else:
            return None

    def _raises(self, line: str) -> raises:

        if ' bets ' in line:
            return raises(line)
        else:
            return None

    def _checks(self, line: str) -> checks:

        if ' checks' in line:
            return checks(line)
        else:
            return None

    def _wins(self, line: str) -> wins:

        if ' collected ' in line:
            return wins(line)
        else:
            return None

    def _shows(self, line: str) -> shows:

        if ' shows a ' in line:
            return shows(line)
        else:
            return None

    def _quits(self, line: str) -> quits:

        if ' quits the game ' in line:
            return quits(line)
        else:
            return None

    def _flop(self, line: str) -> flop:
        
        if 'Flop: ' in line:
            return flop(line)
        else:
            return None

    def _turn(self, line: str) -> turn:
        
        if 'Turn: ' in line:
            return turn(line)
        else:
            return None

    def _river(self, line: str) -> river:
        
        if 'River: ' in line:
            return river(line)
        else:
            return None

    def _undealt(self, line: str) -> undealt:
    
        if 'Undealt cards: ' in line:
            return undealt(line)
        else:
            return None

    def _stand_up(self, line: str) -> stand_up:
    
        if ' stand up with ' in line:
            return stand_up(line)
        else:
            return None

    def _sit_in(self, line: str) -> sit_in:
    
        if ' sit back with ' in line:
            return sit_in(line)
        else:
            return None

    def _player_stacks(self, line: str) -> player_stacks:
    
        if 'Player stacks:' in line:
            return player_stacks(line)
        else:
            return None
        
    def parser(self, hand):
        
        hand_position = []
        start_position = 'Pre Flop'
        for ind, line in enumerate(hand):
            # hand_position.append(start_position)
            if 'Flop:' in line:
                start_position = 'Post Flop'
            if 'Turn:' in line:
                start_position = 'Post Turn'
            if 'River:' in line:
                start_position = 'Post River'
            hand_position.append(start_position)
        
        curr_round = None
        for line in hand:
            if 'starting hand' in line:
                curr_round = int(line.split('starting hand #')[1].split(' (')[0])
                break
        
        lst = []
        for ind, line in enumerate(hand):
            
            if self._request(line) is not None:
                new = request(line)
                new.current_round = curr_round
                
                if new.position is None:
                    new.position = hand_position[ind]
                lst.append(new)
                continue
            
            if self._approved(line) is not None:
                new = approved(line)
                new.current_round = curr_round

                if new.position is None:
                    new.position = hand_position[ind]
                lst.append(new)
                continue
                
            if self._joined(line) is not None:
                new = joined(line)
                new.current_round = curr_round

                if new.position is None:
                    new.position = hand_position[ind]
                lst.append(new)
                continue

            if self._stand_up(line) is not None:
                new = stand_up(line)
                new.current_round = curr_round

                if new.position is None:
                    new.position = hand_position[ind]
                lst.append(new)
                continue
                
            if self._sit_in(line) is not None:
                new = sit_in(line)
                new.current_round = curr_round

                if new.position is None:
                    new.position = hand_position[ind]
                lst.append(new)
                continue
                
            if self._my_cards(line) is not None:
                new = my_cards(line)
                new.current_round = curr_round

                if new.cards is None:
                    new_cards = line.split(' hand is ')[1].split(',')
                    new.cards = [i.strip() for i in new_cards]

                if new.position is None:
                    new.position = hand_position[ind]
                lst.append(new)
                continue
                
            if self._small_blind(line) is not None:
                new = small_blind(line)
                new.current_round = curr_round
                
                if new.stack is None:
                    new.stack = int(line.split('of ')[1])
                    
                if new.position is None:
                    new.position = hand_position[ind]
                lst.append(new)
                continue

            if self._big_blind(line) is not None:
                new = big_blind(line)
                new.current_round = curr_round
                
                if new.stack is None:
                    new.stack = int(line.split('of ')[1])
                    
                if new.position is None:
                    new.position = hand_position[ind]
                lst.append(new)
                continue

            if self._folds(line) is not None:
                new = folds(line)
                new.current_round = curr_round
    
                if new.position is None:
                    new.position = hand_position[ind]
                lst.append(new)
                continue

            if self._calls(line) is not None:
                new = calls(line)
                new.current_round = curr_round
    
                if new.stack is None:
                    new_stack = line.split(' calls ')[1]
                    if ' and ' in new_stack:
                        new_stack = int(new_stack.split(' and ')[0])
                    else:
                        new_stack = int(new_stack)
                    new.stack = new_stack
    
                if new.position is None:
                    new.position = hand_position[ind]
                lst.append(new)
                continue

            if self._raises(line) is not None:
                new = raises(line)
                new.current_round = curr_round
    
                if new.stack is None:
                    new_stack = line.split(' bets ')[1]
                    if ' and ' in new_stack:
                        new_stack = int(new_stack.split(' and ')[0])
                    else:
                        new_stack = int(new_stack)
                    new.stack = new_stack
                    
                if new.position is None:
                    new.position = hand_position[ind]
                lst.append(new)
                continue

            if self._checks(line) is not None:
                new = checks(line)
                new.current_round = curr_round
    
                if new.position is None:
                    new.position = hand_position[ind]
                lst.append(new)
                continue

            if self._wins(line) is not None:
                new = wins(line)
                new.current_round = curr_round

                if new.stack is None:
                    new.stack = int(line.split(' collected ')[1].split(' from ')[0])
                    
                if new.winning_hand is None:
                    if ' from pot with ' in line:
                        new.winning_hand = line.split(' from pot with ')[1].split(',')[0]
                
                if new.cards is None:
                    if 'combination' in line:
                        new_cards = line.split(': ')[1].split(')')[0].split(',')
                        new.cards = [i.strip() for i in new_cards]
                        
                if new.position is None:
                    new.position = hand_position[ind]
                lst.append(new)
                continue

            if self._shows(line) is not None:
                new = shows(line)
                new.current_round = curr_round
                
                if new.cards is None:
                    new_cards = line.split(' shows a ')[1].split('.')[0].split(',')
                    new.cards = [i.strip() for i in new_cards]
                    
                if new.position is None:
                    new.position = hand_position[ind]
                lst.append(new)
                continue

            if self._quits(line) is not None:
                new = quits(line)
                new.current_round = curr_round
    
                if new.position is None:
                    new.position = hand_position[ind]
                lst.append(new)
                continue

            if self._flop(line) is not None:
                new = flop(line)
                new.current_round = curr_round
    
                if new.cards is None:
                    new_cards = line.split(' [')[1].split(']')[0].split(',')
                    new.cards = [i.strip() for i in new_cards]
                    
                if new.position is None:
                    new.position = 'Flop'
                lst.append(new)
                continue

            if self._turn(line) is not None:
                new = turn(line)
                new.current_round = curr_round
    
                if new.cards is None:
                    new.cards = line.split(' [')[1].split(']')[0]
    
                if new.position is None:
                    new.position = 'Turn'
                lst.append(new)
                continue

            if self._river(line) is not None:
                new = river(line)
                new.current_round = curr_round
    
                if new.cards is None:
                    new.cards = line.split(' [')[1].split(']')[0]
    
                if new.position is None:
                    new.position = 'River'
                lst.append(new)
                continue

            if self._undealt(line) is not None:
                new = undealt(line)
                new.current_round = curr_round
    
                if new.cards is None:
                    new_cards = line.split(' [')[1].split(']')[0].split(',')
                    new.cards = [i.strip() for i in new_cards]
                    
                if new.position is None:
                    if len(new.cards) == 1:
                        new.position = 'Post Turn'
                    elif len(new.cards) == 2:
                        new.position = 'Post Flop'
                lst.append(new)
                continue

            if self._player_stacks(line) is not None:
                new = player_stacks(line)
                new.current_round = curr_round
                
                p_name_lst = []
                p_index_lst = []
                p_value_lst = []
                for play in line.split('#')[1:]:
                    p_name = play.split('@')[0].split('"')[1].strip()
                    p_index = play.split('@')[1].split('"')[0].strip()
                    p_value = int(play.split('(')[1].split(')')[0])
                    p_name_lst.append(p_name)
                    p_index_lst.append(p_index)
                    p_value_lst.append(p_value)
                    
                new.player_name = p_name_lst
                new.player_index = p_index_lst
                new.stack = p_value_lst
    
                if new.position is None:
                    new.position = hand_position[ind]
                lst.append(new)
                continue
                
        return lst

