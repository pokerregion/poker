import itertools
from functools import total_ordering
from ._common import _MultiValueEnum, _ReprMixin


class Suit(_MultiValueEnum):
    CLUBS =    '♣', 'c', 'C', 'clubs'
    DIAMONDS = '♦', 'd', 'D', 'diamonds'
    HEARTS =   '♥', 'h', 'H', 'hearts'
    SPADES =   '♠', 's', 'S', 'spades'


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
        # so we always get a Rank instance even if string were passed in
        first, second = cls(first), cls(second)
        rank_list = list(cls)
        return abs(rank_list.index(first) - rank_list.index(second))


FACE_RANKS = Rank('J'), Rank('Q'), Rank('K')

BROADWAY_RANKS = Rank('T'), Rank('J'), Rank('Q'), Rank('K'), Rank('A')


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


DECK = tuple(Card(str(rank) + str(suit)) for rank, suit in
             itertools.product(list(Rank), list(Suit)))
