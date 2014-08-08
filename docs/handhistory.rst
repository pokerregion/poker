Hand history parsing
====================

About
-----

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

    >>> hand.hero
    'W2lkm2n'
    >>> hand.hero_combo
    Combo('7d6h')

