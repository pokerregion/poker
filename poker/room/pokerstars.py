# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function

import re
from decimal import Decimal
from datetime import datetime
from collections import namedtuple
from lxml import etree
import pytz
from pathlib import Path
from zope.interface import implementer
from .. import handhistory as hh
from ..card import Card
from ..hand import Combo
from ..constants import Limit, Game, GameType, Currency, Action



class ParseException(Exception):
    def __init__(self,line):
        super(ParseException,self).__init__("Failed to parse: "+ line)

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

    _cash_header_re = re.compile(r"^PokerStars Hand \#(?P<ident>\d*):  " +
                       r"(?P<game_type>Hold'em No Limit) "+
                       r"\(\$(?P<sb>.*)/\$(?P<bb>.*) (?P<currency>.*)\) - " +
                       r"(?P<date>.*)")

    _table_re = re.compile(r"^Table '(?P<name>.*)' (?P<seats>\d)-max Seat #(?P<button>\d) is the button$")
    _seat_re = re.compile(r"^Seat (?P<seat>\d): (?P<name>.*) \(\$?(?P<stack>\d*) in chips\)$")
    _hero_re = re.compile(r"^Dealt to (?P<name>.*) \[(?P<card1>..) (?P<card2>..)\]$")
    _pot_re = re.compile(r"^Total pot \$?[0-9](\.[0-9]*)? | Rake \$?[0-9]*(\.[0-9]*)?$")
    _winner_re = re.compile(r"^Seat (\d): (.*) collected \((\d*)\)$")
    _showdown_re = re.compile(r"^Seat (\d): (.*) showed .* and won")
    _ante_re = re.compile(r".*posts the ante (\d*)")
    _board_re = re.compile(r"(?<=[\[ ])(..)(?=[\] ])")

    #def _get_curline(self):
    #    return self.__curline

    #curline = property(_get_curline,"the line that is next to be parsed")

    def __seek_next_header(self):
        """seek the character stream such that curline will be the next handhistory header"""
        while not self.curline.startswith("PokerStars"):
            self.curline = self.stream.readline()
            print self.curline,

    def __readline(self):
        self.curline = self.stream.readline()

    def __init__(self, stream = None, filename = None, mode = "full"):
        """
        Create a parser from lines.
        lines can either be a StrinIO object of a string.
        or an open file.
        Arguments: stream The data stream with hand histories, can be an open file.
                   filename: Filename to open as stream.
                    mode: "full" read full handhistory,
                          "header" only read headers,
                          "text" dont parse anything, only split the file into seperate chunks each containing
                          exactly the text of one file.
        """
        if mode != "full":
            raise Exception("Not implemented.")
        if filename is not None:
            assert(stream == None)
            self.stream = open(filename,"r")
        else:
            self.stream  = stream
        self.curline = ""
        #self.__seek_next_header()

    def _parse_header(self):
        properties = dict()
        # try parsing cash game header
        if "Tournament" in self.curline:

            match = self._tournament_header_re.match(self.curline)
            properties["buyin"]            = Decimal(match.group('buyin'))
            properties["tournament_ident"] = match.group('tournament_ident')
            properties["tournament_level"] = match.group('tournament_level')
            properties["rake"]             = Decimal(match.group('rake'))
            properties["game"]             = Game(match.group('game'))
            properties["limit"]            = Limit(match.group('limit'))
            tournament = True
        else:
            match = self._cash_header_re.match(self.curline)
            tournament = False

        if match is None:
            raise ParseException(self.curline)

        properties["game_type"] = match.group('game_type')
        properties["sb"] = Decimal(match.group('sb'))
        properties["bb"] = Decimal(match.group('bb'))
        properties["ident"] = match.group('ident')
        properties["currency"] = Currency(match.group('currency'))
        #self._parse_date(match.group('date'))

        # parse the second line holding table information
        self.__readline()
        match = self._table_re.match(self.curline)
        if match is None:
            raise ParseException(self.curline)
        properties["table_name"]  = match.group("name")
        properties["max_players"] = int(match.group("seats"))
        properties["button"]      = int(match.group("button"))
        self.__readline()
        return properties

    def parse(self):
        """Get the next history (or header or text, see readmode of init) from the file."""
        self.__seek_next_header()

        # all kind of meta information, including button
        properties = self._parse_header()

        hh = HandHistory(text = None, **properties)
        print hh

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

    def _parse_players(self,hh):
        match = self._seat_re.match(self.curline)
        # repeat until the end of the players section
        while match is not None:
            index = int(match.group('seat')) - 1
            hh.seats[index].stack = int(match.group('stack'))
            hh.seats[index].name  = match.group('name')

            self.__readline()
            match = self._seat_re.match(self.curline)

        # ignore some stuff
        while "will be allowed to play" in self.curline:
            self.__readline()


    def _parse_blinds(self,hh):
        blind_re = re.compile(r"(.*): posts (small|big|small & big) blind[s]? \$?(.*)")

        match = blind_re.match(self.curline)

        hh.blinds = []
        while match is not None:
            name = match.group(0)
            value = match.group(2)
            hh.blinds.append((name,value))

            self.__readline()


    def _parse_hero(self,hh):
        if self.curline == "*** HOLE CARDS ***":
            self.__readline()
        match = self._hero_re.match(self.curline)
        if match is not None:
            name = hh.seat(name).holecards = Card(match.group("card1")), Card(match.group("card2"))
            self.__readline()


    def _parse_street(self):
        action_re = re.compile(r"(?P<name>.*): " + \
                               r"(?P<action>checks|folds|calls|bets|raises) " + \
                               r"\$?(?P<value>.*) .*")
        match = action_re.match(self.curline)
        actions = []
        while match is not None:
            name = match.group("name")
            action = match.group("action")
            value  = match.group("value")
            actions.append((name,action, value))

            self.__readline()
            match = action_re.match(self.curline)
        return actions

    def _parse_preflop(self,hh):
        hh.preflopactions = self._parse_street()


    def _parse_flop(self,hh):
        # pattern will be "*** FLOP *** [Ah 7d 5d]"
        board_re =re.compile(r"\*\*\* FLOP \*\*\* " + \
                             r"\[([23456789TJQKA][cdhs]) " + \
                             r"([23456789TJQKA][cdhs]) " + \
                             r"([23456789TJQKA][cdhs])\].*")
        match = board_re.match(self.curline)
        if match is not None:
            hh.board[0] = Card(match.group(0))
            hh.board[1] = Card(match.group(1))
            hh.board[2] = Card(match.group(2))
            self.__readline()

            hh.flopactions = self._parse_street()


    def _parse_turn(self,hh):
        # pattern will be *** TURN *** [Ah 7d 5d] [Qh]
        board_re =re.compile(r"\*\*\* TURN \*\*\* " + \
                             r"\[.{8}\] \[(.{2})\].*")
        match = board_re.match(self.curline)
        if match is not None:
            hh.board[3] = Card(match.group(0))
            self.__readline()

            hh.turnactions = self._parse_street()

    def _parse_river(self,hh):
        # pattern will be *** RIVER *** [Ah 7d 5d] [Qh] [XX]
        board_re =re.compile(r"\*\*\* RIVER \*\*\* " + \
                             r"\[.{8}\] \[.{2}\] [(.{2})].*")
        match = board_re.match(self.curline)
        if match is not None:
            hh.board[4] = Card(match.group(0))
            self.__readline()

            hh.riveractions = self._parse_street()


    def _parse_showdown(self, hh):
        if self.curline == "*** SHOW DOWN***":
            hh.showdown = True
            self.__readline()

            showdown_re = re.compile(r"(.*): shows \[(.{2}) (.{2})\].*")

            match = showdown_re.match(self.curline)

            while match is not None:
                player = match.group(0)
                h1 = match.group(1)
                h2 = match.group(2)
                hh.seat(player).holecards = Card(h1),Card(h2)
                self.__readline()
                match = showdown_re.match(self.curline)

            while "collected" in self.curline \
                    or "mucks" in self.curline \
                    or "doesn't show" in self.curline \
                    or ": shows" in self.curline:
                self.__readline()
