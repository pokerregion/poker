from rangeparser import Combination, Card
from pytest import raises


def test_first_and_second_are_Card_instances():
    assert isinstance(Combination('AsKc').first, Card)
    assert isinstance(Combination('AsKc').second, Card)


def test_case_insensitive():
    assert Combination('ASKC') > Combination('QCJH')
    assert Combination('askc') > Combination('qcjh')
    assert Combination('KSjh').is_broadway() is True

    assert Combination('2s2c') == Combination('2S2C')


def test_card_order_is_not_significant():
    assert Combination('2s2c') == Combination('2c2s')
    assert Combination('AsQc') == Combination('QcAs')


def test_pairs_are_NOT_equal():
    assert Combination('2s2c') != Combination('2d2h')
    assert Combination('5d5h') != Combination('5s5h')


def test_pairs_are_better_than_non_pairs():
    assert Combination('2s2c') > Combination('AsKh')
    assert Combination('5s5h') > Combination('JsTs')


def test_card_are_better_when_ranks_are_higher():
    assert Combination('AsKc') > Combination('QcJh')
    assert Combination('KsJh') > Combination('QcJh')


def test_pair_comparisons():
    assert (Combination('2d2c') < Combination('2s2c')) is True
    # reverse
    assert (Combination('2s2c') < Combination('2d2c')) is False


def test_equal_pairs_are_not_less():
    assert (Combination('2s2c') < Combination('2s2c')) is False
    assert (Combination('2s2c') > Combination('2s2c')) is False


def test_unicode():
    assert Combination('AsAh') == Combination('A♠A♥')
    assert Combination('5s5h') > Combination('J♠T♠')
    assert Combination('5s5h') >= Combination('J♠T♠')


def test_repr():
    assert str(Combination('2s2c')) == '2♠2♣'
    assert str(Combination('KhAs')) == 'A♠K♥'
    assert str(Combination('ThTd')) == 'T♥T♦'


def test_is_suited():
    assert Combination('AdKd').is_suited() is True


def test_is_pair():
    assert Combination('2s2c').is_pair() is True
    assert Combination('AhAd').is_pair() is True


def test_is_connector():
    assert Combination('AdKs').is_connector() is True
    assert Combination('JdTc').is_connector() is True
    assert Combination('KsQs').is_connector() is True


def test_is_suited_connector():
    assert Combination('AdKd').is_connector()
    assert Combination('KsQs').is_suited_connector()


def test_is_broadway():
    assert Combination('KsJc').is_broadway() is True


def test_invalid_combination():
    with raises(ValueError):
        Combination('2s2s')

    with raises(ValueError):
        Combination('2222')

    with raises(ValueError):
        Combination('KQJQ')


def test_hash():
    combination1 = Combination('2s2c')
    combination2 = Combination('2c2s')
    assert hash(combination1) == hash(combination2)

def test_putting_them_in_set_doesnt_raise_Exception():
    {Combination('AsAh'), Combination('2s2c')}


def test_two_set_of_combinations_are_equal_if_they_contains_same_cards():
    assert {Combination('2s2c')} == {Combination('2c2s')}


def test_from_cards():
    assert Combination.from_cards(Card('As'), Card('Kh')) == Combination('AsKh')

    combination = Combination.from_cards(Card('Kh'), Card('As'))
    assert combination == Combination('AsKh')
    assert repr(combination) == "Combination('A♠K♥')"


def test_suitedness_property():
    assert Combination('2s2c').suitedness == Suitedness.NOSUIT
    assert Combination('AsKs').suitedness == Suitedness.SUITED
    assert Combination('AdKs').suitedness == Suitedness.OFFSUIT
