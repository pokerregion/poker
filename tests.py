from unittest import TestCase, skip
import pytz
from decimal import Decimal
from datetime import datetime
from collections import OrderedDict
from handparser import PokerStarsHand


ET = pytz.timezone('US/Eastern')
HAND1 = file('hand1.txt').read()


class TestParseHeader1(TestCase):
    def setUp(self):
        self.hand = PokerStarsHand(HAND1, parse=False)
        self.hand.parse_header()

    def tearDown(self):
        del self.hand

    def test_flag_set(self):
        self.assertTrue(self.hand.header_parsed)
        self.assertFalse(self.hand.parsed)

    def test_poker_room(self):
        self.assertEqual(self.hand.room, "STARS")

    def test_hand_number(self):
        self.assertEqual(self.hand.number, "105024000105")

    def test_tour(self):
        self.assertEqual(self.hand.type, "TOUR")
        self.assertEqual(self.hand.tour_number, "797469411")
        self.assertEqual(self.hand.tour_level, "I")

    def test_currency(self):
        self.assertEqual(self.hand.currency, "USD")

    def test_stake(self):
        self.assertEqual(self.hand.buyin, Decimal('3.19'))
        self.assertEqual(self.hand.rake, Decimal('0.31'))

    def test_game(self):
        self.assertEqual(self.hand.game, "HOLDEM")

    def test_limit(self):
        self.assertEqual(self.hand.limit, "NL")

    def test_blinds(self):
        self.assertEqual(self.hand.sb, Decimal(10))
        self.assertEqual(self.hand.bb, Decimal(20))

    def test_date(self):
        self.assertEqual(self.hand.date, ET.localize(datetime(2013, 10, 4, 13, 53, 27)))


class TestParseBody1(TestCase):
    def setUp(self):
        self.hand = PokerStarsHand(HAND1)

    def tearDown(self):
        del self.hand

    def test_parsed_flags_are_set(self):
        self.assertTrue(self.hand.parsed)
        self.assertTrue(self.hand.header_parsed)

    def test_table_name(self):
        self.assertEqual('797469411 15', self.hand.table_name)

    def test_max_players(self):
        self.assertEqual(9, self.hand.max_players)

    def test_button_seat(self):
        self.assertEqual(1, self.hand.button_seat)

    def test_button(self):
        self.assertEqual('flettl2', self.hand.button)

    def test_hero(self):
        self.assertEqual('W2lkm2n', self.hand.hero)

    def test_hero_seat(self):
        self.assertEqual(5, self.hand.hero_seat)

    def test_players_and_stacks(self):
        self.assertEqual(self.hand.players, OrderedDict([('flettl2', 1500), ('santy312', 3000), ('flavio766', 3000),
                                                         ('strongi82', 3000), ('W2lkm2n', 3000), ('MISTRPerfect', 3000),
                                                         ('blak_douglas', 3000), ('sinus91', 1500), ('STBIJUJA', 1500)])
                        )

    def test_hero(self):
        self.assertEqual('W2lkm2n', self.hand.hero)

    def test_hero_hole_cards(self):
        self.assertEqual(('Ac', 'Jh'), self.hand.hero_hole_cards)

    def test_flop(self):
        self.assertEqual(('2s', '6d', '6h'), self.hand.flop)

    def test_turn(self):
        self.assertIsNone(self.hand.turn)

    def test_river(self):
        self.assertIsNone(self.hand.river)

    def test_board(self):
        self.assertEqual(('2s', '6d', '6h'), self.hand.board)

    def test_winners(self):
        self.assertEqual(('W2lkm2n',), self.hand.winners)

    def test_total_pot(self):
        self.assertEqual(Decimal(150), self.hand.total_pot)

    def test_preflop_actions(self):
        self.assertEqual(("strongi82: folds",
                          "W2lkm2n: raises 40 to 60",
                          "MISTRPerfect: calls 60",
                          "blak_douglas: folds",
                          "sinus91: folds",
                          "STBIJUJA: folds",
                          "flettl2: folds",
                          "santy312: folds",
                          "flavio766: folds"),
                         self.hand.preflop_actions)

    def test_flop_actions(self):
        self.assertEqual(('W2lkm2n: bets 80', 'MISTRPerfect: folds', 'Uncalled bet (80) returned to W2lkm2n',
                          'W2lkm2n collected 150 from pot', "W2lkm2n: doesn't show hand"),
                         self.hand.flop_actions)

    def test_turn_actions(self):
        self.assertIsNone(self.hand.turn_actions)

    def test_river_actions(self):
        self.assertIsNone(self.hand.river_actions)
