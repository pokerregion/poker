"""
    Poker hand history parser module.
"""

import io
import itertools
from datetime import datetime
import attr
import pytz
from zope.interface import Interface, Attribute
from cached_property import cached_property
from .card import Rank


@attr.s(slots=True)
class _Player:
    """Player participating in the hand history."""

    name = attr.ib()
    stack = attr.ib()
    seat = attr.ib()
    combo = attr.ib()


@attr.s(slots=True)
class _PlayerAction:
    """Player actions on the street."""

    name = attr.ib()
    action = attr.ib()
    amount = attr.ib()


class IStreet(Interface):
    actions = Attribute("_StreetAction instances.")
    cards = Attribute("Cards.")
    pot = Attribute("Pot size after actions.")


class IHandHistory(Interface):
    """Interface for all hand histories. Not all attributes are available in all room's hand
    histories, missing attributes are always None. This contains the most properties, available in
    any pokerroom hand history, so you always have to deal with None values.
    """

    # parsing information
    header_parsed = Attribute("Shows wheter header is parsed already or not.")
    parsed = Attribute("Shows wheter the whole hand history is parsed already or not.")
    date = Attribute("Date of the hand history.")

    # Street informations
    preflop = Attribute("_Street instance for preflop actions.")
    flop = Attribute("_Street instance for flop actions.")
    turn = Attribute("_Street instance for turn actions.")
    river = Attribute("_Street instance for river actions.")
    show_down = Attribute("_Street instance for showdown.")

    # Player informations
    table_name = Attribute("Name of")
    max_players = Attribute("Maximum number of players can sit on the table.")
    players = Attribute("Tuple of player instances.")
    hero = Attribute("_Player instance with hero data.")
    button = Attribute("_Player instance of button.")
    winners = Attribute("Tuple of _Player instances with winners.")

    # Game informations
    game_type = Attribute("GameType enum value (CASH, TOUR or SNG)")
    sb = Attribute("Small blind size.")
    bb = Attribute("Big blind size.")
    buyin = Attribute("Buyin with rake.")
    rake = Attribute("Rake only.")
    game = Attribute("Game enum value (HOLDEM, OMAHA? OHILO, RAZZ or STUD)")
    limit = Attribute("Limit enum value (NL, PL or FL)")
    ident = Attribute("Unique id of the hand history.")
    currency = Attribute("Currency of the hand history.")
    total_pot = Attribute("Total pot Decimal.")

    tournament_ident = Attribute("Unique tournament id.")
    tournament_name = Attribute("Name of the tournament.")
    tournament_level = Attribute("Tournament level.")

    def parse_header():
        """Parses only the header of a hand history. It is used for quick looking into the hand
        history for basic informations:
            ident, date, game, game_type, limit, money_type, sb, bb, buyin, rake, currency
        by parsing the least lines possible to get these.
        """

    def parse():
        """Parses the body of the hand history, but first parse header if not yet parsed."""


class _BaseStreet:
    def __init__(self, flop):
        self.pot = None
        self.actions = None
        self.cards = None
        self._parse_cards(flop[0])
        self._parse_actions(flop[1:])
        self._all_combinations = itertools.combinations(self.cards, 2)

    @cached_property
    def is_rainbow(self):
        return all(
            first.suit != second.suit for first, second in self._all_combinations
        )

    @cached_property
    def is_monotone(self):
        return all(
            first.suit == second.suit for first, second in self._all_combinations
        )

    @cached_property
    def is_triplet(self):
        return all(
            first.rank == second.rank for first, second in self._all_combinations
        )

    @cached_property
    def has_pair(self):
        return any(
            first.rank == second.rank for first, second in self._all_combinations
        )

    @cached_property
    def has_straightdraw(self):
        return any(1 <= diff <= 3 for diff in self._get_differences())

    @cached_property
    def has_gutshot(self):
        return any(1 <= diff <= 4 for diff in self._get_differences())

    @cached_property
    def has_flushdraw(self):
        return any(
            first.suit == second.suit for first, second in self._all_combinations
        )

    @cached_property
    def players(self):
        if not self.actions:
            return None
        player_names = []
        for action in self.actions:
            player_name = action.name
            if player_name not in player_names:
                player_names.append(player_name)
        return tuple(player_names)

    def _get_differences(self):
        return (
            Rank.difference(first.rank, second.rank)
            for first, second in self._all_combinations
        )


class _BaseHandHistory:
    """Abstract base class for *all* kinds of parser."""

    def __init__(self, hand_text):
        """Save raw hand history."""
        self.raw = hand_text.strip()
        self.header_parsed = False
        self.parsed = False

    @classmethod
    def from_file(cls, filename):
        with io.open(filename, "rt", encoding="utf-8-sig") as f:
            return cls(f.read())

    def __str__(self):
        return f"<{self.__class__.__name__}: #{self.ident}>"

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
        date = datetime.strptime(date_string, self._DATE_FORMAT)
        self.date = self._TZ.localize(date).astimezone(pytz.UTC)

    def _init_seats(self, player_num):
        players = []
        for seat in range(1, player_num + 1):
            players.append(
                _Player(name="Empty Seat %s" % seat, stack=0, seat=seat, combo=None)
            )

        return players

    def _get_hero_from_players(self, hero_name):
        player_names = [p.name for p in self.players]
        hero_index = player_names.index(hero_name)
        return self.players[hero_index], hero_index


class _SplittableHandHistoryMixin:
    """Class for PokerStars and FullTiltPoker type hand histories, where you can split the hand
    history into sections.
    """

    def _split_raw(self):
        """Split hand history by sections."""

        self._splitted = self._split_re.split(self.raw)
        # search split locations (basically empty strings)
        self._sections = [ind for ind, elem in enumerate(self._splitted) if not elem]

    def _del_split_vars(self):
        del self._splitted, self._sections
