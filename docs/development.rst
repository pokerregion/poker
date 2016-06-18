Development
===========


Git repository
--------------

You find the repository on github:
https://github.com/pokerregion/poker

In the ``dend/`` branches, there are ideas which doesn't work or has been abandoned for some reason.
They are there for reference as "this has been tried".

I develop in a very simple `Workflow`_. (Before 662f5d73be1efbf6eaf173da448e0410da431b2c you can
see bigger merge bubbles, because I handled hand history parser code and the rest as two separate
projects, but made a subtree merge and handle them in this package.)
Feature branches with rebases on top of master.
Only merge stable code into master.

The repository tags will match PyPi release numbers.


Versioning
----------

I use `Semantic Versioning`_, except for major versions like 1.0, 2.0,
because I think 1.0.0 looks stupid :)


Coding style
------------

PEP8 except for line length, which is 99 max (hard limit).
If your code exceeds 99 characters, you do something wrong anyway, you need to refactor it
(e.g. to deeply nested, harder to understand)


Dates and times
---------------

Every datetime throughout the library is in UTC with tzinfo set to ``pytz.UTC``.
If you found a case where it's not, it's a bug, please `report it on GitHub!`_
The right way for setting a date correctly e.g. from PokerStars ET time is:

.. code-block:: python

   >>> import pytz
   >>> ET = pytz.timezone('US/Eastern')
   >>> ET.localize(some_datetime).astimezone(pytz.UTC)

This will consider DST settings and ambiguous times. For more information, see `pytz documentation`_!


Unicode vs Bytes
----------------

The library uses the strategy from Python 3: internally, everything is using unicode, and things are
converted only the I/O boundaries (e.g. opening/writing files).
This is implemented by the future mechanism:

.. code-block:: python

   from __future__ import unicode_literals

this way, all newly defined text will be unicode by default. I only check for unicode everywhere
in the code, not str, please watch this! It might feel strange the first time, but when the time comes
to convert the library to Python3, it will be much easier!


New hand history parser
-----------------------

.. note:: Hand history parsing API will change for sure until 1.0 is done.

If you want to support a new poker room you have to subclass the appropriate class from
:mod:`poker.handhistory` like :class:`poker.handhistory._SplittableHandHistory` depending on the
type of hand history file, like XML, or similar to pokerstars and FTP,
define a couple of methods and done.

.. code-block:: python

   class NewPokerRoomHandHistory(HandHistory):
   """Implement PokerRoom specific parsing."""

      def parse_header(self):
         # Parse header only! Usually just the first line. The whole purpose is to do it fast!
         # No need to call super()

      def _parse_table(self):
         # parses table name

      def _parse_players(self):
         # parses players, player positions, stacks, etc
         # set self.players attribute

      def _parse_button(self):

      def _parse_hero(self):

      def _parse_preflop(self):

      def _parse_street(self):

      def _parse_showdown(self):

      def _parse_pot(self):

      def _parse_board(self):

      def _parse_winners(self):

      def _parse_extra(self):


You **have to** provide all common attributes, and *may* provide PokerRoom specific extra
attributes described in the base :class:`poker.handhistory.HandHistory` class API documentation.



Testing
-------

The framework contains a lot of tests (over 400). The basic elements like Card, Hand, Range, etc.
are fully tested.

All the unit tests are written in `pytest`_. I choose it because it offers very nice functionality,
and no-boilerplate code for tests. No need to subclass anything, just prefix classes with ``Test``
and methods with ``test_``.

All assertion use the default python ``assert`` keyword.

You need to install the ``poker`` package in development mode::

    # from directory where setup.py file is
    $ pip install -e .

and install `pytest`_ and run it directly::

    $ pip install pytest
    $ py.test

from the poker module directory and `pytest`_ will automatically pick up all unit tests.


About the state of Python3
--------------------------

Originally I started the library in Python3.4 only, and though everything worked well for a while and
library support seemed fine, the tooling around Python3 is not there at all yet. PyPy, PyInstaller
Kivy, etc, etc. doesn't support Python3.4 at all, but even if they do, there are bugs/problems which
are hard to solve, because nobody experienced it before. A nice example is that I found a bug in the
3.4 standard library enum module.

As a consequence of this, at v0.22.0 I converted the whole repository to Python2 only. The long-term
strategy is to use Python2 for everything until the tooling for Python3.4 catch up, and at that point,
convert it to Python3.4 and continue from there. I don't want to develop a 2 and 3 compatible library
for such a niche market, because it's very time consuming, please don't even ask me! (E.g. it took
straight 10 hours to convert the whole library to Python2, with no new code at all...)


.. _pytest: http://pytest.org/
.. _Workflow: https://guides.github.com/introduction/flow/index.html
.. _Semantic Versioning: http://semver.org/
.. _report it on GitHub!: https://github.com/pokerregion/poker/issues/new?title=Incorrect+datetime
.. _pytz documentation: http://pytz.sourceforge.net/#localized-times-and-date-arithmetic
