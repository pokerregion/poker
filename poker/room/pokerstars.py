import re
from decimal import Decimal
from collections import OrderedDict
import pytz
from ..handhistory import HandHistory, normalize


__all__ = ['PokerStarsHandHistory']


class PokerStarsHandHistory(HandHistory):
    """Parses PokerStars Tournament hands."""

    poker_room = 'STARS'
    date_format = '%Y/%m/%d %H:%M:%S ET'
    _TZ = pytz.timezone('US/Eastern')  # ET

    _split_re = re.compile(r" ?\*\*\* ?\n?|\n")
    _header_re = re.compile(r"""
                        ^PokerStars[ ]                          # Poker Room
                        Hand[ ]\#(?P<ident>\d*):[ ]             # Hand number
                        (?P<game_type>Tournament)[ ]            # Type
                        \#(?P<tournament_ident>\d*),[ ]         # Tournament Number
                        \$(?P<buyin>\d*\.\d{2})\+               # buyin
                        \$(?P<rake>\d*\.\d{2})[ ]               # rake
                        (?P<currency>USD|EUR)[ ]                # currency
                        (?P<game>.*)[ ]                         # game
                        (?P<limit>No[ ]Limit)[ ]                # limit
                        -[ ]Level[ ](?P<tournament_level>.*)[ ] # Level
                        \((?P<sb>.*)/(?P<bb>.*)\)[ ]            # blinds
                        -[ ].*[ ]                               # localized date
                        \[(?P<date>.*)\]$                       # ET date
                        """, re.VERBOSE)
    _table_re = re.compile(r"^Table '(.*)' (\d)-max Seat #(\d) is the button$")
    _seat_re = re.compile(r"^Seat (\d): (.*) \((\d*) in chips\)$")
    _hole_cards_re = re.compile(r"^Dealt to (.*) \[(..) (..)\]$")
    _pot_re = re.compile(r"^Total pot (\d*) .*\| Rake (\d*)$")
    _winner_re = re.compile(r"^Seat (\d): (.*) collected \((\d*)\)$")
    _showdown_re = re.compile(r"^Seat (\d): (.*) showed .* and won")
    _ante_re = re.compile(r".*posts the ante (\d*)")
    _board_re = re.compile(r"(?<=[\[ ])(..)(?=[\] ])")

    def __init__(self, hand_text, parse=True):
        """Split hand history by sections and parse."""
        super(PokerStarsHandHistory, self).__init__(hand_text, parse)
        self._splitted = self._split_re.split(self.raw)

        # search split locations (basically empty strings)
        # sections[0] is before HOLE CARDS
        # sections[-1] is before SUMMARY
        self._sections = [ind for ind, elem in enumerate(self._splitted) if not elem]

        if parse:
            self.parse()

    def parse_header(self):
        match = self._header_re.match(self._splitted[0])
        self.game_type = normalize(match.group('game_type'))
        self.sb = Decimal(match.group('sb'))
        self.bb = Decimal(match.group('bb'))
        self.buyin = Decimal(match.group('buyin'))
        self.rake = Decimal(match.group('rake'))
        self._parse_date(match.group('date'))
        self.game = normalize(match.group('game'))
        self.limit = normalize(match.group('limit'))
        self.ident = match.group('ident')
        self.tournament_ident = match.group('tournament_ident')
        self.tournament_level = match.group('tournament_level')
        self.currency = match.group('currency')

        self.header_parsed = True

    def parse(self):
        super(PokerStarsHandHistory, self).parse()
        self._parse_table()
        self._parse_seats()
        self._parse_hole_cards()
        self._parse_preflop()
        self._parse_street('flop')
        self._parse_street('turn')
        self._parse_street('river')
        self.show_down = "SHOW DOWN" in self._splitted
        self._parse_pot()
        self._parse_board()
        self._parse_winners()

        self.parsed = True

    def _parse_table(self):
        match = self._table_re.match(self._splitted[1])
        self.table_name = match.group(1)
        self.max_players = int(match.group(2))
        self.button_seat = int(match.group(3))

    def _parse_seats(self):
        players = self._init_seats(self.max_players)
        for line in self._splitted[2:]:
            match = self._seat_re.match(line)
            if not match:
                break
            players[int(match.group(1)) - 1] = (match.group(2), int(match.group(3)))

        self.button = players[self.button_seat - 1][0]
        self.players = OrderedDict(players)

    def _parse_hole_cards(self):
        hole_cards_line = self._splitted[self._sections[0] + 2]
        match = self._hole_cards_re.match(hole_cards_line)
        self.hero = match.group(1)
        self.hero_seat = list(self.players.keys()).index(self.hero) + 1
        self.hero_hole_cards = match.group(2, 3)

    def _parse_preflop(self):
        start = self._sections[0] + 3
        stop = self._sections[1]
        self.preflop_actions = tuple(self._splitted[start:stop])

    def _parse_street(self, street):
        try:
            start = self._splitted.index(street.upper()) + 2
            stop = self._splitted.index('', start)
            street_actions = self._splitted[start:stop]
            setattr(self, "%s_actions" % street.lower(), tuple(street_actions) if street_actions else None)
        except ValueError:
            setattr(self, street, None)
            setattr(self, '%s_actions' % street.lower(), None)

    def _parse_pot(self):
        potline = self._splitted[self._sections[-1] + 2]
        match = self._pot_re.match(potline)
        self.total_pot = int(match.group(1))

    def _parse_board(self):
        boardline = self._splitted[self._sections[-1] + 3]
        if not boardline.startswith('Board'):
            return
        cards = self._board_re.findall(boardline)
        self.flop = tuple(cards[:3]) if cards else None
        self.turn = cards[3] if len(cards) > 3 else None
        self.river = cards[4] if len(cards) > 4 else None

    def _parse_winners(self):
        winners = set()
        start = self._sections[-1] + 4
        for line in self._splitted[start:]:
            if not self.show_down and "collected" in line:
                match = self._winner_re.match(line)
                winners.add(match.group(2))
            elif self.show_down and "won" in line:
                match = self._showdown_re.match(line)
                winners.add(match.group(2))

        self.winners = tuple(winners)
