from dataclasses import dataclass
from poker.utils.functions import parse_games
from poker.utils.class_functions import _get_attributes, _clean_print, _flatten_group, _group_name_blank
from poker.utils.tools import percent


@dataclass
class Poker:
        
    def __init__(self, user_inputs: dict):
        self.me = user_inputs.get('me')
        self.repo = user_inputs.get('repo')
        self.grouped = user_inputs.get('grouped')
        self._line_limit = user_inputs.get('line_limit', 50)
        self._item_limit = user_inputs.get('item_limit', 10)
        self._inputs = list(user_inputs.values())
        self._flat_group_id_name = _flatten_group(self.grouped)
        
        assert self.me is not None
        assert self.repo is not None
        assert self.grouped is not None
        
        self.rows, self.hands = parse_games(self.repo, self.me, self.grouped)
        
    def __str__(self) -> str:
        return (f"Poker Data: ({_clean_print(self._inputs, self._line_limit, self._item_limit, False)})" +
                "\n" +
                f"me: ({self.me})," +
                "\n" +
                f"repo: ({_clean_print(self.repo, self._line_limit, self._item_limit)})" +
                "\n" +
                f"grouped: ({_clean_print(self.grouped, self._line_limit, self._item_limit)})" +
                "\n" +
                f"rows: ({_clean_print(self.rows, self._line_limit, self._item_limit)})" +
                "\n" +
                f"hands: ({_clean_print(self.hands, self._line_limit, self._item_limit)})")
        
    def __repr__(self) -> str:
        return f"Poker Data: ({_clean_print(self._inputs, self._line_limit, self._item_limit, False)})"

    def items(self):
        return _get_attributes(self)
    
    def running_total(self, rows: list = None, dollar_amount: int = 100,) -> dict:
        """Returns the total return for each player."""
        d = _group_name_blank(self.grouped, 0.0)
        
        if not rows:
            rows = self.rows
        
        for i in rows:
            if i.get('move') and i.get('value') and i.get('playerId'):
                n = self._flat_group_id_name.get(i['playerId'], i['playerId'])
                if n:
                    if n not in d:
                        d[n] = 0.0
                    
                    if i['move'] == 'Joined':
                        d[n] -= i['value']
                    elif i['move'] in ('Stands', 'Quits'):
                        d[n] += i['value']
        
        return {k: round(v / dollar_amount, 2) for k, v in d.items()}

    def card_count(self, rows: list = None) -> dict:
        
        if not rows:
            rows = [{'cards': set(i.all_cards)} for i in self.hands]
        
        dct = {}
        for i in rows:
            if i.get('cards') and i['cards']:
                for j in i['cards']:
                    if j not in dct:
                        dct[j] = 0
                    dct[j] += 1
        
        dct = sorted([(v, k) for k, v in dct.items()], reverse=True)
        return {i[1]: i[0] for i in dct}


    def player_stats(self, player_name: str) -> dict:
        """A method for collecting general player stats."""
        
        assert player_name in self.grouped
        assert isinstance(self.grouped[player_name], tuple)
        
        aliases = tuple(f"{player_name} @ {i}" for i in self.grouped[player_name])
        stats = {'chip_turnover': [],
                 'total_game_count': set(),
                 'total_hand_count': 0,
                 'total_win_count': 0,
                 'total_win_amount': 0,
                 'largest_win_amount': 0,
                 'largest_loss_amount': 0}
        # How many games has the player been in.
        # How long has the player played.
        # Cards shown
        # Average Bet amount
        # Average Raise amount
        # Average Fold amount
        
        for h in self.hands:
            # Total Hand Count.
            if hasattr(h, 'starting_chips'):
                for a in aliases:
                    if a in h.starting_chips:
                        stats['total_hand_count'] += 1
                        if h.game_id not in stats['total_game_count']:
                            stats['total_game_count'].add(h.game_id)
                        break
            
            # Total Win Count and Amount.
            if hasattr(h, 'winner'):
                for i in h.winner:
                    if i in aliases:
                        stats['total_win_count'] += 1
                        stats['total_win_amount'] += h.win_stack
                        if stats['largest_win_amount'] <= h.win_stack:
                            stats['largest_win_amount'] = h.win_stack
                        break
            
            # Largest Loss.
            if hasattr(h, 'ending_chips') and hasattr(h, 'starting_chips'):
                for a in aliases:
                    if a in h.ending_chips and a in h.starting_chips:
                        v = h.ending_chips[a] - h.starting_chips[a]
                        if stats['largest_loss_amount'] >= v:
                            stats['largest_loss_amount'] = v
                        break
                
        stats['percent_win'] = percent(stats['total_win_count'], stats['total_hand_count'])
        stats['total_game_count'] = len(stats['total_game_count'])
        return stats
