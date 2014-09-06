from enum34_custom import CaseInsensitiveMultiValueEnum


class PokerRoom(CaseInsensitiveMultiValueEnum):
    STARS = 'POKERSTARS', 'STARS', 'PS'
    FTP =  'FULL TILT POKER', 'FULL TILT', 'FTP'
    PKR = 'PKR', 'PKR POKER'


class Currency(CaseInsensitiveMultiValueEnum):
    USD = 'USD', '$'
    EUR = 'EUR', '€'
    GBP = 'GBP', '£'


class GameType(CaseInsensitiveMultiValueEnum):
    TOUR = 'TOURNAMENT', 'TOUR'
    CASH = 'CASH GAME', 'RING', 'CASH'


class Game(CaseInsensitiveMultiValueEnum):
    HOLDEM = "HOLD'EM", 'HOLDEM'
    OMAHA = 'OMAHA',


class Limit(CaseInsensitiveMultiValueEnum):
    NL = 'NO LIMIT', 'NL'
    PL = 'POT LIMIT', 'PL'
    FL = 'FIX LIMIT', 'FL'


class MoneyType(CaseInsensitiveMultiValueEnum):
    REAL = 'REAL MONEY',
    PLAY = 'PLAY MONEY',
