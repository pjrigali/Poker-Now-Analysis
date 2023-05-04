from dataclasses import dataclass
from poker.utils.functions import parse_games
from poker.utils.class_functions import _get_attributes, _clean_print, _flatten_group, _group_name_blank


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
