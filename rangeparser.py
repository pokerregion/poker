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
from enum import Enum, EnumMeta
from types import DynamicClassAttribute
from functools import total_ordering


class _MultiMeta(EnumMeta):
    def __new__(metacls, cls, bases, classdict):
        # members already collected from Enum class
        enum_class = super(_MultiMeta, metacls).__new__(metacls, cls, bases, classdict)

        # make sure we only have tuple values, not single values
        for member in enum_class.__members__.values():
            if not isinstance(member._value_, tuple):
                raise ValueError('{!r}, should be tuple'.format(member._value_))
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
        return "{0}({1}{2}{1})".format(self.__class__.__qualname__, apostrophe, self)

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


@total_ordering
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
                raise ValueError('{!r}, Not a pair! Maybe you need to specify a suit?'
                                 .format(hand))
            self._suitedness = Suitedness.NOSUIT
        elif len(hand) == 3:
            suitedness = hand[2].lower()
            if first == second:
                raise ValueError("{!r}; pairs can't have a suit: {!r}".format(hand, suitedness))
            self.suitedness = suitedness

        self._set_ranks_in_order(first, second)

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
        first = Rank.make_random()
        second = Rank.make_random()
        self._set_ranks_in_order(first, second)
        if first == second:
            self._suitedness = Suitedness.NOSUIT
        else:
            self._suitedness = random.choice([Suitedness.SUITED, Suitedness.OFFSUIT])
        return self

    def _set_ranks_in_order(self, first, second):
        # set as Rank objects.
        self.first, self.second = first, second
        if self._first < self._second:
            self._first, self._second = self._second, self._first

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
        return (self._first in BROADWAY_RANKS and self._second in BROADWAY_RANKS)

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

SMALL_PAIR_HANDS = (Hand('22'), Hand('33'), Hand('44'), Hand('55'))

MID_PAIR_HANDS = (Hand('66'), Hand('77'), Hand('88'), Hand('99'))

BIG_PAIR_HANDS = (Hand('TT'), Hand('JJ'), Hand('QQ'), Hand('KK'), Hand('AA'))

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
            raise ValueError('{!r}, should have a length of 4'.format(combination))
        elif (combination[0] == combination[2] and combination[1] == combination[3]):
            raise ValueError("{!r}, Pair can't have the same suit: {!r}"
                             .format(combination, combination[1]))

        self = super().__new__(cls)
        self._set_cards_in_order(combination[:2], combination[2:])
        return self

    @classmethod
    def from_cards(cls, first, second):
        self = super().__new__(cls)
        first = first.rank.value + first.suit.value
        second = second.rank.value + second.suit.value
        self._set_cards_in_order(first, second)
        return self

    def __str__(self):
        return '{}{}'.format(self._first, self._second)

    def __hash__(self):
        return hash(self._first) + hash(self._second)

    def __eq__(self, other):
        return self._first == other._first and self._second == other._second

    def __lt__(self, other):
        if not self.is_pair() and other.is_pair():
            return True
        elif self.is_pair() and not other.is_pair():
            return False

        # suits matter
        # these comparisons suppose that cards are ordered (higher first)
        if self._first == other._first:
            return self._second < other._second
        else:
            return self._first < other._first

    def _set_cards_in_order(self, first, second):
        self.first, self.second = first, second
        if self._first < self._second:
            self._first, self._second = self._second, self._first

    def is_suited_connector(self):
        return self.is_suited() and self.is_connector()

    def is_suited(self):
        return self._first._suit == self._second._suit

    def is_connector(self):
        # Creates an offsuit Hand or a pair and check if it is a connector.
        suitedness = '' if self.is_pair() else 'o'
        hand = '{}{}{}'.format(self._first._rank, self._second._rank, suitedness)
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


class Range:
    """Parses a range.

        :ivar str range:    Readable range in unicode
    """
    _separator_re = re.compile(r"[, ;]")

    def __init__(self, range=''):
        range = range.upper()

        self._original = range
        self._hands = dict()
        self._range = ''

        # filter out empty matches
        tokens = [tok for tok in self._separator_re.split(range) if tok]

        for token in tokens:
            # XX
            if len(token) == 2 and token == 'XX':
                pass

            # 22, 33
            elif len(token) == 2 and token[0] == token[1]:
                self._hands[Hand(token)] = self._make_combinations_from_pair(token)
                self._range += token

            # AK, J7, AX
            elif len(token) == 2 and token[0] != token[1]:
                pass

            # 33+, 33-
            elif len(token) == 3 and token[0] == token[1]:
                pass

            # AKo, AKs, KXo, KXs
            elif len(token) == 3 and token[-1] in ('S', 'O'):
                pass

            # A5+, A5-, QX+, 5X-
            elif len(token) == 3 and token[-1] in ('+', '-'):
                pass

            # 2s2h, AsKc
            elif len(token) == 4 and '+' not in token and '-' not in token:
                pass

            # AJo+, AJs+, A5o-, A5s-, 7Xs+, 76s+
            elif len(token) == 4:
                pass

            # 55-33, 33-55, J8-J4
            elif len(token) == 5:
                pass

            # J8o-J4o, J4o-J8o, 76s-74s, 74s-76s
            elif len(token) == 7:
                pass

    def _make_combinations(self, hand_str):
        first, second = hand_str
        return tuple(Combination(first + s1.value + second + s2.value) for
                     s1, s2 in itertools.combinations_with_replacement(Suit, 2))

    def _make_combinations_from_pair(self, pair):
        rank = pair[0]
        return tuple(Combination(rank + s1.value + rank + s2.value) for
                     # there are no suited pairs
                     s1, s2 in itertools.combinations(Suit, 2))

    @property
    def hands(self):
        return tuple(self._hands.keys())

    @property
    def combinations(self):
        # flat out tuple of tuples
        return tuple(v for t in self._hands.values() for v in t)

