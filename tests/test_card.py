import pytest
from poker.card import Card, Rank, Suit


def test_only_cards_with_same_rank_are_equal():
    assert Card("Ah") == Card("Ah")
    assert Card("K♠") == Card("K♠")
    assert Card("Ah") != Card("As")
    assert Card("2c") != Card("2h")


def test_comparisons():
    assert Card("Ac") > Card("Kh")
    assert Card("Ks") > Card("Qd")
    assert Card("Qs") > Card("Js")
    assert Card("Jd") > Card("Th")
    assert Card("Ac") > Card("2s")


def test_comparisons_reverse():
    assert Card("Kh") < Card("Ac")
    assert Card("Qd") < Card("Ks")
    assert Card("Js") < Card("Qs")
    assert Card("Th") < Card("Jd")
    assert Card("2s") < Card("Ac")


def test_better_suits_are_bigger_with_same_ranks():
    assert Card("Ac") < Card("Ad")
    assert Card("Ac") < Card("Ah")
    assert Card("Ac") < Card("As")
    assert Card("Ad") < Card("Ah")
    assert Card("Ad") < Card("As")
    assert Card("Ah") < Card("As")


def test_unicode_suits():
    assert Card("A♠") > Card("Kd")
    assert Card("K♥") > Card("Kc")
    assert Card("aH").suit == Suit("♥")
    assert Card("2d").suit == Suit("♦")


def test_rank_equality():
    assert Card("Ac").rank == Card("Ah").rank
    assert Card("Ts").rank == Card("Ts").rank
    assert Card("2d").rank == Card("2h").rank


def test_rank_inequality():
    assert Card("Ad").rank != Card("Ks").rank
    assert Card("Ts").rank != Card("5h").rank


def test_rank_comparisons():
    assert Card("Ac").rank > Card("Kh").rank
    assert Card("Ks").rank > Card("Qd").rank
    assert Card("Qs").rank > Card("Js").rank
    assert Card("Jd").rank > Card("Th").rank
    assert Card("Ac").rank > Card("2s").rank


def test_rank_comparisons_reverse():
    assert Card("Kh").rank < Card("Ac").rank
    assert Card("Qd").rank < Card("Ks").rank
    assert Card("Js").rank < Card("Qs").rank
    assert Card("Th").rank < Card("Jd").rank
    assert Card("2s").rank < Card("Ac").rank


def test_suit():
    assert Card("Ac").suit == Suit("c")


def test_rank():
    assert Card("Ah").rank == Rank("A")


def test_case_insensitive():
    assert Card("aH").rank == Rank("A")
    assert Card("aH").suit == Suit("h") == Suit("♥")


def test_is_face():
    # A is NOT a face card!
    assert Card("As").is_face is False
    assert Card("2c").is_face is False

    assert Card("Qd").is_face is True


def test_is_broadway():
    assert Card("As").is_broadway is True
    assert Card("Kd").is_broadway is True
    assert Card("Th").is_broadway is True

    assert Card("2s").is_broadway is False


def test_representation():
    assert str(Card("As")) == "A♠"
    assert repr(Card("As")) == "Card('A♠')"
    assert repr(Card("Ad")) == "Card('A♦')"
    assert repr(Card("Kh")) == "Card('K♥')"
    assert repr(Card("Jc")) == "Card('J♣')"


def test_passing_Card_instance_to__init__():
    c1 = Card("As")
    c2 = Card(c1)
    assert c1 == c2
    assert (c1 != c2) is False
    assert id(c1) == id(c2)
    assert repr(c1) == "Card('A♠')"
    assert repr(c2) == "Card('A♠')"


def test_make_random_is_instance_of_Card_Rank_and_Suit():
    card = Card.make_random()
    assert isinstance(card, Card)
    assert isinstance(card.rank, Rank)
    assert isinstance(card.suit, Suit)


def test_invalid_rank_or_card_raises_ValueError():
    with pytest.raises(ValueError):
        Card("Lh")


def test_with_wrong_length_raises_ValueError_and_InvalidCard():
    with pytest.raises(ValueError):
        Card("AKQs")


def test_hash():
    card1 = Card("As")
    card2 = Card("A♠")
    assert hash(card1) == hash(card2)


def test_putting_them_in_set_doesnt_raise_Exception():
    {Card("As"), Card("Kc")}
