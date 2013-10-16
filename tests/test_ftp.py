import pytest
import ftp_hands
from handparser.common import ET
from handparser.ftp import FullTiltHand
from datetime import datetime
from decimal import Decimal

@pytest.fixture
def hand_header(request):
    """Parse hand history header only defined in hand_text and returns a PokerStarsHand instance."""
    h = FullTiltHand(request.instance.hand_text, parse=False)
    h.parse_header()
    return h


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
