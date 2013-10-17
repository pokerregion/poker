import pytest
import ftp_hands
from datetime import datetime
from decimal import Decimal
from collections import OrderedDict
from handparser import FullTiltHand, ET


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
