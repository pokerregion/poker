import random
from enum import Enum, EnumMeta
from functools import total_ordering
from types import DynamicClassAttribute


class _MultiMeta(EnumMeta):
    def __new__(metacls, cls, bases, classdict):
        # members already collected from Enum class
        enum_class = super(_MultiMeta, metacls).__new__(metacls, cls, bases, classdict)

        # make sure we only have tuple values, not single values
        for member in enum_class.__members__.values():
            if not isinstance(member._value_, tuple):
                raise ValueError('{!r}, should be tuple'.format(member._value_))
        return enum_class

    def __call__(cls, suit):
        for member in cls:
            if suit in member._value_:
                return member
        return super().__call__(suit)

    def make_random(cls):
        return random.choice(list(cls))


@total_ordering
class _MultiValueEnum(Enum, metaclass=_MultiMeta):
    # From Python manual:
    # If a class that overrides __eq__() needs to retain the implementation of __hash__()
    # from a parent class, the interpreter must be told this explicitly
    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ == other._value_
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            names = self.__class__._member_names_
            return names.index(self.name) < names.index(other.name)
        return NotImplemented

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        apostrophe = "'" if isinstance(self.value, str) else ''
        return "{0}({1}{2}{1})".format(self.__class__.__qualname__, apostrophe, self)

    @DynamicClassAttribute
    def value(self):
        """The value of the Enum member."""
        return self._value_[0]


class _ReprMixin:
    def __repr__(self):
        return "{}('{}')".format(self.__class__.__qualname__, self)


def _make_float(string):
    return float(string.strip().replace(',', ''))
