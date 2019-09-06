import re
from decimal import Decimal
from datetime import datetime
import attr
from lxml import etree
import pytz
from pathlib import Path
from zope.interface import implementer
from .. import handhistory as hh
from ..card import Card
from ..hand import Combo
from ..constants import Limit, Game, GameType, Currency, Action, MoneyType


__all__ = ["PokerStarsHandHistory", "Notes"]


@implementer(hh.IStreet)
class _Street(hh._BaseStreet):
    def _parse_cards(self, boardline):
        self.cards = (Card(boardline[1:3]), Card(boardline[4:6]), Card(boardline[7:9]))

    def _parse_actions(self, actionlines):
        actions = []
        for line in actionlines:
            if line.startswith("Uncalled bet"):
                action = self._parse_uncalled(line)
            elif "collected" in line:
                action = self._parse_collected(line)
            elif "doesn't show hand" in line:
                action = self._parse_muck(line)
            elif ' said, "' in line:  # skip chat lines
                continue
            elif ":" in line:
                action = self._parse_player_action(line)
            else:
                raise RuntimeError("bad action line: " + line)

            actions.append(hh._PlayerAction(*action))
        self.actions = tuple(actions) if actions else None

    def _parse_uncalled(self, line):
        first_paren_index = line.find("(")
        second_paren_index = line.find(")")
        amount = line[first_paren_index + 1 : second_paren_index]
        name_start_index = line.find("to ") + 3
        name = line[name_start_index:]
        return name, Action.RETURN, Decimal(amount)

    def _parse_collected(self, line):
        first_space_index = line.find(" ")
        name = line[:first_space_index]
        second_space_index = line.find(" ", first_space_index + 1)
        third_space_index = line.find(" ", second_space_index + 1)
        amount = line[second_space_index + 1 : third_space_index]
        self.pot = Decimal(amount)
        return name, Action.WIN, self.pot

    def _parse_muck(self, line):
        colon_index = line.find(":")
        name = line[:colon_index]
        return name, Action.MUCK, None

    def _parse_player_action(self, line):
        name, _, action = line.partition(": ")
        action, _, amount = action.partition(" ")
        amount, _, _ = amount.partition(" ")

        if amount:
            return name, Action(action), Decimal(amount)
        else:
            return name, Action(action), None


@implementer(hh.IHandHistory)
class PokerStarsHandHistory(hh._SplittableHandHistoryMixin, hh._BaseHandHistory):
    """Parses PokerStars Tournament hands."""

    _DATE_FORMAT = "%Y/%m/%d %H:%M:%S ET"
    _TZ = pytz.timezone("US/Eastern")  # ET
    _split_re = re.compile(r" ?\*\*\* ?\n?|\n")
    _header_re = re.compile(
        r"""
                        ^PokerStars\s+                                # Poker Room
                        Hand\s+\#(?P<ident>\d+):\s+                   # Hand history id
                        (Tournament\s+\#(?P<tournament_ident>\d+),\s+ # Tournament Number
                         ((?P<freeroll>Freeroll)|(                    # buyin is Freeroll
                          \$?(?P<buyin>\d+(\.\d+)?)                   # or buyin
                          (\+\$?(?P<rake>\d+(\.\d+)?))?               # and rake
                          (\s+(?P<currency>[A-Z]+))?                  # and currency
                         ))\s+
                        )?
                        (?P<game>.+?)\s+                              # game
                        (?P<limit>(?:Pot\s+|No\s+|)Limit)\s+          # limit
                        (-\s+Level\s+(?P<tournament_level>\S+)\s+)?   # Level (optional)
                        \(
                         (((?P<sb>\d+)/(?P<bb>\d+))|(                 # tournament blinds
                          \$(?P<cash_sb>\d+(\.\d+)?)/                 # cash small blind
                          \$(?P<cash_bb>\d+(\.\d+)?)                  # cash big blind
                          (\s+(?P<cash_currency>\S+))?                # cash currency
                         ))
                        \)\s+
                        -\s+.+?\s+                                    # localized date
                        \[(?P<date>.+?)\]                             # ET date
                        """,
        re.VERBOSE,
    )
    _table_re = re.compile(
        r"^Table '(.*)' (\d+)-max Seat #(?P<button>\d+) is the button"
    )
    _seat_re = re.compile(
        r"^Seat (?P<seat>\d+): (?P<name>.+?) \(\$?(?P<stack>\d+(\.\d+)?) in chips\)"
    )  # noqa
    _hero_re = re.compile(r"^Dealt to (?P<hero_name>.+?) \[(..) (..)\]")
    _pot_re = re.compile(r"^Total pot (\d+(?:\.\d+)?) .*\| Rake (\d+(?:\.\d+)?)")
    _winner_re = re.compile(r"^Seat (\d+): (.+?) collected \((\d+(?:\.\d+)?)\)")
    _showdown_re = re.compile(r"^Seat (\d+): (.+?) showed \[.+?\] and won")
    _ante_re = re.compile(r".*posts the ante (\d+(?:\.\d+)?)")
    _board_re = re.compile(r"(?<=[\[ ])(..)(?=[\] ])")

    def parse_header(self):
        # sections[0] is before HOLE CARDS
        # sections[-1] is before SUMMARY
        self._split_raw()

        match = self._header_re.match(self._splitted[0])

        self.extra = dict()
        self.ident = match.group("ident")

        # We cannot use the knowledege of the game type to pick between the blind
        # and cash blind captures because a cash game play money blind looks exactly
        # like a tournament blind

        self.sb = Decimal(match.group("sb") or match.group("cash_sb"))
        self.bb = Decimal(match.group("bb") or match.group("cash_bb"))

        if match.group("tournament_ident"):
            self.game_type = GameType.TOUR
            self.tournament_ident = match.group("tournament_ident")
            self.tournament_level = match.group("tournament_level")

            currency = match.group("currency")
            self.buyin = Decimal(match.group("buyin") or 0)
            self.rake = Decimal(match.group("rake") or 0)
        else:
            self.game_type = GameType.CASH
            self.tournament_ident = None
            self.tournament_level = None
            currency = match.group("cash_currency")
            self.buyin = None
            self.rake = None

        if match.group("freeroll") and not currency:
            currency = "USD"

        if not currency:
            self.extra["money_type"] = MoneyType.PLAY
            self.currency = None
        else:
            self.extra["money_type"] = MoneyType.REAL
            self.currency = Currency(currency)

        self.game = Game(match.group("game"))
        self.limit = Limit(match.group("limit"))

        self._parse_date(match.group("date"))

        self.header_parsed = True

    def parse(self):
        """Parses the body of the hand history, but first parse header if not yet parsed."""
        if not self.header_parsed:
            self.parse_header()

        self._parse_table()
        self._parse_players()
        self._parse_button()
        self._parse_hero()
        self._parse_preflop()
        self._parse_flop()
        self._parse_street("turn")
        self._parse_street("river")
        self._parse_showdown()
        self._parse_pot()
        self._parse_board()
        self._parse_winners()

        self._del_split_vars()
        self.parsed = True

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
            index = int(match.group("seat")) - 1
            self.players[index] = hh._Player(
                name=match.group("name"),
                stack=int(match.group("stack")),
                seat=int(match.group("seat")),
                combo=None,
            )

    def _parse_button(self):
        button_seat = int(self._table_match.group("button"))
        self.button = self.players[button_seat - 1]

    def _parse_hero(self):
        hole_cards_line = self._splitted[self._sections[0] + 2]
        match = self._hero_re.match(hole_cards_line)
        hero, hero_index = self._get_hero_from_players(match.group("hero_name"))
        hero.combo = Combo(match.group(2) + match.group(3))
        self.hero = self.players[hero_index] = hero
        if self.button.name == self.hero.name:
            self.button = hero

    def _parse_preflop(self):
        start = self._sections[0] + 3
        stop = self._sections[1]
        self.preflop_actions = tuple(self._splitted[start:stop])

    def _parse_flop(self):
        try:
            start = self._splitted.index("FLOP") + 1
        except ValueError:
            self.flop = None
            return
        stop = self._splitted.index("", start)
        floplines = self._splitted[start:stop]
        self.flop = _Street(floplines)

    def _parse_street(self, street):
        try:
            start = self._splitted.index(street.upper()) + 2
            stop = self._splitted.index("", start)
            street_actions = self._splitted[start:stop]
            setattr(
                self,
                f"{street.lower()}_actions",
                tuple(street_actions) if street_actions else None,
            )
        except ValueError:
            setattr(self, street, None)
            setattr(self, f"{street.lower()}_actions", None)

    def _parse_showdown(self):
        self.show_down = "SHOW DOWN" in self._splitted

    def _parse_pot(self):
        potline = self._splitted[self._sections[-1] + 2]
        match = self._pot_re.match(potline)
        self.total_pot = int(match.group(1))

    def _parse_board(self):
        boardline = self._splitted[self._sections[-1] + 3]
        if not boardline.startswith("Board"):
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


@attr.s(slots=True)
class _Label:
    """Labels in Player notes."""

    id = attr.ib()
    color = attr.ib()
    name = attr.ib()


@attr.s(slots=True)
class _Note:
    """Player note."""

    player = attr.ib()
    label = attr.ib()
    update = attr.ib()
    text = attr.ib()


class NoteNotFoundError(ValueError):
    """Note not found for player."""


class LabelNotFoundError(ValueError):
    """Label not found in the player notes."""


class Notes:
    """Class for parsing pokerstars XML notes."""

    _color_re = re.compile("^[0-9A-F]{6}$")

    def __init__(self, notes: str):
        self.raw = notes
        parser = etree.XMLParser(recover=True, resolve_entities=False)
        self.root = etree.XML(notes.encode(), parser)

    def __str__(self):
        return etree.tostring(
            self.root, xml_declaration=True, encoding="UTF-8", pretty_print=True
        ).decode()

    @classmethod
    def from_file(cls, filename):
        """Make an instance from a XML file."""
        return cls(Path(filename).open().read())

    @property
    def players(self):
        """Tuple of player names."""
        return tuple(note.get("player") for note in self.root.iter("note"))

    @property
    def label_names(self):
        """Tuple of label names."""
        return tuple(label.text for label in self.root.iter("label"))

    @property
    def notes(self):
        """Tuple of notes.."""
        return tuple(self._get_note_data(note) for note in self.root.iter("note"))

    @property
    def labels(self):
        """Tuple of labels."""
        return tuple(
            _Label(label.get("id"), label.get("color"), label.text)
            for label in self.root.iter("label")
        )

    def get_note_text(self, player):
        """Return note text for the player."""
        note = self._find_note(player)
        return note.text

    def get_note(self, player):
        """Return :class:`_Note` tuple for the player."""
        return self._get_note_data(self._find_note(player))

    def add_note(self, player, text, label=None, update=None):
        """Add a note to the xml. If update param is None, it will be the current time."""
        if label is not None and (label not in self.label_names):
            raise LabelNotFoundError(f"Invalid label: {label}")
        if update is None:
            update = datetime.utcnow()
        # converted to timestamp, rounded to ones
        update = update.strftime("%s")
        label_id = self._get_label_id(label)
        new_note = etree.Element("note", player=player, label=label_id, update=update)
        new_note.text = text
        self.root.append(new_note)

    def append_note(self, player, text):
        """Append text to an already existing note."""
        note = self._find_note(player)
        note.text += text

    def prepend_note(self, player, text):
        """Prepend text to an already existing note."""
        note = self._find_note(player)
        note.text = text + note.text

    def replace_note(self, player, text):
        """Replace note text with text. (Overwrites previous note!)"""
        note = self._find_note(player)
        note.text = text

    def change_note_label(self, player, label):
        label_id = self._get_label_id(label)
        note = self._find_note(player)
        note.attrib["label"] = label_id

    def del_note(self, player):
        """Delete a note by player name."""
        self.root.remove(self._find_note(player))

    def _find_note(self, player):
        # if player name contains a double quote, the search phrase would be invalid.
        # &quot; entitiy is searched with ", e.g. &quot;bootei&quot; is searched with '"bootei"'
        quote = "'" if '"' in player else '"'
        note = self.root.find(f"note[@player={quote}{player}{quote}]")
        if note is None:
            raise NoteNotFoundError(player)
        return note

    def _get_note_data(self, note):
        labels = {label.get("id"): label.text for label in self.root.iter("label")}
        label = note.get("label")
        label = labels[label] if label != "-1" else None
        timestamp = note.get("update")
        if timestamp:
            timestamp = int(timestamp)
            update = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.UTC)
        else:
            update = None
        return _Note(note.get("player"), label, update, note.text)

    def get_label(self, name):
        """Find the label by name."""
        label_tag = self._find_label(name)
        return _Label(label_tag.get("id"), label_tag.get("color"), label_tag.text)

    def add_label(self, name, color):
        """Add a new label. It's id will automatically be calculated."""
        color_upper = color.upper()
        if not self._color_re.match(color_upper):
            raise ValueError(f"Invalid color: {color}")

        labels_tag = self.root[0]
        last_id = int(labels_tag[-1].get("id"))
        new_id = str(last_id + 1)

        new_label = etree.Element("label", id=new_id, color=color_upper)
        new_label.text = name

        labels_tag.append(new_label)

    def del_label(self, name):
        """Delete a label by name."""
        labels_tag = self.root[0]
        labels_tag.remove(self._find_label(name))

    def _find_label(self, name):
        labels_tag = self.root[0]
        try:
            return labels_tag.xpath('label[text()="%s"]' % name)[0]
        except IndexError:
            raise LabelNotFoundError(name)

    def _get_label_id(self, name):
        return self._find_label(name).get("id") if name else "-1"

    def save(self, filename):
        """Save the note XML to a file."""
        with open(filename, "w") as fp:
            fp.write(str(self))
