Hand history parsing
====================

The classes in :mod:`poker.room` can parse hand histories
for different poker rooms. Right now for PokerStars, Full Tilt Poker and PKR,
very efficiently with a simple API.

Basic example
-------------

.. code-block:: python

    >>> from poker.handhistory import PokerStarsHandHistory
    >>> hand = PokerStarsHandHistory(hand_text)
    >>> hand.players
    OrderedDict([('pjo80', 1500), ('Brimill', 3000), ('XZ18', 1500), ('.prestige.U$', 3000), ('schnetzger', 1500), ('W2lkm2n', 3000), ('sednanref', 1500), ('daoudi007708', 1500), ('IPODpoker88', 3000)])

    >>> hand.date
    datetime.datetime(2013, 10, 4, 19, 18, 18, tzinfo=<DstTzInfo 'US/Eastern' EDT-1 day, 20:00:00 DST>)

    >>> hand.hero
    'W2lkm2n'
    >>> hand.hero_combo
    Combo('7d6h')

API
---

See all the room specific classes in them :doc:`api/handhistory` documentation.
