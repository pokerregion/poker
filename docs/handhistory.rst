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


About hand history changes
--------------------------

Poker rooms sometimes change the hand history format significally. My goal is to cover all hand
histories after 2014.01.01., because it is the best compromise between fast development and good
coverage. This way we don't have to deal with ancient hand history files and overcomplicate the
code and we can concentrate on the future instead of the past. Also, hopefully hand history formats
are stable enough nowadays to follow this plan, less and less new game types coming up.

One of the "recent" changes made by Full Tilt is from 2013.05.10.:

   "In the software update from Wednesday, changed the format of the .
   This means that Hold'em Manager does no longer import these hands, and the HUD is not working.
   ... B.t.w. They just renamed "No Limit Hold'em" to "NL Hold'em",
   and swapped position with the blinds, inside the handhistory files."

Details: http://www.bankrollmob.com/forum.asp?mode=thread&id=307215
