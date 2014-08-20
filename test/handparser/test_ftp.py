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
    """Parse hand history header only defined in hand_text and returns a PokerStarsHandHistory instance."""
    h = FullTiltPokerHandHistory(request.instance.hand_text, parse=False)
    h.parse_header()
    return h


@pytest.fixture
def hand(request):
    """Parse handhistory defined in hand_text class attribute and returns a PokerStarsHandHistory instance."""
    return FullTiltPokerHandHistory(request.instance.hand_text)


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
    hand_text = ftp_hands.HAND2

    @pytest.mark.parametrize('attribute,expected_value',
        [('players', [
            HandHistoryPlayer(name='Player0', stack=5745, seat=1, combo=None),
            HandHistoryPlayer(name='Player1', stack=5930, seat=2, combo=None),
            HandHistoryPlayer(name='Player2', stack=6030, seat=3, combo=None),
            HandHistoryPlayer(name='Player3', stack=2405, seat=4, combo=None),
            HandHistoryPlayer(name='Player4', stack=2275, seat=5, combo=None),
            HandHistoryPlayer(name='Player5', stack=3547, seat=6, combo=None),
            HandHistoryPlayer(name='Hero', stack=4000, seat=7, combo=Combo('Qc9s')),
            HandHistoryPlayer(name='Player6', stack=8043, seat=8, combo=None),
            HandHistoryPlayer(name='Player7', stack=3865, seat=9, combo=None),
        ]),
        ('button', HandHistoryPlayer(name='Player0', stack=5745, seat=1, combo=None)),
        ('max_players', 9),
        ('hero', HandHistoryPlayer(name='Hero', stack=4000, seat=7, combo=Combo('Qc9s'))),
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
        ('flop', (Card('4h'), Card('5d'), Card('Jh'))),
        ('flop_actions', ('Player2 checks',
                        'Player3 bets 165',
                        'Player4 folds',
                        'Player5 has returned',
                        'Player6 calls 165',
                        'Player7 calls 165',
                        'Player2 folds')),
        ('flop_pot', Decimal('165')),
        ('flop_num_players', 5),
        ('turn', Card('8c')),
        ('turn_pot', Decimal(660)),
        ('turn_num_players', 3),
        ('turn_actions', ('Player3 checks',
                        'Player6 checks',
                        'Player7 checks')),
        ('river', Card('7h')),
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
        ('board', (Card('4h'), Card('5d'), Card('Jh'), Card('8c'), Card('7h')))
        ])
    def test_body(self, hand, attribute, expected_value):
        assert getattr(hand, attribute) == expected_value
