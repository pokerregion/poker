Development
===========


Git repository
--------------

You find the repository on github:
https://github.com/pokerregion/poker

In the ``dend/`` branches, there are ideas which doesn't work or has been abandoned for some reason.
They are there for reference as "this has been tried".


Coding style
------------

PEP8 except for line length, which is 99 max (hard limit).
If your code exceeds 99 characters, you do something wrong anyway, you need to refactor it
(e.g. to deeply nested, harder to understand)



New hand history parser
-----------------------

.. note:: Hand history parsing API will change for sure until 1.0 is done.

If you want to support a new poker room you have to subclass the appropriate class from
:mod:`poker.handhistory` like :class:`poker.handhistory.SplittableHandHistory` depending on the type of
hand history file, like XML, or similar to pokerstars and FTP, define a couple of methods and done.

.. code-block:: python

    class PokerRoomHandHistory(HandHistory):
        """Implement PokerRoom specific parsing."""

        def parse_header(self):
            # Parse header only! Usually just first line. The whole purpose is to do it fast.
            # No need to call super()

        def parse(self):
            # base class method strips and saves raw hand history
            super(PokerRoomHand, self).parse()

            # ...


You **have to** provide all common attributes, and *may* provide PokerRoom specific extra
attributes described in the base :class:`poker.handhistory.HandHistory` class API documentation.



Testing
-------

The framework contains a lot of tests (over 400). The basic elements like Card, Hand, Range, etc.
are fully tested.

All the unit tests are written in `pytest`_. I choose it because it offers very nice funcionality,
and no-boilerplate code for tests. No need to sublass anything, just prefix classes with ``Test``
and methods with ``test_``.

All assertion use the default python ``assert`` keyword.

To run the tests, just invoke::

    $ python setup.py test

Or alternatively you need to install the pacakge itself::

    $ python setup.py develop

or::

    $ pip install -e .

and install `pytest`_ and run it directly::

    $ pip install pytest
    $ cd poker
    $ py.test

from the poker module directory and `pytest`_ will automatically pick up all unit tests.

.. _pytest: http://pytest.org/
