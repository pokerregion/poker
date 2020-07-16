import pytest
from poker.card import Card
from poker.jsonencoding import JsonEncoder


class TestCardEncoding:

    def tests_simpleCard(self):
        encoder = JsonEncoder()
        card = Card("Ad")
        assert encoder.encode(card) == "{\"rank\": \"A\", \"suit\": \"DIAMONDS\"}"
