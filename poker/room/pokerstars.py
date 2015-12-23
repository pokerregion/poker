# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function

import re
import pytz
from fractions import Fraction
from datetime import datetime
from ..card import Card
from ..hand import Combo
from ..constants import Limit, Game, GameType, Currency, Action
from ..handhistory import HandHistory, HoleCards, Board, PlayerAction, ParserMode


class ParseError(Exception):
    def __init__(self, line):
        super(ParseException, self).__init__("Failed to parse: %s" % line)


class PokerStarsHandHistoryParser(object):
    """Parses PokerStars Tournament or cash game hands."""

    _DATE_FORMAT = '%Y/%m/%d %H:%M:%S ET'
    _TZ = pytz.timezone('US/Eastern')  # ET
    _split_re = re.compile(r" ?\*\*\* ?\n?|\n")
    _tournament_header_re = re.compile(r"""
        ^PokerStars[ ]                          # Poker Room
        Hand[ ]\#(?P<ident>\d*):[ ]             # Hand history id
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

    _cash_header_re = re.compile(r"""
        ^PokerStars[ ]
        Hand[ ]\#(?P<ident>\d*):[ ]
        (?P<game_type>Hold'em[ ]No[ ]Limit)[ ]
        \(\$(?P<sb>.*)/\$(?P<bb>.*)[ ](?P<currency>.*)\)[ ]-[ ]
        (?P<date>.*)
        """, re.VERBOSE)

    _table_re = re.compile(r"^Table '(?P<name>.*)' (?P<seats>\d)-max Seat #(?P<button>\d) is the button$")
    _seat_re = re.compile(r"^Seat (?P<seat>\d): (?P<name>.*) \(\$?(?P<stack>.*) in chips\).*")
    _hero_re = re.compile(r"^Dealt to (?P<name>.*) \[(?P<card1>..) (?P<card2>..)\]$")
    _pot_re = re.compile(r"^Total pot \$?[0-9](\.[0-9]*)? | Rake \$?[0-9]*(\.[0-9]*)?$")
    _winner_re = re.compile(r"^Seat (\d): (.*) collected \((\d*)\)$")
    _showdown_re = re.compile(r"^Seat (\d): (.*) showed .* and won")
    _ante_re = re.compile(r".*posts the ante (\d*)")
    _board_re = re.compile(r"(?<=[\[ ])(..)(?=[\] ])")

    def __init__(self, stream=None, mode=ParserMode.FULL, save_raw=False, attach_parser=False):
        self.stream = stream
        self._curline = ''
        self._save_raw = save_raw
        self._attach_parser = attach_parser

    @classmethod
    def from_file(cls, filename, mode=ParserMode.FULL):
        return cls(io.open(filename))

    def _readline(self):
        self._curline = self.stream.readline()

    def _seek_next_header(self):
        """seek the character stream such that curline will be the next handhistory header"""
        while not self._curline.startswith("PokerStars"):
            self._readline()
            # abort seeking if eof reached
            if self._curline == '':
                break

    def _parse_header(self):
        header_fields = dict()
        if "Tournament" in self._curline:
            match = self._tournament_header_re.match(self.curline)
            header_fields["buyin"] = Fraction(match.group('buyin'))
            header_fields["tournament_ident"] = match.group('tournament_ident')
            header_fields["tournament_level"] = match.group('tournament_level')
            header_fields["rake"] = Fraction(match.group('rake'))
            header_fields["game"] = Game(match.group('game'))
            header_fields["limit"] = Limit(match.group('limit'))
            tournament = True
        else:
            match = self._cash_header_re.match(self.curline)
            tournament = False

        if match is None:
            raise ParseException(self.curline)

        header_fields["game_type"] = match.group('game_type')
        header_fields["sb"] = Fraction(match.group('sb'))
        header_fields["bb"] = Fraction(match.group('bb'))
        header_fields["ident"] = match.group('ident')
        header_fields["currency"] = Currency(match.group('currency'))
        #self._parse_date(match.group('date'))

        # parse the second line holding table information
        self._readline()
        match = self._table_re.match(self.curline)
        if match is None:
            raise ParseException(self.curline)
        header_fields["table_name"]  = match.group("name")
        header_fields["max_players"] = int(match.group("seats"))
        header_fields["button"]      = int(match.group("button"))
        self._readline()
        return header_fields

    def parse(self):
        """Get the next history (or header or text, see readmode of init) from the file."""
        self._seek_next_header()

        # all kind of meta information, including button
        header_fields = self._parse_header()

        if self._save_raw:

        hh = HandHistory(raw, **header_fields)

        # the player names and stacks
        self._parse_players(hh)
        # blinds and ante
        self._parse_blinds(hh)

        # possibly own holecards
        self._parse_hero(hh)
        # parse different streets including board cards
        self._parse_preflop(hh)
        self._parse_flop(hh)
        self._parse_turn(hh)
        self._parse_river(hh)
        self._parse_showdown(hh)

        return hh

    @property
    def histories(self):
        self.stream.seek(0)

        self.__seek_next_header()
        while self.curline != '':
            yield self.parse()
            self.__seek_next_header()


    def _parse_players(self,hh):
        match = self._seat_re.match(self.curline)
        # we assume that the current line is starting line of seats
        if match is None:
            raise ParseException(self.curline)
        # repeat until the end of the players section
        while match is not None:
            index = int(match.group('seat')) - 1
            hh.seats[index].stack = Fraction(match.group('stack'))
            hh.seats[index].name  = match.group('name')

            self._readline()
            match = self._seat_re.match(self.curline)

        # ignore some stuff
        while "will be allowed to play" in self.curline:
            self._readline()


    def _parse_blinds(self,hh):
        blind_re = re.compile(r"(.*): posts (small|big|small & big) blind[s]? \$?(.*)")

        match = blind_re.match(self.curline)

        if match is None:
            raise ParseException(self.curline)

        hh.blinds = []
        while match is not None:
            name = match.group(1)
            value = Fraction(match.group(3))
            i,s = hh.seat(name)
            hh.blinds.append(PlayerAction(i,Action.BLIND,value))

            self._readline()
            match = blind_re.match(self.curline)

        # skip sitout
        while "sits out" in self.curline:
            self._readline()



    def _parse_hero(self,hh):
        if "*** HOLE CARDS ***" in self.curline:
            self._readline()
        match = self._hero_re.match(self.curline)
        if match is not None:
            name = hh.seat(name).holecards = HoleCards(Card(match.group("card1")), Card(match.group("card2")))
            self._readline()


    def _parse_street(self,hh):
        action_re = re.compile(r"(?P<name>.*): " + \
                               r"(?P<action>checks|folds|calls|bets|raises) " + \
                               r"\$?(?P<value>[0-9]+(\.[0-9]*))?.*")
        match = action_re.match(self.curline)
        actions = []
        while match is not None:
            name = match.group("name")
            action = match.group("action")
            value  = match.group("value")
            i,seat = hh.seat(name)
            a = Action(action)
            if a is Action.RAISE or a is Action.BET:
                pa = PlayerAction(i,a,Fraction(value))
            else:
                pa = PlayerAction(i,a)
            actions.append(pa)

            self._readline()
            match = action_re.match(self.curline)
        return actions

    def _parse_preflop(self,hh):
        hh.preflopactions = self._parse_street(hh)


    def _parse_flop(self,hh):
        # pattern will be "*** FLOP *** [Ah 7d 5d]"
        board_re =re.compile(r"\*\*\* FLOP \*\*\* " + \
                             r"\[([23456789TJQKA][cdhs]) " + \
                             r"([23456789TJQKA][cdhs]) " + \
                             r"([23456789TJQKA][cdhs])\].*")
        match = board_re.match(self.curline)
        if match is not None:
            hh.board = Board(*[Card(match.group(i)) for i in [1,2,3]])
            self._readline()

            hh.flopactions = self._parse_street(hh)


    def _parse_turn(self,hh):
        # pattern will be *** TURN *** [Ah 7d 5d] [Qh]
        board_re =re.compile(r"\*\*\* TURN \*\*\* " + \
                             r"\[.{8}\] \[(.{2})\].*")
        match = board_re.match(self.curline)
        if match is not None:
            hh.board.append(Card(match.group(1)))
            self._readline()

            hh.turnactions = self._parse_street(hh)

    def _parse_river(self,hh):
        # pattern will be *** RIVER *** [Ah 7d 5d] [Qh] [XX]
        board_re =re.compile(r"\*\*\* RIVER \*\*\* " + \
                             r"\[.{11}\] \[(.{2})\].*")
        match = board_re.match(self.curline)
        if match is not None:
            hh.board.append(Card(match.group(1)))
            self._readline()

            hh.riveractions = self._parse_street(hh)


    def _parse_showdown(self, hh):
        if "*** SHOW DOWN ***" in self.curline:
            hh.showdown = True
            self._readline()

            showdown_re = re.compile(r"(.*): shows \[(.{2}) (.{2})\].*")

            match = showdown_re.match(self.curline)

            while match is not None:
                player = match.group(1)
                h1 = match.group(2)
                h2 = match.group(3)
                i,seat = hh.seat(player)
                seat.holecards = HoleCards(Card(h1),Card(h2))
                self._readline()
                match = showdown_re.match(self.curline)

            while "collected" in self.curline \
                    or "mucks" in self.curline \
                    or "doesn't show" in self.curline \
                    or ": shows" in self.curline:
                self._readline()
