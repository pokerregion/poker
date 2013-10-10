import re
from datetime import datetime
from decimal import Decimal
from collections import OrderedDict, MutableMapping
import pytz


ET = pytz.timezone('US/Eastern')
POKER_ROOMS = {'PokerStars': 'STARS'}
TYPES = {'Tournament': 'TOUR'}
GAMES = {"Hold'em": 'HOLDEM'}
LIMITS = {'No Limit': 'NL'}


class PokerStarsHand(MutableMapping):
    date_format = '%Y/%m/%d %H:%M:%S'
    _split_pattern = re.compile(r" ?\*\*\* ?\n?|\n")
    _header_pattern = re.compile(r"""
                                (?P<poker_room>PokerStars)[ ]           # Poker Room
                                Hand[ ]\#(?P<number>\d*):[ ]            # Hand number
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
                                \[(?P<date>.*)[ ]ET\]$                  # ET date
                                """, re.VERBOSE)
    _table_pattern = re.compile(r"Table '(.*)' (\d)-max Seat #(\d) is the button$")
    _seat_pattern = re.compile(r"Seat (\d): (.*) \((\d*) in chips\)$")
    _dealt_to_pattern = re.compile(r"Dealt to (.*) \[(.{2}) (.{2})\]$")
    _pot_pattern = re.compile(r"Total pot (\d*) .*\| Rake (\d*)$")
    _summary_winner_pattern = re.compile(r"Seat (\d): (.*) collected \((\d*)\)$")
    _summary_showdown_pattern = re.compile(r"Seat (\d): (.*) showed .* and won")
    _ante_pattern = re.compile(r".*posts the ante (\d*)")
    _board_pattern = re.compile(r"(?<=[\[ ])(..)(?=[\] ])")

    def __init__(self, hand_text, parse=True):
        self.raw = hand_text
        self._splitted = self._split_pattern.split(hand_text.strip())

        # search split locations
        # sections[0] is before HOLE CARDS
        # sections[-1] is before SUMMARY
        self._sections = [ind for ind, elem in enumerate(self._splitted) if not elem]

        self.header_parsed, self.parsed = False, False

        if parse:
            self.parse()

    def __len__(self):
        return len(self.keys())

    def __getitem__(self, key):
        if key != 'raw':
            return getattr(self, key)
        else:
            raise KeyError('You can only get it via the attribute like "hand.raw"')

    def __setitem__(self, key, value):
        self.header_parsed, self.parsed = False, False
        setattr(self, key, value)

    def __delitem__(self, key):
        self.header_parsed, self.parsed = False, False
        delattr(self, key)

    def keys(self):
        return [attr for attr in vars(self) if not attr.startswith('_') and attr != 'raw']

    def __iter__(self):
        return iter(self.keys())

    def parse_header(self):
        """
        Parses the first line of a hand history.
        """
        match = self._header_pattern.match(self._splitted[0])
        self.poker_room = POKER_ROOMS[match.group('poker_room')]
        self.game_type = TYPES[match.group('game_type')]
        self.sb = Decimal(match.group('sb'))
        self.bb = Decimal(match.group('bb'))
        self.buyin = Decimal(match.group('buyin'))
        self.rake = Decimal(match.group('rake'))
        self.date = ET.localize(datetime.strptime(match.group('date'), self.date_format))
        self.game = GAMES[match.group('game')]
        self.limit = LIMITS[match.group('limit')]
        self.number = match.group('number')
        self.tournament_ident = match.group('tournament_ident')
        self.tournament_level = match.group('tournament_level')
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
        match = self._table_pattern.match(self._splitted[1])
        self.table_name = match.group(1)
        self.max_players = int(match.group(2))
        self.button_seat = int(match.group(3))

    def _parse_players(self):
        players = [('Empty Seat %s' % num, 0) for num in range(1, self.max_players + 1)]
        for line in self._splitted[2:]:
            match = self._seat_pattern.match(line)
            if not match:
                break
            players[int(match.group(1)) - 1] = (match.group(2), int(match.group(3)))

        self.button = players[self.button_seat - 1][0]
        self.players = OrderedDict(players)

    def _parse_hole_cards(self):
        hole_cards_line = self._splitted[self._sections[0] + 2]
        match = self._dealt_to_pattern.match(hole_cards_line)
        self.hero = match.group(1)
        self.hero_seat = self.players.keys().index(self.hero) + 1
        self.hero_hole_cards = match.group(2, 3)

    def _parse_preflop(self):
        start = self._sections[0] + 3
        stop = self._sections[1]
        self.preflop_actions = tuple(self._splitted[start:stop])

    def _parse_street(self, street):
        try:
            start = self._splitted.index(street.upper()) + 2
            stop = start + self._splitted[start:].index('')
            flop_actions = self._splitted[start:stop]
            setattr(self, "%s_actions" % street.lower(), tuple(flop_actions) if flop_actions else None)
        except ValueError:
            setattr(self, street, None)
            setattr(self, '%s_actions' % street.lower(), None)

    def _parse_pot(self):
        potline = self._splitted[self._sections[-1] + 2]
        match = self._pot_pattern.match(potline)
        self.total_pot = int(match.group(1))

    def _parse_board(self):
        self.board = None
        boardline = self._splitted[self._sections[-1] + 3]
        if not boardline.startswith('Board'):
            return
        cards = self._board_pattern.findall(boardline)
        self.board = tuple(cards)
        self.flop = tuple(cards[:3]) if cards else None
        self.turn = cards[3] if len(cards) > 3 else None
        self.river = cards[4] if len(cards) > 4 else None

    def _parse_winners(self):
        winners = set()
        start = self._sections[-1] + 4
        for line in self._splitted[start:]:
            if not self.show_down and "collected" in line:
                match = self._summary_winner_pattern.match(line)
                winners.add(match.group(2))
            elif self.show_down and "won" in line:
                match = self._summary_showdown_pattern.match(line)
                winners.add(match.group(2))

        self.winners = tuple(winners)
