from enum import Enum
from ._common import _CaseInsensitiveMultiValueEnum


class PokerRoom(_CaseInsensitiveMultiValueEnum):
    STARS = 'PokerStars', 'STARS', 'PS'
    FTP =  'Full Tilt Poker', 'FTP', 'FULL TILT'
    PKR = 'PKR', 'PKR POKER'


class Currency(_CaseInsensitiveMultiValueEnum):
    USD = 'USD', '$'
    EUR = 'EUR', '€'
    GBP = 'GBP', '£'


class GameType(_CaseInsensitiveMultiValueEnum):
    TOUR = 'Tournament', 'TOUR',
    CASH = 'Cash game', 'CASH', 'RING',
    SNG = 'Sit & Go', 'SNG', 'SIT AND GO', 'Sit&go'


class Game(_CaseInsensitiveMultiValueEnum):
    HOLDEM = "Hold'em", 'HOLDEM'
    OMAHA = 'Omaha',
    OHILO = 'Omaha Hi/Lo',
    RAZZ = 'Razz',
    STUD = 'Stud',


class Limit(_CaseInsensitiveMultiValueEnum):
    NL = 'NL', 'No limit'
    PL = 'PL', 'Pot limit'
    FL = 'FL', 'Fixed limit'


class TourFormat(_CaseInsensitiveMultiValueEnum):
    ONEREB = '1R1A',
    REBUY = 'Rebuy', '+R'
    SECOND = '2x Chance',  # Second chance tournament, can rebuy twice
    ACTION = 'Action Hour',
    # '2nd Chance' is a regular tournament on sunday evening,
    # after Sunday million (name), NOT a tournament format


class TourType(_CaseInsensitiveMultiValueEnum):
    SNG = 'Sit&Go', 'SNG', 'Sit and go'
    TOUR = 'Tournament', 'TOUR', 'tourney'


class TourSpeed(Enum):
    REGULAR = 'Regular'
    TURBO = 'Turbo'
    HYPER = 'Hyper-Turbo'
    DOUBLE = '2x-Turbo'


class MoneyType(_CaseInsensitiveMultiValueEnum):
    REAL = 'Real money',
    PLAY = 'Play money',


class Action(_CaseInsensitiveMultiValueEnum):
    BET = 'bet', 'bets'
    RAISE = 'raise', 'raises',
    CHECK = 'check', 'checks'
    FOLD = 'fold', 'folded', 'folds'
    CALL = 'call', 'calls'
    RETURN = 'return', 'returned', 'uncalled'
    WIN = 'win', 'won', 'collected'
    SHOW = 'show',
    MUCK = "don't show", "didn't show", 'did not show', 'mucks'
    THINK = 'seconds left to act',


class Position(_CaseInsensitiveMultiValueEnum):
    UTG = 'UTG', 'under the gun'
    UTG1 = 'UTG1', 'utg+1', 'utg + 1'
    UTG2 = 'UTG2', 'utg+2', 'utg + 2'
    UTG3 = 'UTG3', 'utg+3', 'utg + 3'
    UTG4 = 'UTG4', 'utg+4', 'utg + 4'
    CO = 'CO', 'cutoff', 'cut off'
    BTN = 'BTN', 'bu', 'button'
    SB = 'SB', 'small blind'
    BB = 'BB', 'big blind'
