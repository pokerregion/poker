import re
from decimal import Decimal
from collections import OrderedDict
import pytz
from ..handhistory import HandHistoryPlayer, HandHistory, normalize
from ..card import Card
from ..hand import Combo
from .._common import _make_int


__all__ = ['FullTiltPokerHandHistory']


class FullTiltPokerHandHistory(HandHistory):
    """Parses Full Tilt Poker hands the same way as PokerStarsHandHistory class."""

    poker_room = 'FTP'
    date_format = '%H:%M:%S ET - %Y/%m/%d'
    _TZ = pytz.timezone('US/Eastern')  # ET

    _split_re = re.compile(r" ?\*\*\* ?\n?|\n")

    # header patterns
    _tournament_re = re.compile(r"""
                        ^Full[ ]Tilt[ ]Poker[ ]                 # Poker Room
                        Game[ ]\#(?P<ident>\d*):[ ]             # Hand number
                        (?P<tournament_name>.*)[ ]              # Tournament name
                        \((?P<tournament_ident>\d*)\),[ ]       # Tournament Number
                        Table[ ](?P<table_name>\d*)[ ]-[ ]      # Table name
                        """, re.VERBOSE)
    _game_re = re.compile(r" - (?P<limit>NL|PL|FL|No Limit|Pot Limit|Fix Limit) (?P<game>.*?) - ")
    _blind_re = re.compile(r" - (\d*)/(\d*) - ")
    _date_re = re.compile(r" \[(.*)\]$")

    _seat_re = re.compile(r"^Seat (\d): (.*) \(([\d,]*)\)$")
    _button_re = re.compile(r"^The button is in seat #(\d)$")
    _hole_cards_re = re.compile(r"^Dealt to (.*) \[(..) (..)\]$")
    _street_re = re.compile(r"\[([^\]]*)\] \(Total Pot: (\d*)\, (\d) Players")
    _pot_re = re.compile(r"^Total pot ([\d,]*) .*\| Rake (\d*)$")
    _winner_re = re.compile(r"^Seat (\d): (.*) collected \((\d*)\),")
    _showdown_re = re.compile(r"^Seat (\d): (.*) showed .* and won")

    def __init__(self, hand_text, parse=True):
        super(FullTiltPokerHandHistory, self).__init__(hand_text, parse)

        self._splitted = self._split_re.split(self.raw)

        # search split locations (basically empty strings)
        # sections[0] is before HOLE CARDS
        # sections[-1] is before SUMMARY
        self._sections = [ind for ind, elem in enumerate(self._splitted) if not elem]

        if parse:
            self.parse()

    def parse_header(self):
        header_line = self._splitted[0]

        match = self._tournament_re.match(header_line)
        self.game_type = 'TOUR'
        self.ident = match.group('ident')
        self.tournament_name = match.group('tournament_name')
        self.tournament_ident = match.group('tournament_ident')
        self.table_name = match.group('table_name')

        match = self._game_re.search(header_line)
        self.limit = normalize(match.group('limit'))
        self.game = normalize(match.group('game'))

        match = self._blind_re.search(header_line)
        self.sb = Decimal(match.group(1))
        self.bb = Decimal(match.group(2))

        match = self._date_re.search(header_line)
        self._parse_date(match.group(1))

        self.tournament_level = self.buyin = self.rake = self.currency = None

        self.header_parsed = True

    def parse(self):
        super(FullTiltPokerHandHistory, self).parse()

        self._parse_seats()
        self._parse_hole_cards()
        self._parse_preflop()
        self._parse_street('flop')
        self._parse_street('turn')
        self._parse_street('river')
        self.show_down = 'SHOW DOWN' in self._splitted
        self._parse_pot()
        self._parse_winners()

        del self._splitted

        self.parsed = True

    def _parse_seats(self):
        # In hh there is no indication of max_players, so init for 9.
        players = self._init_seats(9)
        for line in self._splitted[1:]:
            match = self._seat_re.match(line)
            if not match:
                break
            seat = int(match.group(1))
            players[seat - 1] = HandHistoryPlayer(
                name=match.group(2),
                seat=seat,
                stack=_make_int(match.group(3)),
                combo=None
            )
        self.max_players = seat
        self.players = players[:seat]  # cut off unneccesary seats

        # one line before the first split.
        button_line = self._splitted[self._sections[0] - 1]
        button_seat = int(self._button_re.match(button_line).group(1))
        self.button = players[button_seat - 1]

    def _parse_hole_cards(self):
        hole_cards_line = self._splitted[self._sections[0] + 2]
        match = self._hole_cards_re.match(hole_cards_line)
        hero_name = match.group(1)
        player_names = [p.name for p in self.players]
        hero_index = player_names.index(hero_name)
        hero = self.players[hero_index]
        self.hero = self.players[hero_index] = hero._replace(
            combo=Combo(match.group(2) + match.group(3))
        )

        if self.button.name == self.hero.name:
            self.button = self.hero

    def _parse_preflop(self):
        start = self._sections[0] + 3
        stop = self._sections[1]
        self.preflop_actions = tuple(self._splitted[start:stop])

    def _parse_street(self, street):
        try:
            start = self._splitted.index(street.upper()) + 1
            self._parse_boardline(start, street)
            stop = next(v for v in self._sections if v > start)
            street_actions = self._splitted[start + 1:stop]
            setattr(self, "%s_actions" % street, tuple(street_actions) if street_actions else None)
        except ValueError:
            setattr(self, street, None)
            setattr(self, '%s_actions' % street, None)
            setattr(self, '%s_pot' % street, None)
            setattr(self, '%s_num_players' % street, None)

    def _parse_boardline(self, start, street):
        """Parse pot, num players and cards."""
        # Exceptions caught in _parse_street.
        board_line = self._splitted[start]

        match = self._street_re.search(board_line)
        cards = match.group(1)
        cards = tuple(map(Card, cards.split())) if street == 'flop' else Card(cards)
        setattr(self, street, cards)

        pot = match.group(2)
        setattr(self, "%s_pot" % street, Decimal(pot))

        num_players = int(match.group(3))
        setattr(self, "%s_num_players" % street, num_players)

    def _parse_pot(self):
        potline = self._splitted[self._sections[-1] + 2]
        match = self._pot_re.match(potline.replace(',', ''))
        self.total_pot = int(match.group(1))

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
