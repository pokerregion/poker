from datetime import datetime
from decimal import Decimal

import pytest
import pytz

from poker.card import Card
from poker.constants import Action, Currency, Game, GameType, Limit
from poker.hand import Combo
from poker.handhistory import _Player, _PlayerAction
from poker.room.fulltiltpoker import FullTiltPokerHandHistory, _Street

from . import ftp_hands

ET = pytz.timezone("US/Eastern")


@pytest.fixture
def hand_header(request):
    """Parse hand history header only defined in hand_text
    and returns a FullTiltPokerHandHistory instance.
    """
    h = FullTiltPokerHandHistory(request.instance.hand_text)
    h.parse_header()
    return h


@pytest.fixture
def hand(request):
    """Parse handhistory defined in hand_text class attribute
    and returns a FullTiltPokerHandHistory instance.
    """
    hh = FullTiltPokerHandHistory(request.instance.hand_text)
    hh.parse()
    return hh


class TestHandWithFlopOnly:
    hand_text = ftp_hands.HAND1

    @pytest.mark.parametrize(
        ("attribute", "expected_value"),
        [
            ("game_type", GameType.TOUR),
            ("sb", Decimal(10)),
            ("bb", Decimal(20)),
            ("date", ET.localize(datetime(2013, 9, 22, 13, 26, 50))),
            ("game", Game.HOLDEM),
            ("limit", Limit.NL),
            ("ident", "33286946295"),
            ("tournament_ident", "255707037"),
            ("table_name", "179"),
            ("tournament_level", None),
            ("buyin", None),
            ("rake", None),
            ("currency", None),
        ],
    )
    def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value

    @pytest.mark.parametrize(
        "attribute,expected_value",
        [
            (
                "players",
                [
                    _Player(name="Popp1987", stack=13587, seat=1, combo=None),
                    _Player(name="Luckytobgood", stack=10110, seat=2, combo=None),
                    _Player(name="FatalRevange", stack=9970, seat=3, combo=None),
                    _Player(
                        name="IgaziFerfi", stack=10000, seat=4, combo=Combo("Ks9d")
                    ),
                    _Player(name="egis25", stack=6873, seat=5, combo=None),
                    _Player(name="gamblie", stack=9880, seat=6, combo=None),
                    _Player(name="idanuTz1", stack=10180, seat=7, combo=None),
                    _Player(name="PtheProphet", stack=9930, seat=8, combo=None),
                    _Player(name="JohnyyR", stack=9840, seat=9, combo=None),
                ],
            ),
            ("button", _Player(name="egis25", stack=6873, seat=5, combo=None)),
            ("max_players", 9),
            (
                "hero",
                _Player(name="IgaziFerfi", stack=10000, seat=4, combo=Combo("Ks9d")),
            ),
            (
                "preflop_actions",
                (
                    "PtheProphet has 15 seconds left to act",
                    "PtheProphet folds",
                    "JohnyyR raises to 40",
                    "Popp1987 has 15 seconds left to act",
                    "Popp1987 folds",
                    "Luckytobgood folds",
                    "FatalRevange raises to 100",
                    "IgaziFerfi folds",
                    "egis25 folds",
                    "gamblie folds",
                    "idanuTz1 folds",
                    "JohnyyR has 15 seconds left to act",
                    "JohnyyR calls 60",
                ),
            ),
            ("turn", None),
            ("river", None),
            ("total_pot", Decimal(230)),
            ("show_down", False),
            ("winners", ("FatalRevange",)),
            ("board", (Card("8h"), Card("4h"), Card("Tc"))),
            (
                "extra",
                dict(
                    tournament_name="MiniFTOPS Main Event",
                    turn_pot=None,
                    turn_num_players=None,
                    river_pot=None,
                    river_num_players=None,
                ),
            ),
        ],
    )
    def test_body(self, hand, attribute, expected_value):
        assert getattr(hand, attribute) == expected_value

    @pytest.mark.parametrize(
        ("attribute", "expected_value"),
        [
            (
                "actions",
                (
                    _PlayerAction("JohnyyR", Action.CHECK, None),
                    _PlayerAction("FatalRevange", Action.THINK, None),
                    _PlayerAction("FatalRevange", Action.BET, Decimal(120)),
                    _PlayerAction("JohnyyR", Action.FOLD, None),
                    _PlayerAction("FatalRevange", Action.RETURN, Decimal(120)),
                    _PlayerAction("FatalRevange", Action.MUCK, None),
                    _PlayerAction("FatalRevange", Action.WIN, Decimal(230)),
                ),
            ),
            ("cards", (Card("8h"), Card("4h"), Card("Tc"))),
            ("is_rainbow", False),
            ("is_monotone", False),
            ("is_triplet", False),
            # TODO: http://www.pokerology.com/lessons/flop-texture/
            # assert flop.is_dry
            ("has_pair", False),
            ("has_straightdraw", True),
            ("has_gutshot", True),
            ("has_flushdraw", True),
            ("players", ("JohnyyR", "FatalRevange")),
            ("pot", Decimal(230)),
        ],
    )
    def test_flop_attributes(self, hand, attribute, expected_value):
        assert getattr(hand.flop, attribute) == expected_value

    def test_flop(self, hand):
        assert isinstance(hand.flop, _Street)


class TestHandWithFlopTurnRiver:
    hand_text = ftp_hands.TURBO_SNG

    @pytest.mark.parametrize(
        "attribute,expected_value",
        [
            ("game_type", GameType.SNG),
            ("sb", Decimal(15)),
            ("bb", Decimal(30)),
            ("date", ET.localize(datetime(2014, 6, 29, 5, 57, 1))),
            ("game", Game.HOLDEM),
            ("limit", Limit.NL),
            ("ident", "34374264321"),
            ("tournament_ident", "268569961"),
            ("table_name", "1"),
            ("tournament_level", None),
            ("buyin", Decimal(10)),
            ("rake", None),
            ("currency", Currency.USD),
        ],
    )
    def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value

    @pytest.mark.parametrize(
        "attribute,expected_value",
        [
            (
                "players",
                [
                    _Player(name="snake 422", stack=1500, seat=1, combo=None),
                    _Player(name="IgaziFerfi", stack=1500, seat=2, combo=Combo("5d2h")),
                    _Player(name="MixaOne", stack=1500, seat=3, combo=None),
                    _Player(name="BokkaBlake", stack=1500, seat=4, combo=None),
                    _Player(name="Sajiee", stack=1500, seat=5, combo=None),
                    _Player(name="AzzzJJ", stack=1500, seat=6, combo=None),
                ],
            ),
            ("button", _Player(name="AzzzJJ", stack=1500, seat=6, combo=None)),
            ("max_players", 6),
            (
                "hero",
                _Player(name="IgaziFerfi", stack=1500, seat=2, combo=Combo("5d2h")),
            ),
            (
                "preflop_actions",
                (
                    "MixaOne calls 30",
                    "BokkaBlake folds",
                    "Sajiee folds",
                    "AzzzJJ raises to 90",
                    "snake 422 folds",
                    "IgaziFerfi folds",
                    "MixaOne calls 60",
                ),
            ),
            ("turn", None),
            ("turn_actions", None),
            ("river", None),
            ("river_actions", None),
            ("total_pot", Decimal("285")),
            ("show_down", False),
            ("winners", ("AzzzJJ",)),
            ("board", (Card("6s"), Card("9c"), Card("3d"))),
            (
                "extra",
                dict(
                    tournament_name="$10 Sit & Go (Turbo)",
                    turn_pot=None,
                    turn_num_players=None,
                    river_pot=None,
                    river_num_players=None,
                ),
            ),
        ],
    )
    def test_body(self, hand, attribute, expected_value):
        assert getattr(hand, attribute) == expected_value

    @pytest.mark.parametrize(
        ("attribute", "expected_value"),
        [
            (
                "actions",
                (
                    _PlayerAction("MixaOne", Action.BET, Decimal(30)),
                    _PlayerAction("AzzzJJ", Action.RAISE, Decimal(120)),
                    _PlayerAction("MixaOne", Action.FOLD, None),
                    _PlayerAction("AzzzJJ", Action.RETURN, Decimal(90)),
                    _PlayerAction("AzzzJJ", Action.MUCK, None),
                    _PlayerAction("AzzzJJ", Action.WIN, Decimal(285)),
                ),
            ),
            ("cards", (Card("6s"), Card("9c"), Card("3d"))),
            ("is_rainbow", True),
            ("is_monotone", False),
            ("is_triplet", False),
            # TODO: http://www.pokerology.com/lessons/flop-texture/
            # assert flop.is_dry
            ("has_pair", False),
            ("has_straightdraw", True),
            ("has_gutshot", True),
            ("has_flushdraw", False),
            ("players", ("MixaOne", "AzzzJJ")),
            ("pot", Decimal(285)),
        ],
    )
    def test_flop_attributes(self, hand, attribute, expected_value):
        assert getattr(hand.flop, attribute) == expected_value

    def test_flop(self, hand):
        assert isinstance(hand.flop, _Street)
