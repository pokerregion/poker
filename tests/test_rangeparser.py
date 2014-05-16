# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pytest import raises
from rangeparser import Range, RangeSyntaxError, RangeError


ALL_DEUCES = {'2s2c', '2s2d', '2s2h', '2c2d', '2c2h', '2d2h'}
ALL_THREES = {'3s3c', '3s3d', '3s3h', '3c3d', '3c3h', '3d3h'}

ALL_PAIRS = {'AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', '44', '33', '22'}
BROADWAY_PAIRS = {'AA', 'KK', 'QQ', 'JJ', 'TT', }


class TestHandsResultsAfterParse:
    def test_pairs_simple(self):
        assert Range('22').hands == {'22'}

    def test_pairs_multiple(self):
        assert Range('22 33').hands == {'22', '33'}

    def test_pairs_with_plus(self):
        assert Range('88+').hands == BROADWAY_PAIRS + {'99', '88'}
        assert Range('22+').hands == ALL_PAIRS

    def test_pairs_with_dash(self):
        assert Range('22-55').hands == {'22', '33', '44', '55'}
        assert Range('22-33').hands == {'22', '33'}

    def test_pairs_with_dash_reverse(self):
        assert Range('55-22').hands == {'55', '44', '33', '22'}
        assert Range('33-22').hands == {'22', '33'}

    def test_multiple_offsuit_hands(self):
        assert Range('AKo 84o').hands == {'AKo', '84o'}

    def test_hands_without_suit(self):
        assert Range('AK 48').hands == {'AKo', 'AKs', '84o', '84s'}

    def test_dash_offsuit(self):
        assert Range('J8o-J4o').hands == {'J8o', 'J7o', 'J6o', 'J5o', 'J4o'}

    def test_dash_suited(self):
        assert Range('J8s-J4s').hands == {'J8s', 'J7s', 'J6s', 'J5s', 'J4s'}


class TestCombinationsResultsAfterParse:
    def test_pairs_simple(self):
        """Test if pairs get all the combinations."""
        assert Range('22').combinations == ALL_DEUCES

    def test_pairs_multiple(self):
        assert Range('22 33').combinations == ALL_DEUCES | ALL_THREES

    def test_pairs_with_dash(self):
        assert Range('22-33').combinations == ALL_DEUCES | ALL_THREES

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
        assert Range.from_hands({'AA', 'KK', 'QQ'}) == Range('QQ+')
        assert Range.from_hands(('AA', 'KK', 'QQ')) == Range('QQ+')
        assert Range.from_hands(['AA', 'KK', 'QQ']) == Range('QQ+')

    def test_pairs_from_combinations(self):
        assert Range.from_combinations(ALL_DEUCES) == Range('22')

    def test_from_percent(self):
        assert Range.from_percent(0.9) == Range('KK+')

    def test_from_percent_comparison(self):
        assert Range('AKo') != Range.from_percent(0.9)


class TestRangeEquality:
    """Tests if two range objects are equal."""

    def test_pairs_with_dash_equals_pairs_with_dash_reverse(self):
        assert Range('33-22').hands == Range('22-33').hands

    def test_offsuit_multiple_with_AK(self):
        assert Range('AKo 22+ 45 33') == Range('22+ AKo 54')


class TestSyntaxCheck:
    """Test separation by space, comma, semicolon and a mix of those."""

    def test_invalid_hands(self):
        with raises(TypeError):
            Range.from_hands('this makes no sense')

        with raises(TypeError):
            Range.from_hands('AA KK')

    def test_invalid_pair(self):
        with raises(RangeSyntaxError):
            Range('HH')

    def test_invalid_offsuit(self):
        with raises(RangeSyntaxError):
            Range('KKo')

    def test_multiple_ranges_one_invalid(self):
        with raises(RangeSyntaxError):
            Range('22+ AKo JK2')

    def test_invalid_range_from_hands_should_raise_sytanxerror(self):
        invalid_hands = {'AA', 'KK+'}
        with raises(RangeError):
            Range.from_hands(invalid_hands)

    def test_invalid_combinations(self):
        with raises(RangeSyntaxError):
            Range('AsKq')


class TestNormalization:
    """Test for repr, str representation and range normalization."""

    def test_str_and_range(self):
        range = Range('77+ AKo')
        assert repr(range) == "Range({})".format(str(range))

    def test_order_with_suit_and_without_suit(self):
        range = Range('Kas 48')
        assert repr(range) == "Range('AKs 84')"
        assert str(range) == 'AKs 84'

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
