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


__all__ = ['Suit', 'Rank']


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
        return self.value[0]

    def __repr__(self):
        return "{}('{!s}')".format(self.__class__.__qualname__, self)


class Suit(_MultiValueEnum):
    CLUBS =    '♣', 'c', 'C'
    DIAMONDS = '♦', 'd', 'D'
    HEARTS =   '♥', 'h', 'H'
    SPADES =   '♠', 's', 'S'


class Rank(_MultiValueEnum):
    DEUCE = '2',
    THREE = '3',
    FOUR = '4',
    FIVE = '5',
    SIX = '6',
    SEVEN = '7',
    EIGHT = '8',
    NINE = '9',
    TEN = 'T', 't'
    JACK = 'J', 'j'
    QUEEN = 'Q', 'q'
    KING = 'K', 'k'
    ACE = 'A', 'a'

