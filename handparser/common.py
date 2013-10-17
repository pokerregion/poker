from abc import ABCMeta, abstractmethod
from collections import MutableMapping
from inspect import ismethod
import pytz


ET = pytz.timezone('US/Eastern')
UTC = pytz.UTC
POKER_ROOMS = {'PokerStars': 'STARS', 'Full Tilt Poker': 'FTP'}
TYPES = {'Tournament': 'TOUR'}
GAMES = {"Hold'em": 'HOLDEM'}
LIMITS = {'No Limit': 'NL', 'NL': 'NL'}


class PokerHand(MutableMapping):
    """Abstract base class for parsers.

    The attributes can be iterated
    The class can read like a dictionary.
    Every attribute default value is None.

    Public attributes:
        poker_room          -- room ID (4 byte max) ex. STARS, FTP
        ident               -- hand id
        game_type           -- TOUR for tournaments or SNG for Sit&Go-s
        tournament_ident    -- tournament id
        tournament_level
        currency            -- 3 letter iso code USD, HUF, EUR, etc.
        buyin               -- buyin without rake
        rake
        game                -- game type: HOLDEM, OMAHA, STUD, RAZZ, etc.
        limit               -- NL, PL or FL
        sb                  -- amount of small blind
        bb                  -- amount of big blind
        date                -- hand date in UTC

        table_name      -- name of the table. it's 'tournament number[ ]table number'
        max_player      -- maximum players can sit on the table, 2, 4, 6, 7, 8, 9
        button_seat     -- seat of button player, starting from 1
        button          -- player name on the button
        hero            -- name of hero
        hero_seat (int) -- seat of hero, starting from 1
        players         -- OrderedDict of tuples in form (playername, starting_stack)
                           the sequence is the seating order at the table at the start of the hand
        hero_hole_cards -- tuple of two cards, ex. ('Ah', 'As')
        flop            -- tuple of flop cards, ex. ('Ah', '2s', '2h')
        turn            -- str of turn card, ex. 'Ah'
        river           -- str of river card, ex. '2d'
        board           -- tuple of board cards, ex. ('4s', 4d', '4c', '5h')
        preflop actions -- tuple of action lines in str
        flop_actions    -- tuple of flop action lines
        turn_actions
        river_actions
        total_pot       -- total pot after end of actions
        show_down       -- There was showd_down or wasn't (bool)
        winners         -- tuple of winner names, even when there is only one winner. ex. ('W2lkm2n')
    """
    __metaclass__ = ABCMeta

    _non_hand_attributes = ('raw', 'parsed', 'header_parsed', 'date_format')

    @abstractmethod
    def __init__(self, hand_text, parse=True):
        """Save raw hand history.

        Parameters:
            hand_text   -- str of poker hand
            parse       -- if False, hand will not parsed immediately.
                           Useful if you just want to quickly check header first.
        """
        self.raw = hand_text.strip()
        self.header_parsed = False
        self.parsed = False

    def __len__(self):
        return len(self.keys())

    def __getitem__(self, key):
        if key not in self._non_hand_attributes:
            return getattr(self, key)
        else:
            raise KeyError('You can only get it via the attribute like "hand.%s"' % key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __delitem__(self, key):
        delattr(self, key)

    def __iter__(self):
        return iter(self.keys())

    def __unicode__(self):
        return "<%s: %s hand #%s>" % (self.__class__.__name__, self.poker_room, self.ident)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def keys(self):
        return [attr for attr in dir(self) if not attr.startswith('_') and
                                              attr not in self._non_hand_attributes and
                                              not ismethod(getattr(self, attr))]

    @abstractmethod
    def parse_header(self):
        """Parses the first line of a hand history."""
        pass

    @abstractmethod
    def parse(self):
        """Parse the body of the hand history, but first parse header if not yet parsed."""
        if not self.header_parsed:
            self.parse_header()

