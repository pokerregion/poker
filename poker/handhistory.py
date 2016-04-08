# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function

"""
    Poker hand history parser module.
"""

import itertools
import enum
from cached_property import cached_property
from . import Action
from .card import Card
from ._common import _ReprMixin


class Player(_ReprMixin):
    __slots__ = ('name', 'stack', 'combo')

    def __init__(self):
        self.name = None
        """The player name."""

        self.seat = None
        """Seat number of the player."""

        self.stack = None
        """The intial stack of the player at the beginning of the hand."""

        self.combo = None
        """The two cards of the player. :class:`hand.Combo` instance"""

    def __unicode__(self):
        if self.name is None:
            return "<N/A>"
        return '{} [{}] ({})'.format(self.name, self.stack, self.combo)


class PlayerAction(_ReprMixin):
    __slots__ = ('player_name', 'action', 'amount')

    def __init__(self, player_name, action, amount=None):
        self.player_name = player_name

        self.action = action
        """The kind of action. I.e. Fold, Check, Call, Bet or Raise."""

        self.amount = amount
        """The amount of Bet/Call/Raise."""

    def __unicode__(self):
        action = "{}: {}".format(self.player_name, self.action)
        if self.action in (Action.RAISE, Action.BET):
            action += " {()}".format(self.amount)
        return action


class Board(_ReprMixin):

    def __init__(self, *cards):
        self.cards = [Card(c) for c in cards]
        self._all_combinations = itertools.combinations(self.cards, 2)

    def __unicode__(self):
        return ' '.join(unicode(c) for c in self.cards)

    @cached_property
    def is_rainbow(self):
        return all(first.suit != second.suit for first, second in
                   self._all_combinations)

    @cached_property
    def is_monotone(self):
        return all(first.suit == second.suit for first, second in
                   self._all_combinations)

    @cached_property
    def is_triplet(self):
        return all(first.rank == second.rank for first, second in
                   self._all_combinations)

    @cached_property
    def has_pair(self):
        return any(first.rank == second.rank for first, second in
                   self._all_combinations)

    @cached_property
    def has_straightdraw(self):
        return any(1 <= diff <= 3 for diff in self._get_differences())

    @cached_property
    def has_gutshot(self):
        return any(1 <= diff <= 4 for diff in self._get_differences())

    @cached_property
    def has_flushdraw(self):
        return any(first.suit == second.suit for first, second in
                   self._all_combinations)


class HandHistory(_ReprMixin):
    """Hand history data for every poker room.
    Not all attributes are available in all room's hand histories, missing attributes are
    always None. This contains the most properties, available in any pokerroom hand history,
    so you always have to deal with None values.
    """
    def __init__(self, parser, **overwrite_attributes):
        self.parser = parser

        # Header informations. Usually comes from first line of the HandHistory.
        self.date = None
        self.room = None

        self.game = None
        """Game enum value (HOLDEM, OMAHA, OHILO, RAZZ or STUD"""

        self.game_type = None
        """GameType enum value (CASH, TOUR or SNG)"""

        self.limit = None
        """Limit enum value (NL, PL or FL)"""

        self.ident = None
        """Unique id of the hand history."""

        self.currency = None

        self.tournament_ident = None
        """Unique tournament id."""

        self.tournament_name = None
        self.tournament_level = None
        self.table_name = None

        self.max_players = None
        """Maximum number of players can sit on the table."""

        self.sb = None
        self.bb = None

        self.buyin = None
        """Buyin with rake."""

        self.blinds = None
        """The amount of blinds payed before holecards are dealt."""

        # Player informations
        self.players = None
        """Tuple of player instances."""

        self.button = None
        """The :class:`Player` player of the button seat."""

        # Street informations
        self.preflop = None
        """Street instance for preflop actions."""

        self.flop = None
        """Street instance for flop actions. None hand ended preflop."""

        self.turn = None
        """Street instance for turn actions. None if hand ended on flop."""

        self.river = None
        """Street instance for river actions. None if hand ended on turn."""

        self.showdown = None
        """Showdown instance for showdown actions and card. None if there was no showdown."""

        # Game informations
        self.rake = None

        self.total_pot = None

        self.__dict__.update(overwrite_attributes)

    def __unicode__(self):
        return "<{}HandHistory: #{}>" .format(self.room, self.ident)

    @property
    def board(self):
        """The cards of the Board. Tuple of 3, 4 or 5 cards"""
        board = []
        if self.flop:
            board.extend(self.flop.cards)
            if self.turn:
                board.extend(self.turn.cards)
                if self.river:
                    board.extend(self.river.cards)
        return tuple(board)

    def get_player(self, name):
        """Get the :class:`Player` by name."""
        for player in self.players:
            if player.name == name:
                return player


            for ParserClass in self.parserclasses:
                if line.startswith(parser.start_word):
                    yield ParserClass(self.mode, self.raw)


class ParserMode(enum.Enum):
    """Parser mode for hand history parsing"""

    RAW = 'raw'
    """Don't parse anything, only split the lines into separate chunks,
       each containing just one hand history."""

    IDENT = 'ident'
    """Get only hand history IDs nothing else from the stream."""

    HEADER = 'header'
    """Only read headers."""

    FULL = 'full'
    """Read full handhistory."""
