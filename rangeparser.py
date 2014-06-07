"""
    Rangeparser
    ~~~~~~~~~~~

    Parses human readable ranges like "22+ 54s 76s 98s AQo+" to a set of hands.

    It's very fault tolerant, makes it possible to make ranges fast.

    :copyright: (c) 2014 by Walkman
    :license: MIT, see LICENSE file for more details.
"""
import random
from enum import Enum, EnumMeta


__all__ = ['Suit', 'Rank', 'Card', 'FACE_RANKS', 'BROADWAY_RANKS']


class _MultiMeta(EnumMeta):
    def __new__(metacls, cls, bases, classdict):
        # members already collected from Enum class
        enum_class = super(_MultiMeta, metacls).__new__(metacls, cls, bases, classdict)
        # make sure we only have tuple values, not single values
        for member in enum_class.__members__.values():
            if not isinstance(member.value, tuple):
                raise ValueError('{!r}, should be tuple'.format(member.value))
        return enum_class

    def __call__(cls, suit):
        for member in cls:
            if suit in member.value:
                return member
        return super().__call__(suit)


class _MultiValueEnum(Enum, metaclass=_MultiMeta):
    @classmethod
    def make_random(cls):
        return random.choice(list(cls))

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            names = self.__class__._member_names_
            return names.index(self.name) < names.index(other.name)
        return NotImplemented

    def __str__(self):
        return str(self.value[0])

    def __repr__(self):
        apostrophe = "'" if isinstance(self.value[0], str) else ''
        return "{0}({1}{2}{1})".format(self.__class__.__qualname__, apostrophe,
                                       self)


class Suit(_MultiValueEnum):
    CLUBS =    '♣', 'c', 'C'
    DIAMONDS = '♦', 'd', 'D'
    HEARTS =   '♥', 'h', 'H'
    SPADES =   '♠', 's', 'S'


class Suitedness(_MultiValueEnum):
    SUITED =  's', 'S'
    OFFSUIT = 'o', 'O'
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
