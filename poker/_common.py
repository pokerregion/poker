import random
from enum import Enum
from enum34_custom import (
    _MultiValueMeta, OrderableMixin, CaseInsensitiveMultiValueEnum, MultiValueEnum
)
from types import DynamicClassAttribute


class _RandomMultiValueMeta(_MultiValueMeta):
    def make_random(cls):
        return random.choice(list(cls))


class _MultiValueEnum(OrderableMixin, MultiValueEnum, metaclass=_RandomMultiValueMeta):
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        apostrophe = "'" if isinstance(self.value, str) else ''
        return "{0}({1}{2}{1})".format(self.__class__.__qualname__, apostrophe, self)

    @DynamicClassAttribute
    def value(self):
        """The value of the Enum member."""
        return self._value_[0]


class _CaseInsensitiveMultiValueEnum(CaseInsensitiveMultiValueEnum):
    def __str__(self):
        return self.value[0]


class _ReprMixin:
    def __repr__(self):
        return "{}('{}')".format(self.__class__.__qualname__, self)


def _make_float(string):
    return float(string.strip().replace(',', ''))


def _make_int(string):
    return int(string.strip().replace(',', ''))
