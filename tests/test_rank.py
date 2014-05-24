# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function

from rangeparser import Rank, InvalidRank
from pytest import raises


def test_comparisons():
    assert Rank('A') > Rank('K')
    assert Rank('K') > Rank('Q')
    assert Rank('Q') > Rank('J')
    assert Rank('J') > Rank('T')
    assert Rank('T') > Rank('9')
    assert Rank('9') > Rank('2')
    assert Rank('A') > Rank('2')


def test_case_insensitive():
    assert Rank('A') == Rank('a')
    assert Rank('t').rank == 'T'


def test_rank():
    assert Rank('A').rank == 'A'
    assert Rank('2').rank == '2'
    assert Rank('T').rank == 'T'


def test_invalid_rank_raises_InvalidRank_Exception():
    with raises(InvalidRank):
        Rank('L')


def test_rank_type_should_be_str_only():
    with raises(TypeError):
        Rank(2)

    with raises(TypeError):
        Rank(['2'])
