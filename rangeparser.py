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
_FACE_CARDS = ('J', 'Q', 'K')
_BROADWAY_CARDS = ('T', 'J', 'Q', 'K', 'A')
_SUITS = 'cdhs'

class RangeSyntaxError(SyntaxError):
    """Thrown when range syntax cannot be parsed."""

class InvalidRank(ValueError):
    pass

class InvalidCard(ValueError):
    pass

class InvalidHand(ValueError):
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
        if len(rank) != 1:
            raise InvalidRank('{!r}, should be 1 char long. Rank has no suit.'.format(rank))
        if rank not in RANKS:
            raise InvalidRank('{!r}, should be one of {}'.format(rank, RANKS))

        self.rank = rank

    @classmethod
    def make_random(cls):
        return cls(random.choice(RANKS))

    def __eq__(self, other):
        return self.rank == other.rank

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return RANKS.index(self.rank) < RANKS.index(other.rank)

    def __unicode__(self):
        return self.rank

    def __str__(self):
        return unicode(self).encode('utf8')

    def __repr__(self):
        return "{}('{!s}')".format(self.__class__.__name__, self)


class Card(Rank):
    __slots__ = ('rank', 'suit')

    def __init__(self, card):
        if len(card) != 2:
            raise InvalidCard('length should be two in {!r}'.format(card))
        elif not isinstance(card, basestring):
            raise TypeError('Should be text!')

        super(Card, self).__init__(card[0])
        suit = card[1].lower()

        if suit not in SUITS:
            raise InvalidCard('{!r}, suit "{}" should be one of {}'.format(card, suit, SUITS))

        self.suit = suit

    @classmethod
    def make_random(cls):
        rank = super(Card).make_random(cls)
        suit = random.choice(SUITS)
        return cls(rank + suit)

    @classmethod
    def from_rank(cls, rank, suit):
        if not isinstance(rank, Rank):
            raise TypeError('Should be Rank')
        return cls(rank.rank + suit)

    def __unicode__(self):
        return self.rank + self.suit

    def is_face(self):
        return self.rank in _FACE_CARDS

    def is_broadway(self):
        return self.rank in _BROADWAY_CARDS


@total_ordering
class Hand(object):
    """General hand without a precise suit.

    Only knows about two ranks and suitedness.
    :ivar Rank first:    first rank
    :ivar Rank second:   second ank
    :ivar unicode suit:  'o' for offsuit 's' for suited, '' for pairs
    """
    __slots__ = ('first', 'second', 'suit')

    def __init__(self, hand):
        if not isinstance(hand, basestring):
            raise TypeError('Should be unicode!')
        elif len(hand) not in (2, 3):
            raise InvalidHand('Length should be 2 (pair) or 3 (hand)')

        try:
            first, second = Rank(hand[0]), Rank(hand[1])
        except InvalidRank as e:
            raise InvalidHand('{!r}, invalid rank: {}'.format(hand, e))

        if len(hand) == 2:
            if first != second:
                raise InvalidHand('{!r}, Not a pair! Maybe you need to specify a suit?'
                                  .format(hand))
            self.suit = ''
        elif len(hand) == 3:
            suit = hand[2].lower()
            if first == second:
                raise InvalidHand("{!r}; pairs can't have a suit: {!r}".format(hand, suit))
            elif suit not in ('s', 'o'):
                raise InvalidHand('{!r}, wrong suit: {!r}'.format(hand, suit))
            self.suit = suit

        if first > second:
            self.first, self.second = first, second
        else:
            self.first, self.second = second, first

    @classmethod
    def from_ranks(cls, first, second, suit=''):
        if not isinstance(first, Rank) or not isinstance(second, Rank):
            raise TypeError('Should be Rank!')
        return cls(first.rank + second.rank + suit)

    def __eq__(self, other):
        # AKs != AKo, because AKs is better
        return (self.first == other.first and
                self.second == other.second and
                self.suit == other.suit)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        # pairs are better than non-pairs
        if not self.is_pair() and other.is_pair():
            return True
        elif self.is_pair() and not other.is_pair():
            return False
        elif (not self.is_pair() and not other.is_pair() and
                self.first == other.first and self.second == other.second
                and self.suit != other.suit):
            # when Rank match, only suit is the deciding factor
            # so, offsuit hand is 'less' than suited
            return self.suit == 'o'
        else:
            return self.first <= other.first and self.second < other.second

    def __unicode__(self):
        return '{}{}{}'.format(self.first, self.second, self.suit)

    def __str__(self):
        return unicode(self).encode('utf8')

    def __repr__(self):
        return "Hand('{!s}')".format(self)

    def is_suited(self):
        # pairs are neither suited
        return self.suit == 's'

    def is_offsuit(self):
        # nor offsuits
        return self.suit == 'o'

    def is_connector(self):
        return RANKS.index(self.first.rank) - RANKS.index(self.second.rank) == 1

    def is_one_gapper(self):
        return RANKS.index(self.first.rank) - RANKS.index(self.second.rank) == 2

    def is_two_gapper(self):
        return RANKS.index(self.first.rank) - RANKS.index(self.second.rank) == 3

    def is_suited_connector(self):
        return self.is_connector() and self.is_suited()

    def is_broadway(self):
        return (self.first.rank in _BROADWAY_CARDS
                and self.second.rank in _BROADWAY_CARDS)

    def is_pair(self):
        return self.first == self.second

class Range(object):
    """Parses a range.

        :ivar set hands:    Set of hands
        :ivar str range:    Readable range in unicode
    """
