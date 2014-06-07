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


def test_ofsuit_pairs_are_equals():
    assert Combination('2s2c') == Combination('2d2h')
    assert Combination('5d5h') == Combination('5s5h')


def test_pair_equality():
    assert Combination('2s2c') == Combination('2h2d')


def test_pairs_are_better_than_non_pairs():
    assert Combination('2s2c') > Combination('AsKh')
    assert Combination('5s5h') > Combination('JsTs')


def test_card_are_better_when_ranks_are_higher():
    assert Combination('AsKc') > Combination('QcJh')
    assert Combination('KsJh') > Combination('QcJh')


def test_unicode():
    assert Combination('AsAh') == Combination('A♠A♥')
    assert Combination('5s5h') > Combination('J♠T♠')


def test_is_suited():
    assert Combination('AdKd').is_suited() is True


def test_is_pair():
    assert Combination('2s2c').is_pair() is True
    assert Combination('AhAd').is_pair() is True


def test_is_connector():
    assert Combination('AdKs').is_connector()
    assert Combination('JdTc').is_connector()
    assert Combination('KsQs').is_connector()


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
