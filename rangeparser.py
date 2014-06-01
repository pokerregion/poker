"""
    Rangeparser
    ~~~~~~~~~~~

    Parses human readable ranges like "22+ 54s 76s 98s AQo+" to a set of hands.

    It's very fault tolerant, makes it possible to make ranges fast.

    :copyright: (c) 2014 by Walkman
    :license: MIT, see LICENSE file for more details.
"""

import re
import random
import itertools
from functools import total_ordering


RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
FACE_RANKS = ('J', 'Q', 'K')
BROADWAY_RANKS = ('T', 'J', 'Q', 'K', 'A')
SUITS = ('c', 'd', 'h', 's')    # clubs, diamonds, hearts, spades in increasing order
UNICODE_SUITS = ('♣', '♦', '♥', '♠')

CARDS = tuple(r + s for r, s in itertools.product(RANKS, UNICODE_SUITS))
FACE_CARDS = tuple(r + s for r, s in itertools.product(FACE_RANKS, UNICODE_SUITS))
BROADWAY_CARDS = tuple(r + s for r, s in itertools.product(BROADWAY_RANKS, UNICODE_SUITS))

class RangeSyntaxError(SyntaxError):
    """Thrown when range syntax cannot be parsed."""

class InvalidSuit(ValueError):
    pass

class InvalidRank(ValueError):
    pass

class InvalidCard(ValueError):
    pass

class InvalidHand(ValueError):
    pass

class InvalidCombo(Exception):
    pass

class RangeError(Exception):
    """General Exception with Range objects."""

class ReprMixin:
    def __repr__(self):
        return "{}('{!s}')".format(self.__class__.__qualname__, self)


@total_ordering
class Suit(ReprMixin):
    __slots__ = '_suit'

    def __init__(self, suit: str or Suit):
        if isinstance(suit, Suit):
            self._suit = suit._suit
            return

        suit = suit.lower()
        if suit in SUITS:
            self._suit = suit
        elif suit in UNICODE_SUITS:
            # search c, d, h, s value from unicode value
            self._suit = SUITS[UNICODE_SUITS.index(suit)]
        else:
            raise InvalidSuit(repr(suit))

    def __eq__(self, other):
        return self._suit == other._suit

    def __lt__(self, other):
        return self._suit < other._suit

    def __str__(self):
        return UNICODE_SUITS[SUITS.index(self._suit)]


@total_ordering
class Rank(ReprMixin):
    __slots__ = '_rank'

    def __init__(self, rank: str or Rank):
        if isinstance(rank, Rank):
            self._rank = rank._rank
            return

        rank = rank.upper()
        if len(rank) != 1:
            raise InvalidRank('{!r}, should be 1 char long. Rank has no suit.'.format(rank))

        if rank not in RANKS:
            raise InvalidRank('{!r}, should be one of {}'.format(rank, RANKS))

        self._rank = rank

    @classmethod
    def make_random(cls):
        return cls(random.choice(RANKS))

    def __eq__(self, other):
        return self._rank == other._rank

    def __lt__(self, other):
        return RANKS.index(self._rank) < RANKS.index(other._rank)

    def __str__(self):
        return self._rank


class Card(ReprMixin):
    __slots__ = ('_rank', '_suit')

    def __init__(self, card: str or Card):
        if isinstance(card, Card):
            self.rank = card.rank
            self.suit = card.suit
            return

        if len(card) != 2:
            raise InvalidCard('length should be two in {!r}'.format(card))

        self.rank, self.suit = card

    @classmethod
    def make_random(cls):
        rank = super().make_random(cls)
        suit = random.choice(SUITS)
        return cls(rank._rank + suit)

    @classmethod
    def from_rank(cls, rank: Rank, suit: str):
        return cls(rank._rank + suit)

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other):
        # with same ranks, suit counts
        if self.rank == other.rank:
            return self.suit < other.suit
        return self.rank < other.rank

    def __str__(self):
        return self.rank._rank + str(self._suit)

    def is_face(self):
        return self.rank._rank in FACE_RANKS

    def is_broadway(self):
        return self.rank._rank in BROADWAY_RANKS

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value: str or Rank):
        try:
            self._rank = Rank(value)
        except InvalidRank:
            # implicit exception chaining
            raise InvalidCard(repr(value))

    @property
    def suit(self):
        return self._suit

    @suit.setter
    def suit(self, value: str or Suit):
        try:
            self._suit = Suit(value)
        except InvalidSuit:
            # implicit exception chaining
            raise InvalidCard(repr(value))


@total_ordering
class Hand(ReprMixin):
    """General hand without a precise suit.

    Only knows about two ranks and suitedness.
    :ivar Rank first:   first rank
    :ivar Rank second:  second ank
    :ivar str suited:   'o' for offsuit, 's' for suited, '' for pairs
    """
    __slots__ = ('_first', '_second', '_suited')

    def __init__(self, hand: str or Hand):
        if isinstance(hand, Hand):
            self._first = hand._first
            self._second = hand._second
            self._suited = hand._suited

        if len(hand) not in (2, 3):
            raise InvalidHand('Length should be 2 (pair) or 3 (hand)')

        first, second = hand[:2]

        if len(hand) == 2:
            if first != second:
                raise InvalidHand('{!r}, Not a pair! Maybe you need to specify a suit?'
                                  .format(hand))
            self._suited = ''
        elif len(hand) == 3:
            suited = hand[2].lower()
            if first == second:
                raise InvalidHand("{!r}; pairs can't have a suit: {!r}".format(hand, suited))
            self.suited = suited

        self.first, self.second = first, second
        if self.first < self.second:
            self.first, self.second = second, first

    @classmethod
    def from_ranks(cls, first: Rank, second: Rank, suited=''):
        return cls(first.rank._rank + second.rank._rank + suited)

    def __eq__(self, other):
        # AKs != AKo, because AKs is better
        return (self._first == other._first and
                self._second == other._second and
                self._suited == other._suited)

    def __lt__(self, other):
        # pairs are better than non-pairs
        if not self.is_pair() and other.is_pair():
            return True
        elif self.is_pair() and not other.is_pair():
            return False
        elif (not self.is_pair() and not other.is_pair() and
                self._first == other._first and self._second == other._second
                and self._suited != other._suited):
            # when Rank match, only suit is the deciding factor
            # so, offsuit hand is 'less' than suited
            return self._suited == 'o'
        else:
            return self._first <= other._first and self._second < other._second

    def __str__(self):
        return '{}{}{}'.format(self._first, self._second, self._suited)

    def is_suited(self):
        # pairs are neither suited
        return self._suited == 's'

    def is_offsuit(self):
        # nor offsuits
        return self._suited == 'o'

    def is_connector(self):
        return RANKS.index(self._first._rank) - RANKS.index(self._second._rank) == 1

    def is_one_gapper(self):
        return RANKS.index(self._first._rank) - RANKS.index(self._second._rank) == 2

    def is_two_gapper(self):
        return RANKS.index(self._first._rank) - RANKS.index(self._second._rank) == 3

    def is_suited_connector(self):
        return self.is_suited() and self.is_connector()

    def is_broadway(self):
        return (self._first._rank in BROADWAY_RANKS
                and self._second._rank in BROADWAY_RANKS)

    def is_pair(self):
        return self._first == self._second

    def _setrank(self, attribute, value):
        try:
            setattr(self, attribute, Rank(value))
        except InvalidRank as e:
            # implicit exception chain
            raise InvalidHand('{!r}'.format(value))

    @property
    def first(self):
        return self._first

    @first.setter
    def first(self, value: str or Rank):
        self._setrank('_first', value)

    @property
    def second(self):
        return self._second

    @second.setter
    def second(self, value: str or Rank):
        self._setrank('_second', value)

    @property
    def suited(self):
        return self._suited

    @suited.setter
    def suited(self, value):
        value = value.lower()
        if value.lower() not in ('s', 'o', None):
            raise InvalidHand('wrong suit: {!r}'.format(value))
        self._suited = value


@total_ordering
class Combo(ReprMixin):
    __slots__ = ('_first', '_second')

    def __init__(self, combo):
        if len(combo) != 4:
            raise InvalidCombo('{!r}, should have a length of 4'.format(combo))
        elif combo[0] == combo[2] and combo[1] == combo[3]:
            raise InvalidCombo("{!r}, Pair can't have the same suit: {!r}".format(combo, combo[1]))
        self.first, self.second = combo[:2], combo[2:]

    def _make_hands(self, other):
        if self.is_pair():
            suit1 = ''
        elif self.is_suited():
            suit1 = 's'
        else:
            suit1 = 'o'

        if other.is_pair():
            suit2 = ''
        elif other.is_suited():
            suit2 = 's'
        else:
            suit2 = 'o'

        h1 = Hand('{}{}{}'.format(self._first._rank, self._second._rank, suit1))
        h2 = Hand('{}{}{}'.format(other._first._rank, other._second._rank, suit2))
        return h1, h2

    def __eq__(self, other):
        hand1, hand2 = self._make_hands(other)
        return hand1 == hand2

    def __lt__(self, other):
        hand1, hand2 = self._make_hands(other)
        return hand1 < hand2

    def __str__(self):
        return '{}{}'.format(self._first, self._second)

    def is_pair(self):
        return self._first._rank == self._second._rank

    def is_suited(self):
        return self._first._suit == self._second._suit

    def is_connector(self):
        # creates an offsuit Hand or a pair and check if that Hand is a connector
        suit = '' if self.is_pair() else 'o'
        hand = '{}{}{}'.format(self._first._rank, self._second._rank, suit)
        return Hand(hand).is_connector()

    def is_suited_connector(self):
        return self.is_suited() and self.is_connector()

    def is_broadway(self):
        return self._first.is_broadway() and self._second.is_broadway()

    def _set_card(self, attribute, value):
        try:
            setattr(self, attribute, Card(value))
        except InvalidCard:
            raise InvalidCombo(repr(value))

    @property
    def first(self):
        return self._first

    @first.setter
    def first(self, value):
        self._set_card('_first', value)

    @property
    def second(self):
        return self._second

    @second.setter
    def second(self, value):
        self._set_card('_second', value)

    """Parses a range.

        :ivar set hands:    Set of hands
        :ivar str range:    Readable range in unicode
    """
