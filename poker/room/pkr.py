import re
from decimal import Decimal
from collections import OrderedDict
import pytz
from ..handhistory import HandHistory, normalize, HandHistoryPlayer
from ..hand import Combo, Card


__all__ = ['PKRHandHistory']


class PKRHandHistory(HandHistory):
    """Parses PKR hand histories."""

    poker_room = 'PKR'
    date_format = '%d %b %Y %H:%M:%S'
    currency = 'USD'
    _TZ = pytz.UTC

    _split_re = re.compile(r"Dealing |\nDealing Cards\n|Taking |Moving |\n")
    _blinds_re = re.compile(r"^Blinds are now \$([\d.]*) / \$([\d.]*)$")
    _dealt_re = re.compile(r"^\[(. .)\]\[(. .)\] to (.*)$")
    _seat_re = re.compile(r"^Seat (\d\d?): (.*) - \$([\d.]*) ?(.*)$")
    _sizes_re = re.compile(r"^Pot sizes: \$([\d.]*)$")
    _card_re = re.compile(r"\[(. .)\]")
    _rake_re = re.compile(r"Rake of \$([\d.]*) from pot \d$")
    _win_re = re.compile(r"^(.*) wins \$([\d.]*) with: ")
    SPLIT_CARD_SPACE = slice(0, 3, 2)

    def __init__(self, hand_text, parse=True):
        """Split hand history by sections and parse."""
        super(PKRHandHistory, self).__init__(hand_text, parse)

        self._splitted = self._split_re.split(self.raw)

        # search split locations (basically empty strings)
        # sections[1] is after blinds, before preflop
        # section[2] is before flop
        # sections[-1] is before showdown
        self._sections = [ind for ind, elem in enumerate(self._splitted) if not elem]

        if parse:
            self.parse()

    def parse_header(self):
        self.table_name = self._splitted[0][6:]          # cut off "Table "
        self.ident = self._splitted[1][15:]              # cut off "Starting Hand #"
        self._parse_date(self._splitted[2][20:])         # cut off "Start time of hand: "
        self.last_ident = self._splitted[3][11:]         # cut off "Last Hand #"
        self.game = normalize(self._splitted[4][11:])        # cut off "Game Type: "
        self.limit = normalize(self._splitted[5][12:])      # cut off "Limit Type: "
        self.game_type = normalize(self._splitted[6][12:])   # cut off "Table Type: "
        self.money_type = normalize(self._splitted[7][12:])  # cut off "Money Type: "

        match = self._blinds_re.match(self._splitted[8])
        self.sb = Decimal(match.group(1))
        self.bb = Decimal(match.group(2))
        self.buyin = self.bb * 100

        self.button = int(self._splitted[9][18:])  # cut off "Button is at seat "

        self.tournament_ident = None
        self.tournament_name = None
        self.tournament_level = None

    def parse(self):
        super(PKRHandHistory, self).parse()

        self._parse_seats()
        self._parse_hero()
        self._parse_preflop()
        self._parse_street('flop')
        self._parse_street('turn')
        self._parse_street('river')
        self._parse_showdown()

    def _parse_seats(self):
        # In hh there is no indication of max_players,
        # so init for 10, as there are 10 player tables on PKR.
        players = self._init_seats(10)
        for line in self._splitted[10:]:
            match = self._seat_re.match(line)
            if not match:
                break
            seat_number = int(match.group(1))
            players[seat_number - 1] = HandHistoryPlayer(
                name=match.group(2), stack=Decimal(match.group(3)), seat=seat_number, combo=None
            )
        self.max_players = seat_number
        self.players = players[:self.max_players]

        button_row = self._splitted[self._sections[0] + 1]

        # cut last two because there can be 10 seats also
        # in case of one digit, the first char will be a space
        # but int() can convert it without hiccups :)
        button_seat = int(button_row[-2:])
        self.button = players[button_seat - 1]

    def _parse_hero(self):
        dealt_row = self._splitted[self._sections[1] + 1]
        match = self._dealt_re.match(dealt_row)

        first = match.group(1)[self.SPLIT_CARD_SPACE]
        second = match.group(2)[self.SPLIT_CARD_SPACE]
        hero_name = match.group(3)
        player_names = [p.name for p in self.players]
        hero_index = player_names.index(hero_name)
        hero = self.players[hero_index]
        self.hero = self.players[hero_index] = hero._replace(combo=Combo(first + second))
        if self.button.name == self.hero.name:
            self.button = self.hero

    def _parse_preflop(self):
        start = self._sections[1] + 2
        stop = self._splitted.index('', start + 1) - 1
        self.preflop_actions = tuple(self._splitted[start:stop])

    def _parse_street(self, street):
        street_sections = {'flop': 2, 'turn': 3, 'river': 4}
        section = street_sections[street]
        try:
            start = self._sections[section] + 1

            street_line = self._splitted[start]
            cards = list(map(lambda x: x[self.SPLIT_CARD_SPACE], self._card_re.findall(street_line)))
            setattr(self, street, tuple(map(Card, cards)) if street == 'flop' else Card(cards[0]))

            stop = next(v for v in self._sections if v > start) - 1
            setattr(self, "%s_actions" % street, tuple(self._splitted[start + 1:stop]))

            sizes_line = self._splitted[start - 2]
            pot = Decimal(self._sizes_re.match(sizes_line).group(1))
            setattr(self, "%s_pot" % street, pot)
        except IndexError:
            setattr(self, street, None)
            setattr(self, "%s_actions" % street, None)
            setattr(self, "%s_pot" % street, None)

    def _parse_showdown(self):
        start = self._sections[-1] + 1

        rake_line = self._splitted[start]
        match = self._rake_re.match(rake_line)
        self.rake = Decimal(match.group(1))

        winners = []
        total_pot = self.rake
        for line in self._splitted[start:]:
            if 'shows' in line:
                self.show_down = True
            elif 'wins' in line:
                match = self._win_re.match(line)
                winners.append(match.group(1))
                total_pot += Decimal(match.group(2))

        self.winners = tuple(winners)
        self.total_pot = total_pot
