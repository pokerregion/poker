import random
from functools import total_ordering
from collections.abc import Iterable
from enum import Enum, EnumMeta
from types import DynamicClassAttribute


class _PokerEnumMeta(EnumMeta):
    def __init__(self, clsname, bases, classdict):
        # make sure we only have tuple values, not single values
        for member in self.__members__.values():
            values = member._value_
            if not isinstance(values, Iterable) or isinstance(values, str):
                raise TypeError('{} = {!r}, should be iterable, not {}!'
                    .format(member._name_, values, type(values))
                )
            for alias in values:
                if isinstance(alias, str):
                    alias = alias.upper()
                self._value2member_map_.setdefault(alias, member)

    def __call__(cls, value):
        """Return the appropriate instance with any of the values listed. If values contains
        text types, those will be looked up in a case insensitive manner."""
        if isinstance(value, str):
            value = value.upper()
        return super().__call__(value)

    def make_random(cls):
        return random.choice(list(cls))


@total_ordering
class PokerEnum(Enum, metaclass=_PokerEnumMeta):
    # From Python manual:
    # If a class that overrides __eq__() needs to retain
    # the implementation of __hash__() from a parent class,
    # the interpreter must be told this explicitly
    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ == other._value_
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            names = self.__class__._member_names_
            return names.index(self._name_) < names.index(other._name_)
        return NotImplemented

    def __str__(self):
        return str(self._value_[0])

    def __repr__(self):
        apostrophe = "'" if isinstance(self._value_[0], str) else ''
        return "{0}({1}{2}{1})".format(self.__class__.__qualname__, apostrophe, self)

    @DynamicClassAttribute
    def val(self):
        return self._value_[0]


class _ReprMixin:
    def __repr__(self):
        return "{}('{}')".format(self.__class__.__qualname__, self)


def _make_float(string):
    return float(string.strip().replace(',', ''))


def _make_int(string):
    return int(string.strip().replace(',', ''))
