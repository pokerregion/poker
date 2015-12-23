# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function

"""
    Poker hand history parser module.
"""

import itertools
from cached_property import cached_property
from . import Action
from .card import Card
from ._common import _ReprMixin


class Player(_ReprMixin):
    __slots__ = ('name', 'stack', 'combo')

    def __init__(self):
        self.name  = None
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


class HandHistoryHeader(object):
    """Header information for Hand histories like date, hand id

    Not all attributes are available in all room's hand histories, missing
    attributes are always None. This contains the most properties, available in
    any pokerroom hand history, so you always have to deal with None values.
    """
    def __init__(self, **kwargs):
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

        # overwrite all header attributes with the constructor arguments
        header_attributes = {name: value for name, value in kwargs.iteritems() if
                             name in self.__dict__.keys() and not name.startswith('_')}
        self.__dict__.update(header_attributes)


class HandHistory(_ReprMixin, HandHistoryHeader):
    """Extend the Header by the real game information"""
    def __init__(self, raw=None, **kwargs):
        super(HandHistory, self).__init__(**kwargs)
        # now the header is initialized, i.e. we know number of players etc.

        self.raw = raw
        """Store the original text of the handhistory (stripped)."""

        self.blinds = None
        """The amount of blinds payed before holecards are dealt."""

        # Player informations
        self.players = [Player() for _ in range(self.max_players)]
        """List of player instances. (List because we need it to be mutable.)"""

        self.button = None
        """The :class:`Player` player of the button seat."""

        # Street informations
        self.preflopactions = None
        """Street instance for preflop actions."""

        self.flopactions = None
        """Street instance for flop actions. None hand ended preflop."""

        self.turnactions = None
        """Street instance for turn actions. None if hand ended on flop."""

        self.riveractions = None
        """Street instance for river actions. None if hand ended on turn."""

        self.has_showdown = None
        """True if there was a showdown, False otherwise."""

        # Game informations
        self.rake = None

        self.total_pot = None

        self.board = None
        """The cards of the Board. Tuple of 3, 4 or 5 cards"""

        # overwrite all attributes with the constructor arguments
        self.__dict__.update(kwargs)

    def player(self, name):
        """Get the :class:`Player` by name."""
        for player in self.players:
            if player.name == name:
                return player

    def __unicode__(self):
        return "<{}HandHistory: #{}>" .format(self.room, self.ident)


class ParserMode(enum.Enum):
    FULL = 'full'
    """Read full handhistory"""

    HEADER = 'header'
    """Only read headers"""

    RAW = 'raw'
    """Don't parse anything, only split the lines into separate chunks,
    each containing just one hand history."""

