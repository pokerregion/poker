from rangeparser import Suit
from pytest import raises


def test_suit_order():
    assert Suit('c') < Suit('d')
    assert Suit('c') < Suit('h')
    assert Suit('c') < Suit('s')
    assert Suit('d') < Suit('h')
    assert Suit('d') < Suit('s')
    assert Suit('h') < Suit('s')


def test_unicode_suit_order():
    assert Suit('♣') < Suit('♦')
    assert Suit('♣') < Suit('♥')
    assert Suit('♣') < Suit('♠')
    assert Suit('♦') < Suit('♥')
    assert Suit('♦') < Suit('♠')
    assert Suit('♥') < Suit('♠')


def test_suit_order_reverse():
    assert Suit('d') > Suit('c')
    assert Suit('h') > Suit('c')
    assert Suit('s') > Suit('c')
    assert Suit('h') > Suit('d')
    assert Suit('s') > Suit('d')
    assert Suit('s') > Suit('h')


def test_case_insensitive():
    assert Suit('C') == Suit('c')
    assert Suit('C') < Suit('d')
    assert Suit('C') < Suit('h')
    assert Suit('C') < Suit('s')
    assert Suit('D') < Suit('h')
    assert Suit('D') < Suit('s')
    assert Suit('H') < Suit('s')


def test_case_insensitive_reverse():
    assert Suit('c') == Suit('C')
    assert Suit('d') > Suit('C')
    assert Suit('h') > Suit('C')
    assert Suit('s') > Suit('C')
    assert Suit('h') > Suit('D')
    assert Suit('s') > Suit('D')
    assert Suit('s') > Suit('H')


def test_wrong_value_raises_ValueError():
    with raises(ValueError):
        Suit('k')


def test_str():
    assert str(Suit('c')) == '♣'
    assert str(Suit('d')) == '♦'
    assert str(Suit('h')) == '♥'
    assert str(Suit('s')) == '♠'


def test_repr():
    assert repr(Suit('c')) == "Suit('♣')"
    assert repr(Suit('d')) == "Suit('♦')"
    assert repr(Suit('h')) == "Suit('♥')"
    assert repr(Suit('s')) == "Suit('♠')"
