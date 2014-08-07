import pytest
from datetime import datetime
from decimal import Decimal
from collections import OrderedDict
import pytz
from poker.handhistory import FullTiltHand
from . import ftp_hands


ET = pytz.timezone('US/Eastern')


@pytest.fixture
def hand_header(request):
    """Parse hand history header only defined in hand_text and returns a PokerStarsHand instance."""
    h = FullTiltHand(request.instance.hand_text, parse=False)
    h.parse_header()
    return h


@pytest.fixture
def hand(request):
    """Parse handhistory defined in hand_text class attribute and returns a PokerStarsHand instance."""
    return FullTiltHand(request.instance.hand_text)


class TestHandWithFlopOnly:
    hand_text = ftp_hands.HAND1

    @pytest.mark.parametrize('attribute,expected_value',
                             [('game_type', 'TOUR'),
                              ('sb', Decimal(10)),
                              ('bb', Decimal(20)),
                              ('date', ET.localize(datetime(2013, 9, 22, 13, 26, 50))),
                              ('game', 'HOLDEM'),
                              ('limit', 'NL'),
                              ('ident', '33286946295'),
                              ('tournament_ident', '255707037'),
                              ('tournament_name', 'MiniFTOPS Main Event'),
                              ('table_name', '179'),
                              ('tournament_level', None),
                              ('buyin', None),
                              ('rake', None),
                              ('currency', None),
                             ])
    def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value

    @pytest.mark.parametrize('attribute,expected_value',
                             [('players', OrderedDict([('Popp1987', 13587), ('Luckytobgood', 10110),
                                                       ('FatalRevange', 9970), ('IgaziFerfi', 10000),
                                                       ('egis25', 6873), ('gamblie', 9880), ('idanuTz1', 10180),
                                                       ('PtheProphet', 9930), ('JohnyyR', 9840)])),
                              ('button', 'egis25'),
                              ('button_seat', 5),
                              ('max_players', 9),
                              ('hero', 'IgaziFerfi'),
                              ('hero_seat', 4),
                              ('hero_hole_cards', ('9d', 'Ks')),
                              ('preflop_actions', ('PtheProphet has 15 seconds left to act',
                                                   'PtheProphet folds',
                                                   'JohnyyR raises to 40',
                                                   'Popp1987 has 15 seconds left to act',
                                                   'Popp1987 folds',
                                                   'Luckytobgood folds',
                                                   'FatalRevange raises to 100',
                                                   'IgaziFerfi folds',
                                                   'egis25 folds',
                                                   'gamblie folds',
                                                   'idanuTz1 folds',
                                                   'JohnyyR has 15 seconds left to act',
                                                   'JohnyyR calls 60')),
                              ('flop', ('8h', '4h', 'Tc')),
                              ('flop_pot', Decimal(230)),
                              ('flop_num_players', 2),
                              ('flop_actions', ('JohnyyR checks',
                                                'FatalRevange has 15 seconds left to act',
                                                'FatalRevange bets 120',
                                                'JohnyyR folds',
                                                'Uncalled bet of 120 returned to FatalRevange',
                                                'FatalRevange mucks',
                                                'FatalRevange wins the pot (230)')),
                              ('turn', None),
                              ('turn_pot', None),
                              ('turn_actions', None),
                              ('turn_num_players', None),
                              ('river', None),
                              ('river_pot', None),
                              ('river_actions', None),
                              ('river_num_players', None),
                              ('total_pot', Decimal(230)),
                              ('show_down', False),
                              ('winners', ('FatalRevange',)),
                              ('board', ('8h', '4h', 'Tc'))
                             ])
    def test_body(self, hand, attribute, expected_value):
        assert getattr(hand, attribute) == expected_value


class TestHandWithFlopTurnRiver:
    hand_text = ftp_hands.HAND2

    @pytest.mark.parametrize('attribute,expected_value',
                             [('players', OrderedDict([('Player0', 5745), ('Player1', 5930),
                                                       ('Player2', 6030), ('Player3', 2405),
                                                       ('Player4', 2275), ('Player5', 3547),
                                                       ('Hero', 4000), ('Player6', 8043),
                                                       ('Player7', 3865)])),
                              ('button', 'Player0'),
                              ('button_seat', 1),
                              ('max_players', 9),
                              ('hero', 'Hero'),
                              ('hero_seat', 7),
                              ('hero_hole_cards', ('Qc', '9s')),
                              ('preflop_actions', ('Player3 calls 30',
                                                   'Player4 has 15 seconds left to act',
                                                   'Player4 calls 30',
                                                   'Player5 has 15 seconds left to act',
                                                   'Player5 has timed out',
                                                   'Player5 folds',
                                                   'Player5 is sitting out',
                                                   'Hero folds',
                                                   'Player6 calls 30',
                                                   'Player7 calls 30',
                                                   'Player0 folds',
                                                   'Player1 folds',
                                                   'Player2 checks')),
                              ('flop', ('4h', '5d', 'Jh')),
                              ('flop_actions', ('Player2 checks',
                                                'Player3 bets 165',
                                                'Player4 folds',
                                                'Player5 has returned',
                                                'Player6 calls 165',
                                                'Player7 calls 165',
                                                'Player2 folds')),
                              ('flop_pot', Decimal('165')),
                              ('flop_num_players', 5),
                              ('turn', '8c'),
                              ('turn_pot', Decimal(660)),
                              ('turn_num_players', 3),
                              ('turn_actions', ('Player3 checks',
                                                'Player6 checks',
                                                'Player7 checks')),
                              ('river', '7h'),
                              ('river_pot', Decimal(660)),
                              ('river_num_players', 3),
                              ('river_actions', ('Player3 bets 660',
                                                 'Player6 folds',
                                                 'Player7 has 15 seconds left to act',
                                                 'Player7 raises to 1,665',
                                                 'Player3 calls 1,005')),
                              ('total_pot', Decimal('3990')),
                              ('show_down', True),
                              ('winners', ('Player7',)),
                              ('board', ('4h', '5d', 'Jh', '8c', '7h'))
                             ])
    def test_body(self, hand, attribute, expected_value):
        assert getattr(hand, attribute) == expected_value
