from dataclasses import dataclass
from poker.utils.functions import parse_games
from poker.utils.class_functions import _get_attributes, _clean_print


@dataclass
class Poker:
        
    def __init__(self, user_inputs: dict):
        self.me = user_inputs.get('me')
        self.repo = user_inputs.get('repo')
        self.grouped = user_inputs.get('grouped')
        self._line_limit = user_inputs.get('line_limit', 50)
        self._item_limit = user_inputs.get('item_limit', 10)
        self._inputs = list(user_inputs.values())
        
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
    