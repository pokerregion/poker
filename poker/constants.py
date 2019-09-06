from ._common import PokerEnum


class PokerRoom(PokerEnum):
    STARS = "PokerStars", "STARS", "PS"
    FTP = "Full Tilt Poker", "FTP", "FULL TILT"
    PKR = "PKR", "PKR POKER"
    EIGHT = "888", "888poker"


class Currency(PokerEnum):
    USD = "USD", "$"
    EUR = "EUR", "€"
    GBP = "GBP", "£"
    STARS_COIN = "SC", "StarsCoin"


class GameType(PokerEnum):
    TOUR = "Tournament", "TOUR"
    CASH = "Cash game", "CASH", "RING"
    SNG = "Sit & Go", "SNG", "SIT AND GO", "Sit&go"


class Game(PokerEnum):
    HOLDEM = "Hold'em", "HOLDEM"
    OMAHA = ("Omaha",)
    OHILO = ("Omaha Hi/Lo",)
    RAZZ = ("Razz",)
    STUD = ("Stud",)


class Limit(PokerEnum):
    NL = "NL", "No limit"
    PL = "PL", "Pot limit"
    FL = "FL", "Fixed limit", "Limit"


class TourFormat(PokerEnum):
    ONEREB = ("1R1A",)
    REBUY = "Rebuy", "+R"
    SECOND = ("2x Chance",)  # Second chance tournament, can rebuy twice
    ACTION = ("Action Hour",)
    # '2nd Chance' is a regular tournament on sunday evening,
    # after Sunday million (name), NOT a tournament format


class TourSpeed(PokerEnum):
    SLOW = ("Slow",)
    REGULAR = ("Regular",)
    TURBO = ("Turbo",)
    HYPER = ("Hyper-Turbo",)
    DOUBLE = ("2x-Turbo",)


class MoneyType(PokerEnum):
    REAL = ("Real money",)
    PLAY = ("Play money",)


class Action(PokerEnum):
    BET = "bet", "bets"
    RAISE = "raise", "raises"
    CHECK = "check", "checks"
    FOLD = "fold", "folded", "folds"
    CALL = "call", "calls"
    RETURN = "return", "returned", "uncalled"
    WIN = "win", "won", "collected"
    SHOW = ("show",)
    MUCK = "don't show", "didn't show", "did not show", "mucks"
    THINK = ("seconds left to act",)


class Position(PokerEnum):
    UTG = "UTG", "under the gun"
    UTG1 = "UTG1", "utg+1", "utg + 1"
    UTG2 = "UTG2", "utg+2", "utg + 2"
    UTG3 = "UTG3", "utg+3", "utg + 3"
    UTG4 = "UTG4", "utg+4", "utg + 4"
    HJ = "HJ", "hijack", "utg+5", "utg + 5"
    CO = "CO", "cutoff", "cut off"
    BTN = "BTN", "bu", "button"
    SB = "SB", "small blind"
    BB = "BB", "big blind"
