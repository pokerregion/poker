"""Poker hand history parser module.

For now, it only parser PokerStars and Full Tilt Poker Tournament hands, but the plan is to parse a lot.

"""
from handparser.stars import PokerStarsHand
from handparser.ftp import FullTiltHand
from handparser.common import ET, UTC
