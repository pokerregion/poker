from decimal import Decimal
from poker import Card, Action
from poker.room.pokerstars import _Flop
import pytest


@pytest.fixture(scope='session')
def flop():
    return _Flop([
        '[2s 6d 6h]',
        'W2lkm2n: bets 80',
        'MISTRPerfect: folds',
        'Uncalled bet (80) returned to W2lkm2n',
        'W2lkm2n collected 150 from pot',
        "W2lkm2n: doesn't show hand"
    ])


def test_flop_actions(flop):
    assert flop.actions == (
        ('W2lkm2n', Action.BET, Decimal(80)),
        ('MISTRPerfect', Action.FOLD),
        ('W2lkm2n', Action.RETURN, Decimal(80)),
        ('W2lkm2n', Action.WIN, Decimal(150)),
        ('W2lkm2n', Action.NOSHOW)
    )


def test_flop_cards(flop):
    assert flop.cards == (Card('2s'), Card('6d'), Card('6h'))


def test_flop_attributes(flop):
    assert flop.is_rainbow == True
    assert flop.is_monotone == False
    assert flop.is_triplet == False
    # TODO: http://www.pokerology.com/lessons/flop-texture/
    # assert flop.is_dry

    assert flop.has_pair == True
    assert flop.has_straightdraw == False
    assert flop.has_gutshot == True
    assert flop.has_flushdraw == False


def test_flop_players(flop):
    assert flop.players == ('W2lkm2n', 'MISTRPerfect')


def test_pot(flop):
    assert flop.pot == 150
