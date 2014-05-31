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


def test_comparisons_reverse():
    assert Rank('K') < Rank('A')
    assert Rank('Q') < Rank('K')
    assert Rank('J') < Rank('Q')
    assert Rank('T') < Rank('J')
    assert Rank('9') < Rank('T')
    assert Rank('2') < Rank('9')
    assert Rank('2') < Rank('A')


def test_equality_comparisons():
    assert Rank('A') == Rank('A')
    assert Rank('T') == Rank('T')
    assert Rank('2') == Rank('2')


def test_case_insensitive():
    assert Rank('A') == Rank('a')


def test_invalid_rank_raises_InvalidRank_Exception():
    with raises(InvalidRank):
        Rank('L')
