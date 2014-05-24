# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division

"""
    Rangeparser
    ~~~~~~~~~~~

    Parses human readable ranges like "22+ 54s 76s 98s AQo+" to a set of hands.

    It's very fault tolerant, makes it possible to make ranges fast.

    :copyright: (c) 2014 by Walkman
    :license: MIT, see LICENSE file for more details.
"""

import re
from functools import total_ordering


RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
SUITS = ('c', 'd', 'h', 's')    # clubs, diamonds, spades, hearts in increasing order
_SUITS = 'cdhs'

class RangeSyntaxError(SyntaxError):
    """Thrown when range syntax cannot be parsed."""

class InvalidRank(ValueError):
    pass

class InvalidCard(ValueError):
    pass

    pass

class RangeError(Exception):
    """General Exception with Range objects."""

@total_ordering
class Rank(object):
    __slots__ = 'rank'

    def __init__(self, rank):
        if not isinstance(rank, basestring):
            raise TypeError('Should be text!')

        rank = rank.upper()

        if rank not in RANKS:
            raise InvalidRank(repr(rank))

        self.rank = rank

    @classmethod
    def make_random(cls):
        return cls(random.choice(RANKS))

    def __eq__(self, other):
        return self.rank == other.rank

    def __lt__(self, other):
        return RANKS.index(self.rank) < RANKS.index(other.rank)

    def __unicode__(self):
        return self.rank

    def __str__(self):
        return unicode(self).encode('utf8')

    def __repr__(self):
        return "Rank('{}')".format(self).encode('utf8')


@total_ordering
class Card(object):
    __slots__ = ('rank', 'suit')

    def __init__(self, card):
        if len(card) != 2:
            raise InvalidCard('length should be two in {!r}'.format(card))

        if not isinstance(card, basestring):
            raise TypeError('Should be text!')

        rank, suit = card[0].upper(), card[1].lower()

        if rank not in RANKS:
            raise InvalidCard('Rank {}, should be one of {}'
                              .format(rank, RANKS))
        if suit not in SUITS:
            raise InvalidCard('suit "{}" should be one of {}'
                              .format(suit, SUITS))
        self.rank, self.suit = Rank(rank), suit

    @classmethod
    def make_random(cls):
        rank = random.choice(RANKS)
        suit = random.choice(SUITS)
        return cls(rank + suit)

    @classmethod
    def from_rank(cls, rank, suit):
        if not isinstance(rank, Rank):
            raise TypeError('Should be Rank')
        return cls(rank.rank + suit)

    def __eq__(self, other):
        return self.rank == other.rank

    def __lt__(self, other):
        return self.rank < other.rank

    def __unicode__(self):
        return self.rank.rank + self.suit

    def __str__(self):
        return unicode(self).encode('utf8')

    def __repr__(self):
        return "Card('{}')".format(self).encode('utf8')

    def is_face(self):
        return self.rank.rank in ('J', 'Q', 'K')

    def is_broadway(self):
        return self.rank.rank in ('T', 'J', 'Q', 'K', 'A')

class Range(object):
    """Parses a range.

        :ivar set hands:    Set of hands
        :ivar str range:    Readable range in unicode
    """
