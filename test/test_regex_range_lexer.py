from poker.card import Rank
from poker.hand import RegexRangeLexer
import pytest


# pytestmark = pytest.mark.xfail

def test_all():
    lexer = RegexRangeLexer('XX')
    assert list(lexer) == [('ALL', None)]


def test_pair_simple():
    lexer = RegexRangeLexer('44')
    assert list(lexer) == [('PAIR', Rank('4'))]


def test_pair_plus():
    lexer = RegexRangeLexer('TT+')
    assert list(lexer) == [('PAIR_PLUS', Rank('T'))]


def test_pair_minus():
    lexer = RegexRangeLexer('55-')
    assert list(lexer) == [('PAIR_MINUS', Rank('5'))]


def test_pair_with_dash():
    lexer = RegexRangeLexer('55-TT')
    result = [('PAIR_DASH', (Rank('5'), Rank('T')))]
    assert list(lexer) == result

    lexer_reversed = RegexRangeLexer('55-TT')
    assert list(lexer_reversed) == result


def test_both_suited_and_offsuit():
    lexer = RegexRangeLexer('AK')
    assert list(lexer) == [('BOTH', (Rank('K'), Rank('A')))]


def test_both_suited_and_offsuit_plus():
    lexer = RegexRangeLexer('KJ+')
    assert list(lexer) == [('BOTH_PLUS', (Rank('J'), Rank('K')))]
