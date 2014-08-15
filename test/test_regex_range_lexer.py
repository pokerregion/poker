from poker.card import Rank
from poker.hand import _RegexRangeLexer
import pytest


# pytestmark = pytest.mark.xfail

def test_all():
    lexer = RegexRangeLexer('XX')
    assert list(lexer) == [('ALL', 'XX')]


def test_pair_simple():
    lexer = RegexRangeLexer('44')
    assert list(lexer) == [('PAIR', '4')]


def test_pair_plus():
    lexer = RegexRangeLexer('TT+')
    assert list(lexer) == [('PAIR_PLUS', 'T')]


def test_pair_minus():
    lexer = RegexRangeLexer('55-')
    assert list(lexer) == [('PAIR_MINUS', '5')]


def test_pair_with_dash():
    lexer = RegexRangeLexer('55-TT')
    result = [('PAIR_DASH', ('5', 'T'))]
    assert list(lexer) == result

    lexer_reversed = RegexRangeLexer('55-TT')
    assert list(lexer_reversed) == result


def test_both_suited_and_offsuit():
    lexer = RegexRangeLexer('AK')
    assert list(lexer) == [('BOTH', ('K', 'A'))]


def test_both_suited_and_offsuit_plus():
    lexer = RegexRangeLexer('KJ+')
    assert list(lexer) == [('BOTH_PLUS', ('J', 'K'))]
