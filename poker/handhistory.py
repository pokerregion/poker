# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division

"""
    Poker hand history parser module.
"""

import re
import io
import itertools
from collections import namedtuple
from datetime import datetime
import pytz
from zope.interface import Interface, Attribute
from cached_property import cached_property
from .card import Rank
from .hand import Combo
from ._common import _make_int


_Player = namedtuple('_Player', 'name, stack, seat, combo')
"""Named tuple for players participating in the hand history."""

_PlayerAction = namedtuple('_PlayerAction', 'name, action, amount')
"""Named tuple for player actions on the street."""


class IStreet(Interface):
    pot = Attribute('Pot size after actions.')
    cards = Attribute('Cards.')
    actions = Attribute('_StreetAction instances.')


class IHandHistory(Interface):
    """Interface for all hand histories. Not all attributes are available in all room's hand
    histories, missing attributes are always None. This contains the most properties, available in
    any pokerroom hand history, so you always have to deal with None values.
    """
    # parsing information
    raw = Attribute('Raw hand history as it is passed to the constructor. Only stripped.')

    # Street informations
    preflop = Attribute('_Street instance for preflop actions.')
    flop = Attribute('_Street instance for flop actions.')
    turn = Attribute('_Street instance for turn actions.')
    river = Attribute('_Street instance for river actions.')
    show_down = Attribute('_Street instance for showdown.')

    # Player informations
    table_name = Attribute('Name of')
    max_players = Attribute('Maximum number of players can sit on the table.')
    players = Attribute('Tuple of player instances.')
    hero = Attribute('_Player instance with hero data.')
    button = Attribute('_Player instance of button.')
    winners = Attribute('Tuple of _Player instances with winners.')

    # Game informations
    date = Attribute('Date of the hand history.')
    game_type = Attribute('GameType enum value (CASH, TOUR or SNG)')
    money_type = Attribute('MoneyType enum value (REAL, PLAY)')
    sb = Attribute('Small blind size.')
    bb = Attribute('Big blind size.')
    buyin = Attribute('Buyin with rake.')
    rake = Attribute('Rake only.')
    game = Attribute('Game enum value (HOLDEM, OMAHA? OHILO, RAZZ or STUD)')
    limit = Attribute('Limit enum value (NL, PL or FL)')
    ident = Attribute('Unique id of the hand history.')
    last_ident = Attribute('Previous hand history id.')
    currency = Attribute('Currency of the hand history.')
    total_pot = Attribute('Total pot Decimal.')

    tournament_ident = Attribute('Unique tournament id.')
    tournament_name = Attribute('Name of the tournament.')
    tournament_level = Attribute('Tournament level.')

    def parse_header():
        """Parses only the header of a hand history. It is used for quick looking into the hand
        history for basic informations:
            ident, date, game, game_type, limit, money_type, sb, bb, buyin, rake, currency
        by parsing the least lines possible to get these.
        """

    def parse():
        """Parses the body of the hand history, but first parse header if not yet parsed."""


class HandHistoryError(Exception):
    pass


class StreetError(HandHistoryError):
    pass


class _BaseStreet(object):
    def __init__(self, street_lines):
        self.pot = None
        self.cards = None
        self.actions = None
        # Street can be empty with no board and no actions
        if street_lines:
            self._parse_board(street_lines[0])
            self._parse_actions(street_lines[1:])

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

    def __repr__(self):
        return unicode(self).encode('utf8')

    def __unicode__(self):
        cards = " ".join(unicode(c) for c in self.cards)
        return "[%s] (%s)" % (cards, self.pot)

    @property
    def _all_combinations(self):
        if len(self.cards) < 3:
            raise StreetError('Not enough cards')
        return itertools.combinations(self.cards, 2)

    @cached_property
    def is_rainbow(self):
        return all(first.suit != second.suit for first, second in self._all_combinations)

    @cached_property
    def is_monotone(self):
        return all(first.suit == second.suit for first, second in self._all_combinations)

    @cached_property
    def has_triplet(self):
        return all(first.rank == second.rank for first, second in self._all_combinations)

    @cached_property
    def has_pair(self):
        return any(first.rank == second.rank for first, second in self._all_combinations)

    @cached_property
    def has_straightdraw(self):
        return any(1 <= diff <= 3 for diff in self._get_differences())

    @cached_property
    def has_gutshot(self):
        return any(1 <= diff <= 4 for diff in self._get_differences())

    @cached_property
    def has_flushdraw(self):
        return any(first.suit == second.suit for first, second in self._all_combinations)

    def _get_differences(self):
        return (Rank.difference(first.rank, second.rank)
                for first, second in self._all_combinations)


class _BaseHandHistory(object):
    """Abstract base class for *all* kinds of parser."""

    def __init__(self, hand_text):
        """Save raw hand history."""
        self.raw = hand_text.strip()
        self._header_parsed = False
        self._parsed = False

    @classmethod
    def from_file(cls, filename):
        with io.open(filename) as f:
            return cls(f.read())

    def __unicode__(self):
        return "<{}: #{}>" .format(self.__class__.__name__, self.ident)

    def __str__(self):
        return unicode(self).decode('utf-8')

    @property
    def board(self):
        """Calculates board from flop, turn and river."""
        board = []
        if self.flop:
            board.extend(self.flop.cards)
            if self.turn:
                board.extend(self.turn.cards)
                if self.river:
                    board.extend(self.river.cards)
        return tuple(board) if board else None

    def _parse_date(self, date_string):
        """Parse the date_string and return a datetime object as UTC."""
        date = datetime.strptime(date_string, self._date_format)
        return self._tz.localize(date).astimezone(pytz.UTC)

    def _init_seats(self, player_num):
        return [_Player(name='Empty Seat %s' % seat, stack=0, seat=seat, combo=None)
                for seat in range(1, player_num + 1)]


class _SplittableHandHistoryMixin(object):
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


class _FullTiltPokerStarsMixin(object):
    """Common functionality between Full Tilt Poker and PokerStars hand histories."""

    _hero_re = re.compile(r"^Dealt to (?P<hero_name>.*) \[(..) (..)\]$")
    _showdown_re = re.compile(r"^Seat (\d): (?P<name>.*) showed .* and won")

    def parse(self):
        """Parses the body of the hand history, but first parse header if not yet parsed."""
        if not self._header_parsed:
            self.parse_header()

        self._parse_seats()
        self._parse_streets()
        self._parse_show_down()

        self._del_split_vars()
        self._parsed = True

    def _get_preflop_lines(self):
        start = self._sections[0] + 3
        stop = self._sections[1]
        return self._splitted[start + 1:stop]

    def _get_street_lines(self, street):
        try:
            start = self._splitted.index(street) + 1
        except ValueError:
            return
        stop = self._splitted.index('', start)
        return self._splitted[start:stop]

    def _get_players(self, init_seats, start_line_index):
        hole_cards_line = self._splitted[self._sections[0] + 2]
        hero_match = self._hero_re.match(hole_cards_line)
        hero_name = hero_match.group('hero_name')

        players = self._init_seats(init_seats)
        for line in self._splitted[start_line_index:]:
            match = self._seat_re.match(line)
            if not match:
                # we reached the end of the players section
                break
            seat = int(match.group('seat'))
            player_name = match.group('name')
            index = seat - 1
            combo = None
            if player_name == hero_name:
                combo = Combo(hero_match.group(2) + hero_match.group(3))
                hero_index = index
            players[index] = _Player(name=player_name, seat=seat, combo=combo,
                                     stack=_make_int(match.group('stack')))

        return players, seat, hero_index

    def _parse_show_down(self):
        potline = self._splitted[self._sections[-1] + 2]
        pot_match = self._pot_re.match(potline)
        self.total_pot = int(pot_match.group(1))

        self.show_down = 'SHOW DOWN' in self._splitted

        winners = set()
        start = self._sections[-1] + 4
        for line in self._splitted[start:]:
            if not self.show_down and "collected" in line:
                winner_match = self._winner_re.match(line)
                winners.add(winner_match.group('name'))
            elif self.show_down and "won" in line:
                showdown_match = self._showdown_re.match(line)
                winners.add(showdown_match.group('name'))

        self.winners = tuple(winners)
