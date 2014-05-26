# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function

from rangeparser import Hand, Rank, InvalidHand, InvalidRank
from pytest import raises


def test_first_and_second_are_instances_of_Rank():
    assert isinstance(Hand('22').first, Rank)
    assert Hand('22').first == Rank('2')
    assert isinstance(Hand('22').second, Rank)
    assert Hand('22').second == Rank('2')


def test_representations():
    assert str(Hand('22')) == '22'
    assert unicode(Hand('22')) == u'22'
    assert repr(Hand('22')) == "Hand('22')"


def test_ordering():
    assert Hand('AKo') > Hand('AQs')
    assert Hand('AKo') > Hand('KQo')
    assert Hand('AKs') > Hand('54o')
    assert Hand('AJo') > Hand('A2s')
    assert Hand('AJo') > Hand('A2o')
    assert Hand('KQo') > Hand('KJo')
    assert Hand('76s') > Hand('75s')
    assert Hand('76o') > Hand('75s')

    assert Hand('33') > Hand('22')
    assert Hand('22') > Hand('JTo')
    assert Hand('22') > Hand('A2o')
    assert Hand('22') > Hand('A3s')
    assert Hand('JJ') > Hand('JTs')
    assert Hand('JJ') > Hand('AJs')

    assert Hand('76s') > Hand('76o')


def test_different_suits_are_equal_if_ranks_are_the_same():
    assert Hand('AKo') == Hand('AKo')


def test_case_insensitive():
    assert Hand('AKo') == Hand('akO')


def test_equality():
    assert Hand('AKs') != Hand('44')
    assert Hand('22') != Hand('33')
    assert Hand('22') == Hand('22')


def test_is_suited():
    assert Hand('AKs').is_suited() is True

    assert Hand('AKo').is_suited() is False
    assert Hand('22').is_suited() is False


def test_is_offsuit():
    assert Hand('AKs').is_offsuit() is False
    assert Hand('AKo').is_offsuit() is True
    assert Hand('22').is_offsuit() is False


def test_is_connector():
    assert Hand('76o').is_connector() is True
    assert Hand('AKo').is_connector() is True

    assert Hand('22').is_connector() is False
    assert Hand('85o').is_connector() is False


def test_is_one_gapper():
    assert Hand('86s').is_one_gapper() is True
    assert Hand('AQo').is_one_gapper() is True


def test_is_two_gapper():
    assert Hand('85s').is_two_gapper() is True
    assert Hand('AJo').is_two_gapper() is True

    assert Hand('86s').is_two_gapper() is False
    assert Hand('ATo').is_two_gapper() is False


def test_is_suited_connector():
    assert Hand('76s').is_suited_connector() is True
    assert Hand('45s').is_suited_connector() is True

    assert Hand('55').is_suited_connector() is False
    assert Hand('76o').is_suited_connector() is False


def test_is_broadway():
    assert Hand('AKo').is_broadway() is True
    assert Hand('J9o').is_broadway() is False
    assert Hand('99').is_broadway() is False


def test_is_pair():
    assert Hand('22').is_pair() is True
    assert Hand('86s').is_pair() is False


class TestInvalidHands:
    def test_invalid_suit(self):
        with raises(InvalidHand):
            Hand('32l')

    def test_invalid_rank(self):
        with raises(InvalidRank):
            Hand('AMs')

    def test_pair_with_suit(self):
        with raises(InvalidHand):
            Hand('22s')

    def test_hand_without_suit(self):
        with raises(InvalidHand):
            Hand('AK')
