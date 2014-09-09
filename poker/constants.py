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


class Limit(_CaseInsensitiveMultiValueEnum):
    NL = 'NL', 'NO LIMIT'
    PL = 'PL', 'POT LIMIT'
    FL = 'FL', 'FIX LIMIT'


class MoneyType(_CaseInsensitiveMultiValueEnum):
    REAL = 'Real money',
    PLAY = 'Play money',


class Action(_CaseInsensitiveMultiValueEnum):
    BET = 'bet', 'bets'
    FOLD = 'fold', 'folded', 'folds'
    RETURN = 'return', 'returned', 'uncalled'
    WIN = 'win', 'won', 'collected'
    SHOW = 'show',
    NOSHOW = "don't show", "didn't show", 'did not show'
