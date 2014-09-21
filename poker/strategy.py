from configparser import ConfigParser
from collections import OrderedDict as odict
from .hand import Range


class Strategy:
    _positions = {'utg', 'utg1', 'utg2', 'utg3', 'utg4', 'co', 'btn', 'sb', 'bb'}

    def __init__(self, strategy: str):
        self._config = ConfigParser(default_section='strategy', interpolation=None)
        self._config.read_string(strategy)
        self._process_sections()
        self.name = self._config.get('strategy', 'name')
        self.inaction = self._config.get('strategy', 'inaction')
        self.outaction = self._config.get('strategy', 'outaction')

    @classmethod
    def from_file(cls, filename):
        strategy = open(filename).read()
        return cls(strategy)

    @property
    def section_names(self):
        return tuple(self.sections)

    def _process_sections(self):
        self.sections = odict()
        # cut off [strategy] section
        for name in self._config.sections():
            section = dict()
            for key, val in self._config[name].items():
                # set positions as Range-es
                if key in self._positions:
                    section.setdefault(key, Range(val))
                # The whole strategy only has one name
                # set the others like inaction the same
                elif key != 'name':
                    section.setdefault(key, val)
            self.sections[name] = section
