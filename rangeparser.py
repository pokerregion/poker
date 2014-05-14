# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division


"""
    Rangeparser
    ~~~~~~~~~~~

    Parses human readable ranges like "22+ 54s 76s 98s AQo+" to a set of hands.

    It's very fault tolerant, makes it possible to make ranges fast.

    :copyright: (c) 2014 by Walkman
    :license: MIT, see LICENSE file for more details.
"""


CARDS = ('A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2')


class RangeSyntaxError(SyntaxError):
    """Thrown when range syntax cannot be parsed."""


class RangeError(Exception):
    """General Exception with Range objects."""


class Range(object):
    """Parses a range.

        :ivar set hands:    Set of hands
        :ivar str range:    Readable range in unicode
    """
