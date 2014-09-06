import itertools
from functools import total_ordering
from ._common import _MultiValueEnum, _ReprMixin


__all__ = ['Suit', 'Rank', 'Card', 'FACE_RANKS', 'BROADWAY_RANKS']


class Suit(_MultiValueEnum):
    CLUBS =    '♣', 'c', 'C', 'clubs'
    DIAMONDS = '♦', 'd', 'D', 'diamonds'
    HEARTS =   '♥', 'h', 'H', 'hearts'
    SPADES =   '♠', 's', 'S', 'spades'
    # Can't make alias with redefined value property
    # because of a bug in stdlib enum module (line 162)
    # C = '♣', 'c', 'C', 'clubs'


class Rank(_MultiValueEnum):
    DEUCE = '2', 2
    THREE = '3', 3
    FOUR =  '4', 4
    FIVE =  '5', 5
    SIX =   '6', 6
    SEVEN = '7', 7
    EIGHT = '8', 8
    NINE =  '9', 9
    TEN =   'T', 't', 10
    JACK =  'J', 'j'
    QUEEN = 'Q', 'q'
    KING =  'K', 'k'
    ACE =   'A', 'a', 1

    @classmethod
    def difference(cls, first, second):
        """Tells the numerical difference between two ranks."""

        # so we always get a Rank instance even if string were passed in
        first, second = cls(first), cls(second)
        rank_list = list(cls)
        return abs(rank_list.index(first) - rank_list.index(second))


FACE_RANKS = Rank('J'), Rank('Q'), Rank('K')

BROADWAY_RANKS = Rank('T'), Rank('J'), Rank('Q'), Rank('K'), Rank('A')


class _CardMeta(type):
    def __new__(metacls, clsname, bases, classdict):
        """Cache all possible Card instances on the class itself."""
        cls = super().__new__(metacls, clsname, bases, classdict)
        cls._all_cards = list(cls(str(rank) + str(suit))
                              for rank, suit in itertools.product(Rank, Suit))
        return cls

    def make_random(cls):
        """Returns a random Card instance."""
        self = object.__new__(cls)
        self._rank = Rank.make_random()
        self._suit = Suit.make_random()
        return self

    def __iter__(cls):
        return iter(cls._all_cards)


@total_ordering
class Card(_ReprMixin, metaclass=_CardMeta):
    """Represents a Card, which consists a Rank and a Suit."""

    __slots__ = ('_rank', '_suit')

    def __new__(cls, card):
        if isinstance(card, cls):
            return card

        if len(card) != 2:
            raise ValueError('length should be two in {!r}'.format(card))

        self = object.__new__(cls)
        self.rank, self.suit = card
        return self

    def __hash__(self):
        return hash(self._rank) + hash(self._suit)

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self._rank == other._rank and self._suit == other._suit
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented

        # with same ranks, suit counts
        if self.rank == other.rank:
            return self.suit < other.suit
        return self.rank < other.rank

    def __str__(self):
        return '{}{}'.format(self._rank, self._suit)

    @property
    def is_face(self):
        return self._rank in FACE_RANKS

    @property
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
