"""
    Rangeparser
    ~~~~~~~~~~~

    Parses human readable ranges like "22+ 54s 76s 98s AQo+" to a set of hands.

    It's very fault tolerant, makes it possible to make ranges fast.

    :copyright: (c) 2014 by Walkman
    :license: MIT, see LICENSE file for more details.
"""
import random
import itertools
from enum import Enum, EnumMeta
from types import DynamicClassAttribute
from functools import total_ordering

__all__ = ['Suit', 'Suitedness', 'Rank', 'Card', 'Hand', 'Combination',
           'FACE_RANKS', 'BROADWAY_RANKS', 'DECK']


class _MultiMeta(EnumMeta):
    def __new__(metacls, cls, bases, classdict):
        # members already collected from Enum class
        enum_class = super(_MultiMeta, metacls).__new__(metacls, cls, bases,
                                                        classdict)
        # make sure we only have tuple values, not single values
        for member in enum_class.__members__.values():
            if not isinstance(member._value_, tuple):
                raise ValueError('{!r}, should be tuple'
                                 .format(member._value_))
        return enum_class

    def __call__(cls, suit):
        for member in cls:
            if suit in member._value_:
                return member
        return super().__call__(suit)


@total_ordering
class _MultiValueEnum(Enum, metaclass=_MultiMeta):
    @classmethod
    def make_random(cls):
        return random.choice(list(cls))

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ == other._value_
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            names = self.__class__._member_names_
            return names.index(self.name) < names.index(other.name)
        return NotImplemented

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        apostrophe = "'" if isinstance(self.value, str) else ''
        return "{0}({1}{2}{1})".format(self.__class__.__qualname__, apostrophe,
                                       self)

    @DynamicClassAttribute
    def value(self):
        """The value of the Enum member."""
        return self._value_[0]


class Suit(_MultiValueEnum):
    CLUBS =    '♣', 'c', 'C'
    DIAMONDS = '♦', 'd', 'D'
    HEARTS =   '♥', 'h', 'H'
    SPADES =   '♠', 's', 'S'


class Suitedness(_MultiValueEnum):
    OFFSUIT = 'o', 'O'
    SUITED =  's', 'S'
    NOSUIT =  '', None


class Rank(_MultiValueEnum):
    DEUCE = '2',
    THREE = '3',
    FOUR =  '4',
    FIVE =  '5',
    SIX =   '6',
    SEVEN = '7',
    EIGHT = '8',
    NINE =  '9',
    TEN =   'T', 't'
    JACK =  'J', 'j'
    QUEEN = 'Q', 'q'
    KING =  'K', 'k'
    ACE =   'A', 'a'


FACE_RANKS = Rank('J'), Rank('Q'), Rank('K')
BROADWAY_RANKS = Rank('T'), Rank('J'), Rank('Q'), Rank('K'), Rank('A')


class _ReprMixin:
    def __repr__(self):
        return "{}('{}')".format(self.__class__.__qualname__, self)


class Card(_ReprMixin):
    __slots__ = ('_rank', '_suit')

    def __new__(cls, card):
        if isinstance(card, Card):
            return card

        if len(card) != 2:
            raise ValueError('length should be two in {!r}'.format(card))

        self = super().__new__(cls)
        self.rank, self.suit = card
        return self

    @classmethod
    def make_random(cls):
        self = super().__new__(cls)
        self._rank = Rank.make_random()
        self._suit = Suit.make_random()
        return self

    def __hash__(self):
        return hash(self._rank) + hash(self._suit)

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other):
        # with same ranks, suit counts
        if self.rank == other.rank:
            return self.suit < other.suit
        return self.rank < other.rank

    def __str__(self):
        return '{}{}'.format(self._rank, self._suit)

    def is_face(self):
        return self._rank in FACE_RANKS

    def is_broadway(self):
        return self._rank in BROADWAY_RANKS

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value):
        self._rank = Rank(value)

    @property
    def suit(self):
        return self._suit

    @suit.setter
    def suit(self, value):
        self._suit = Suit(value)


DECK = tuple(Card(str(rank) + str(suit)) for rank, suit in
             itertools.product(list(Rank), list(Suit)))


@total_ordering
class Hand(_ReprMixin):
    """General hand without a precise suit.

    Only knows about two ranks and suitedness.
    :ivar Rank first:   first Rank
    :ivar Rank second:  second Rank
    :ivar Suitedness suitedness:  Suitedness signal
    """
    __slots__ = ('_first', '_second', '_suitedness')

    def __new__(cls, hand):
        if isinstance(hand, Hand):
            return hand

        if len(hand) not in (2, 3):
            raise ValueError('Length should be 2 (pair) or 3 (hand)')

        first, second = hand[:2]

        self = super().__new__(cls)

        if len(hand) == 2:
            if first != second:
                raise ValueError('{!r}, Not a pair! '
                                 'Maybe you need to specify a suit?'
                                 .format(hand))
            self._suitedness = Suitedness(None)
        elif len(hand) == 3:
            suitedness = hand[2].lower()
            if first == second:
                raise ValueError("{!r}; pairs can't have a suit: {!r}"
                                 .format(hand, suitedness))
            self.suitedness = suitedness

        self.first, self.second = first, second
        if self._first < self._second:
            self.first, self.second = second, first

        return self

    def __str__(self):
        return '{}{}{}'.format(self._first, self._second, self._suitedness)

    def __hash__(self):
        return hash(self._first) + hash(self._second) + hash(self._suitedness)

    def __eq__(self, other):
        # AKs != AKo, because AKs is better
        return (self._first == other._first and
                self._second == other._second and
                self._suitedness == other._suitedness)

    def __lt__(self, other):
        # pairs are better than non-pairs
        if not self.is_pair() and other.is_pair():
            return True
        elif self.is_pair() and not other.is_pair():
            return False
        elif (not self.is_pair() and not other.is_pair() and
                self._first == other._first and self._second == other._second
                and self._suitedness != other._suitedness):
            # when Rank match, only suit is the deciding factor
            # so, offsuit hand is 'less' than suited
            return self._suitedness == Suitedness.OFFSUIT
        else:
            return self._first <= other._first and self._second < other._second

    @classmethod
    def make_random(cls):
        self = super().__new__(cls)
        self._first = Rank.make_random()
        self._second = Rank.make_random()
        self._suitedness = Suitedness.make_random()
        return self

    def is_suited_connector(self):
        return self.is_suited() and self.is_connector()

    def is_suited(self):
        # pairs are not SUITED
        return self._suitedness == Suitedness.SUITED

    def is_offsuit(self):
        # pairs are not OFFSUITs
        return self._suitedness == Suitedness.OFFSUIT

    def is_connector(self):
        return self.rank_difference == 1

    def is_one_gapper(self):
        return self.rank_difference == 2

    def is_two_gapper(self):
        return self.rank_difference == 3

    @property
    def rank_difference(self):
        rank_list = list(Rank)
        first = rank_list.index(self._first)
        second = rank_list.index(self._second)
        # first >= second always
        return first - second

    def is_broadway(self):
        return (self._first in BROADWAY_RANKS and
                self._second in BROADWAY_RANKS)

    def is_pair(self):
        return self._first == self._second

    @property
    def first(self):
        return self._first

    @first.setter
    def first(self, value):
        self._first = Rank(value)

    @property
    def second(self):
        return self._second

    @second.setter
    def second(self, value):
        self._second = Rank(value)

    @property
    def suitedness(self):
        return self._suitedness

    @suitedness.setter
    def suitedness(self, value):
        self._suitedness = Suitedness(value)


PAIR_HANDS = tuple(Hand(rank.value * 2) for rank in list(Rank))
BIG_PAIR_HANDS = tuple(hand for hand in PAIR_HANDS if hand > Hand('99'))
OFFSUIT_HANDS = tuple(Hand(hand1.value + hand2.value + 'o') for hand1, hand2 in
                      itertools.combinations(list(Rank), 2))
SUITED_HANDS = tuple(Hand(hand1.value + hand2.value + 's') for hand1, hand2 in
                      itertools.combinations(list(Rank), 2))


@total_ordering
class Combination(_ReprMixin):
    __slots__ = ('_first', '_second')

    def __new__(cls, combination):
        if isinstance(combination, Combination):
            return combination

        if len(combination) != 4:
            raise ValueError('{!r}, should have a length of 4'
                             .format(combination))
        elif (combination[0] == combination[2] and
                combination[1] == combination[3]):
            raise ValueError("{!r}, Pair can't have the same suit: {!r}"
                             .format(combination, combination[1]))

        self = super().__new__(cls)
        self.first, self.second = combination[:2], combination[2:]
        return self

    def __str__(self):
        return '{}{}'.format(self._first, self._second)

    def __hash__(self):
        return hash(self._first) + hash(self._second)

    def __eq__(self, other):
        hand1, hand2 = self._make_hands(other)
        return hand1 == hand2

    def __lt__(self, other):
        hand1, hand2 = self._make_hands(other)
        return hand1 < hand2

    def _make_hands(self, other):
        suitedness1 = self._make_suitedness(self)
        suitedness2 = self._make_suitedness(other)
        h1 = Hand('{}{}{}'.format(self._first._rank, self._second._rank,
                                  suitedness1))
        h2 = Hand('{}{}{}'.format(other._first._rank, other._second._rank,
                                  suitedness2))
        return h1, h2

    def _make_suitedness(self, combination):
        if combination.is_pair():
            return Suitedness(None)
        elif combination.is_suited():
            return Suitedness.SUITED
        else:
            return Suitedness.OFFSUIT

    def is_suited_connector(self):
        return self.is_suited() and self.is_connector()

    def is_suited(self):
        return self._first._suit == self._second._suit

    def is_connector(self):
        # Creates an offsuit Hand or a pair and check if it is a connector.
        suitedness = '' if self.is_pair() else 'o'
        hand = '{}{}{}'.format(self._first._rank, self._second._rank,
                               suitedness)
        return Hand(hand).is_connector()

    def is_pair(self):
        return self._first._rank == self._second._rank

    def is_broadway(self):
        return self._first.is_broadway() and self._second.is_broadway()

    @property
    def first(self):
        return self._first

    @first.setter
    def first(self, value):
        self._first = Card(value)

    @property
    def second(self):
        return self._second

    @second.setter
    def second(self, value):
        self._second = Card(value)
