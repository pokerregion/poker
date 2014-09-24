from configparser import ConfigParser
from collections import namedtuple, OrderedDict as odict
from collections.abc import Mapping, Iterable
from .hand import Range
from .constants import Position


_Strategy = namedtuple('_Strategy', 'UTG UTG1 UTG2 UTG3 UTG4 CO BTN SB BB '
                       'inaction outaction comment')
_Situation = namedtuple('_Situation', 'position range posindex')


class Strategy(Mapping):
    def __init__(self, strategy: str):
        self._config = ConfigParser(default_section='strategy', interpolation=None)
        self._config['strategy'] = dict(name='', inaction='', outaction='', comment='')
        self._config.read_string(strategy)
        strategy_section = self._config['strategy']
        self.name = strategy_section.get('name', '')
        self.inaction = strategy_section.get('inaction', '')
        self.outaction = strategy_section.get('outaction', '')
        self.comment = strategy_section.get('comment', '')

        self._situations = odict()
        for name in self._config.sections():
            values = dict(self._config[name].items())
            # values.setdefault('inaction', self.inaction)
            # values.setdefault('outaction', self.outaction)
            # values.setdefault('comment', self.comment)
            for pos in Position:
                pos = pos.value[0]
                pos_low = pos.lower()
                if values.get(pos_low):
                    values[pos] = Range(values[pos_low])
                    del values[pos_low]
                else:
                    values[pos] = None
            del values['name']
            self._situations[name] = _Strategy(**values)
        self._tuple = tuple(self._situations.values())

    def __iter__(self):
        return iter(self._situations)

    def items(self):
        return self._situations.items()

    def keys(self):
        return self._situations.keys()

    def get(self, key, default=None):
        return self._situations.get(key, default)

    def __getitem__(self, key):
        if isinstance(key, str):
            return self._situations.__getitem__(key)
        elif isinstance(key, int):
            return self._tuple[key]
        raise TypeError('You can lookup by int or str')

    def values(self):
        return self._situations.values()

    def __contains__(self, key):
        return self._situations.__contains__(key)

    def __len__(self):
        return len(self._situations)

    @classmethod
    def from_file(cls, filename):
        strategy = open(filename).read()
        return cls(strategy)

    def get_first(self, situation=0):
        situation = self[situation]
        for posindex, position in enumerate(Position):
            range = getattr(situation, position.value[0])
            if range:
                return _Situation(position, range, posindex)
