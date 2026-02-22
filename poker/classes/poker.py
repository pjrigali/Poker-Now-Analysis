"""
"""
from dataclasses import dataclass
from poker.utils.functions import parse_games
from poker.utils.class_functions import _get_attributes, _clean_print, _flatten_group, _group_name_blank
from poker.utils.tools import percent, native_median


@dataclass
class Poker:
    """
    A class that collects and parses Poker Now Logs.

    Attributes:
        user (str): The player's identifier.
        repo (str): The directory containing the log files.
        grouped (dict): A dictionary mapping player names to their possible identifiers.
        rows (list): A list of parsed log rows representing individual actions.
        hands (list): A list of Hand objects representing individual games played.

    Methods:
        items(): Return the attributes of the class.
        running_total(): Calculate the running total of chips for each player.
        card_count(): Calculate the frequency of cards drawn.
        player_stats(): Calculate specific statistics for a player.
    """
    def __init__(self, user_inputs: dict):
        """
        Initialize a Poker instance.

        Args:
            user_inputs (dict): A dictionary containing user configurations, including 'me', 'repo', and 'grouped'.
        """
        self.user = user_inputs.get('me')
        self.repo = user_inputs.get('repo')
        self.grouped = user_inputs.get('grouped')
        self._line_limit = user_inputs.get('line_limit', 50)
        self._item_limit = user_inputs.get('item_limit', 10)
        self._inputs = list(user_inputs.values())
        self._flat_group_id_name = _flatten_group(self.grouped)
        assert self.user is not None
        assert self.repo is not None
        assert self.grouped is not None
        self.rows, self.hands = parse_games(self.repo, self.user, self.grouped)


    def __str__(self) -> str:
        return (f"Poker Data: ({_clean_print(self._inputs, self._line_limit, self._item_limit, False)})" +
                "\n" +
                f"me: ({self.user})," +
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
        """
        Return the attributes of the class.

        Returns:
            dict: The attributes of the Poker object.
        """
        return _get_attributes(self)


    def running_total(self, rows: list = None, dollar_amount: int = 100,) -> dict:
        """
        Calculate the running total of dollars/chips won/lost based on buy-ins and cash-outs.

        Returns:
            dict: A dictionary mapping player names to their net chip/dollar changes.
        """
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
        """
        Calculate the frequency of each card drawn across the provided hands/rows.

        Returns:
            dict: A dictionary mapping a card to its frequency count, sorted in descending order.
        """
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
        """
        Calculate specific statistics for a given player based on all hands played.

        Returns:
            dict: A dictionary of statistics including counts, averages, and extreme values.
        """
        assert player_name in self.grouped
        assert isinstance(self.grouped[player_name], tuple)
        stats = {'total_game_count': set(),
                 'total_hand_count': 0,
                 'total_win_count': 0,
                 'total_win_amount': 0,
                 'largest_win_amount': 0,
                 'largest_loss_amount': 0,
                 'average_bet_amount': [],
                 'average_call_amount': [],
                 'average_raise_amount': [],
                 'average_fold_amount': []}
        # How long has the player played.
        # Cards shown
        for h in self.hands:
            p = None
            if hasattr(h, 'starting_chips'):
                for k, v in h.starting_chips.items():
                    for a in self.grouped[player_name]:
                        if k.endswith(a):
                            p = k
                            break
            if p:
                # Total Hand Count.
                stats['total_hand_count'] += 1
                if h.game_id not in stats['total_game_count']:
                    stats['total_game_count'].add(h.game_id)
                # Largest Loss.
                if hasattr(h, 'ending_chips'):
                    if p in h.ending_chips:
                        v = h.ending_chips[p] - h.starting_chips[p]
                        if stats['largest_loss_amount'] >= v:
                            stats['largest_loss_amount'] = v
                if hasattr(h, 'event_dct'):
                    for en in ('Bet', 'Call', 'Raise', 'Fold'):
                        if en in h.event_dct:
                            for e in h.event_dct[en]:
                                if e['player'] == p:
                                    if en != 'Fold':
                                        if 'value' in e and e['value']:
                                            stats[f"average_{en.lower()}_amount"].append(e['value'])
                                    else:
                                        if 'actionAmount' in e and e['actionAmount']:
                                            stats[f"average_{en.lower()}_amount"].append(e['actionAmount'])
                    # Total Win Count and Amount.
                    if 'Win' in h.event_dct and h.event_dct['Win']:
                        for e in h.event_dct['Win']:
                            if e['player'] == p:
                                stats['total_win_count'] += 1
                                stats['total_win_amount'] += e['value']
                                if stats['largest_win_amount'] <= e['value']:
                                    stats['largest_win_amount'] = e['value']
                                break
        for en in ('bet', 'call', 'raise', 'fold'):
            if stats[f"average_{en}_amount"]:
                stats[f"average_{en}_amount"] = native_median(stats[f"average_{en}_amount"])
            else:
                stats[f"average_{en}_amount"] = None
        stats['percent_win'] = percent(stats['total_win_count'], stats['total_hand_count'])
        stats['total_game_count'] = len(stats['total_game_count'])
        return stats
