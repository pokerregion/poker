import re
from decimal import Decimal
from collections import OrderedDict
import pytz
from ..handhistory import HandHistoryPlayer, SplittableHandHistory, normalize
from ..card import Card
from ..hand import Combo
from .._common import _make_int


__all__ = ['FullTiltPokerHandHistory']


class FullTiltPokerHandHistory(SplittableHandHistory):
    """Parses Full Tilt Poker hands the same way as PokerStarsHandHistory class."""

    poker_room = 'FTP'
    date_format = '%H:%M:%S ET - %Y/%m/%d'
    tournament_level = None     # FTP hands doesn't contains tournament level information
    rake = None

    _TZ = pytz.timezone('US/Eastern')  # ET

    _split_re = re.compile(r" ?\*\*\* ?\n?|\n")
    # header patterns
    _header_re = re.compile(r"""
        ^Full[ ]Tilt[ ]Poker[ ]                                 # Poker Room
        Game[ ]\#(?P<ident>\d*):[ ]                             # Hand history id
        (?P<tournament_name>                                    # Tournament name
            \$?(?P<buyin>\d*)?                                  # buyin, not always there,
                                                                # part of tournament_name
        .*)[ ]                                                  # end of tournament_name
        \((?P<tournament_ident>\d*)\),[ ]                       # Tournament Number
        Table[ ](?P<table_name>\d*)[ ]-[ ]                      # Table name
        (?P<limit>NL|PL|FL|No Limit|Pot Limit|Fix Limit)[ ]     # limit
        (?P<game>.*?)[ ]-[ ]                                    # game
        (?P<sb>\d*)/(?P<bb>\d*)[ ]-[ ].*                        # blinds
        \[(?P<date>.*)\]$                                       # date in ET
        """, re.VERBOSE)
    _seat_re = re.compile(r"^Seat (\d): (.*) \(([\d,]*)\)$")
    _button_re = re.compile(r"^The button is in seat #(\d)$")
    _hero_re = re.compile(r"^Dealt to (?P<hero_name>.*) \[(..) (..)\]$")
    _street_re = re.compile(r"\[([^\]]*)\] \(Total Pot: (\d*)\, (\d) Players")
    _pot_re = re.compile(r"^Total pot ([\d,]*) .*\| Rake (\d*)$")
    _winner_re = re.compile(r"^Seat (?P<seat>\d): (?P<name>.*?) .*collected \((\d*)\),")
    _showdown_re = re.compile(r"^Seat (\d): (.*) showed .* and won")
    _board_re = re.compile(r"(?<=[\[ ])(..)(?=[\] ])")

    # search split locations (basically empty strings)
    # sections[0] is before HOLE CARDS
    # sections[-1] is before SUMMARY

    def parse_header(self):
        header_line = self._splitted[0]
        match = self._header_re.match(header_line)
        self.sb = Decimal(match.group('sb'))
        self.bb = Decimal(match.group('bb'))
        self._parse_date(match.group('date'))
        self.ident = match.group('ident')
        self.tournament_name = match.group('tournament_name')
        self.game_type = 'SNG' if 'Sit & Go' in self.tournament_name else 'TOUR'
        self.tournament_ident = match.group('tournament_ident')
        self.table_name = match.group('table_name')
        self.currency = 'USD' if '$' in self.tournament_name else None
        self.limit = normalize(match.group('limit'))
        self.game = normalize(match.group('game'))
        buyin = match.group('buyin')
        self.buyin = Decimal(buyin) if buyin else None

        self.header_parsed = True

    def _parse_table(self):
        # table already parsed in parse_header()
        pass

    def _parse_players(self):
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

    def _parse_button(self):
        # one line before the first split.
        button_line = self._splitted[self._sections[0] - 1]
        button_seat = int(self._button_re.match(button_line).group(1))
        self.button = self.players[button_seat - 1]

    def _parse_hero(self):
        hole_cards_line = self._splitted[self._sections[0] + 2]
        match = self._hero_re.match(hole_cards_line)
        hero, hero_index = self._get_hero_from_players(match.group('hero_name'))
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
            self._parse_streetline(start, street)
            stop = next(v for v in self._sections if v > start)
            street_actions = self._splitted[start + 1:stop]
            setattr(self, "%s_actions" % street, tuple(street_actions) if street_actions else None)
        except ValueError:
            setattr(self, street, None)
            setattr(self, '%s_actions' % street, None)
            setattr(self, '%s_pot' % street, None)
            setattr(self, '%s_num_players' % street, None)

    def _parse_streetline(self, start, street):
        """Parse pot, num players and cards."""
        # Exceptions caught in _parse_street.
        board_line = self._splitted[start]
        match = self._street_re.search(board_line)

        pot = match.group(2)
        setattr(self, "%s_pot" % street, Decimal(pot))

        num_players = int(match.group(3))
        setattr(self, "%s_num_players" % street, num_players)

    def _parse_showdown(self):
        self.show_down = 'SHOW DOWN' in self._splitted

    def _parse_pot(self):
        potline = self._splitted[self._sections[-1] + 2]
        match = self._pot_re.match(potline.replace(',', ''))
        self.total_pot = int(match.group(1))

    def _parse_board(self):
        boardline = self._splitted[self._sections[-1] + 3]
        if not boardline.startswith('Board'):
            return
        cards = self._board_re.findall(boardline)
        self.flop = tuple(map(Card, cards[:3])) if cards else None
        self.turn = Card(cards[3]) if len(cards) > 3 else None
        self.river = Card(cards[4]) if len(cards) > 4 else None

    def _parse_winners(self):
        winners = set()
        start = self._sections[-1] + 4
        for line in self._splitted[start:]:
            if not self.show_down and "collected" in line:
                match = self._winner_re.match(line)
                winners.add(match.group('name'))
            elif self.show_down and "won" in line:
                match = self._showdown_re.match(line)
                winners.add(match.group('name'))

        self.winners = tuple(winners)

    def _parse_extra(self):
        pass
