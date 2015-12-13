# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function

"""
    Poker hand history parser module.
"""

import io
import itertools
from collections import namedtuple
from datetime import datetime
import pytz
from zope.interface import Interface, Attribute
from cached_property import cached_property
from .card import Rank


class Seat(object):
    def __init__(self):
        self.name  = None
        """The player name."""
        self.stack = None
        """The intial stack of the player at the beginning of the hand."""
        self.holecards = None
        """rename to Combo? the two cards of the player (None if unknown)"""

class PlayerAction(object):
    def __init__(self):
        self.seat = None
        """The seat index of the player perfoming the action."""
        self.action = None
        """The kind of action. I.e. Fold, Check, Call, Bet or Raise."""
        self.amount = None
        """The amount of Bet/Call/Raise."""

class Board(object):
    def __init__(self, cards):
        self.cards = cards
        self._all_combinations = itertools.combinations(self.cards, 2)

    @cached_property
    def is_rainbow(self):
        return all(first.suit != second.suit for first, second in self._all_combinations)

    @cached_property
    def is_monotone(self):
        return all(first.suit == second.suit for first, second in self._all_combinations)

    @cached_property
    def is_triplet(self):
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

class HandHistoryHeader(object):
    """Not all attributes are available in all room's hand
    histories, missing attributes are always None. This contains the most properties, available in
    any pokerroom hand history, so you always have to deal with None values.
    """
    def __init__(self, **kwargs):
        self.date = None
        """Date of the hand history."""
        self.game = None
        """Game enum value (HOLDEM, OMAHA? OHILO, RAZZ or STUD"""
        self.game_type = None
        """GameType enum value (CASH, TOUR or SNG)"""
        self.limit = None
        """Limit enum value (NL, PL or FL)"""
        self.ident = None
        """Unique id of the hand history."""
        self.currency = None
        """Currency of the hand history."""
        self.tournament_ident = None
        """Unique tournament id."""
        self.tournament_name = None
        """Name of the tournament."""
        self.tournament_level = None
        """Tournament level."""
        self.table_name = None
        """Name of the Table"""
        self.max_players = None
        """Maximum number of players can sit on the table."""
        self.sb = None
        """Small blind size."""
        self.bb = None
        """Big blind size."""
        self.buyin = None
        """Buyin with rake."""

        # overwrite all attributes with the constructor arguments
        self.__dict__.update(kwargs)

class HandHistory(HandHistoryHeader):
    """Extend the Header by the real game information"""
    def __intit__(self, text, **kwargs):
        super(HandHistory,self).__init__(**kwargs)
        # now the header is initialized, i.e. we know number of players etc.

        self.text = text
        """Store the original text of the handhistory."""

        self.blinds = None
        """ The amount of blinds payd bevore holecards are dealt."""

        # Street informations
        self.preflopactions = None
        """Street instance for preflop actions."""
        self.flopactions = None
        """Street instance for flop actions. None hand ended preflop."""
        self.turnactions = None
        """Street instance for turn actions. None if hand ended on flop."""
        self.riveractions = None
        """Street instance for river actions. None if hand ended on turn."""
        self.showdown = None
        """True if there was a showdown, False otherwise."""

        # Player informations
        self.seats = [Seat() for i in range(self.max_players)]
        """List of player instances. (List because we need it to be mutable.)"""
        self.button = None
        """The seat index (int) of the button seat."""

        # Game informations
        self.rake = None
        """The amoutn rake paid."""
        self.total_pot = None
        """Total pot Decimal."""
        self.board = None
        """The cards of the Board. Tuple of 3,4 or 5 cards"""

    def __unicode__(self):
        return "<{}: #{}>" .format(self.__class__.__name__, self.ident)

    def __str__(self):
        return unicode(self).decode('utf-8')
