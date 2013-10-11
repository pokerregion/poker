import collections
import pytest
from handparser import PokerStarsHand, ET
import test_data
from decimal import Decimal
from datetime import datetime


all_test_hands = [eval('test_data.HAND%d' % num) for num in range(1, 6)]

@pytest.fixture(params=all_test_hands)
def all_hands(request):
    return PokerStarsHand(request.param)


@pytest.fixture
def hand_header():
    h = PokerStarsHand(test_data.HAND1, parse=False)
    h.parse_header()
    return h


class TestDictBehavior:
    def test_hand_is_mutablemapping(self, all_hands):
        assert isinstance(all_hands, collections.MutableMapping)

    def test_all_keys_set(self, all_hands):
        excpected_keys = {'ident', 'currency', 'hero_hole_cards', 'preflop_actions', 'turn', 'show_down', 'poker_room',
                          'winners', 'board', 'limit', 'river_actions', 'hero', 'turn_actions', 'bb', 'button_seat',
                          'tournament_ident', 'rake', 'buyin', 'game', 'hero_seat', 'date', 'max_players',
                          'flop_actions', 'button', 'flop', 'game_type', 'players', 'table_name', 'sb', 'total_pot',
                          'river', 'tournament_level'}
        assert excpected_keys == set(all_hands.keys())

    def test_raw_is_not_a_key(self, all_hands):
        with pytest.raises(KeyError):
            all_hands['raw']

    def test_raw_is_an_attribute(self, all_hands):
        assert hasattr(all_hands, 'raw')

    def test_there_should_be_not_only_one_but_thirtyfour_keys(self, all_hands):
        assert 32 == len(all_hands) == len(all_hands.keys())


class TestHeaderHand1:
    @pytest.fixture(params=[('poker_room', 'STARS'),
                            ('ident', '105024000105'),
                            ('game_type', 'TOUR'),
                            ('tournament_ident', '797469411'),
                            ('tournament_level', 'I'),
                            ('currency', 'USD'),
                            ('buyin', Decimal('3.19')),
                            ('rake', Decimal('0.31')),
                            ('game', 'HOLDEM'),
                            ('limit', 'NL'),
                            ('sb', Decimal(10)),
                            ('bb', Decimal(20)),
                            ('date', ET.localize(datetime(2013, 10, 4, 13, 53, 27)))
                            ])
    def hand_header(self, request):
        self.attribute, self.attribute_result = request.param
        return PokerStarsHand(test_data.HAND1)

    def test_value(self, hand_header):
        assert getattr(hand_header, self.attribute) == self.attribute_result

