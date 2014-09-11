Hand history parsing
====================

The classes in :mod:`poker.room` can parse hand histories
for different poker rooms. Right now for PokerStars, Full Tilt Poker and PKR,
very efficiently with a simple API.


Parsing from hand history text
------------------------------

In one step::

   from poker.room.pokerstars import PokerStarsHandHistory
   # First step, only raw hand history is saved, no parsing will happen yet
   hh = PokerStarsHandHistory(hand_text)
   # You need to explicitly parse. This will parse the whole hh at once.
   hh.parse()

**Or** in two steps:

.. code-block:: python

   from poker.room.pokerstars import PokerStarsHandHistory
   hh = PokerStarsHandHistory(hand_text)
   # parse the basic information only (really fast)
   hh.parse_header()
   # And later parse the body part. This might happen e.g. in a background task
   >>> hh.parse()


I decided to implement this way, and not parse right away at object instantiation, because probably
the most common operation will be looking into the hand history as fast as possible for basic
information like hand id, *or* deferring the parsing e.g. to a message queue. This way, you
basically just save the raw hand history in the instance, pass it to the queue and it will take
care of parsing by the parse() call.

And also because "Explicit is better than implicit."


Parsing from file
-----------------

   >>> hh = PokerStarsHandHistory.from_file(filename)
   >>> hh.parse()


Example
-------

.. code-block:: python

   >>> from poker.room.pokerstars import PokerStarsHandHistory
   >>> hh = PokerStarsHandHistory(hand_text)
   >>> hh.parse()
   >>> hh.players
   [_Player(name='flettl2', stack=1500, seat=1, combo=None),
    _Player(name='santy312', stack=3000, seat=2, combo=None),
    _Player(name='flavio766', stack=3000, seat=3, combo=None),
    _Player(name='strongi82', stack=3000, seat=4, combo=None),
    _Player(name='W2lkm2n', stack=3000, seat=5, combo=Combo('A♣J♥')),
    _Player(name='MISTRPerfect', stack=3000, seat=6, combo=None),
    _Player(name='blak_douglas', stack=3000, seat=7, combo=None),
    _Player(name='sinus91', stack=1500, seat=8, combo=None),
    _Player(name='STBIJUJA', stack=1500, seat=9, combo=None)]
   >>> hh.date
   datetime.datetime(2013, 10, 4, 19, 18, 18, tzinfo=<DstTzInfo 'US/Eastern' EDT-1 day, 20:00:00 DST>)
   >>> hh.hero
   _Player(name='W2lkm2n', stack=3000, seat=5, combo=Combo('A♣J♥')),
   >>> hh.limit, hh.game
   ('NL', 'HOLDEM')
   >>> hh.board
   (Card('2♠'), Card('6♦'), Card('6♥'))
   >>> hh.flop.is_rainbow
   True
   >>> hh.flop.has_pair
   True
   >>> hh.flop.actions
   (('W2lkm2n', <Action.BET: ('bet', 'bets')>, Decimal('80')),
    ('MISTRPerfect', <Action.FOLD: ('fold', 'folded', 'folds')>),
    ('W2lkm2n', <Action.RETURN: ('return', 'returned', 'uncalled')>, Decimal('80')),
    ('W2lkm2n', <Action.WIN: ('win', 'won', 'collected')>, Decimal('150')),
    ('W2lkm2n', <Action.MUCK: ("don't show", "didn't show", 'did not show', 'mucks')>))


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
