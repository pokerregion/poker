import pytest
from poker.card import Suit


def test_suit_order():
    assert Suit("c") < Suit("d")
    assert Suit("c") < Suit("h")
    assert Suit("c") < Suit("s")
    assert Suit("d") < Suit("h")
    assert Suit("d") < Suit("s")
    assert Suit("h") < Suit("s")


def test_unicode_suit_order():
    assert Suit("♣") < Suit("♦")
    assert Suit("♣") < Suit("♥")
    assert Suit("♣") < Suit("♠")
    assert Suit("♦") < Suit("♥")
    assert Suit("♦") < Suit("♠")
    assert Suit("♥") < Suit("♠")


def test_suit_order_reverse():
    assert Suit("d") > Suit("c")
    assert Suit("h") > Suit("c")
    assert Suit("s") > Suit("c")
    assert Suit("h") > Suit("d")
    assert Suit("s") > Suit("d")
    assert Suit("s") > Suit("h")

    assert (Suit("d") < Suit("c")) is False
    assert (Suit("h") < Suit("c")) is False
    assert (Suit("s") < Suit("c")) is False
    assert (Suit("h") < Suit("d")) is False
    assert (Suit("s") < Suit("d")) is False
    assert (Suit("s") < Suit("h")) is False


def test_case_insensitive():
    assert Suit("C") == Suit("c")
    assert Suit("C") < Suit("d")
    assert Suit("C") < Suit("h")
    assert Suit("C") < Suit("s")
    assert Suit("D") < Suit("h")
    assert Suit("D") < Suit("s")
    assert Suit("H") < Suit("s")


def test_case_insensitive_reverse():
    assert Suit("c") == Suit("C")
    assert Suit("d") > Suit("C")
    assert Suit("h") > Suit("C")
    assert Suit("s") > Suit("C")
    assert Suit("h") > Suit("D")
    assert Suit("s") > Suit("D")
    assert Suit("s") > Suit("H")


def test_wrong_value_raises_ValueError():
    with pytest.raises(ValueError):
        Suit("k")


def test_str():
    assert str(Suit("c")) == "♣"
    assert str(Suit("d")) == "♦"
    assert str(Suit("h")) == "♥"
    assert str(Suit("s")) == "♠"


def test_repr():
    assert repr(Suit("c")) == "Suit('♣')"
    assert repr(Suit("d")) == "Suit('♦')"
    assert repr(Suit("h")) == "Suit('♥')"
    assert repr(Suit("s")) == "Suit('♠')"


def test_passing_Suit_instance_to__init__():
    s1 = Suit("c")
    s2 = Suit(s1)
    assert s1 == s2
    assert s1 is s2
    assert id(s1) == id(s2)
    assert repr(s1) == "Suit('♣')"
    assert repr(s2) == "Suit('♣')"
    assert isinstance(repr(s1), str)
    assert isinstance(repr(s2), str)


def test_class_is_iterable():
    assert list(Suit) == [Suit("♣"), Suit("♦"), Suit("♥"), Suit("♠")]
    assert list(Suit) == list(tuple(Suit))


def test_class_variables_are_comparable():
    assert Suit.CLUBS < Suit.DIAMONDS
    assert Suit.CLUBS < Suit.HEARTS
    assert Suit.CLUBS < Suit.SPADES
    assert Suit.DIAMONDS < Suit.HEARTS
    assert Suit.DIAMONDS < Suit.SPADES
    assert Suit.HEARTS < Suit.SPADES


def test_suits_are_singletons():
    assert Suit("c") is Suit.CLUBS
    assert Suit("c") is Suit("c")
    assert Suit("c") is Suit("♣")

    assert Suit("s") is Suit.SPADES


def test_make_random_is_instance_of_Suit():
    assert isinstance(Suit.make_random(), Suit)


def test_hash():
    assert hash(Suit.CLUBS) == hash(Suit("c")) == hash(Suit("C")) == hash(Suit("♣"))

    assert hash(Suit.SPADES) == hash(Suit("s"))


def test_putting_them_in_set_doesnt_raise_Exception():
    {Suit("c")}

    {Suit.CLUBS, Suit.SPADES}
