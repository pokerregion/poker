from collections import MutableMapping, OrderedDict
import pytest
from handparser import PokerStarsHand, ET
import hand_data
from decimal import Decimal
from datetime import datetime


class TestDictBehavior:
    def test_hand_is_mutablemapping(self, all_hands):
        assert isinstance(all_hands, MutableMapping)

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
    hand_text = hand_data.HAND1
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
    def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value

    @pytest.mark.parametrize(('attribute', 'expected_value'),
                             [('table_name', '797469411 15'),
                              ('max_players', 9),
                              ('button_seat', 1),
                              ('button', 'flettl2'),
                              ('hero', 'W2lkm2n'),
                              ('hero_seat', 5),
                              ('players', OrderedDict([('flettl2', 1500), ('santy312', 3000), ('flavio766', 3000),
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
    def test_body(self, hand, attribute, expected_value):
        assert getattr(hand, attribute) == expected_value


class TestAllinPreflopHand:
    hand_text = hand_data.HAND2

    @pytest.mark.parametrize(('attribute', 'expected_value'),
                             [('poker_room', 'STARS'),
                              ('ident', '105034215446'),
                              ('game_type', 'TOUR'),
                              ('tournament_ident', '797536898'),
                              ('tournament_level', 'XI'),
                              ('currency', 'USD'),
                              ('buyin', Decimal('3.19')),
                              ('rake', Decimal('0.31')),
                              ('game', 'HOLDEM'),
                              ('limit', 'NL'),
                              ('sb', Decimal(400)),
                              ('bb', Decimal(800)),
                              ('date', ET.localize(datetime(2013, 10, 4, 17, 22, 20))),
                              ])
    def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value

    @pytest.mark.parametrize(('attribute', 'expected_value'),
                             [('table_name', '797536898 9'),
                              ('max_players', 9),
                              ('button_seat', 2),
                              ('button', 'W2lkm2n'),
                              ('hero', 'W2lkm2n'),
                              ('hero_seat', 2),
                              ('players', OrderedDict([('RichFatWhale', 12910), ('W2lkm2n', 11815), ('Labahra', 7395),
                                                       ('Lean Abadia', 7765), ('lkenny44', 10080), ('Newfie_187', 1030),
                                                       ('Hokolix', 13175), ('pmmr', 2415), ('costamar', 13070)])),
                              ('hero_hole_cards', ('Jd', 'Js')),
                              ('flop', ('3c', '6s', '9d')),
                              ('turn', '8d'),
                              ('river', 'Ks'),
                              ('board', ('3c', '6s', '9d', '8d', 'Ks')),
                              ('preflop_actions', ("lkenny44: folds",
                                                   "Newfie_187: raises 155 to 955 and is all-in",
                                                   "Hokolix: folds",
                                                   "pmmr: folds",
                                                   "costamar: raises 12040 to 12995 and is all-in",
                                                   "RichFatWhale: folds",
                                                   "W2lkm2n: calls 11740 and is all-in",
                                                   "Labahra: folds",
                                                   "Lean Abadia: folds",
                                                   "Uncalled bet (1255) returned to costamar")),
                              ('flop_actions', None),
                              ('turn_actions', None),
                              ('river_actions', None),
                              ('total_pot', Decimal(26310)),
                              ('show_down', True),
                              ('winners', ('costamar',)),
                              ])
    def test_body(self, hand, attribute, expected_value):
        assert getattr(hand, attribute) == expected_value


class TestBodyMissingPlayerNoBoard:
    hand_text = hand_data.HAND3

    @pytest.mark.parametrize(('attribute', 'expected_value'),
                             [('poker_room', 'STARS'),
                              ('ident', '105026771696'),
                              ('game_type', 'TOUR'),
                              ('tournament_ident', '797469411'),
                              ('tournament_level', 'X'),
                              ('currency', 'USD'),
                              ('buyin', Decimal('3.19')),
                              ('rake', Decimal('0.31')),
                              ('game', 'HOLDEM'),
                              ('limit', 'NL'),
                              ('sb', Decimal(300)),
                              ('bb', Decimal(600)),
                              ('date', ET.localize(datetime(2013, 10, 4, 14, 50, 56)))
                             ])
    def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value

    @pytest.mark.parametrize(('attribute', 'expected_value'),
                             [('table_name', '797469411 11'),
                              ('max_players', 9),
                              ('button_seat', 8),
                              ('button', 'W2lkm2n'),
                              ('hero', 'W2lkm2n'),
                              ('hero_seat', 8),
                              ('players', OrderedDict([('Empty Seat 1', 0), ('snelle_jel', 4295), ('EuSh0wTelm0', 11501),
                                                       ('panost3', 7014), ('Samovlyblen', 7620), ('Theralion', 4378),
                                                       ('wrsport1015', 9880), ('W2lkm2n', 10714), ('fischero68', 8724)])),
                              ('hero_hole_cards', ('6d', '8d')),
                              ('flop', None),
                              ('turn', None),
                              ('river', None),
                              ('board', None),
                              ('preflop_actions', ('EuSh0wTelm0: folds',
                                                   'panost3: folds',
                                                   'Samovlyblen: folds',
                                                   'Theralion: raises 600 to 1200',
                                                   'wrsport1015: folds',
                                                   'W2lkm2n: folds',
                                                   'fischero68: folds',
                                                   'snelle_jel: folds',
                                                   'Uncalled bet (600) returned to Theralion',
                                                   'Theralion collected 1900 from pot',
                                                   "Theralion: doesn't show hand")),
                              ('flop_actions', None),
                              ('turn_actions', None),
                              ('river_actions', None),
                              ('total_pot', Decimal(1900)),
                              ('show_down', False),
                              ('winners', ('Theralion',)),
                              ])
    def test_body(self, hand, attribute, expected_value):
        assert getattr(hand, attribute) == expected_value


class TestBodyEveryStreet:
    hand_text = hand_data.HAND4

    @pytest.mark.parametrize(('attribute', 'expected_value'),
                             [('poker_room', 'STARS'),
                              ('ident', '105025168298'),
                              ('game_type', 'TOUR'),
                              ('tournament_ident', '797469411'),
                              ('tournament_level', 'IV'),
                              ('currency', 'USD'),
                              ('buyin', Decimal('3.19')),
                              ('rake', Decimal('0.31')),
                              ('game', 'HOLDEM'),
                              ('limit', 'NL'),
                              ('sb', Decimal(50)),
                              ('bb', Decimal(100)),
                              ('date', ET.localize(datetime(2013, 10, 4, 14, 19, 17)))
                             ])
    def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value

    @pytest.mark.parametrize(('attribute', 'expected_value'),
                             [('table_name', '797469411 15'),
                              ('max_players', 9),
                              ('button_seat', 5),
                              ('button', 'W2lkm2n'),
                              ('hero', 'W2lkm2n'),
                              ('hero_seat', 5),
                              ('players', OrderedDict([('flettl2', 3000), ('santy312', 5890), ('flavio766', 11010),
                                                       ('strongi82', 2855), ('W2lkm2n', 5145), ('MISTRPerfect', 2395),
                                                       ('blak_douglas', 3000), ('sinus91', 3000), ('STBIJUJA', 1205)])),
                              ('hero_hole_cards', ('Jc', '5c')),
                              ('flop', ('6s', '4d', '3s')),
                              ('turn', '8c'),
                              ('river', 'Kd'),
                              ('board', ('6s', '4d', '3s', '8c', 'Kd')),
                              ('preflop_actions', ('sinus91: folds',
                                                   'STBIJUJA: folds',
                                                   'flettl2: raises 125 to 225',
                                                   'santy312: folds',
                                                   'flavio766: folds',
                                                   'strongi82: folds',
                                                   'W2lkm2n: folds',
                                                   'MISTRPerfect: folds',
                                                   'blak_douglas: calls 125')),
                              ('flop_actions', ('blak_douglas: checks',
                                                'flettl2: bets 150',
                                                'blak_douglas: calls 150')),
                              ('turn_actions', ('blak_douglas: checks',
                                                'flettl2: bets 250',
                                                'blak_douglas: calls 250')),
                              ('river_actions', ('blak_douglas: checks',
                                                 'flettl2: bets 1300',
                                                 'blak_douglas: folds',
                                                 'Uncalled bet (1300) returned to flettl2',
                                                 'flettl2 collected 1300 from pot',
                                                 "flettl2: doesn't show hand")),
                              ('total_pot', Decimal(1300)),
                              ('show_down', False),
                              ('winners', ('flettl2',)),
                              ])
    def test_body(self, hand, attribute, expected_value):
        assert getattr(hand, attribute) == expected_value


class TestClassRepresentation:
    hand_text = hand_data.HAND1

    def test_unicode(self, hand_header):
        assert u'<PokerStarsHand: STARS hand #105024000105>' == unicode(hand_header)

    def test_str(self, hand_header):
        assert '<PokerStarsHand: STARS hand #105024000105>' == str(hand_header)


class TestPlayerNameWithDot:
    hand_text = hand_data.HAND5

    def test_player_is_in_player_list(self, hand):
        assert '.prestige.U$' in hand.players

    def test_player_stack(self, hand):
        assert hand.players['.prestige.U$'] == 3000
