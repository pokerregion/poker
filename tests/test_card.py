# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function


from rangeparser import Card, Rank


def test_same_ranks_are_equeal_no_matter_what_suit():
    assert Card('Ac') == Card('Ah')


def test_comparisons():
    assert Card('Ac') > Card('Kh')
    assert Card('Ks') > Card('Qd')
    assert Card('Qs') > Card('Js')
    assert Card('Jd') > Card('Th')
    assert Card('Ac') > Card('2s')


def test_comparisons_reverse():
    assert Card('Kh') < Card('Ac')
    assert Card('Qd') < Card('Ks')
    assert Card('Js') < Card('Qs')
    assert Card('Th') < Card('Jd')
    assert Card('2s') < Card('Ac')


def test_suit():
    assert Card('Ac').suit == 'c'


def test_rank():
    assert Card('Ah').rank == 'A'


def test_case_insensitive():
    assert Card('aH').rank == 'A'
    assert Card('aH').suit == 'h'


def test_is_face():
    # A is NOT a face card!
    assert Card('As').is_face() is False
    assert Card('2c').is_face() is False

    assert Card('Qd').is_face() is True


def test_is_broadway():
    assert Card('As').is_broadway() is True
    assert Card('Kd').is_broadway() is True
    assert Card('Th').is_broadway() is True

    assert Card('2s').is_broadway() is False


def test_alternative_constructor():
    rank = Rank('A')
    card = Card.from_rank(rank, 'c')
    assert isinstance(card, Card)
    assert card == Card('Ac')


def test_representation():
    assert str(Card('As')) == 'As'
    assert repr(Card('As')) == "Card('As')"
