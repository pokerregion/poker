from enum34_custom import CaseInsensitiveMultiValueEnum


class PokerRoom(CaseInsensitiveMultiValueEnum):
    STARS = 'PokerStars', 'STARS', 'PS'
    FTP =  'Full Tilt Poker', 'FTP', 'FULL TILT'
    PKR = 'PKR', 'PKR POKER'


class Currency(CaseInsensitiveMultiValueEnum):
    USD = 'USD', '$'
    EUR = 'EUR', '€'
    GBP = 'GBP', '£'


class GameType(CaseInsensitiveMultiValueEnum):
    TOUR = 'Tournament', 'TOUR',
    CASH = 'Cash game', 'CASH', 'RING',
    SNG = 'Sit & Go', 'SNG', 'SIT AND GO', 'Sit&go'


class Game(CaseInsensitiveMultiValueEnum):
    HOLDEM = "Hold'em", 'HOLDEM'
    OMAHA = 'Omaha',


class Limit(CaseInsensitiveMultiValueEnum):
    NL = 'NL', 'NO LIMIT'
    PL = 'PL', 'POT LIMIT'
    FL = 'FL', 'FIX LIMIT'


class MoneyType(CaseInsensitiveMultiValueEnum):
    REAL = 'Real money',
    PLAY = 'Play money',
