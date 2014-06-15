from pytest import raises
from rangeparser import *


# from worse to best (suit matter)
DEUCE_COMBINATIONS = (
    Combination('2d2c'), Combination('2h2c'), Combination('2h2d'),
    Combination('2s2c'), Combination('2s2d'), Combination('2s2h')
)

THREE_COMBINATIONS = (
    Combination('3d3c'), Combination('3h3c'), Combination('3h3d'),
    Combination('3s3c'), Combination('3s3d'), Combination('3s3h')
)

# from worse to best (suit matter)
TEN_COMBINATIONS = (
    Combination('TdTc'), Combination('ThTc'), Combination('ThTd'),
    Combination('TsTc'), Combination('TsTd'), Combination('TsTh')
)


class TestHandsResultsAfterParse:
    def test_pairs_simple(self):
        assert Range('22').hands == (Hand('22'),)
        assert Range('22').combinations == DEUCE_COMBINATIONS

    def test_combination_simple(self):
        assert Range('2s2c').hands == (Hand('22'),)
        assert Range('2s2c').combinations == (Combination('2c2s'),)

    def test_pairs_multiple(self):
        assert Range('22 33').hands == (Hand('22'), Hand('33'))
        assert Range('33 22').hands == (Hand('22'), Hand('33'))

    def test_pairs_with_plus(self):
        assert Range('88+').hands == (Hand('88'), Hand('99')) + BIG_PAIR_HANDS
        assert Range('22+').hands == PAIR_HANDS

    def test_pairs_with_dash(self):
        assert Range('22-55').hands == SMALL_PAIR_HANDS
        assert Range('22-33').hands == (Hand('22'), Hand('33'))

    def test_pairs_with_dash_reverse(self):
        assert Range('55-22').hands == SMALL_PAIR_HANDS
        assert Range('33-22').hands == (Hand('22'), Hand('33'))

    def test_multiple_offsuit_hands(self):
        assert Range('AKo 84o').hands == (Hand('AKo'), Hand('84o'))

    def test_hands_without_suit(self):
        assert Range('AK 48').hands == (Hand('84o'), Hand('84s'), Hand('AKo'), Hand('AKs'))

    def test_dash_offsuit(self):
        assert Range('J8o-J4o').hands == (Hand('J4o'), Hand('J5o'), Hand('J6o'),
                                          Hand('J7o'), Hand('J8o'))

    def test_dash_suited(self):
        assert Range('J8s-J4s').hands == (Hand('J4s'), Hand('J5s'), Hand('J6s'),
                                          Hand('J7s'), Hand('J8s'))

    def test_empty_range(self):
        assert Range().hands == tuple()
        assert Range().combinations == tuple()

        assert Range('').hands == tuple()
        assert Range('').combinations == tuple()


class TestCombinationsResultsAfterParse:
    def test_pairs_simple(self):
        """Test if pairs get all the combinations."""
        assert Range('22').combinations == DEUCE_COMBINATIONS

    def test_pairs_multiple(self):
        assert Range('22 33').combinations == DEUCE_COMBINATIONS + THREE_COMBINATIONS

    def test_pairs_with_dash(self):
        assert Range('22-33').combinations == DEUCE_COMBINATIONS + THREE_COMBINATIONS

    def test_pairs_with_dash_are_equal_with_spaces(self):
        assert Range('22-33').combinations == Range('22 33').combinations
        assert Range('55-33').combinations == Range('22 33 44 55').combinations


class TestCaseInsensitive:
    def test_pairs(self):
        assert Range('aA') == Range('AA')
        assert Range('TT') == Range('tt')

    def test_offsuit(self):
        assert Range('AkO') == Range('AKo')

    def test_suited(self):
        assert Range('AKs') == Range('kaS')


class TestPercentages:
    def test_one_pair(self):
        assert Range('22').percent == 0.45

    def test_one_suited_card(self):
        assert Range('AKs').percent == 0.3

    def test_one_offsuit_card(self):
        assert Range('Ako').percent == 0.9

    def test_pair_range(self):
        assert Range('88+').percent == 3.17

    def test_pair_and_offsuit(self):
        assert Range('22 AKo').percent == 1.36


class TestNumberOfCombinations:
    """Test number of hand combinations by suits."""

    def test_one_pair(self):
        assert len(Range('22')) == 6
        assert len(Range('QQ')) == 6

    def test_pair_range(self):
        assert len(Range('22-55')) == 24
        assert len(Range('55-22')) == 24

    def test_one_suited_hand(self):
        assert len(Range('AKs')) == 4
        assert len(Range('76s')) == 4

    def test_one_offsuit_card(self):
        assert len(Range('AKo')) == 12


class TestComposeHands:
    """Test different constructors and composition of hands."""

    def test_pairs_from_hands(self):
        assert Range.from_hands({Hand('AA'), Hand('KK'), Hand('QQ')}) == Range('QQ+')

    def test_pairs_from_strings(self):
        assert Range.from_strings(('AA', 'KK', 'QQ')) == Range('QQ+')
        assert Range.from_strings(['AA', 'KK', 'QQ']) == Range('QQ+')

    def test_from_combinations(self):
        range = Range.from_combinations(DEUCE_COMBINATIONS)
        assert range == Range('22')
        assert range.combinations == DEUCE_COMBINATIONS
        assert range.hands == (Hand('22'))

    def test_from_percent(self):
        assert Range.from_percent(0.9) == Range('KK+')

    def test_from_percent_comparison(self):
        # both represents 0.9%, but they should not be equal
        assert Range('AKo') != Range.from_percent(0.9)


class TestRangeEquality:
    """Tests if two range objects are equal."""

    def test_pairs_with_dash_equals_pairs_with_dash_reverse(self):
        assert Range('33-22').hands == Range('22-33').hands

    def test_offsuit_multiple_with_AK(self):
        assert Range('AKo 22+ 45 33') == Range('22+ AKo 54')

    def test_empty_range(self):
        assert Range() == Range('')


class ValueChecks:
    def test_invalid_pair(self):
        with raises(ValueError):
            Range('HH')

    def test_invalid_offsuit(self):
        with raises(ValueError):
            Range('KKo')

    def test_multiple_ranges_one_invalid(self):
        with raises(ValueError):
            Range('22+ AKo JK2')

    def test_invalid_range_from_hands_should_raise_ValueError(self):
        with raises(ValueError):
            Range.from_strings(['AA', 'KK+'])

    def test_invalid_combinations(self):
        with raises(ValueError):
            Range('AsKq')


class TestNormalization:
    """Test for repr, str representation and range normalization."""

    def test_str_and_range(self):
        range = Range('77+ AKo')
        assert repr(range) == "Range({})".format(str(range))

    def test_order_with_suit_and_without_suit(self):
        range = Range('Kas 48')
        assert repr(range) == "Range('AKs 84')"
        assert str(range) == 'AKs, 84'

    def test_pairs_order(self):
        range = Range('22-55')
        assert repr(range) == "Range('55-22')"
        assert str(range) == '55-22'

    def test_reduntant_pairs(self):
        range = Range('22-44 33')
        assert str(range) == '44-22'
        assert repr(range) == "Range('44-22')"

    def test_redundant_offsuit_hands(self):
        range = Range('A2o+ 2Ao 8ao')
        assert str(range) == 'A2o+'
        assert repr(range) == "Range('A2o+')"

    def test_redundant_suited_hands(self):
        range = Range('2as+ A5s A7s')
        assert str(range) == 'A2s+'
        assert repr(range) == "Range('A2s+')"

    def test_redundant_plus_in_pair(self):
        assert str(Range('AA+')) == 'AA'

    def test_redundant_plus_in_suited_hand(self):
        assert str(Range('87s+')) == '87s'

    def test_redundant_plus_in_offsuit_hand(self):
        assert str(Range('AKo+')) == 'AKo'
