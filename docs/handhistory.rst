.. handparser documentation master file, created by
   sphinx-quickstart on Fri Oct 25 14:21:31 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

====================
Hand history parsing
====================

About
-----

Hand history parser library.
It parses:

* PokerStars
* Full Tilt

tournament hands and

* PKR

cash games right now, very efficiently and with a simple API.

Basic example
-------------

.. code-block:: python

    >>> from handhistory import PokerStarsHandHistory
    >>> hand = PokerStarsHandHistory(hand_text)
    >>> hand.players
    OrderedDict([('pjo80', 1500), ('Brimill', 3000), ('XZ18', 1500), ('.prestige.U$', 3000), ('schnetzger', 1500), ('W2lkm2n', 3000), ('sednanref', 1500), ('daoudi007708', 1500), ('IPODpoker88', 3000)])

    >>> hand.date
    datetime.datetime(2013, 10, 4, 19, 18, 18, tzinfo=<DstTzInfo 'US/Eastern' EDT-1 day, 20:00:00 DST>)

    >>> hand.hero, hand.hero_hole_cards
    ('W2lkm2n', ('7d', '6h'))


Contributing
------------

If you want to support a new poker room, do this:

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
attributes described in the base :class:`HandHistory` class API documentation.
