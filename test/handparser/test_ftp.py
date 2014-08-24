import pytest
from datetime import datetime
from decimal import Decimal
from collections import OrderedDict
import pytz
from poker.room.fulltiltpoker import FullTiltPokerHandHistory
from poker.card import Card
from poker.hand import Combo
from poker.handhistory import HandHistoryPlayer
from . import ftp_hands


ET = pytz.timezone('US/Eastern')


@pytest.fixture
def hand_header(request):
    """Parse hand history header only defined in hand_text and returns a FullTiltPokerHandHistory instance."""
    h = FullTiltPokerHandHistory(request.instance.hand_text)
    h.parse_header()
    return h


@pytest.fixture
def hand(request):
    """Parse handhistory defined in hand_text class attribute and returns a FullTiltPokerHandHistory instance."""
    hh = FullTiltPokerHandHistory(request.instance.hand_text)
    hh.parse()
    return hh


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
        [('players', [
            HandHistoryPlayer(name='Popp1987', stack=13587, seat=1, combo=None),
            HandHistoryPlayer(name='Luckytobgood', stack=10110, seat=2, combo=None),
            HandHistoryPlayer(name='FatalRevange', stack=9970, seat=3, combo=None),
            HandHistoryPlayer(name='IgaziFerfi', stack=10000, seat=4, combo=Combo('Ks9d')),
            HandHistoryPlayer(name='egis25', stack=6873, seat=5, combo=None),
            HandHistoryPlayer(name='gamblie', stack=9880, seat=6, combo=None),
            HandHistoryPlayer(name='idanuTz1', stack=10180, seat=7, combo=None),
            HandHistoryPlayer(name='PtheProphet', stack=9930, seat=8, combo=None),
            HandHistoryPlayer(name='JohnyyR', stack=9840, seat=9, combo=None),
        ]),
        ('button', HandHistoryPlayer(name='egis25', stack=6873, seat=5, combo=None)),
        ('max_players', 9),
        ('hero', HandHistoryPlayer(name='IgaziFerfi', stack=10000, seat=4, combo=Combo('Ks9d'))),
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
        ('flop', (Card('8h'), Card('4h'), Card('Tc'))),
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
        ('board', (Card('8h'), Card('4h'), Card('Tc')))
        ])
    def test_body(self, hand, attribute, expected_value):
        assert getattr(hand, attribute) == expected_value


class TestHandWithFlopTurnRiver:
    hand_text = ftp_hands.TURBO_SNG

    @pytest.mark.parametrize('attribute,expected_value',
        [('game_type', 'SNG'),
         ('sb', Decimal(15)),
         ('bb', Decimal(30)),
         ('date', ET.localize(datetime(2014, 6, 29, 5, 57, 1))),
         ('game', 'HOLDEM'),
         ('limit', 'NL'),
         ('ident', '34374264321'),
         ('tournament_ident', '268569961'),
         ('tournament_name', '$10 Sit & Go (Turbo)'),
         ('table_name', '1'),
         ('tournament_level', None),
         ('buyin', Decimal(10)),
         ('rake', None),
         ('currency', 'USD'),
        ])
    def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value

    @pytest.mark.parametrize('attribute,expected_value',
        [('players', [
            HandHistoryPlayer(name='snake 422', stack=1500, seat=1, combo=None),
            HandHistoryPlayer(name='IgaziFerfi', stack=1500, seat=2, combo=Combo('5d2h')),
            HandHistoryPlayer(name='MixaOne', stack=1500, seat=3, combo=None),
            HandHistoryPlayer(name='BokkaBlake', stack=1500, seat=4, combo=None),
            HandHistoryPlayer(name='Sajiee', stack=1500, seat=5, combo=None),
            HandHistoryPlayer(name='AzzzJJ', stack=1500, seat=6, combo=None),
        ]),
        ('button', HandHistoryPlayer(name='AzzzJJ', stack=1500, seat=6, combo=None)),
        ('max_players', 6),
        ('hero', HandHistoryPlayer(name='IgaziFerfi', stack=1500, seat=2, combo=Combo('5d2h'))),
        ('preflop_actions', ('MixaOne calls 30',
                             'BokkaBlake folds',
                             'Sajiee folds',
                             'AzzzJJ raises to 90',
                             'snake 422 folds',
                             'IgaziFerfi folds',
                             'MixaOne calls 60',)
        ),
        ('flop', (Card('6s'), Card('9c'), Card('3d'))),
        ('flop_actions', ('MixaOne bets 30',
                          'AzzzJJ raises to 120',
                          'MixaOne folds',
                          'Uncalled bet of 90 returned to AzzzJJ',
                          'AzzzJJ mucks',
                          'AzzzJJ wins the pot (285)',)
        ),
        ('flop_pot', Decimal('225')),
        ('flop_num_players', 2),
        ('turn', None),
        ('turn_pot', None),
        ('turn_num_players', None),
        ('turn_actions', None),
        ('river', None),
        ('river_pot', None),
        ('river_num_players', None),
        ('river_actions', None),
        ('total_pot', Decimal('285')),
        ('show_down', False),
        ('winners', ('AzzzJJ',)),
        ('board', (Card('6s'), Card('9c'), Card('3d')))
        ])
    def test_body(self, hand, attribute, expected_value):
        assert getattr(hand, attribute) == expected_value
