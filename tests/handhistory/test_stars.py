from datetime import datetime
from decimal import Decimal

import pytest
import pytz

from poker.card import Card
from poker.constants import Action, Currency, Game, GameType, Limit, MoneyType
from poker.hand import Combo
from poker.handhistory import _Player, _PlayerAction
from poker.room.pokerstars import PokerStarsHandHistory, _Street

from . import stars_hands

ET = pytz.timezone("US/Eastern")


@pytest.fixture
def hand(request):
    """Parse handhistory defined in hand_text class attribute
    and returns a PokerStarsHandHistory instance.
    """
    hh = PokerStarsHandHistory(request.instance.hand_text)
    hh.parse()
    return hh


@pytest.fixture
def hand_header(request):
    """Parse hand history header only defined in hand_text
    and returns a PokerStarsHandHistory instance.
    """
    hh = PokerStarsHandHistory(request.instance.hand_text)
    hh.parse_header()
    return hh


def test_open_from_file(testdir):
    bbb_path = str(testdir.joinpath("handhistory/bbb.txt"))
    hh = PokerStarsHandHistory.from_file(bbb_path)
    hh.parse()
    assert hh.ident == "138364355489"
    assert isinstance(hh.raw, str)


class TestHandHeaderNoLimitHoldemTourFreeroll:
    hand_text = """
PokerStars Hand #152455023342: Tournament #1545783901, Freeroll  Hold'em No Limit - Level I (10/20) - 2016/04/25 23:22:00 BRT [2016/04/25 22:22:00 ET]
    """  # noqa

    @pytest.mark.parametrize(
        ("attribute", "expected_value"),
        [
            ("ident", "152455023342"),
            ("game_type", GameType.TOUR),
            ("tournament_ident", "1545783901"),
            ("tournament_level", "I"),
            ("currency", Currency("USD")),
            ("buyin", Decimal("0")),
            ("rake", Decimal("0")),
            ("game", Game.HOLDEM),
            ("limit", Limit.NL),
            ("sb", Decimal(10)),
            ("bb", Decimal(20)),
            ("date", ET.localize(datetime(2016, 4, 25, 22, 22, 0))),
            ("extra", {"money_type": MoneyType.REAL}),
        ],
    )
    def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value


class TestHandHeaderNoLimitHoldemTourPlayMoney:
    hand_text = """
PokerStars Hand #152504147861: Tournament #1545751329, 870+130 Hold'em No Limit - Level I (10/20) - 2016/04/27 1:17:16 BRT [2016/04/27 0:17:16 ET]
    """  # noqa

    @pytest.mark.parametrize(
        ("attribute", "expected_value"),
        [
            ("ident", "152504147861"),
            ("game_type", GameType.TOUR),
            ("tournament_ident", "1545751329"),
            ("tournament_level", "I"),
            ("currency", None),
            ("buyin", Decimal("870")),
            ("rake", Decimal("130")),
            ("game", Game.HOLDEM),
            ("limit", Limit.NL),
            ("sb", Decimal(10)),
            ("bb", Decimal(20)),
            ("date", ET.localize(datetime(2016, 4, 27, 00, 17, 16))),
            ("extra", {"money_type": MoneyType.PLAY}),
        ],
    )
    def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value


class TestHandHeaderLimitHoldemCashPlayMoney:
    hand_text = """
PokerStars Hand #153769972916:  Hold'em Limit (10/20) - 2016/05/24 8:52:39 BRT [2016/05/24 7:52:39 ET]
    """  # noqa

    @pytest.mark.parametrize(
        ("attribute", "expected_value"),
        [
            ("ident", "153769972916"),
            ("game_type", GameType.CASH),
            ("tournament_ident", None),
            ("tournament_level", None),
            ("currency", None),
            ("buyin", None),
            ("rake", None),
            ("game", Game.HOLDEM),
            ("limit", Limit.FL),
            ("sb", Decimal(10)),
            ("bb", Decimal(20)),
            ("date", ET.localize(datetime(2016, 5, 24, 7, 52, 39))),
            ("extra", {"money_type": MoneyType.PLAY}),
        ],
    )
    def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value


class TestHandHeaderNoLimitHoldemTourStarcoin:
    hand_text = """
PokerStars Hand #153719873192: Tournament #1573768726, 184 SC Hold'em No Limit - Level I (25/50) - 2016/05/23 6:48:22 BRT [2016/05/23 5:48:22 ET]
    """  # noqa

    @pytest.mark.parametrize(
        ("attribute", "expected_value"),
        [
            ("ident", "153719873192"),
            ("game_type", GameType.TOUR),
            ("tournament_ident", "1573768726"),
            ("tournament_level", "I"),
            ("currency", Currency.STARS_COIN),
            ("buyin", Decimal(184)),
            ("rake", Decimal(0)),
            ("game", Game.HOLDEM),
            ("limit", Limit.NL),
            ("sb", Decimal(25)),
            ("bb", Decimal(50)),
            ("date", ET.localize(datetime(2016, 5, 23, 5, 48, 22))),
            ("extra", {"money_type": MoneyType.REAL}),
        ],
    )
    def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value


class TestHandHeaderPotLimitOmahaCash:
    hand_text = """
PokerStars Hand #107030112846: Omaha Pot Limit ($0.01/$0.02 USD) - 2013/11/15 9:03:10 AWST [2013/11/14 20:03:10 ET]
    """  # noqa

    @pytest.mark.parametrize(
        ("attribute", "expected_value"),
        [
            ("ident", "107030112846"),
            ("game_type", GameType.CASH),
            ("tournament_ident", None),
            ("tournament_level", None),
            ("currency", Currency.USD),
            ("buyin", None),
            ("rake", None),
            ("game", Game.OMAHA),
            ("limit", Limit.PL),
            ("sb", Decimal("0.01")),
            ("bb", Decimal("0.02")),
            ("date", ET.localize(datetime(2013, 11, 14, 20, 3, 10))),
            ("extra", {"money_type": MoneyType.REAL}),
        ],
    )
    def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value


class TestHandWithFlopOnly:
    hand_text = stars_hands.HAND1

    # in py.test 2.4 it is recommended to use string like "attribute,expected",
    # but with tuple, it works in both 2.3.5 and 2.4
    @pytest.mark.parametrize(
        ("attribute", "expected_value"),
        [
            ("ident", "105024000105"),
            ("game_type", GameType.TOUR),
            ("tournament_ident", "797469411"),
            ("tournament_level", "I"),
            ("currency", Currency.USD),
            ("buyin", Decimal("3.19")),
            ("rake", Decimal("0.31")),
            ("game", Game.HOLDEM),
            ("limit", Limit.NL),
            ("sb", Decimal(10)),
            ("bb", Decimal(20)),
            ("date", ET.localize(datetime(2013, 10, 4, 13, 53, 27))),
        ],
    )
    def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value

    @pytest.mark.parametrize(
        ("attribute", "expected_value"),
        [
            ("table_name", "797469411 15"),
            ("max_players", 9),
            ("button", _Player(name="flettl2", stack=1500, seat=1, combo=None)),
            ("hero", _Player(name="W2lkm2n", stack=3000, seat=5, combo=Combo("AcJh"))),
            (
                "players",
                [
                    _Player(name="flettl2", stack=1500, seat=1, combo=None),
                    _Player(name="santy312", stack=3000, seat=2, combo=None),
                    _Player(name="flavio766", stack=3000, seat=3, combo=None),
                    _Player(name="strongi82", stack=3000, seat=4, combo=None),
                    _Player(name="W2lkm2n", stack=3000, seat=5, combo=Combo("AcJh")),
                    _Player(name="MISTRPerfect", stack=3000, seat=6, combo=None),
                    _Player(name="blak_douglas", stack=3000, seat=7, combo=None),
                    _Player(name="sinus91", stack=1500, seat=8, combo=None),
                    _Player(name="STBIJUJA", stack=1500, seat=9, combo=None),
                ],
            ),
            ("turn", None),
            ("river", None),
            ("board", (Card("2s"), Card("6d"), Card("6h"))),
            (
                "preflop_actions",
                (
                    "strongi82: folds",
                    "W2lkm2n: raises 40 to 60",
                    "MISTRPerfect: calls 60",
                    "blak_douglas: folds",
                    "sinus91: folds",
                    "STBIJUJA: folds",
                    "flettl2: folds",
                    "santy312: folds",
                    "flavio766: folds",
                ),
            ),
            ("turn_actions", None),
            ("river_actions", None),
            ("total_pot", Decimal(150)),
            ("show_down", False),
            ("winners", ("W2lkm2n",)),
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
                    _PlayerAction("W2lkm2n", Action.BET, Decimal(80)),
                    _PlayerAction("MISTRPerfect", Action.FOLD, None),
                    _PlayerAction("W2lkm2n", Action.RETURN, Decimal(80)),
                    _PlayerAction("W2lkm2n", Action.WIN, Decimal(150)),
                    _PlayerAction("W2lkm2n", Action.MUCK, None),
                ),
            ),
            ("cards", (Card("2s"), Card("6d"), Card("6h"))),
            ("is_rainbow", True),
            ("is_monotone", False),
            ("is_triplet", False),
            # TODO: http://www.pokerology.com/lessons/flop-texture/
            # assert flop.is_dry
            ("has_pair", True),
            ("has_straightdraw", False),
            ("has_gutshot", True),
            ("has_flushdraw", False),
            ("players", ("W2lkm2n", "MISTRPerfect")),
            ("pot", Decimal(150)),
        ],
    )
    def test_flop_attributes(self, hand, attribute, expected_value):
        assert getattr(hand.flop, attribute) == expected_value

    def test_flop(self, hand):
        assert isinstance(hand.flop, _Street)


class TestAllinPreflopHand:
    hand_text = stars_hands.HAND2

    @pytest.mark.parametrize(
        ("attribute", "expected_value"),
        [
            ("ident", "105034215446"),
            ("game_type", GameType.TOUR),
            ("tournament_ident", "797536898"),
            ("tournament_level", "XI"),
            ("currency", Currency.USD),
            ("buyin", Decimal("3.19")),
            ("rake", Decimal("0.31")),
            ("game", Game.HOLDEM),
            ("limit", Limit.NL),
            ("sb", Decimal(400)),
            ("bb", Decimal(800)),
            ("date", ET.localize(datetime(2013, 10, 4, 17, 22, 20))),
        ],
    )
    def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value

    @pytest.mark.parametrize(
        ("attribute", "expected_value"),
        [
            ("table_name", "797536898 9"),
            ("max_players", 9),
            (
                "button",
                _Player(name="W2lkm2n", stack=11815, seat=2, combo=Combo("JdJs")),
            ),
            ("hero", _Player(name="W2lkm2n", stack=11815, seat=2, combo=Combo("JdJs"))),
            (
                "players",
                [
                    _Player(name="RichFatWhale", stack=12910, seat=1, combo=None),
                    _Player(name="W2lkm2n", stack=11815, seat=2, combo=Combo("JdJs")),
                    _Player(name="Labahra", stack=7395, seat=3, combo=None),
                    _Player(name="Lean Abadia", stack=7765, seat=4, combo=None),
                    _Player(name="lkenny44", stack=10080, seat=5, combo=None),
                    _Player(name="Newfie_187", stack=1030, seat=6, combo=None),
                    _Player(name="Hokolix", stack=13175, seat=7, combo=None),
                    _Player(name="pmmr", stack=2415, seat=8, combo=None),
                    _Player(name="costamar", stack=13070, seat=9, combo=None),
                ],
            ),
            ("turn", Card("8d")),
            ("river", Card("Ks")),
            ("board", (Card("3c"), Card("6s"), Card("9d"), Card("8d"), Card("Ks"))),
            (
                "preflop_actions",
                (
                    "lkenny44: folds",
                    "Newfie_187: raises 155 to 955 and is all-in",
                    "Hokolix: folds",
                    "pmmr: folds",
                    "costamar: raises 12040 to 12995 and is all-in",
                    "RichFatWhale: folds",
                    "W2lkm2n: calls 11740 and is all-in",
                    "Labahra: folds",
                    "Lean Abadia: folds",
                    "Uncalled bet (1255) returned to costamar",
                ),
            ),
            ("turn_actions", None),
            ("river_actions", None),
            ("total_pot", Decimal(26310)),
            ("show_down", True),
            ("winners", ("costamar",)),
        ],
    )
    def test_body(self, hand, attribute, expected_value):
        assert getattr(hand, attribute) == expected_value

    @pytest.mark.parametrize(
        ("attribute", "expected_value"),
        [
            ("actions", None),
            ("cards", (Card("3c"), Card("6s"), Card("9d"))),
            ("is_rainbow", True),
            ("is_monotone", False),
            ("is_triplet", False),
            # TODO: http://www.pokerology.com/lessons/flop-texture/
            # assert flop.is_dry
            ("has_pair", False),
            ("has_straightdraw", True),
            ("has_gutshot", True),
            ("has_flushdraw", False),
            ("players", None),
        ],
    )
    def test_flop_attributes(self, hand, attribute, expected_value):
        assert getattr(hand.flop, attribute) == expected_value

    def test_flop(self, hand):
        assert isinstance(hand.flop, _Street)

    @pytest.mark.xfail
    def test_flop_pot(self, hand):
        assert hand.flop.pot == Decimal(26310)


class TestBodyMissingPlayerNoBoard:
    hand_text = stars_hands.HAND3

    @pytest.mark.parametrize(
        ("attribute", "expected_value"),
        [
            ("ident", "105026771696"),
            ("game_type", GameType.TOUR),
            ("tournament_ident", "797469411"),
            ("tournament_level", "X"),
            ("currency", Currency.USD),
            ("buyin", Decimal("3.19")),
            ("rake", Decimal("0.31")),
            ("game", Game.HOLDEM),
            ("limit", Limit.NL),
            ("sb", Decimal(300)),
            ("bb", Decimal(600)),
            ("date", ET.localize(datetime(2013, 10, 4, 14, 50, 56))),
        ],
    )
    def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value

    @pytest.mark.parametrize(
        ("attribute", "expected_value"),
        [
            ("table_name", "797469411 11"),
            ("max_players", 9),
            (
                "button",
                _Player(name="W2lkm2n", stack=10714, seat=8, combo=Combo("6d8d")),
            ),
            ("hero", _Player(name="W2lkm2n", stack=10714, seat=8, combo=Combo("6d8d"))),
            (
                "players",
                [
                    _Player(name="Empty Seat 1", stack=0, seat=1, combo=None),
                    _Player(name="snelle_jel", stack=4295, seat=2, combo=None),
                    _Player(name="EuSh0wTelm0", stack=11501, seat=3, combo=None),
                    _Player(name="panost3", stack=7014, seat=4, combo=None),
                    _Player(name="Samovlyblen", stack=7620, seat=5, combo=None),
                    _Player(name="Theralion", stack=4378, seat=6, combo=None),
                    _Player(name="wrsport1015", stack=9880, seat=7, combo=None),
                    _Player(name="W2lkm2n", stack=10714, seat=8, combo=Combo("6d8d")),
                    _Player(name="fischero68", stack=8724, seat=9, combo=None),
                ],
            ),
            ("turn", None),
            ("river", None),
            ("board", None),
            (
                "preflop_actions",
                (
                    "EuSh0wTelm0: folds",
                    "panost3: folds",
                    "Samovlyblen: folds",
                    "Theralion: raises 600 to 1200",
                    "wrsport1015: folds",
                    "W2lkm2n: folds",
                    "fischero68: folds",
                    "snelle_jel: folds",
                    "Uncalled bet (600) returned to Theralion",
                    "Theralion collected 1900 from pot",
                    "Theralion: doesn't show hand",
                ),
            ),
            ("turn_actions", None),
            ("river_actions", None),
            ("total_pot", Decimal(1900)),
            ("show_down", False),
            ("winners", ("Theralion",)),
        ],
    )
    def test_body(self, hand, attribute, expected_value):
        assert getattr(hand, attribute) == expected_value

    def test_flop(self, hand):
        assert hand.flop is None


class TestBodyEveryStreet:
    hand_text = stars_hands.HAND4

    @pytest.mark.parametrize(
        ("attribute", "expected_value"),
        [
            ("ident", "105025168298"),
            ("game_type", GameType.TOUR),
            ("tournament_ident", "797469411"),
            ("tournament_level", "IV"),
            ("currency", Currency.USD),
            ("buyin", Decimal("3.19")),
            ("rake", Decimal("0.31")),
            ("game", Game.HOLDEM),
            ("limit", Limit.NL),
            ("sb", Decimal(50)),
            ("bb", Decimal(100)),
            ("date", ET.localize(datetime(2013, 10, 4, 14, 19, 17))),
        ],
    )
    def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value

    @pytest.mark.parametrize(
        ("attribute", "expected_value"),
        [
            ("table_name", "797469411 15"),
            ("max_players", 9),
            (
                "button",
                _Player(name="W2lkm2n", stack=5145, seat=5, combo=Combo("Jc5c")),
            ),
            ("hero", _Player(name="W2lkm2n", stack=5145, seat=5, combo=Combo("Jc5c"))),
            (
                "players",
                [
                    _Player(name="flettl2", stack=3000, seat=1, combo=None),
                    _Player(name="santy312", stack=5890, seat=2, combo=None),
                    _Player(name="flavio766", stack=11010, seat=3, combo=None),
                    _Player(name="strongi82", stack=2855, seat=4, combo=None),
                    _Player(name="W2lkm2n", stack=5145, seat=5, combo=Combo("Jc5c")),
                    _Player(name="MISTRPerfect", stack=2395, seat=6, combo=None),
                    _Player(name="blak_douglas", stack=3000, seat=7, combo=None),
                    _Player(name="sinus91", stack=3000, seat=8, combo=None),
                    _Player(name="STBIJUJA", stack=1205, seat=9, combo=None),
                ],
            ),
            ("turn", Card("8c")),
            ("river", Card("Kd")),
            ("board", (Card("6s"), Card("4d"), Card("3s"), Card("8c"), Card("Kd"))),
            (
                "preflop_actions",
                (
                    "sinus91: folds",
                    "STBIJUJA: folds",
                    "flettl2: raises 125 to 225",
                    "santy312: folds",
                    "flavio766: folds",
                    "strongi82: folds",
                    "W2lkm2n: folds",
                    "MISTRPerfect: folds",
                    "blak_douglas: calls 125",
                ),
            ),
            (
                "turn_actions",
                (
                    "blak_douglas: checks",
                    "flettl2: bets 250",
                    "blak_douglas: calls 250",
                ),
            ),
            (
                "river_actions",
                (
                    "blak_douglas: checks",
                    "flettl2: bets 1300",
                    "blak_douglas: folds",
                    "Uncalled bet (1300) returned to flettl2",
                    "flettl2 collected 1300 from pot",
                    "flettl2: doesn't show hand",
                ),
            ),
            ("total_pot", Decimal(1300)),
            ("show_down", False),
            ("winners", ("flettl2",)),
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
                    _PlayerAction("blak_douglas", Action.CHECK, None),
                    _PlayerAction("flettl2", Action.BET, Decimal(150)),
                    _PlayerAction("blak_douglas", Action.CALL, Decimal(150)),
                ),
            ),
            ("cards", (Card("6s"), Card("4d"), Card("3s"))),
            ("is_rainbow", False),
            ("is_monotone", False),
            ("is_triplet", False),
            # TODO: http://www.pokerology.com/lessons/flop-texture/
            # assert flop.is_dry
            ("has_pair", False),
            ("has_straightdraw", True),
            ("has_gutshot", True),
            ("has_flushdraw", True),
            ("players", ("blak_douglas", "flettl2")),
        ],
    )
    def test_flop_attributes(self, hand, attribute, expected_value):
        assert getattr(hand.flop, attribute) == expected_value

    def test_flop(self, hand):
        assert isinstance(hand.flop, _Street)

    @pytest.mark.xfail
    def test_flop_pot(self, hand):
        assert hand.flop.pot == Decimal(800)


class TestClassRepresentation:
    hand_text = stars_hands.HAND1

    def test_unicode(self, hand_header):
        assert str(hand_header) == "<PokerStarsHandHistory: #105024000105>"

    def test_str(self, hand_header):
        assert str(hand_header) == "<PokerStarsHandHistory: #105024000105>"


class TestPlayerNameWithDot:
    hand_text = stars_hands.HAND5

    def test_player_is_in_player_list(self, hand):
        assert ".prestige.U$" in [p.name for p in hand.players]

    def test_player_stack(self, hand):
        player_names = [p.name for p in hand.players]
        player_index = player_names.index(".prestige.U$")
        assert hand.players[player_index].stack == 3000
