import re
from decimal import Decimal
from collections import namedtuple
import pytz
from ..handhistory import _Player, _SplittableHandHistory, _BaseFlop
from ..card import Card
from ..hand import Combo
from ..constants import Limit, Game, GameType, Currency, Action


__all__ = ['PokerStarsHandHistory']


class _Flop(_BaseFlop):
    _board_re = re.compile(r"(?<=[\[ ])(..)(?=[\] ])")

    def __init__(self, flop: list):
        self.pot = None
        self.actions = None
        self.cards = None
        self._parse_cards(flop[0])
        self._parse_actions(flop[1:])

    def _parse_cards(self, boardline):
        self.cards = (Card(boardline[1:3]), Card(boardline[4:6]), Card(boardline[7:9]))

    def _parse_actions(self, actionlines):
        actions = []
        for line in actionlines:
            if line.startswith('Uncalled bet'):
                actions.append(self._parse_uncalled(line))
            elif 'collected' in line:
                actions.append(self._parse_collected(line))
            elif "doesn't show hand" in line:
                actions.append(self._parse_noshow(line))
            elif ':' in line:
                actions.append(self._parse_player_action(line))
            else:
                raise
        self.actions = tuple(actions) if actions else None

    def _parse_uncalled(self, line):
        first_paren_index = line.find('(')
        second_paren_index = line.find(')')
        amount = line[first_paren_index + 1:second_paren_index]
        name_start_index = line.find('to ') + 3
        name = line[name_start_index:]
        return name, Action.RETURN, Decimal(amount)

    def _parse_collected(self, line):
        first_space_index = line.find(' ')
        name = line[:first_space_index]
        second_space_index = line.find(' ', first_space_index + 1)
        third_space_index = line.find(' ', second_space_index + 1)
        amount = line[second_space_index + 1:third_space_index]
        self.pot = Decimal(amount)
        return name, Action.WIN, self.pot

    def _parse_noshow(self, line):
        colon_index = line.find(':')
        name = line[:colon_index]
        return name, Action.NOSHOW

    def _parse_player_action(self, line):
        colon_index = line.find(':')
        name = line[:colon_index]
        end_action_index = line.find(' ', colon_index + 2)
        # -1 means not found
        if end_action_index == -1:
            end_action_index = None  # until the end
        action = Action(line[colon_index + 2:end_action_index])
        if end_action_index:
            amount = line[end_action_index+1:]
            return name, action, Decimal(amount)
        else:
            return name, action



class PokerStarsHandHistory(_SplittableHandHistory):
    """Parses PokerStars Tournament hands."""

    date_format = '%Y/%m/%d %H:%M:%S ET'
    _TZ = pytz.timezone('US/Eastern')  # ET

    _split_re = re.compile(r" ?\*\*\* ?\n?|\n")
    _header_re = re.compile(r"""
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
    _table_re = re.compile(r"^Table '(.*)' (\d)-max Seat #(?P<button>\d) is the button$")
    _seat_re = re.compile(r"^Seat (?P<seat>\d): (?P<name>.*) \((?P<stack>\d*) in chips\)$")
    _hero_re = re.compile(r"^Dealt to (?P<hero_name>.*) \[(..) (..)\]$")
    _pot_re = re.compile(r"^Total pot (\d*) .*\| Rake (\d*)$")
    _winner_re = re.compile(r"^Seat (\d): (.*) collected \((\d*)\)$")
    _showdown_re = re.compile(r"^Seat (\d): (.*) showed .* and won")
    _ante_re = re.compile(r".*posts the ante (\d*)")
    _board_re = re.compile(r"(?<=[\[ ])(..)(?=[\] ])")

    # search split locations (basically empty strings)
    # sections[0] is before HOLE CARDS
    # sections[-1] is before SUMMARY

    def parse_header(self):
        header_line = self._splitted[0]
        match = self._header_re.match(header_line)
        self.game_type = GameType(match.group('game_type'))
        self.sb = Decimal(match.group('sb'))
        self.bb = Decimal(match.group('bb'))
        self.buyin = Decimal(match.group('buyin'))
        self.rake = Decimal(match.group('rake'))
        self._parse_date(match.group('date'))
        self.game = Game(match.group('game'))
        self.limit = Limit(match.group('limit'))
        self.ident = match.group('ident')
        self.tournament_ident = match.group('tournament_ident')
        self.tournament_level = match.group('tournament_level')
        self.currency = Currency(match.group('currency'))

        self.header_parsed = True

    def _parse_table(self):
        self._table_match = self._table_re.match(self._splitted[1])
        self.table_name = self._table_match.group(1)
        self.max_players = int(self._table_match.group(2))

    def _parse_players(self):
        self.players = self._init_seats(self.max_players)
        for line in self._splitted[2:]:
            match = self._seat_re.match(line)
            # we reached the end of the players section
            if not match:
                break
            index = int(match.group('seat')) - 1
            self.players[index] = _Player(
                name=match.group('name'),
                stack=int(match.group('stack')),
                seat=int(match.group('seat')),
                combo=None
            )

    def _parse_button(self):
        button_seat = int(self._table_match.group('button'))
        self.button = self.players[button_seat - 1]

    def _parse_hero(self):
        hole_cards_line = self._splitted[self._sections[0] + 2]
        match = self._hero_re.match(hole_cards_line)
        hero, hero_index = self._get_hero_from_players(match.group('hero_name'))
        hero = hero._replace(combo=Combo(match.group(2) + match.group(3)))
        self.hero = self.players[hero_index] = hero
        if self.button.name == self.hero.name:
            self.button = hero

    def _parse_preflop(self):
        start = self._sections[0] + 3
        stop = self._sections[1]
        self.preflop_actions = tuple(self._splitted[start:stop])

    def _parse_flop(self):
        try:
            start = self._splitted.index('FLOP') + 1
        except ValueError:
            self.flop = None
            return
        stop = self._splitted.index('', start)
        floplines = self._splitted[start:stop]
        self.flop = _Flop(floplines)

    def _parse_street(self, street):
        try:
            start = self._splitted.index(street.upper()) + 2
            stop = self._splitted.index('', start)
            street_actions = self._splitted[start:stop]
            setattr(self, "{}_actions".format(street.lower()),
                    tuple(street_actions) if street_actions else None)
        except ValueError:
            setattr(self, street, None)
            setattr(self, '{}_actions'.format(street.lower()), None)

    def _parse_showdown(self):
        self.show_down = 'SHOW DOWN' in self._splitted

    def _parse_pot(self):
        potline = self._splitted[self._sections[-1] + 2]
        match = self._pot_re.match(potline)
        self.total_pot = int(match.group(1))

    def _parse_board(self):
        boardline = self._splitted[self._sections[-1] + 3]
        if not boardline.startswith('Board'):
            return
        cards = self._board_re.findall(boardline)
        self.turn = Card(cards[3]) if len(cards) > 3 else None
        self.river = Card(cards[4]) if len(cards) > 4 else None

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

    def _parse_extra(self):
        pass
