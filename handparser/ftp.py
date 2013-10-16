from handparser.common import PokerHand


class FullTiltHand(PokerHand):
    """Parses Full Tilt Poker hands.

    Class specific attributes:
        poker_room      -- FTP

    """
    poker_room = 'FTP'
    date_format = '%H:%M:%S ET - %Y/%m/%d'
