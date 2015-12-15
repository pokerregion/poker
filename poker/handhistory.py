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
from . import Action
from .card import Rank, Card
from ._common import _ReprMixin

class HoleCards(_ReprMixin):
    def __init__(self,c1,c2):
        self.c1 = c1
        self.c2 = c2

    def __unicode__(self):
        return '{} {}'.format(self.c1,self.c2)#.encode('utf-8')

class Seat(_ReprMixin):
    def __init__(self):
        self.name  = None
        """The player name."""
        self.stack = None
        """The intial stack of the player at the beginning of the hand."""
        self.holecards = None
        """rename to Combo? the two cards of the player (None if unknown)"""

    #def __unicode__(self):
    #    return u"{}: {} ({})".format(self.name,float(self.stack), unicode(self.holecards)).decode('utf-8')

    def __unicode__(self):
        if self.name is None:
            return "<empty>"
        return '{}: {} ({})'.format(self.name,float(self.stack), self.holecards)#.encode('utf-8')


class PlayerAction(_ReprMixin):
    def __init__(self, seat, action, amount = None):
        self.seat = seat
        """The seat index of the player perfoming the action."""
        self.action = action
        """The kind of action. I.e. Fold, Check, Call, Bet or Raise."""
        self.amount = amount
        """The amount of Bet/Call/Raise."""

    def __unicode__(self):
        if self.action is Action.RAISE or self.action is Action.BET:
            return "{} {} {}".format(self.seat, self.action, float(self.amount))
        else:
            return "{} {}".format(self.seat, self.action)

class Board(_ReprMixin):

    def __init__(self, *args):
        self.cards = [arg if type(arg) is Card else Card(arg) for arg in args]
        self._all_combinations = itertools.combinations(self.cards, 2)

    def __unicode__(self):
        return ' '.join([unicode(c) for c in self.cards])

    def append(self,c):
        self.cards.append(c)

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
    def __init__(self, text, **kwargs):
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

    def seat(self,name):
        """
        Get the seat number and the seatinstance by name of player. Return tuple(int, seat)
        """
        for i,s in enumerate(self.seats):
            if s.name == name:
                return i,s


    def __unicode__(self):
        return "<{}: #{}>" .format(self.__class__.__name__, self.ident)

    def __str__(self):
        return unicode(self).decode('utf-8')
