import pytest
from poker.card import Rank


def test_comparisons():
    assert Rank("A") > Rank("K")
    assert Rank("K") > Rank("Q")
    assert Rank("Q") > Rank("J")
    assert Rank("J") > Rank("T")
    assert Rank("T") > Rank("9")
    assert Rank("9") > Rank("2")
    assert Rank("A") > Rank("2")


def test_comparisons_reverse():
    assert Rank("K") < Rank("A")
    assert Rank("Q") < Rank("K")
    assert Rank("J") < Rank("Q")
    assert Rank("T") < Rank("J")
    assert Rank("9") < Rank("T")
    assert Rank("2") < Rank("9")
    assert Rank("2") < Rank("A")


def test_comparisons_less_or_equal():
    assert Rank("K") <= Rank("A")
    assert Rank("Q") <= Rank("K")
    assert Rank("J") <= Rank("Q")
    assert Rank("T") <= Rank("J")
    assert Rank("9") <= Rank("T")
    assert Rank("2") <= Rank("9")
    assert Rank("2") <= Rank("A")


def test_comparisons_bigger_or_equal():
    assert Rank("A") >= Rank("K")
    assert Rank("K") >= Rank("Q")
    assert Rank("Q") >= Rank("J")
    assert Rank("J") >= Rank("T")
    assert Rank("T") >= Rank("9")
    assert Rank("9") >= Rank("2")
    assert Rank("A") >= Rank("2")


def test_equality_comparisons():
    assert Rank("A") == Rank("A")
    assert Rank("T") == Rank("T")
    assert Rank("2") == Rank("2")


def test_not_equal_comparisons():
    assert (Rank("A") != Rank("A")) is False
    assert (Rank("T") != Rank("T")) is False
    assert (Rank("2") != Rank("2")) is False

    assert Rank("A") != Rank("K")
    assert Rank("6") != Rank("2")


def test_case_insensitive():
    assert Rank("A") == Rank("a")
    assert (Rank("A") != Rank("a")) is False


def test_invalid_rank_raises_InvalidRank_Exception():
    with pytest.raises(ValueError):
        Rank("L")


def test_passing_Rank_instance_to__init__():
    r1 = Rank("A")
    r2 = Rank(r1)
    assert r1 == r2
    assert (r1 != r2) is False
    assert repr(r1) == "Rank('A')"
    assert repr(r2) == "Rank('A')"


def test_hash():
    rank1 = Rank("A")
    rank2 = Rank("a")
    assert hash(rank1) == hash(rank2)


def test_putting_them_in_set_doesnt_raise_Exception():
    {Rank.ACE, Rank.KING}


def test_rank_difference():
    assert Rank.difference("6", "4") == 2
    assert Rank.difference("A", "2") == 12
    assert Rank.difference("K", "K") == 0
    assert Rank.difference("K", "Q") == 1
