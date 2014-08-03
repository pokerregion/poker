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
from decimal import Decimal
from enum import Enum, EnumMeta
from functools import total_ordering
from types import DynamicClassAttribute


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

    # From Python manual:
    # If a class that overrides __eq__() needs to retain the implementation of __hash__()
    # from a parent class, the interpreter must be told this explicitly
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
    CLUBS =    '♣', 'c', 'C', 'clubs'
    DIAMONDS = '♦', 'd', 'D', 'diamonds'
    HEARTS =   '♥', 'h', 'H', 'hearts'
    SPADES =   '♠', 's', 'S', 'spades'


class Shape(_MultiValueEnum):
    OFFSUIT = 'o', 'O', 'offsuit', 'off'
    SUITED =  's', 'S', 'suited'
    PAIR =  '',


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


@total_ordering
class Hand(_ReprMixin):
    """General hand without a precise suit.

    Only knows about two ranks and shape.
    :ivar Rank first:   first Rank
    :ivar Rank second:  second Rank
    :ivar Shape shape:  Hand shape (pair, suited or offsuit)
    """
    __slots__ = ('_first', '_second', '_shape')

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
            self._shape = Shape.PAIR
        elif len(hand) == 3:
            shape = hand[2].lower()
            if first == second:
                raise ValueError("{!r}; pairs can't have a suit: {!r}".format(hand, shape))
            self.shape = shape

        self._set_ranks_in_order(first, second)

        return self

    def __str__(self):
        return '{}{}{}'.format(self._first, self._second, self._shape)

    def __hash__(self):
        return hash(self._first) + hash(self._second) + hash(self._shape)

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented

        # AKs != AKo, because AKs is better
        return (self._first == other._first and
                self._second == other._second and
                self._shape == other._shape)

    def __lt__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented

        # pairs are better than non-pairs
        if not self.is_pair and other.is_pair:
            return True
        elif self.is_pair and not other.is_pair:
            return False
        elif (not self.is_pair and not other.is_pair and
                self._first == other._first and self._second == other._second
                and self._shape != other._shape):
            # when Rank match, only suit is the deciding factor
            # so, offsuit hand is 'less' than suited
            return self._shape == Shape.OFFSUIT
        elif self._first == other._first:
            return self._second < other._second
        else:
            return self._first < other._first

    @classmethod
    def make_random(cls):
        self = super().__new__(cls)
        first = Rank.make_random()
        second = Rank.make_random()
        self._set_ranks_in_order(first, second)
        if first == second:
            self._shape = Shape.PAIR
        else:
            self._shape = random.choice([Shape.SUITED, Shape.OFFSUIT])
        return self

    def _set_ranks_in_order(self, first, second):
        # set as Rank objects.
        self.first, self.second = first, second
        if self._first < self._second:
            self._first, self._second = self._second, self._first

    @property
    def is_suited_connector(self):
        return self.is_suited and self.is_connector

    @property
    def is_suited(self):
        return self._shape == Shape.SUITED

    @property
    def is_offsuit(self):
        return self._shape == Shape.OFFSUIT

    @property
    def is_connector(self):
        return self.rank_difference == 1

    @property
    def is_one_gapper(self):
        return self.rank_difference == 2

    @property
    def is_two_gapper(self):
        return self.rank_difference == 3

    @property
    def rank_difference(self):
        # self._first >= self._second
        return Rank.difference(self._first, self._second)

    @property
    def is_broadway(self):
        return (self._first in BROADWAY_RANKS and self._second in BROADWAY_RANKS)

    @property
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
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        self._shape = Shape(value)


PAIR_HANDS = tuple(Hand(rank.value * 2) for rank in list(Rank))

OFFSUIT_HANDS = tuple(Hand(hand1.value + hand2.value + 'o') for hand1, hand2 in
                      itertools.combinations(list(Rank), 2))

SUITED_HANDS = tuple(Hand(hand1.value + hand2.value + 's') for hand1, hand2 in
                     itertools.combinations(list(Rank), 2))


@total_ordering
class Combo(_ReprMixin):
    __slots__ = ('_first', '_second')

    def __new__(cls, combo):
        if isinstance(combo, Combo):
            return combo

        if len(combo) != 4:
            raise ValueError('{!r}, should have a length of 4'.format(combo))
        elif (combo[0] == combo[2] and combo[1] == combo[3]):
            raise ValueError("{!r}, Pair can't have the same suit: {!r}"
                             .format(combo, combo[1]))

        self = super().__new__(cls)
        self._set_cards_in_order(combo[:2], combo[2:])
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
        if self.__class__ is other.__class__:
            return self._first == other._first and self._second == other._second
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented

        # Pairs are better than non-pairs
        if not self.is_pair and other.is_pair:
            return True

        elif self.is_pair and not other.is_pair:
            return False

        # suits matter
        # these comparisons suppose that cards are ordered (higher first)
        # pairs are special, because any 2 card can be equal
        elif ((self.is_pair and other.is_pair and self._first == other._first) or
                (self._first._rank == other._first._rank and
                 self._second._rank != other._second._rank)):
            return self._second < other._second

        # same ranks suited go first, in order by Suit rank
        elif (self._first._rank == other._first._rank and
                self._second._rank == other._second._rank):
            if self.is_suited and other.is_offsuit:
                return False
            elif self.is_offsuit and other.is_suited:
                return True
            else:
                # both are suited
                return self._first._suit < other._first._suit
        else:
            return self._first < other._first

    def _set_cards_in_order(self, first, second):
        self.first, self.second = first, second
        if self._first < self._second:
            self._first, self._second = self._second, self._first

    def to_hand(self):
        """Convert combo to Hand object."""
        return Hand('{}{}{}'.format(self.first.rank, self.second.rank, self.shape))

    @property
    def is_suited_connector(self):
        return self.is_suited and self.is_connector

    @property
    def is_suited(self):
        return self._first._suit == self._second._suit

    @property
    def is_offsuit(self):
        return not self.is_suited

    @property
    def is_connector(self):
        # Creates an offsuit Hand or a pair and check if it is a connector.
        shape = '' if self.is_pair else 'o'
        hand = '{}{}{}'.format(self._first._rank, self._second._rank, shape)
        return Hand(hand).is_connector

    @property
    def is_pair(self):
        return self._first._rank == self._second._rank

    @property
    def is_broadway(self):
        return self._first.is_broadway and self._second.is_broadway

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

    @property
    def shape(self):
        if self.is_pair:
            return Shape.PAIR
        elif self.is_suited:
            return Shape.SUITED
        else:
            return Shape.OFFSUIT


@total_ordering
class Range:
    """Parses a range.

        :ivar str range:    Readable range in unicode
    """
    _separator_re = re.compile(r"[, ;]")

    def __init__(self, range=''):
        range = range.upper()

        self._pairs = set()
        self._suiteds = set()
        self._offsuits = set()
        self._range = ''

        # filter out empty matches
        tokens = [tok for tok in self._separator_re.split(range) if tok]

        for token in tokens:
            # XX
            if len(token) == 2 and token == 'XX':
                for card in itertools.combinations('AKQJT98765432', 2):
                    self._add_offsuit(card)
                    self._add_suited(card)
                for rank in 'AKQJT98765432':
                    self._add_pair(rank * 2)

                # full range, no need to parse any more token
                break

            # 22, 33
            elif len(token) == 2 and token[0] == token[1]:
                self._add_pair(token)

            # AK, J7, AX
            elif len(token) == 2 and token[0] != token[1]:
                if token[1] == 'X':
                    for rank in (rank.value for rank in Rank if rank < Rank(token[0])):
                        self._add_suited(token[0] + rank)
                        self._add_offsuit(token[0] + rank)
                else:
                    self._add_offsuit(token)
                    self._add_suited(token)

            # 33+, 33-
            elif len(token) == 3 and token[0] == token[1] and token[-1] in ('+', '-'):
                backward = token[-1] == '-'
                first = Hand(token[:2])
                for pair in sorted(PAIR_HANDS, reverse=backward):
                    if ((not backward and pair >= first) or (backward and pair <= first)):
                        self._add_pair(str(pair))

            # AKo, AKs,
            elif (len(token) == 3 and (token[0] != token[1]) and
                  ('X' not in token) and (token[-1] in ('S', 'O'))):
                if token[-1] == 'S':
                    self._add_suited(token)
                elif token[-1] == 'O':
                    self._add_offsuit(token)

            # KXo, KXs
            elif len(token) == 3 and token[0] != token[1] and token[-1] in ('S', 'O'):
                ranks_to_add = (rank.value for rank in Rank if rank < Rank(token[0]))
                if token[-1] == 'S':
                    func = self._add_suited
                else:
                    func = self._add_offsuit

                for rank in ranks_to_add:
                    func(token[0] + rank)

            # A5+, A5-,
            elif (len(token) == 3 and token[0] != token[1] and
                  token[-1] in ('+', '-') and 'X' not in token):
                smaller, bigger = self._get_ordered(Rank, token[0], token[1])
                if token[-1] == '-':
                    ranks = (rank.value for rank in Rank if rank <= smaller)
                else:
                    ranks = (rank.value for rank in Rank if smaller <= rank < bigger)

                for rank in ranks:
                    self._add_suited(token[0] + rank)
                    self._add_offsuit(token[0] + rank)

            # QX+, 5X-
            elif len(token) == 3 and token[1] == 'X' and token[-1] in ('+', '-'):
                if token[-1] == '-':
                    first_ranks = (rank for rank in Rank if rank <= Rank(token[0]))
                else:
                    first_ranks = (rank for rank in Rank if rank >= Rank(token[0]))

                for rank1 in first_ranks:
                    second_ranks = (rank for rank in Rank if rank < rank1)
                    for rank2 in second_ranks:
                        self._add_suited(rank1.value + rank2.value)
                        self._add_offsuit(rank1.value + rank2.value)

            # 2s2h, AsKc
            elif len(token) == 4 and token[-1] not in ('+', '-'):
                combo = Combo(token)
                if combo.is_pair:
                    self._pairs.add(combo)
                elif combo.is_suited:
                    self._suiteds.add(combo)
                else:
                    self._offsuits.add(combo)

            # AJo+, AJs+, A5o-, A5s-, 7Xs+, 76s+
            elif len(token) == 4:
                smaller, bigger = self._get_ordered(Rank, token[0], token[1])
                if token[-1] == '-':
                    second_ranks = (rank.value for rank in Rank if rank <= smaller)
                else:
                    second_ranks = (rank.value for rank in Rank if smaller <= rank < bigger)

                add_func = self._add_offsuit if token[2] == 'O' else self._add_suited

                for rank in second_ranks:
                    add_func(token[0] + rank)


            # 55-33, 33-55
            elif len(token) == 5 and token[0] == token[1]:
                smaller, bigger = self._get_ordered(Hand, token[:2], token[3:])
                pairs = (str(pair) for pair in PAIR_HANDS if smaller <= pair <= bigger)
                for pair in pairs:
                    self._add_pair(pair)

            # J8-J4
            elif len(token) == 5:
                smaller1, bigger1 = self._get_ordered(Rank, token[0], token[1])
                smaller2, bigger2 = self._get_ordered(Rank, token[3], token[4])

                if bigger1 != bigger2:
                    raise ValueError('Invalid token: {}'.format(token))

                bigger = bigger1.value
                ranks = (rank.value for rank in Rank if smaller2 <= rank <= smaller1)

                for rank in ranks:
                    self._add_offsuit(bigger + rank)
                    self._add_suited(bigger + rank)

            # J8o-J4o, J4o-J8o, 76s-74s, 74s-76s
            elif len(token) == 7:
                smaller, bigger = self._get_ordered(Hand, token[:3], token[4:])
                first_rank = bigger.first
                bigger_rank = bigger.second
                smaller_rank = smaller.second
                for rank in list(Rank):
                    if smaller_rank <= rank <= bigger_rank:
                        hand = first_rank.value + rank.value
                        if token[-1] == 'O':
                            self._add_offsuit(hand)
                        elif token[-1] == 'S':
                            self._add_suited(hand)

            else:
                raise ValueError('Invalid token: {}'.format(token))

    @classmethod
    def from_hands(cls, hands):
        return cls._from_objects(hands)

    @classmethod
    def from_combos(cls, combos):
        return cls._from_objects(combos)

    @classmethod
    def _from_objects(cls, objects):
        range_string = ' '.join(str(obj) for obj in objects)
        return cls(range_string)

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self._combos == other._combos
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return len(self._combos) < len(other._combos)
        return NotImplemented

    def __len__(self):
        return len(self._combos)

    def __str__(self):
        return ', '.join(self.rep_pieces)

    def __repr__(self):
        range = ' '.join(self.rep_pieces)
        return "{}('{}')".format(self.__class__.__qualname__, range)

    @property
    def rep_pieces(self):
        if len(self._combos) == 1326:
            return ['XX']

        pair_pieces = self._get_pieces(self._pairs, 6)
        suited_pieces = self._get_pieces(self._suiteds, 4)
        offsuit_pieces = self._get_pieces(self._offsuits, 12)

        pair_strs = self._shorten_pieces(pair_pieces)
        suited_strs = self._shorten_pieces(suited_pieces)
        offsuit_strs = self._shorten_pieces(offsuit_pieces)

        return pair_strs + suited_strs + offsuit_strs

    def _get_pieces(self, combos, combos_in_hand):
        if not combos:
            return []

        sorted_combos = sorted(combos, reverse=True)
        hands_and_combos = []
        current_combos = []
        last_combo = sorted_combos[0]

        for combo in sorted_combos:
            if (last_combo.first.rank == combo.first.rank and
                    last_combo.second.rank == combo.second.rank):
                current_combos.append(combo)
                length = len(current_combos)

                if length == combos_in_hand:
                    hands_and_combos.append(combo.to_hand())
                    current_combos = []
            else:
                hands_and_combos.extend(current_combos)
                current_combos = [combo]

            last_combo = combo

        # add the remainder if any, current_combos might be empty
        hands_and_combos.extend(current_combos)

        return hands_and_combos

    def _shorten_pieces(self, pieces):
        if not pieces:
            return []

        str_pieces = []
        first = last = pieces[0]
        for current in pieces[1:]:
            if isinstance(last, Combo):
                str_pieces.append(str(last))
                first = last = current
            elif isinstance(current, Combo):
                str_pieces.append(self._get_format(first, last))
                first = last = current
            elif ((current.is_pair and Rank.difference(last.first, current.first) == 1) or
                  (last.first == current.first and
                   Rank.difference(last.second, current.second) == 1)):
                last = current
            else:
                str_pieces.append(self._get_format(first, last))
                first = last = current

        # write out any remaining pieces
        str_pieces.append(self._get_format(first, last))

        return str_pieces

    def _get_format(self, first, last):
        if first == last:
            return str(first)
        elif (first.is_pair and first.first.value == 'A' or
                    Rank.difference(first.first, first.second) == 1):
            return '{}+'.format(last)
        elif last.second.value == '2':
            return '{}-'.format(first)
        else:
            return '{}-{}'.format(first, last)

    def _get_ordered(self, type_, part1, part2):
        first, second = type_(part1), type_(part2)
        return min(first, second), max(first, second)

    def _add_pair(self, tok):
        self._pairs |= {Combo(tok[0] + s1.value + tok[1] + s2.value)
                        for s1, s2 in itertools.combinations(Suit, 2)}

    def _add_offsuit(self, tok):
        self._offsuits |= {Combo(tok[0] + s1.value + tok[1] + s2.value)
                           for s1, s2 in itertools.product(Suit, Suit) if s1 != s2}

    def _add_suited(self, tok):
        self._suiteds |= {Combo(tok[0] + s1.value + tok[1] + s2.value)
                          for s1, s2 in itertools.product(Suit, Suit) if s1 == s2}

    @property
    def hands(self):
        hands = {combo.to_hand() for combo in self._combos}
        return tuple(sorted(hands))

    @property
    def combos(self):
        return tuple(sorted(self._combos))

    @property
    def percent(self):
        """What percent of combos does this range have
        compared to all the possible combos.

        There are 1326 total combos in Hold'em: 52 * 51 / 2 (because order doesn't matter)
        """
        dec_percent = (Decimal(len(self._combos)) / 1326 * 100)

        # round to two decimal point
        return float(dec_percent.quantize(Decimal('1.00')))

    @property
    def _combos(self):
        return self._pairs | self._suiteds | self._offsuits
