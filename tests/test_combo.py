import pytest
from poker.card import Card
from poker.hand import Shape, Hand, Combo


def test_first_and_second_are_Card_instances():
    assert isinstance(Combo("AsKc").first, Card)
    assert isinstance(Combo("AsKc").second, Card)


def test_case_insensitive():
    assert Combo("ASKC") > Combo("QCJH")
    assert Combo("askc") > Combo("qcjh")
    assert Combo("KSjh").is_broadway is True

    assert Combo("2s2c") == Combo("2S2C")


def test_card_order_is_not_significant():
    assert Combo("2s2c") == Combo("2c2s")
    assert Combo("AsQc") == Combo("QcAs")


def test_pairs_are_NOT_equal():
    assert Combo("2s2c") != Combo("2d2h")
    assert Combo("5d5h") != Combo("5s5h")


def test_pairs_are_better_than_non_pairs():
    assert Combo("2s2c") > Combo("AsKh")
    assert Combo("5s5h") > Combo("JsTs")


def test_card_are_better_when_ranks_are_higher():
    assert Combo("AsKc") > Combo("QcJh")
    assert Combo("KsJh") > Combo("QcJh")


def test_card_are_only_depends_from_rank_not_suit_when_different():
    assert Combo("Kc7s") > Combo("Kd4c")
    assert Combo("Kd4c") < Combo("Kc7s")

    assert Combo("K♠5♣") < Combo("K♥7♠")
    assert Combo("K♥7♠") > Combo("K♠5♣")


def test_first_hand_suit_also_matters():
    assert Combo("K♠4♣") > Combo("K♥4♣")
    assert Combo("K♥4♣") < Combo("K♠4♣")


def test_suited_combos_are_higher_than_offsuit():
    assert Combo("AcKc") > Combo("AsKd")
    assert Combo("AsKd") < Combo("AcKc")

    assert Combo("AsKs") > Combo("AdKd")
    assert Combo("AdKd") > Combo("AcKc")


def test_pair_comparisons():
    assert (Combo("2d2c") < Combo("2s2c")) is True
    # reverse
    assert (Combo("2s2c") < Combo("2d2c")) is False

    assert Combo("2d2c") < Combo("2s2h")
    assert Combo("2s2h") > Combo("2d2c")


def test_pair_when_first_card_are_the_same():
    assert Combo("2d2c") < Combo("2d2h")


def test_equal_pairs_are_not_less():
    assert (Combo("2s2c") < Combo("2s2c")) is False
    assert (Combo("2s2c") > Combo("2s2c")) is False


def test_unicode():
    assert Combo("AsAh") == Combo("A♠A♥")
    assert Combo("5s5h") > Combo("J♠T♠")
    assert Combo("5s5h") >= Combo("J♠T♠")


def test_repr():
    assert str(Combo("2s2c")) == "2♠2♣"
    assert str(Combo("KhAs")) == "A♠K♥"
    assert str(Combo("ThTd")) == "T♥T♦"


def test_is_suited():
    assert Combo("AdKd").is_suited is True


def test_is_offsuit():
    assert Combo("AcKh").is_offsuit is True
    assert Combo("AcKh").is_suited is False


def test_is_pair():
    assert Combo("2s2c").is_pair is True
    assert Combo("AhAd").is_pair is True


def test_is_connector():
    assert Combo("AdKs").is_connector is True
    assert Combo("JdTc").is_connector is True
    assert Combo("KsQs").is_connector is True


def test_is_one_gapper():
    assert Combo("Jd9s").is_one_gapper is True


def test_is_two_gapper():
    assert Combo("Jd8s").is_two_gapper is True


def test_is_suited_connector():
    assert Combo("AdKd").is_connector
    assert Combo("KsQs").is_suited_connector


def test_is_broadway():
    assert Combo("KsJc").is_broadway is True


def test_invalid_combination():
    with pytest.raises(ValueError):
        Combo("2s2s")

    with pytest.raises(ValueError):
        Combo("2222")

    with pytest.raises(ValueError):
        Combo("KQJQ")


def test_hash():
    combination1 = Combo("2s2c")
    combination2 = Combo("2c2s")
    assert hash(combination1) == hash(combination2)


def test_putting_them_in_set_doesnt_raise_Exception():
    {Combo("AsAh"), Combo("2s2c")}


def test_two_set_of_combinations_are_equal_if_they_contains_same_cards():
    assert {Combo("2s2c")} == {Combo("2c2s")}


def test_from_cards():
    assert Combo.from_cards(Card("As"), Card("Kh")) == Combo("AsKh")

    combination = Combo.from_cards(Card("Kh"), Card("As"))
    assert combination == Combo("AsKh")
    assert repr(combination) == "Combo('A♠K♥')"


def test_shape_property():
    assert Combo("2s2c").shape == Shape.PAIR
    assert Combo("AsKs").shape == Shape.SUITED
    assert Combo("AdKs").shape == Shape.OFFSUIT


def test_to_hand_converter_method():
    assert Combo("2s2c").to_hand() == Hand("22")
    assert Combo("AsKc").to_hand() == Hand("AKo")
    assert Combo("7s6s").to_hand() == Hand("76s")


def test_pairs_are_not_offsuits():
    assert Combo("2s2c").is_offsuit is False
