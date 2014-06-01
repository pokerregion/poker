from rangeparser import Combo, Card, InvalidCombo
from pytest import raises


def test_first_and_second_are_Card_instances():
    assert isinstance(Combo('AsKc').first, Card)
    assert isinstance(Combo('AsKc').second, Card)


def test_case_insensitive():
    assert Combo('ASKC') > Combo('QCJH')
    assert Combo('askc') > Combo('qcjh')
    assert Combo('KSjh').is_broadway() is True

    assert Combo('2s2c') == Combo('2S2C')


def test_card_order_is_not_significant():
    assert Combo('2s2c') == Combo('2c2s')
    assert Combo('AsQc') == Combo('QcAs')


def test_ofsuit_pairs_are_equals():
    assert Combo('2s2c') == Combo('2d2h')
    assert Combo('5d5h') == Combo('5s5h')


def test_pair_equality():
    assert Combo('2s2c') == Combo('2h2d')


def test_pairs_are_better_than_non_pairs():
    assert Combo('2s2c') > Combo('AsKh')
    assert Combo('5s5h') > Combo('JsTs')


def test_card_are_better_when_ranks_are_higher():
    assert Combo('AsKc') > Combo('QcJh')
    assert Combo('KsJh') > Combo('QcJh')


def test_unicode():
    assert Combo('AsAh') == Combo('A♠A♥')
    assert Combo('5s5h') > Combo('J♠T♠')


def test_is_suited():
    assert Combo('AdKd').is_suited() is True


def test_is_pair():
    assert Combo('2s2c').is_pair() is True
    assert Combo('AhAd').is_pair() is True


def test_is_connector():
    assert Combo('AdKs').is_connector()
    assert Combo('JdTc').is_connector()
    assert Combo('KsQs').is_connector()


def test_is_suited_connector():
    assert Combo('AdKd').is_connector()
    assert Combo('KsQs').is_suited_connector()


def test_is_broadway():
    assert Combo('KsJc').is_broadway() is True


def test_invalid_combo():
    with raises(InvalidCombo):
        Combo('2s2s')

    with raises(InvalidCombo):
        Combo('2222')

    with raises(InvalidCombo):
        Combo('KQJQ')
