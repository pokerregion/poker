# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function

from collections import Mapping, OrderedDict as odict
from pathlib import Path
import attr
from configparser import ConfigParser
from .hand import Range
from .constants import Position


@attr.s(slots=True)
class _Situation(object):
    utg = attr.ib()
    utg1 = attr.ib()
    utg2 = attr.ib()
    utg3 = attr.ib()
    utg4 = attr.ib()
    co = attr.ib()
    btn = attr.ib()
    sb = attr.ib()
    bb = attr.ib()
    inaction = attr.ib()
    outaction = attr.ib()
    comment = attr.ib()


@attr.s(slots=True)
class _Spot(object):
    position = attr.ib()
    range = attr.ib()
    posindex = attr.ib()


_POSITIONS = {'utg', 'utg1', 'utg2', 'utg3', 'utg4', 'co', 'btn', 'sb', 'bb'}


class Strategy(Mapping):
    def __init__(self, strategy, source='<string>'):
        self._config = ConfigParser(default_section='strategy', interpolation=None)
        self._config.read_string(strategy, source)

        self._situations = odict()
        for name in self._config.sections():
            # configparser set non-specified values to '', we want default to None
            values = dict.fromkeys(_Situation.__slots__, None)
            for key, val in self._config[name].items():
                # filter out fields not implemented, otherwise it would
                # cause TypeError for _Situation constructor
                if (not val) or (key not in _Situation.__slots__):
                    continue
                elif key in _POSITIONS:
                    values[key] = Range(val)
                else:
                    values[key] = val
            self._situations[name] = _Situation(**values)

        self._tuple = tuple(self._situations.values())

    @classmethod
    def from_file(cls, filename):
        # Path accept str or Path
        strategy = Path(filename).open(encoding='utf-8').read()
        return cls(strategy, source=filename)

    def __getattr__(self, name):
        # Strategy uses only _Situation._fields, but this way .strategy files are more flexible,
        # because can contain extra values without breaking anything
        return self._config['strategy'][name]

    def __iter__(self):
        return iter(self._situations)

    def items(self):
        return self._situations.items()

    def keys(self):
        return self._situations.keys()

    def get(self, key, default=None):
        return self._situations.get(key, default)

    def __getitem__(self, key):
        if isinstance(key, unicode):
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

    def get_first_spot(self, situation=0):
        situation = self[situation]
        for posindex, position in enumerate(Position):
            range = getattr(situation, position.name.lower())
            if range:
                return _Spot(position, range, posindex)
