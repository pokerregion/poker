import pytest
from poker.hand import Combo

from poker.room.pokerstars import _Street, PokerStarsHandHistory

from poker.handhistory import _BaseStreet

from poker.card import Card
from poker.jsonencoding import JsonEncoder
from tests.handhistory import stars_hands


@pytest.fixture(scope='function')
def json_encoder():
    return JsonEncoder()


class TestCardEncoding:

    def tests_simple_card(self, json_encoder):
        card = Card("Ad")
        assert json_encoder.encode(card) == "{\"rank\": \"A\", \"suit\": \"DIAMONDS\"}"

    def test_combo_encoding(self, json_encoder):
        combo = Combo.from_cards(Card("Ad"), Card("Kc"))
        assert json_encoder.encode(combo) == "{\"1\": {\"rank\": \"A\", \"suit\": \"DIAMONDS\"}, \"2\": {\"rank\": \"K\", \"suit\": \"CLUBS\"}}"


class TestHeaderEncoding:
    # TODO: date, gametype etc.
    def test_test(self, json_encoder):
        raise

class TestStreetEncoding:
    # TODO: date, gametype etc.
    def test_street_flop_encoding(self, json_encoder):
        street = _Street(["[Ad Ks Qc]",],)
        assert json_encoder.encode(street) == """{"cards": [{"rank": "A", "suit": "DIAMONDS"}, {"rank": "K", "suit": "SPADES"}, {"rank": "Q", "suit": "CLUBS"}]}"""

    def test_board_tuple_encoding(self, json_encoder):
        board = tuple([Card("Ad"), Card("Ks"), Card("Qc"), Card("Jh"), Card("Ts")])
        data={}
        data['board'] = list(board)
        assert json_encoder.encode(data) == """{"board": [{"rank": "A", "suit": "DIAMONDS"}, {"rank": "K", "suit": "SPADES"}, {"rank": "Q", "suit": "CLUBS"}, {"rank": "J", "suit": "HEARTS"}, {"rank": "T", "suit": "SPADES"}]}"""

    def test_actions_encoding(self, json_encoder):
        # TODO
        raise

    def test_street_property_encoding(self, json_encoder):
        # TODO
        raise

class TestFullPokerstarsHand:

    def test_hand(self, json_encoder):
        hand_text = stars_hands.HAND12

        hh = PokerStarsHandHistory(hand_text)
        hh.parse()
        json = json_encoder.encode(hh)
        print(json)
        assert "\"board\": " in json
