from poker.constants import PokerRoom


def test_first_values_are_represeantional():
    # other words: printed to the user
    assert str(PokerRoom.STARS) == "PokerStars"
    assert str(PokerRoom.STARS) == "PokerStars"

    assert str(PokerRoom.FTP) == "Full Tilt Poker"
    assert str(PokerRoom.FTP) == "Full Tilt Poker"

    assert str(PokerRoom.PKR) == "PKR"
    assert str(PokerRoom.PKR) == "PKR"
