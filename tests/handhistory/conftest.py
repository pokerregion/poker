import pytest
from poker.room.pokerstars import PokerStarsHandHistory
from . import stars_hands


# get every variable starting with 'HAND' from hand_data module
all_test_hands = [
    getattr(stars_hands, hand_text)
    for hand_text in dir(stars_hands)
    if hand_text.startswith("HAND")
]


@pytest.fixture(params=all_test_hands)
def all_stars_hands(request):
    """Parse all hands from test_data and returns a PokerStarsHandHistory instance."""
    hh = PokerStarsHandHistory(request.param)
    hh.parse()
    return hh
