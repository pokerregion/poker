import collections
import pytest
from handparser import PokerStarsHand, ET
import test_data
from decimal import Decimal
from datetime import datetime


all_test_hands = [eval('test_data.HAND%d' % num) for num in range(1, 6)]

@pytest.fixture(params=all_test_hands)
def all_hands(request):
    """Parse all hands from test_data and gives back a PokerStarsHand instance."""
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


class TestHandWithFlopOnly:
    hand_text = test_data.HAND1
    # in py.test 2.4 it is recommended to use string like "attribute,expected",
    # but with tuple, it works in both 2.3.5 and 2.4
    @pytest.mark.parametrize(('attribute', 'expected_value'),
                              [('poker_room', 'STARS'),
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
    def test_header(self, attribute, expected_value):
        hand = PokerStarsHand(self.hand_text)
        assert getattr(hand, attribute) == expected_value

    @pytest.mark.parametrize(('attribute', 'expected_value'),
                             [('table_name', '797469411 15'),
                              ('max_players', 9),
                              ('button_seat', 1),
                              ('button', 'flettl2'),
                              ('hero', 'W2lkm2n'),
                              ('hero_seat', 5),
                              ('players', collections.OrderedDict(
                                                       [('flettl2', 1500), ('santy312', 3000), ('flavio766', 3000),
                                                       ('strongi82', 3000), ('W2lkm2n', 3000), ('MISTRPerfect', 3000),
                                                       ('blak_douglas', 3000), ('sinus91', 1500), ('STBIJUJA', 1500)])),
                              ('hero_hole_cards', ('Ac', 'Jh')),
                              ('flop', ('2s', '6d', '6h')),
                              ('turn', None),
                              ('river', None),
                              ('board', ('2s', '6d', '6h')),
                              ('preflop_actions', ("strongi82: folds",
                                                   "W2lkm2n: raises 40 to 60",
                                                   "MISTRPerfect: calls 60",
                                                   "blak_douglas: folds",
                                                   "sinus91: folds",
                                                   "STBIJUJA: folds",
                                                   "flettl2: folds",
                                                   "santy312: folds",
                                                   "flavio766: folds")),
                              ('flop_actions', ('W2lkm2n: bets 80',
                                                'MISTRPerfect: folds',
                                                'Uncalled bet (80) returned to W2lkm2n',
                                                'W2lkm2n collected 150 from pot',
                                                "W2lkm2n: doesn't show hand")),
                              ('turn_actions', None),
                              ('river_actions', None),
                              ('total_pot', Decimal(150)),
                              ('show_down', False),
                              ('winners', ('W2lkm2n',)),
                              ])
    def test_body(self, attribute, expected_value):
        hand = PokerStarsHand(self.hand_text)
        assert getattr(hand, attribute) == expected_value
