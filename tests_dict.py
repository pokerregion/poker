from unittest import TestCase
import pytz
from decimal import Decimal
from datetime import datetime
from collections import OrderedDict
from handparser import PokerStarsHand


ET = pytz.timezone('US/Eastern')

HAND1 = {'file': file('hand1.txt').read(),
         'header_results':
             {'room': 'STARS',
              'number': '105024000105',
              'type': 'TOUR',
              'tour_number': '797469411',
              'tour_level': 'I',
              'currency': 'USD',
              'buyin': Decimal('3.19'),
              'rake': Decimal('0.31'),
              'game': 'HOLDEM',
              'limit': 'NL',
              'sb': Decimal(10),
              'bb': Decimal(20),
              'date': ET.localize(datetime(2013, 10, 4, 13, 53, 27))
             },
         'body_results':
             {'table_name': '797469411 15',
              'max_players': 9,
              'button_seat': 1,
              'button': 'flettl2',
              'hero': 'W2lkm2n',
              'hero_seat': 5,
              'players': OrderedDict([('flettl2', 1500), ('santy312', 3000), ('flavio766', 3000),
                                      ('strongi82', 3000), ('W2lkm2n', 3000), ('MISTRPerfect', 3000),
                                      ('blak_douglas', 3000), ('sinus91', 1500), ('STBIJUJA', 1500)]),
              'hero_hole_cards': ('Ac', 'Jh'),
              'flop': ('2s', '6d', '6h'),
              'turn': None,
              'river': None,
              'board': ('2s', '6d', '6h'),
              'preflop_actions': ("strongi82: folds",
                                  "W2lkm2n: raises 40 to 60",
                                  "MISTRPerfect: calls 60",
                                  "blak_douglas: folds",
                                  "sinus91: folds",
                                  "STBIJUJA: folds",
                                  "flettl2: folds",
                                  "santy312: folds",
                                  "flavio766: folds"),
              'flop_actions': ('W2lkm2n: bets 80', 'MISTRPerfect: folds', 'Uncalled bet (80) returned to W2lkm2n',
                               'W2lkm2n collected 150 from pot', "W2lkm2n: doesn't show hand"),
              'turn_actions': None,
              'river_actions': None,
              'total_pot': Decimal(150),
              'winners': ('W2lkm2n',),
             }
}

HAND2 = {'file': file('hand2.txt').read(),
         'header_results': {
             'room': 'STARS',
             'number': '105034215446',
             'type': 'TOUR',
             'tour_number': '797536898',
             'tour_level': 'XI',
             'currency': 'USD',
             'buyin': Decimal('3.19'),
             'rake': Decimal('0.31'),
             'game': 'HOLDEM',
             'limit': 'NL',
             'sb': Decimal(400),
             'bb': Decimal(800),
             'date': ET.localize(datetime(2013, 10, 4, 17, 22, 20)),
         },
         'body_results': {
             'table_name': '797536898 9',
             'max_players': 9,
             'button_seat': 2,
             'button': 'W2lkm2n',
             'hero': 'W2lkm2n',
             'hero_seat': 2,
             'players': OrderedDict([('RichFatWhale', 12910), ('W2lkm2n', 11815), ('Labahra', 7395),
                                     ('Lean Abadia', 7765), ('lkenny44', 10080), ('Newfie_187', 1030),
                                     ('Hokolix', 13175), ('pmmr', 2415), ('costamar', 13070)]),
             'hero_hole_cards': ('Jd', 'Js'),
             'flop': ('3c', '6s', '9d'),
             'turn': '8d',
             'river': 'Ks',
             'board': ('2s', '6d', '6h'),
             'preflop_actions': ("lkenny44: folds",
                                "Newfie_187: raises 155 to 955 and is all-in",
                                "Hokolix: folds",
                                "pmmr: folds",
                                "costamar: raises 12040 to 12995 and is all-in"
                                "RichFatWhale: folds"
                                "W2lkm2n: calls 11740 and is all-in"
                                "Labahra: folds"
                                "Lean Abadia: folds"
                                "Uncalled bet (1255) returned to costamar"),
             'flop_actions': None,
             'turn_actions': None,
             'river_actions': None,
             'total_pot': Decimal(26310),
             'winners': ('costamar',),
         }
}


class TestParseHand1(TestCase):
    def test_header(self):
        hand = PokerStarsHand(HAND1['file'], parse=False)
        hand.parse_header()

        self.assertTrue(hand.header_parsed)
        self.assertFalse(hand.parsed)

        for attr, result in HAND1['header_results'].items():
            self.assertEqual(getattr(hand, attr), result)

    def test_body(self):
        hand = PokerStarsHand(HAND1['file'])

        self.assertTrue(hand.header_parsed)
        self.assertTrue(hand.parsed)

        for attr, result in HAND1['body_results'].items():
            self.assertEqual(getattr(hand, attr), result)


class TestParseHand2(TestCase):
    def test_header(self):
        hand = PokerStarsHand(HAND2['file'], parse=False)
        hand.parse_header()

        for attr, result in HAND2['header_results'].items():
            self.assertEqual(getattr(hand, attr), result)

    def test_body(self):
        hand = PokerStarsHand(HAND2['file'])

        for attr, result in HAND2['body_results'].items():
            self.assertEqual(getattr(hand, attr), result)
