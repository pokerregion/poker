from datetime import datetime
from decimal import Decimal as D

import pytest
from pytz import UTC

from poker.card import Card
from poker.constants import Action, Currency, Game, GameType, Limit, MoneyType
from poker.hand import Combo
from poker.handhistory import _Player, _PlayerAction
from poker.room.pkr import PKRHandHistory, _Street

from .pkr_hands import HANDS


@pytest.fixture
def hand_header(request):
    h = PKRHandHistory(request.instance.hand_text)
    h.parse_header()
    return h


@pytest.fixture
def hand(request):
    hh = PKRHandHistory(request.instance.hand_text)
    hh.parse()
    return hh


class TestHoldemHand:
    hand_text = HANDS["holdem_full"]

    @pytest.mark.parametrize(
        "attribute, expected_value",
        [
            ("game_type", GameType.CASH),
            ("sb", D("0.25")),
            ("bb", D("0.50")),
            ("date", UTC.localize(datetime(2013, 10, 5, 1, 15, 45))),
            ("game", Game.HOLDEM),
            ("limit", Limit.NL),
            ("ident", "2433297728"),
            ("tournament_ident", None),
            ("tournament_name", None),
            ("tournament_level", None),
            ("table_name", "#52121155 - Rapanui's Leela"),
            ("buyin", D("50")),
            ("currency", Currency.USD),
        ],
    )
    def test_header(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value

    @pytest.mark.parametrize(
        "attribute, expected_value",
        [
            (
                "players",
                [
                    _Player(name="laxi23", stack=D("51.89"), seat=1, combo=None),
                    _Player(name="NikosMRF", stack=D("50"), seat=2, combo=None),
                    _Player(name="Capricorn", stack=D("33.6"), seat=3, combo=None),
                    _Player(name="Walkman", stack=D("50"), seat=4, combo=Combo("9s6d")),
                    _Player(name="Empty Seat 5", stack=0, seat=5, combo=None),
                    _Player(name="barly123", stack=D("50.35"), seat=6, combo=None),
                ],
            ),
            ("button", _Player(name="Capricorn", stack=D("33.6"), seat=3, combo=None)),
            ("max_players", 6),  # maybe imprecise
            (
                "hero",
                _Player(name="Walkman", stack=D("50"), seat=4, combo=Combo("9s6d")),
            ),
            (
                "preflop_actions",
                (
                    "laxi23 folds",
                    "Capricorn calls $0.50",
                    "Walkman folds",
                    "barly123 raises to $1.25",
                    "Capricorn calls $1.25",
                ),
            ),
            ("turn", Card("Js")),
            ("turn_pot", D("10.97")),
            ("turn_actions", ("barly123 checks", "Capricorn checks")),
            ("river", Card("5h")),
            ("river_pot", D("10.97")),
            ("river_actions", ("barly123 checks", "Capricorn checks")),
            ("total_pot", D("10.97")),
            ("rake", D("0.54")),
            ("winners", ("barly123",)),
            ("show_down", True),
            ("board", (Card("7d"), Card("3c"), Card("Jd"), Card("Js"), Card("5h"))),
            ("extra", dict(money_type=MoneyType.REAL, last_ident="2433297369")),
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
                    _PlayerAction("barly123", Action.CHECK, None),
                    _PlayerAction("Capricorn", Action.BET, D("1.37")),
                    _PlayerAction("barly123", Action.RAISE, D("4.11")),
                    _PlayerAction("Capricorn", Action.CALL, D("4.11")),
                ),
            ),
            ("cards", (Card("7d"), Card("3c"), Card("Jd"))),
            ("is_rainbow", False),
            ("is_monotone", False),
            ("is_triplet", False),
            ("has_pair", False),
            ("has_straightdraw", False),
            ("has_gutshot", True),
            ("has_flushdraw", True),
            ("players", ("barly123", "Capricorn")),
            ("pot", D("10.97")),
        ],
    )
    def test_flop_attributes(self, hand, attribute, expected_value):
        assert getattr(hand.flop, attribute) == expected_value

    def test_flop(self, hand):
        assert isinstance(hand.flop, _Street)
