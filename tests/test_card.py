from rangeparser import Card, Rank


def test_only_cards_with_same_rank_are_equal():
    assert Card('Ah') == Card('Ah')
    assert Card('Ah') != Card('As')
    assert Card('2c') != Card('2h')


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


def test_better_suits_are_bigger_with_same_ranks():
    assert Card('Ac') < Card('Ad')
    assert Card('Ac') < Card('Ah')
    assert Card('Ac') < Card('As')
    assert Card('Ad') < Card('Ah')
    assert Card('Ad') < Card('As')
    assert Card('Ah') < Card('As')


def test_rank_comparisons():
    assert Card('Ac').rank > Card('Kh').rank
    assert Card('Ks').rank > Card('Qd').rank
    assert Card('Qs').rank > Card('Js').rank
    assert Card('Jd').rank > Card('Th').rank
    assert Card('Ac').rank > Card('2s').rank


def test_rank_comparisons_reverse():
    assert Card('Kh').rank < Card('Ac').rank
    assert Card('Qd').rank < Card('Ks').rank
    assert Card('Js').rank < Card('Qs').rank
    assert Card('Th').rank < Card('Jd').rank
    assert Card('2s').rank < Card('Ac').rank


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
