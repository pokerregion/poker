import pytest
import hand_data
from handparser import PokerStarsHand

# get every variable starting with 'HAND' from hand_data module
all_test_hands = [getattr(hand_data, hand_text) for hand_text in dir(hand_data) if hand_text.startswith('HAND')]

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
