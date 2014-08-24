"""
    Poker hand history parser module.
"""

from abc import ABCMeta, abstractmethod
from collections import MutableMapping, namedtuple
from inspect import ismethod
from decimal import Decimal
from datetime import datetime
import pytz


__all__ = ['HandHistoryPlayer']


_NORMALIZE = {'STARS': {'POKERSTARS', 'STARS', 'PS'},
              'FTP': {'FULL TILT POKER', 'FULL TILT', 'FTP'},
              'PKR': {'PKR', 'PKR POKER'},

              'USD': {'USD', '$'},
              'EUR': {'EUR', '€'},
              'GBP': {'GBP', '£'},

              'TOUR': {'TOURNAMENT', 'TOUR'},
              'CASH': {'CASH GAME', 'RING', 'CASH'},

              'HOLDEM': {"HOLD'EM", 'HOLDEM'},
              'OMAHA': {'OMAHA'},

              'NL': {'NO LIMIT', 'NL'},
              'PL': {'POT LIMIT', 'PL'},
              'FL': {'FIX LIMIT', 'FL'},

              'R': {'REAL MONEY'},
              'P': {'PLAY MONEY'}}


def normalize(value):
    """Normalize common words which can be in multiple form, but all means the same."""

    value = value.upper()
    for normalized, compare in _NORMALIZE.items():
        if value in compare:
            return normalized
    return value.upper()


HandHistoryPlayer = namedtuple('HandHistoryPlayer', 'name, stack, seat, combo')
"""Named tuple for players participating in the hand history."""


class BaseHandHistory(MutableMapping, metaclass=ABCMeta):
    """Abstract base class for *all* kind of parser."""

    _non_hand_attributes = ('raw', 'parsed', 'header_parsed', 'date_format')

    @abstractmethod
    def __init__(self, hand_text):
        """Save raw hand history."""

        self.raw = hand_text.strip()
        self.header_parsed = False
        self.parsed = False

    @classmethod
    def from_file(cls, filename):
        hand_text = open(filename).read()
        self = cls(hand_text)
        return self

    def __len__(self):
        return len(self.keys())

    def __getitem__(self, key):
        if key not in self._non_hand_attributes:
            return getattr(self, key)
        else:
            raise KeyError('You can only get it via ''the attribute like "hand.{}"'.format(key))

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __delitem__(self, key):
        delattr(self, key)

    def __iter__(self):
        return iter(self.keys())

    def __str__(self):
        return "<{}: {} hand #{}>" .format(
            self.__class__.__name__, self.poker_room, self.ident
        )

    def keys(self):
        return [attr for attr in dir(self) if not attr.startswith('_') and
                                              attr not in self._non_hand_attributes and
                                              not ismethod(getattr(self, attr))]

    @abstractmethod
    def parse_header(self):
        """Parses only the header of a hand history. It is used for sort of looking into
        the hand history for basic informations.
        """

    @abstractmethod
    def parse(self):
        """Parses the body of the hand history, but first parse header if not yet parsed."""

        if not self.header_parsed:
            self.parse_header()

    @property
    def board(self):
        """Calculates board from flop, turn and river."""
        board = []
        if self.flop:
            board.extend(self.flop)
            if self.turn:
                board.append(self.turn)
                if self.river:
                    board.append(self.river)
        return tuple(board) if board else None

    def _parse_date(self, date_string):
        """Parse the date_string and return a datetime object as UTC."""
        date = datetime.strptime(date_string, self.date_format)
        self.date = self._TZ.localize(date).astimezone(pytz.UTC)

    def _init_seats(self, player_num):
        players = []
        for seat in range(1, player_num + 1):
            players.append(
                HandHistoryPlayer(name='Empty Seat {}'.format(seat),
                                  stack=0,
                                  seat=seat,
                                  combo=None)
            )

        return players

    def _get_hero_from_players(self, hero_name):
        player_names = [p.name for p in self.players]
        hero_index = player_names.index(hero_name)
        return self.players[hero_index], hero_index


class SplittableHandHistory(BaseHandHistory):
    def __init__(self, hand_text):
        """Split hand history by sections."""

        super().__init__(hand_text)

        self._splitted = self._split_re.split(self.raw)

        # search split locations (basically empty strings)
        # sections[0] is before HOLE CARDS
        # sections[-1] is before SUMMARY
        self._sections = [ind for ind, elem in enumerate(self._splitted) if not elem]

    def parse(self):
        super().parse()

        self._parse_table()
        self._parse_players()
        self._parse_button()
        self._parse_hero()
        self._parse_preflop()
        self._parse_street('flop')
        self._parse_street('turn')
        self._parse_street('river')
        self._parse_showdown()
        self._parse_pot()
        self._parse_board()
        self._parse_winners()
        self._parse_extra()

        del self._splitted
        self.parsed = True
