# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function

import re
from decimal import Decimal
import pytz
from zope.interface import implementer
from .. import handhistory as hh
from ..card import Card
from ..hand import Combo
from ..constants import Limit, Game, GameType, Currency, Action
from .._common import _make_int


__all__ = ['FullTiltPokerHandHistory']


class _Street(hh._BaseStreet):
    def _parse_actions(self, actionlines):
        actions = []
        for line in actionlines:
            if line.startswith('Uncalled bet'):
                action = self._parse_uncalled(line)
            elif 'raises to' in line:
                action = self._parse_raise(line)
            elif 'wins the pot' in line:
                action = self._parse_win(line)
            elif 'mucks' in line:
                action = self._parse_muck(line)
            elif 'seconds left to act' in line:
                action = self._parse_think(line)
            elif ' ' in line:
                action = self._parse_player_action(line)
            else:
                raise
            actions.append(hh._PlayerAction(*action))
        self.actions = tuple(actions) if actions else None

    def _parse_uncalled(self, line):
        amount_start_index = 16
        space_after_amount_index = line.find(' ', amount_start_index)
        amount = line[amount_start_index:space_after_amount_index]
        name_start_index = line.find('to ') + 3
        name = line[name_start_index:]
        return name, Action.RETURN, Decimal(amount)

    def _parse_raise(self, line):
        first_space_index = line.find(' ')
        name = line[:first_space_index]
        amount_start_index = line.find('to ') + 3
        amount = line[amount_start_index:]
        return name, Action.RAISE, Decimal(amount)

    def _parse_win(self, line):
        first_space_index = line.find(' ')
        name = line[:first_space_index]
        first_paren_index = line.find('(')
        last_paren_index = -1
        amount = line[first_paren_index + 1:last_paren_index]
        self.pot = Decimal(amount)
        return name, Action.WIN, self.pot

    def _parse_muck(self, line):
        space_index = line.find(' ')
        name = line[:space_index]
        return name, Action.MUCK, None

    def _parse_think(self, line):
        space_index = line.find(' ')
        name = line[:space_index]
        return name, Action.THINK, None

    def _parse_player_action(self, line):
        space_index = line.find(' ')
        name = line[:space_index]
        end_action_index = line.find(' ', space_index + 1)
        # -1 means not found
        if end_action_index == -1:
            end_action_index = None  # until the end
        action = Action(line[space_index + 1:end_action_index])
        if end_action_index:
            amount = line[end_action_index + 1:]
            return name, action, Decimal(amount)
        else:
            return name, action, None


@implementer(hh.IStreet)
class _Preflop():
    def _parse_board(self, boardline):
        self.cards = None


@implementer(hh.IStreet)
class _Flop():
    def _parse_board(self, boardline):
        self.cards = (Card(boardline[1:3]), Card(boardline[4:6]), Card(boardline[7:9]))


@implementer(hh.IStreet)
class _Turn():
    def _parse_board(self, boardline):
        self.cards = (Card(boardline[12:14]),)


@implementer(hh.IStreet)
class _River():
    def _parse_board(self, boardline):
        self.cards = (Card(boardline[12:14]),)


@implementer(hh.IHandHistory)
class FullTiltPokerHandHistory(hh._SplittableHandHistoryMixin, hh._FullTiltPokerStarsMixin,
                               hh._BaseHandHistory):
    """Parses Full Tilt Poker hands the same way as PokerStarsHandHistory class."""

    rake = None
    tournament_level = None

    _date_format = '%H:%M:%S ET - %Y/%m/%d'
    _tz = pytz.timezone('US/Eastern')  # ET
    _split_re = re.compile(r" ?\*\*\* ?\n?|\n")
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
    _seat_re = re.compile(r"^Seat (?P<seat>\d): (?P<name>.*) \((?P<stack>[\d,]*)\)$")
    _button_re = re.compile(r"^The button is in seat #(\d)$")
    _street_re = re.compile(r"\[([^\]]*)\] \(Total Pot: (\d*)\, (\d) Players")
    _pot_re = re.compile(r"^Total pot ([\d,]*) .*\| Rake (\d*)$")
    _winner_re = re.compile(r"^Seat (?P<seat>\d): (?P<name>.*?) .*collected \((\d*)\),")

    def parse_header(self):
        # sections[0] is before HOLE CARDS
        # sections[-1] is before SUMMARY
        self._split_raw()

        header_match = self._header_re.match(self._splitted[0])
        self.ident = header_match.group('ident')
        self.date = self._parse_date(header_match.group('date'))
        self.sb = Decimal(header_match.group('sb'))
        self.bb = Decimal(header_match.group('bb'))
        self.limit = Limit(header_match.group('limit'))
        self.game = Game(header_match.group('game'))
        self.game_type = GameType.SNG if 'Sit & Go' in self.tournament_name else GameType.TOUR
        self.table_name = header_match.group('table_name')
        self.currency = Currency.USD if '$' in self.tournament_name else None
        self.tournament_name = header_match.group('tournament_name')
        self.tournament_ident = header_match.group('tournament_ident')
        buyin = header_match.group('buyin')
        self.buyin = Decimal(buyin) if buyin else None

        self._header_parsed = True

    def _parse_seats(self):
        # There is no indication of max_players, so init for 9.
        players, seat, hero_index = self._get_players(init_seats=9, start_line_index=1)
        self.max_players = seat
        self.players = players[:seat]  # cut off unnecessary seats

        # one line before the first split.
        button_line = self._splitted[self._sections[0] - 1]
        button_seat = int(self._button_re.match(button_line).group(1))
        self.button = self.players[button_seat - 1]
        self.hero = self.players[hero_index]

    def _parse_streets(self):
        lines = self._get_preflop_lines()
        self.preflop = _Preflop(lines) if lines else None

        lines = self._get_street_lines('FLOP')
        self.flop = _Flop(lines) if lines else None

        lines = self._get_street_lines('TURN')
        self.turn = _Turn(lines) if lines else None

        lines = self._get_street_lines('RIVER')
        self.river = _River(lines) if lines else None
