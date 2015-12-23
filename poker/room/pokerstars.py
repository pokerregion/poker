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
from ..constants import Limit, Game, GameType, Currency, Action


__all__ = ['PokerStarsHandHistory', 'Notes']


class _Street(object):
    def _parse_actions(self, actionlines):
        actions = []
        for line in actionlines:
            if line.startswith('Uncalled bet'):
                action = self._parse_uncalled(line)
            elif 'collected' in line:
                action = self._parse_collected(line)
            elif "doesn't show hand" in line:
                action = self._parse_muck(line)
            elif ':' in line:
                action = self._parse_player_action(line)
            else:
                raise hh.StreetError(line)
            actions.append(hh._PlayerAction(*action))
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

    def _parse_muck(self, line):
        colon_index = line.find(':')
        name = line[:colon_index]
        return name, Action.MUCK, None

    def _parse_player_action(self, line):
        colon_index = line.find(':')
        name = line[:colon_index]
        end_action_index = line.find(' ', colon_index + 2)
        if end_action_index == -1:  # not found
            end_action_index = None  # until the end
        action = Action(line[colon_index + 2:end_action_index])
        if end_action_index:
            end_amount_index = line.find(' ', end_action_index + 1)
            if end_amount_index == -1:
                end_amount_index = None  # until the end of the line
            # import pdb; pdb.set_trace()
            amount = line[end_action_index + 1:end_amount_index]
            return name, action, Decimal(amount)
        else:
            return name, action, None


@implementer(hh.IStreet)
class _Preflop(hh._BaseStreet, _Street):
    def _parse_board(self, boardline):
        self.cards = None


@implementer(hh.IStreet)
class _Flop(hh._BaseStreet, _Street):
    def _parse_board(self, boardline):
        self.cards = (Card(boardline[1:3]), Card(boardline[4:6]), Card(boardline[7:9]))


@implementer(hh.IStreet)
class _Turn(hh._BaseStreet, _Street):
    def _parse_board(self, boardline):
        self.cards = (Card(boardline[-3:-1]),)


@implementer(hh.IStreet)
class _River(hh._BaseStreet, _Street):
    def _parse_board(self, boardline):
        self.cards = (Card(boardline[-3:-1]),)


@implementer(hh.IHandHistory)
class PokerStarsHandHistory(hh._SplittableHandHistoryMixin, hh._FullTiltPokerStarsMixin,
                            hh._BaseHandHistory):
    """Parses PokerStars Tournament hands."""

    _date_format = '%Y/%m/%d %H:%M:%S ET'
    _tz = pytz.timezone('US/Eastern')  # ET
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
    _pot_re = re.compile(r"^Total pot (\d*) .*\| Rake (\d*)$")
    _winner_re = re.compile(r"^Seat (\d): (?P<name>.*) collected \((\d*)\)$")
    _ante_re = re.compile(r".*posts the ante (\d*)")
    _board_re = re.compile(r"(?<=[\[ ])(..)(?=[\] ])")

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
        self.game_type = GameType(header_match.group('game_type'))
        self.tournament_ident = header_match.group('tournament_ident')
        self.tournament_level = header_match.group('tournament_level')
        self.buyin = Decimal(header_match.group('buyin'))
        self.rake = Decimal(header_match.group('rake'))
        self.currency = Currency(header_match.group('currency'))

        self._header_parsed = True

    def _parse_seats(self):
        table_match = self._table_re.match(self._splitted[1])
        self.table_name = table_match.group(1)
        self.max_players = int(table_match.group(2))
        self.players, __, hero_index = self._get_players(init_seats=self.max_players,
                                                         start_line_index=2)
        button_seat = int(table_match.group('button'))
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


_Label = namedtuple('_Label', 'id, color, name')
"""Named tuple for labels in Player notes."""

_Note = namedtuple('_Note', 'player, label, update, text')
"""Named tuple for player notes."""


class NoteNotFoundError(ValueError):
    """Note not found for player."""


class LabelNotFoundError(ValueError):
    """Label not found in the player notes."""


class Notes(object):
    """Class for parsing pokerstars XML notes."""

    _color_re = re.compile('^[0-9A-F]{6}$')

    def __init__(self, notes):
        # notes need to be a unicode object
        self.raw = notes
        parser = etree.XMLParser(recover=True, resolve_entities=False)
        self.root = etree.XML(notes.encode('utf-8'), parser)

    def __unicode__(self):
        return str(self).decode('utf-8')

    def __str__(self):
        return etree.tostring(self.root, xml_declaration=True, encoding='UTF-8', pretty_print=True)

    @classmethod
    def from_file(cls, filename):
        """Make an instance from a XML file."""
        return cls(Path(filename).open().read())

    @property
    def players(self):
        """Tuple of player names."""
        return tuple(note.get('player') for note in self.root.iter('note'))

    @property
    def label_names(self):
        """Tuple of label names."""
        return tuple(label.text for label in self.root.iter('label'))

    @property
    def notes(self):
        """Tuple of notes wrapped in namedtuples."""
        return tuple(self._get_note_data(note) for note in self.root.iter('note'))

    @property
    def labels(self):
        """Tuple of labels."""
        return tuple(_Label(label.get('id'), label.get('color'), label.text) for label
                     in self.root.iter('label'))

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
            raise LabelNotFoundError('Invalid label: {}'.format(label))
        if update is None:
            update = datetime.utcnow()
        # converted to timestamp, rounded to ones
        update = update.strftime('%s')
        label_id = self._get_label_id(label)
        new_note = etree.Element('note', player=player, label=label_id, update=update)
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
        note.attrib['label'] = label_id

    def del_note(self, player):
        """Delete a note by player name."""
        self.root.remove(self._find_note(player))

    def _find_note(self, player):
        # if player name contains a double quote, the search phrase would be invalid.
        # &quot; entitiy is searched with ", e.g. &quot;bootei&quot; is searched with '"bootei"'
        quote = "'" if '"' in player else '"'
        note = self.root.find('note[@player={0}{1}{0}]'.format(quote, player))
        if note is None:
            raise NoteNotFoundError(player)
        return note

    def _get_note_data(self, note):
        labels = {label.get('id'): label.text for label in self.root.iter('label')}
        label = note.get('label')
        label = labels[label] if label != "-1" else None
        timestamp = note.get('update')
        if timestamp:
            timestamp = int(timestamp)
            update = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.UTC)
        else:
            update = None
        return _Note(note.get('player'), label, update, note.text)

    def get_label(self, name):
        """Find the label by name."""
        label_tag = self._find_label(name)
        return _Label(label_tag.get('id'), label_tag.get('color'), label_tag.text)

    def add_label(self, name, color):
        """Add a new label. It's id will automatically be calculated."""
        color_upper = color.upper()
        if not self._color_re.match(color_upper):
            raise ValueError('Invalid color: {}'.format(color))

        labels_tag = self.root[0]
        last_id = int(labels_tag[-1].get('id'))
        new_id = str(last_id + 1)

        new_label = etree.Element('label', id=new_id, color=color_upper)
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
        return self._find_label(name).get('id') if name else '-1'

    def save(self, filename):
        """Save the note XML to a file."""
        with open(filename, 'w') as fp:
            fp.write(str(self))
