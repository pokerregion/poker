from poker.hand import _RegexRangeLexer


def test_all():
    lexer = _RegexRangeLexer("XX")
    assert list(lexer) == [("ALL", "XX")]


def test_pair_simple():
    lexer = _RegexRangeLexer("44")
    assert list(lexer) == [("PAIR", "4")]


def test_pair_plus():
    lexer = _RegexRangeLexer("TT+")
    assert list(lexer) == [("PAIR_PLUS", "T")]


def test_pair_minus():
    lexer = _RegexRangeLexer("55-")
    assert list(lexer) == [("PAIR_MINUS", "5")]


def test_pair_with_dash():
    lexer = _RegexRangeLexer("55-TT")
    result = [("PAIR_DASH", ("5", "T"))]
    assert list(lexer) == result

    lexer_reversed = _RegexRangeLexer("55-TT")
    assert list(lexer_reversed) == result


def test_both_suited_and_offsuit():
    lexer = _RegexRangeLexer("AK")
    assert list(lexer) == [("BOTH", ("K", "A"))]


def test_both_suited_and_offsuit_plus():
    lexer = _RegexRangeLexer("KJ+")
    assert list(lexer) == [("BOTH_PLUS", ("J", "K"))]
