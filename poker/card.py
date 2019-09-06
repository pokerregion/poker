import itertools
from functools import total_ordering
from ._common import PokerEnum, _ReprMixin


__all__ = ["Suit", "Rank", "Card", "FACE_RANKS", "BROADWAY_RANKS"]


class Suit(PokerEnum):
    CLUBS = "♣", "c", "clubs"
    DIAMONDS = "♦", "d", "diamonds"
    HEARTS = "♥", "h", "hearts"
    SPADES = "♠", "s", "spades"
    # Can't make alias with redefined value property
    # because of a bug in stdlib enum module (line 162)
    # C = '♣', 'c', 'C', 'clubs'


class Rank(PokerEnum):
    DEUCE = "2", 2
    THREE = "3", 3
    FOUR = "4", 4
    FIVE = "5", 5
    SIX = "6", 6
    SEVEN = "7", 7
    EIGHT = "8", 8
    NINE = "9", 9
    TEN = "T", 10
    JACK = ("J",)
    QUEEN = ("Q",)
    KING = ("K",)
    ACE = "A", 1

    @classmethod
    def difference(cls, first, second):
        """Tells the numerical difference between two ranks."""

        # so we always get a Rank instance even if string were passed in
        first, second = cls(first), cls(second)
        rank_list = list(cls)
        return abs(rank_list.index(first) - rank_list.index(second))


FACE_RANKS = Rank("J"), Rank("Q"), Rank("K")

BROADWAY_RANKS = Rank("T"), Rank("J"), Rank("Q"), Rank("K"), Rank("A")


class _CardMeta(type):
    def __new__(metacls, clsname, bases, classdict):
        """Cache all possible Card instances on the class itself."""
        cls = super(_CardMeta, metacls).__new__(metacls, clsname, bases, classdict)
        cls._all_cards = list(
            cls(f"{rank}{suit}") for rank, suit in itertools.product(Rank, Suit)
        )
        return cls

    def make_random(cls):
        """Returns a random Card instance."""
        self = object.__new__(cls)
        self.rank = Rank.make_random()
        self.suit = Suit.make_random()
        return self

    def __iter__(cls):
        return iter(cls._all_cards)


@total_ordering
class Card(_ReprMixin, metaclass=_CardMeta):
    """Represents a Card, which consists a Rank and a Suit."""

    __slots__ = ("rank", "suit")

    def __new__(cls, card):
        if isinstance(card, cls):
            return card

        if len(card) != 2:
            raise ValueError("length should be two in %r" % card)

        self = object.__new__(cls)
        self.rank = Rank(card[0])
        self.suit = Suit(card[1])
        return self

    def __hash__(self):
        return hash(self.rank) + hash(self.suit)

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.rank == other.rank and self.suit == other.suit
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented

        # with same ranks, suit counts
        if self.rank == other.rank:
            return self.suit < other.suit
        return self.rank < other.rank

    def __str__(self):
        return f"{self.rank}{self.suit}"

    @property
    def is_face(self):
        return self.rank in FACE_RANKS

    @property
    def is_broadway(self):
        return self.rank in BROADWAY_RANKS
