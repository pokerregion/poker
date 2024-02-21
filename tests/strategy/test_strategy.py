from pathlib import Path

import pytest

from poker import Range, Strategy
from poker.constants import Position
from poker.strategy import _Situation

filedir = Path(__file__).parent
strategy = Strategy.from_file(filedir / "push.strategy")


tenBB = _Situation(
    utg=Range("JJ+ ATs+ AQo+ KQs QTs+ JTs"),
    utg1=Range("77+ ATs+ AQo+ KQs QTs+ JTs"),
    utg2=Range("66+ ATs+ AQo+ KQs QTs+ JTs"),
    utg3=Range("55+ ATs+ AQo+ KQs QTs+ JTs"),
    utg4=Range("44+ ATs+ AQo+ KQs QTs+ JTs"),
    co=Range("33+ ATs+ AQo+ KQs QTs+ JTs"),
    btn=Range("22+ ATs+ AQo+ KQs QTs+ JTs"),
    sb=Range("XX"),
    bb=None,
    inaction="PUSH",
    outaction="FOLD",
    comment=None,
)

twelveBB = _Situation(
    utg=Range("JJ+ AQs+ AKo"),
    utg1=Range("JJ+ AQs+ AKo"),
    utg2=Range("JJ+ AQs+ AKo"),
    utg3=Range("JJ+ AQs+ AKo"),
    utg4=Range("JJ+ AQs+ AKo"),
    co=Range("JJ+ AQs+ AKo"),
    btn=Range("JJ+ AQs+ AKo"),
    sb=Range("55- A2+"),
    bb=None,
    inaction="PUSH",
    outaction="FOLD",
    comment=None,
)

elevenBB = _Situation(
    utg=Range("77+ A5s+ AKo KJs+ QJs"),
    utg1=Range("66+ A5s+ AKo KJs+ QJs"),
    utg2=Range("55+ A5s+ AKo KJs+ QJs"),
    utg3=Range("44+ A5s+ AKo KJs+ QJs"),
    utg4=Range("33+ A5s+ AKo KJs+ QJs"),
    co=Range("22+ A3s+ AKo KJs+ QJs"),
    btn=Range("22+ A2s+ AKo KJs+ QJs"),
    sb=Range("XX"),
    bb=None,
    inaction="PUSH",
    outaction="FOLD",
    comment=None,
)


def test_situation_names():
    assert list(strategy) == ["10 BB", "11 BB", "12 BB"]
    assert tuple(strategy) == ("10 BB", "11 BB", "12 BB")


def test_name():
    assert strategy.name == "Preflop PUSH"
    assert strategy.name2 == ""


def test_non_existing_key_raises_KeyError_as_expected():
    with pytest.raises(KeyError):
        strategy.name3 == "Nonexisting"


def test_situation_values():
    assert strategy["10 BB"] == tenBB
    assert strategy["11 BB"] == elevenBB
    assert strategy["12 BB"] == twelveBB


def test_iterable():
    assert [(name, strat) for name, strat in strategy.items()]


def test_subscriptable_by_Situation_name():
    assert strategy["10 BB"] == tenBB


def test_subscriptable_by_situation_position_int():
    assert strategy[0] == tenBB
    assert strategy[1] == elevenBB
    assert strategy[2] == twelveBB


def test_len():
    assert len(strategy) == 3


def test_get():
    assert strategy.get("10 BB") == tenBB
    assert strategy.get("20 BB") is None


def test_values():
    # ordereddict ValuesView
    assert tuple(strategy.values()) == (tenBB, elevenBB, twelveBB)


def test_get_first_position():
    assert strategy.get_first_spot().position is Position.UTG
