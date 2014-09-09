"""
    Poker hand history parser module.
"""

from abc import ABCMeta, abstractmethod
from collections import namedtuple
from inspect import ismethod
from decimal import Decimal
from datetime import datetime
import pytz
from cached_property import cached_property
from poker.card import Rank


_Player = namedtuple('_Player', 'name, stack, seat, combo')
"""Named tuple for players participating in the hand history."""


class _BaseFlop(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, flop: list, initial_pot):
        pass

    @cached_property
    def is_rainbow(self):
        return self.cards[0].suit != self.cards[1].suit != self.cards[2].suit != self.cards[0].suit

    @cached_property
    def is_monotone(self):
        return self.cards[0].suit == self.cards[1].suit == self.cards[2].suit

    @cached_property
    def is_triplet(self):
        return self.cards[0].rank == self.cards[1].rank == self.cards[2].rank

    @cached_property
    def has_pair(self):
        return (self.cards[0].rank == self.cards[1].rank or
                self.cards[0].rank == self.cards[2].rank or
                self.cards[1].rank == self.cards[2].rank)

    @cached_property
    def has_straightdraw(self):
        return any(1 <= diff <= 3 for diff in self._get_differences())

    @cached_property
    def has_gutshot(self):
        return any(1 <= diff <= 4 for diff in self._get_differences())

    @cached_property
    def has_flushdraw(self):
        return (self.cards[0].suit == self.cards[1].suit or
                self.cards[0].suit == self.cards[2].suit or
                self.cards[1].suit == self.cards[2].suit)

    @cached_property
    def players(self):
        if not self.actions:
            return None
        player_names = []
        for action in self.actions:
            player_name = action[0]
            if player_name not in player_names:
                player_names.append(player_name)
        return tuple(player_names)

    def _get_differences(self):
        return (Rank.difference(self.cards[0].rank, self.cards[1].rank),
                Rank.difference(self.cards[0].rank, self.cards[2].rank),
                Rank.difference(self.cards[1].rank, self.cards[2].rank))


class _BaseHandHistory(metaclass=ABCMeta):
    """Abstract base class for *all* kind of parser."""

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

    def __str__(self):
        return "<{}: #{}>" .format(self.__class__.__name__, self.ident)

    @property
    def board(self):
        """Calculates board from flop, turn and river."""
        board = []
        if self.flop:
            board.extend(self.flop.cards)
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
                _Player(name='Empty Seat {}'.format(seat), stack=0, seat=seat, combo=None)
            )

        return players

    def _get_hero_from_players(self, hero_name):
        player_names = [p.name for p in self.players]
        hero_index = player_names.index(hero_name)
        return self.players[hero_index], hero_index


class _SplittableHandHistory(_BaseHandHistory):
    """Base class for PokerStars and FullTiltPoker type hand histories, where you can split
    the hand history into sections.
    """

    def __init__(self, hand_text):
        """Split hand history by sections."""

        super().__init__(hand_text)

        self._splitted = self._split_re.split(self.raw)

        # search split locations (basically empty strings)
        # sections[0] is before HOLE CARDS
        # sections[-1] is before SUMMARY
        self._sections = [ind for ind, elem in enumerate(self._splitted) if not elem]

    @abstractmethod
    def parse_header(self):
        """Parses only the header of a hand history. It is used for sort of looking into
        the hand history for basic informations:
            ident, date, game, game_type, limit, money_type, sb, bb, buyin, rake, currency
        """

    def parse(self):
        """Parses the body of the hand history, but first parse header if not yet parsed."""
        if not self.header_parsed:
            self.parse_header()

        self._parse_table()
        self._parse_players()
        self._parse_button()
        self._parse_hero()
        pot = self._parse_preflop()
        self._parse_flop(pot)
        self._parse_street('turn')
        self._parse_street('river')
        self._parse_showdown()
        self._parse_pot()
        self._parse_board()
        self._parse_winners()
        self._parse_extra()

        del self._splitted
        self.parsed = True

    @abstractmethod
    def _parse_table(self):
        pass

    @abstractmethod
    def _parse_players(self):
        pass

    @abstractmethod
    def _parse_button(self):
        pass

    @abstractmethod
    def _parse_hero(self):
        pass

    @abstractmethod
    def _parse_preflop(self):
        pass

    @abstractmethod
    def _parse_street(self):
        pass

    @abstractmethod
    def _parse_showdown(self):
        pass

    @abstractmethod
    def _parse_pot(self):
        pass

    @abstractmethod
    def _parse_board(self):
        pass

    @abstractmethod
    def _parse_winners(self):
        pass

    @abstractmethod
    def _parse_extra(self):
        pass
