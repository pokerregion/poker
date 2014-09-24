from pathlib import Path
from poker import Strategy, Range
from poker.constants import Position
from poker.strategy import _Strategy
import pytest


filedir = Path(__file__).parent
strategy = Strategy.from_file(str(filedir / 'push.strategy'))


tenBB = _Strategy(
    UTG=Range('JJ+ ATs+ AQo+ KQs QTs+ JTs'), UTG1=Range('77+ ATs+ AQo+ KQs QTs+ JTs'),
    UTG2=Range('66+ ATs+ AQo+ KQs QTs+ JTs'), UTG3=Range('55+ ATs+ AQo+ KQs QTs+ JTs'),
    UTG4=Range('44+ ATs+ AQo+ KQs QTs+ JTs'), CO=Range('33+ ATs+ AQo+ KQs QTs+ JTs'),
    BTN=Range('22+ ATs+ AQo+ KQs QTs+ JTs'), SB=Range('XX'), BB=None, inaction='PUSH',
    outaction='FOLD'
)

twelveBB = _Strategy(
    UTG=Range('JJ+ AQs+ AKo'), UTG1=Range('JJ+ AQs+ AKo'),UTG2=Range('JJ+ AQs+ AKo'),
    UTG3=Range('JJ+ AQs+ AKo'), UTG4=Range('JJ+ AQs+ AKo'), CO=Range('JJ+ AQs+ AKo'),
    BTN=Range('JJ+ AQs+ AKo'), SB=Range('55- A2+'), BB=None, inaction='PUSH', outaction='FOLD',
)

elevenBB = _Strategy(
    UTG=Range('77+ A5s+ AKo KJs+ QJs'), UTG1=Range('66+ A5s+ AKo KJs+ QJs'),
    UTG2=Range('55+ A5s+ AKo KJs+ QJs'), UTG3=Range('44+ A5s+ AKo KJs+ QJs'),
    UTG4=Range('33+ A5s+ AKo KJs+ QJs'), CO=Range('22+ A3s+ AKo KJs+ QJs'),
    BTN=Range('22+ A2s+ AKo KJs+ QJs'), SB=Range('XX'), BB=None, inaction='PUSH', outaction='FOLD',
)


def test_section_names():
    assert list(strategy) == ['10 BB', '11 BB', '12 BB']
    assert tuple(strategy) == ('10 BB', '11 BB', '12 BB')


def test_name():
    assert strategy.name == 'Preflop PUSH'


def test_section_values():
    assert strategy['10 BB'] == tenBB
    assert strategy['11 BB'] == elevenBB
    assert strategy['12 BB'] == twelveBB


def test_iterable():
    assert [(name, strat) for name, strat in strategy.items()]


def test_subscriptable_by_strategy_name():
    assert strategy['10 BB'] == tenBB


def test_subscriptable_by_section_position_int():
    assert strategy[0] == tenBB
    assert strategy[1] == elevenBB
    assert strategy[2] == twelveBB


def test_len():
    assert len(strategy) == 3


def test_get():
    assert strategy.get('10 BB') == tenBB
    assert strategy.get('20 BB') == None


def test_values():
    # ordereddict ValuesView
    assert tuple(strategy.values()) == (tenBB, elevenBB, twelveBB)


def test_first_position():
    assert strategy.get_first().position == Position.UTG
