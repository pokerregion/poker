import unittest
import pytz
from decimal import Decimal
from datetime import datetime
from collections import OrderedDict
from handparser import PokerStarsHand


ET = pytz.timezone('US/Eastern')

HAND1 = {'file': """PokerStars Hand #105024000105: Tournament #797469411, $3.19+$0.31 USD Hold'em No Limit - Level I (10/20) - 2013/10/04 19:53:27 CET [2013/10/04 13:53:27 ET]
Table '797469411 15' 9-max Seat #1 is the button
Seat 1: flettl2 (1500 in chips)
Seat 2: santy312 (3000 in chips)
Seat 3: flavio766 (3000 in chips)
Seat 4: strongi82 (3000 in chips)
Seat 5: W2lkm2n (3000 in chips)
Seat 6: MISTRPerfect (3000 in chips)
Seat 7: blak_douglas (3000 in chips)
Seat 8: sinus91 (1500 in chips)
Seat 9: STBIJUJA (1500 in chips)
santy312: posts small blind 10
flavio766: posts big blind 20
*** HOLE CARDS ***
Dealt to W2lkm2n [Ac Jh]
strongi82: folds
W2lkm2n: raises 40 to 60
MISTRPerfect: calls 60
blak_douglas: folds
sinus91: folds
STBIJUJA: folds
flettl2: folds
santy312: folds
flavio766: folds
*** FLOP *** [2s 6d 6h]
W2lkm2n: bets 80
MISTRPerfect: folds
Uncalled bet (80) returned to W2lkm2n
W2lkm2n collected 150 from pot
W2lkm2n: doesn't show hand
*** SUMMARY ***
Total pot 150 | Rake 0
Board [2s 6d 6h]
Seat 1: flettl2 (button) folded before Flop (didn't bet)
Seat 2: santy312 (small blind) folded before Flop
Seat 3: flavio766 (big blind) folded before Flop
Seat 4: strongi82 folded before Flop (didn't bet)
Seat 5: W2lkm2n collected (150)
Seat 6: MISTRPerfect folded on the Flop
Seat 7: blak_douglas folded before Flop (didn't bet)
Seat 8: sinus91 folded before Flop (didn't bet)
Seat 9: STBIJUJA folded before Flop (didn't bet)""",
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

HAND2 = {'file': """PokerStars Hand #105034215446: Tournament #797536898, $3.19+$0.31 USD Hold'em No Limit - Level XI (400/800) - 2013/10/04 23:22:20 CET [2013/10/04 17:22:20 ET]
Table '797536898 9' 9-max Seat #2 is the button
Seat 1: RichFatWhale (12910 in chips)
Seat 2: W2lkm2n (11815 in chips)
Seat 3: Labahra (7395 in chips)
Seat 4: Lean Abadia (7765 in chips)
Seat 5: lkenny44 (10080 in chips)
Seat 6: Newfie_187 (1030 in chips)
Seat 7: Hokolix (13175 in chips)
Seat 8: pmmr (2415 in chips)
Seat 9: costamar (13070 in chips)
RichFatWhale: posts the ante 75
W2lkm2n: posts the ante 75
Labahra: posts the ante 75
Lean Abadia: posts the ante 75
lkenny44: posts the ante 75
Newfie_187: posts the ante 75
Hokolix: posts the ante 75
pmmr: posts the ante 75
costamar: posts the ante 75
Labahra: posts small blind 400
Lean Abadia: posts big blind 800
*** HOLE CARDS ***
Dealt to W2lkm2n [Jd Js]
lkenny44: folds
Newfie_187: raises 155 to 955 and is all-in
Hokolix: folds
pmmr: folds
costamar: raises 12040 to 12995 and is all-in
RichFatWhale: folds
W2lkm2n: calls 11740 and is all-in
Labahra: folds
Lean Abadia: folds
Uncalled bet (1255) returned to costamar
*** FLOP *** [3c 6s 9d]
*** TURN *** [3c 6s 9d] [8d]
*** RIVER *** [3c 6s 9d 8d] [Ks]
*** SHOW DOWN ***
costamar: shows [Kd Ac] (a pair of Kings)
W2lkm2n: shows [Jd Js] (a pair of Jacks)
costamar collected 21570 from side pot
Newfie_187: shows [9c Qd] (a pair of Nines)
costamar collected 4740 from main pot
W2lkm2n finished the tournament in 80th place
Newfie_187 finished the tournament in 81st place
*** SUMMARY ***
Total pot 26310 Main pot 4740. Side pot 21570. | Rake 0
Board [3c 6s 9d 8d Ks]
Seat 1: RichFatWhale folded before Flop (didn't bet)
Seat 2: W2lkm2n (button) showed [Jd Js] and lost with a pair of Jacks
Seat 3: Labahra (small blind) folded before Flop
Seat 4: Lean Abadia (big blind) folded before Flop
Seat 5: lkenny44 folded before Flop (didn't bet)
Seat 6: Newfie_187 showed [9c Qd] and lost with a pair of Nines
Seat 7: Hokolix folded before Flop (didn't bet)
Seat 8: pmmr folded before Flop (didn't bet)
Seat 9: costamar showed [Kd Ac] and won (26310) with a pair of Kings""",
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


class TestParseHand1(unittest.TestCase):
    def test_header(self):
        self.assertTrue(hand.header_parsed)
        self.assertFalse(hand.parsed)


def create_test_function(hand, attribute, result):
    def test_function(self):
        self.assertEqual(getattr(hand, attribute), result)
    return test_function


for attr, result in HAND1['header_results'].items():
    hand = PokerStarsHand(HAND1['file'], parse=False)
    hand.parse_header()
    test_function = create_test_function(hand, attr, result)
    test_function.__name__ = 'test_%s' % attr
    setattr(TestParseHand1, test_function.__name__, test_function)
