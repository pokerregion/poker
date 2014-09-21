from pathlib import Path
from collections import OrderedDict as odict
from poker import Strategy, Range
import pytest


@pytest.fixture(scope='session')
def strategy():
    filedir = Path(__file__).parent
    return Strategy.from_file(str(filedir / 'push.strategy'))


def test_sections(strategy):
    assert strategy.sections == odict()


def test_section_names(strategy):
    assert strategy.section_names == ('10 BB', '11 BB', '12 BB')


def test_name(strategy):
    assert strategy.name == 'Preflop PUSH'


def test_sections(strategy):
    assert strategy.sections == odict((
        ('10 BB', dict(utg=Range('JJ+ ATs+ AQo+ KQs QTs+ JTs'),
                       utg1=Range('77+ ATs+ AQo+ KQs QTs+ JTs'),
                       utg2=Range('66+ ATs+ AQo+ KQs QTs+ JTs'),
                       utg3=Range('55+ ATs+ AQo+ KQs QTs+ JTs'),
                       utg4=Range('44+ ATs+ AQo+ KQs QTs+ JTs'),
                       co=Range('33+ ATs+ AQo+ KQs QTs+ JTs'),
                       btn=Range('22+ ATs+ AQo+ KQs QTs+ JTs'),
                       sb=Range('XX'),
                       inaction='PUSH',
                       outaction='FOLD',
                       )
        ),
        ('11 BB', dict(utg=Range('77+ A5s+ AKo KJs+ QJs'),
                       utg1=Range('66+ A5s+ AKo KJs+ QJs'),
                       utg2=Range('55+ A5s+ AKo KJs+ QJs'),
                       utg3=Range('44+ A5s+ AKo KJs+ QJs'),
                       utg4=Range('33+ A5s+ AKo KJs+ QJs'),
                       co=Range('22+ A3s+ AKo KJs+ QJs'),
                       btn=Range('22+ A2s+ AKo KJs+ QJs'),
                       sb=Range('XX'),
                       inaction='PUSH',
                       outaction='FOLD',
                       )
        ),
        ('12 BB', dict(utg=Range('JJ+ AQs+ AKo'),
                       utg1=Range('JJ+ AQs+ AKo'),
                       utg2=Range('JJ+ AQs+ AKo'),
                       utg3=Range('JJ+ AQs+ AKo'),
                       utg4=Range('JJ+ AQs+ AKo'),
                       co=Range('JJ+ AQs+ AKo'),
                       btn=Range('JJ+ AQs+ AKo'),
                       sb=Range('55- A2+'),
                       inaction='PUSH',
                       outaction='FOLD',
                       )
        ),
    ))
