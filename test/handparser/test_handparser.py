from collections import MutableMapping
import pytest
from poker.handparser import PokerStarsHand
from . import stars_hands


class TestDictBehavior:
    expected_keys = {'ident', 'currency', 'hero_hole_cards', 'preflop_actions', 'turn', 'show_down', 'poker_room',
                     'winners', 'board', 'limit', 'river_actions', 'hero', 'turn_actions', 'bb', 'button_seat',
                     'tournament_ident', 'rake', 'buyin', 'game', 'hero_seat', 'date', 'max_players',
                     'flop_actions', 'button', 'flop', 'game_type', 'players', 'table_name', 'sb', 'total_pot',
                     'river', 'tournament_level'}

    def test_hand_is_mutablemapping(self, all_hands):
        assert isinstance(all_hands, MutableMapping)

    def test_all_keys_set(self, all_hands):
        assert self.expected_keys == set(all_hands.keys())

    def test_raw_is_not_a_key(self, all_hands):
        with pytest.raises(KeyError):
            all_hands['raw']

    def test_raw_is_an_attribute(self, all_hands):
        assert hasattr(all_hands, 'raw')

    def test_there_should_be_not_only_one_but_thirtyfour_keys(self, all_hands):
        assert 32 == len(all_hands) == len(all_hands.keys())

    def test_keys_never_gives_back_class_attributes(self):
        class ModdedPokerStarsHand(PokerStarsHand):
            _non_hand_attributes = ()

        hand = ModdedPokerStarsHand(stars_hands.HAND1)
        assert self.expected_keys | set(PokerStarsHand._non_hand_attributes) == set(hand.keys())
