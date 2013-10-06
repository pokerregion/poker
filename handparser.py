import re
from StringIO import StringIO
from datetime import datetime
from decimal import Decimal
from collections import OrderedDict
import pytz


ET = pytz.timezone('US/Eastern')
POKER_ROOMS = {'PokerStars': 'STARS'}
TYPES = {'Tournament': 'TOUR'}
GAMES = {"Hold'em": 'HOLDEM'}
LIMITS = {'No Limit': 'NL'}


class _StringIONoNewLine(StringIO):
    last_line = None

    def readline(self, length=None):
        return StringIO.readline(self, length=length).rstrip()


class PokerStarsHand(object):
    date_format = '%Y/%m/%d %H:%M:%S'
    _header_pattern = re.compile(r"""
                                (?P<room>PokerStars)[ ]         # Poker Room
                                Hand[ ]\#(?P<number>\d*):[ ]    # Hand number
                                (?P<type>Tournament)[ ]         # Type
                                \#(?P<tour_number>\d*),[ ]      # Tournament Number
                                \$(?P<buyin>\d*\.\d{2})\+       # buyin
                                \$(?P<rake>\d*\.\d{2})[ ]       # rake
                                (?P<currency>USD|EUR)[ ]        # currency
                                (?P<game>.*)[ ]                 # game
                                (?P<limit>No[ ]Limit)[ ]        # limit
                                -[ ]Level[ ](?P<tour_level>.*)[ ] # Level
                                \((?P<sb>.*)/(?P<bb>.*)\)[ ]    # blinds
                                -[ ].*[ ]                       # localized date
                                \[(?P<date>.*)[ ]ET\]$          # ET date
                                """, re.VERBOSE)
    _table_pattern = re.compile(r"Table '(.*)' (\d)-max Seat #(\d) is the button$")
    _seat_pattern = re.compile(r"Seat (\d): (.*) \((\d*) in chips\)$")
    _dealt_to_pattern = re.compile(r"Dealt to (.*) \[(.{2}) (.{2})\]$")
    _flop_pattern = re.compile(r"\*\*\* FLOP \*\*\* \[(.{2}) (.{2}) (.{2})\]$")
    _turn_pattern = re.compile(r"\*\*\* TURN \*\*\* \[.*\] \[(.{2})\]")
    _river_pattern = re.compile(r"\*\*\* RIVER \*\*\* \[.*\] \[(.{2})\]")
    _pot_pattern = re.compile(r"Total pot (\d*) .*\| Rake (\d*)$")
    _summary_pattern = re.compile(r"Seat (\d): (.*) collected \((\d*)\)$")
    _ante_pattern = re.compile(r".*posts the ante (\d*)")

    def __init__(self, hand_text, parse=True):
        self.raw = hand_text
        self._hand = _StringIONoNewLine(hand_text.strip())
        self.header_parsed, self.parsed = False, False

        if parse:
            self.parse()

    def parse_header(self):
        """
        Parses the first line of a hand history.
        """
        match = self._header_pattern.match(self._hand.readline())
        self.room = POKER_ROOMS[match.group('room')]
        self.type = TYPES[match.group('type')]
        self.sb = Decimal(match.group('sb'))
        self.bb = Decimal(match.group('bb'))
        self.buyin = Decimal(match.group('buyin'))
        self.rake = Decimal(match.group('rake'))
        self.date = ET.localize(datetime.strptime(match.group('date'), self.date_format))
        self.game = GAMES[match.group('game')]
        self.limit = LIMITS[match.group('limit')]
        self.number = match.group('number')
        self.tour_number = match.group('tour_number')
        self.tour_level = match.group('tour_level')
        self.currency = match.group('currency')

        self.header_parsed = True

    def parse(self):
        """
        Parse the body of the hand history, but first parse header if not yet parsed.
        """
        if not self.header_parsed:
            self.parse_header()

        self._parse_table()
        self._parse_players()
        self._parse_preflop()
        self._parse_flop()
        print "FLOP PARSED"
        self._parse_turn()
        print "TURN PARSED"
        self._parse_river()
        print "RIVER PARSED"
        self._parse_showdown()
        print "SHOWDOWN PARSED"
        self._parse_summary()

        self.parsed = True

    def _parse_table(self):
        match = self._table_pattern.match(self._hand.readline())
        self.table_name = match.group(1)
        self.max_players = int(match.group(2))
        self.button_seat = int(match.group(3))

    def _parse_players(self):
        players = [None] * self.max_players
        for line in self._hand:
            if not line.startswith('Seat'):
                self._hand.last_line = line
                break
            match = self._seat_pattern.match(line)
            players[int(match.group(1)) - 1] = (match.group(2), int(match.group(3)))
        self.button = players[self.button_seat - 1][0]
        self.players = OrderedDict(players)

    def _parse_preflop(self):
        if 'ante' in self._hand.last_line:
            match = self._ante_pattern.match(self._hand.last_line)
            self.ante = int(match.group(1))

        for line in self._hand:
            if line.startswith('*** HOLE CARDS'):
                break

        match = self._dealt_to_pattern.match(self._hand.readline())
        self.hero = match.group(1)
        self.hero_seat = self.players.keys().index(self.hero) + 1
        self.hero_hole_cards = match.group(2, 3)
        self.preflop_actions = self._parse_actions()

    def _parse_flop(self):
        try:
            print " FLOP VONALA:", self._hand.last_line
            self.flop = self._flop_pattern.match(self._hand.last_line).group(1, 2, 3)
        except AttributeError:
            self.flop = None

        try:
            self.flop_actions = self._parse_actions()
        except AttributeError:
            self.flop_actions = None

    def _parse_turn(self):
        try:
            self.turn = self._turn_pattern.match(self._hand.last_line).group(1)
        except AttributeError:
            self.turn = None

        try:
            self.turn_actions = self._parse_actions()
        except AttributeError:
            self.turn_actions = None

    def _parse_river(self):
        try:
            self.river = self._river_pattern.match(self._hand.last_line).group(1)
        except AttributeError:
            self.river = None

        try:
            self.river_actions = self._parse_actions()
        except AttributeError:
            self.river_actions = None

    def _parse_showdown(self):
        self._parse_actions()

    def _parse_summary(self):
        print "LAST LINE:", self._hand.last_line
        hand_readline = self._hand.readline()
        print "     READ LINE:", hand_readline
        match = self._pot_pattern.match(hand_readline)
        self.total_pot = int(match.group(1))

        # Skip Board [.. .. .. .. ..]
        self._hand.readline()

        winners = []
        for line in self._hand:
            if "collected" in line:
                match = self._summary_pattern.match(line)
                winners.append(match.group(2))
        self.winners = tuple(winners)

    def _parse_actions(self):
        actions = []
        for line in self._hand:
            print line
            if line.startswith("***"):
                self._hand.last_line = line
                break
            actions.append(line)
        else:
            return
        return tuple(actions)

    @property
    def board(self):
        board = []
        for street in (self.flop, self.turn, self.river):
            if street:
                board.extend(street)
            else:
                break
        return tuple(board)

