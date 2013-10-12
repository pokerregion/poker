import pytest
import hand_data
from handparser import PokerStarsHand

all_test_hands = [eval('hand_data.HAND%d' % num) for num in range(1, 6)]

@pytest.fixture(params=all_test_hands)
def all_hands(request):
    """Parse all hands from test_data and returns a PokerStarsHand instance."""
    return PokerStarsHand(request.param)


@pytest.fixture
def hand(request):
    """Parse handhistory defined in hand_text class attribute and returns a PokerStarsHand instance."""
    return PokerStarsHand(request.instance.hand_text)


@pytest.fixture
def hand_header(request):
    """Parse hand history header only defined in hand_text and returns a PokerStarsHand instance."""
    h = PokerStarsHand(request.instance.hand_text, parse=False)
    h.parse_header()
    return h
