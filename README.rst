handparser |travis| |coveralls|
===============================

.. |travis| image:: https://travis-ci.org/stakingadmin/handparser.png?branch=dend/module_refactoring
   :target: https://travis-ci.org/stakingadmin/handparser
.. |coveralls| image:: https://coveralls.io/repos/stakingadmin/handparser/badge.png?branch=master
   :target: https://coveralls.io/r/stakingadmin/handparser?branch=master


Hand history parser library.
It parses:

* PokerStars
* Full Tilt

tournament hands and

* PKR

cash games right now, very efficiently and with a simple API.

Usage
-----

.. code-block:: python

    >>> from handparser import PokerStarsHand
    >>> hand_text = open("HH20131004 T797613600 No Limit Hold'em $3.19 + $0.31").read()
    >>> hand = PokerStarsHand(hand_text)

    >>> hand['players']
    OrderedDict([('pjo80', 1500), ('Brimill', 3000), ('XZ18', 1500), ('.prestige.U$', 3000), ('schnetzger', 1500), ('W2lkm2n', 3000), ('sednanref', 1500), ('daoudi007708', 1500), ('IPODpoker88', 3000)])

    >>> hand.date	# or hand['date']
    datetime.datetime(2013, 10, 4, 19, 18, 18, tzinfo=<DstTzInfo 'US/Eastern' EDT-1 day, 20:00:00 DST>)

    >>> hand.hero, hand.hero_hole_cards
    ('W2lkm2n', ('7d', '6h'))

Parsed attributes
-----------------

.. code-block::

    poker_room          -- STARS for PokerStars
    ident               -- hand id
    game_type           -- TOUR for tournaments or SNG for Sit&Go-s
    tournament_ident    -- tournament id
    tournament_level
    currency            -- 3 letter iso code USD, HUF, EUR, etc.
    buyin               -- buyin without rake
    rake
    game                -- game type: HOLDEM, OMAHA, STUD, RAZZ, etc.
    limit               -- NL, PL or FL
    sb                  -- amount of small blind
    bb                  -- amount of big blind
    date                -- hand date in UTC

    table_name      -- name of the table. it's 'tournament number[ ]table number'
    max_player      -- maximum players can sit on the table, 2, 4, 6, 7, 8, 9
    button_seat     -- seat of button player, starting from 1
    button          -- player name on the button
    hero            -- name of hero
    hero_seat (int) -- seat of hero, starting from 1
    players         -- OrderedDict of tuples in form (playername, starting_stack)
                       the sequence is the seating order at the table at the start of the hand
    hero_hole_cards -- tuple of two cards, ex. ('Ah', 'As')
    flop            -- tuple of flop cards, ex. ('Ah', '2s', '2h')
    turn            -- str of turn card, ex. 'Ah'
    river           -- str of river card, ex. '2d'
    board           -- tuple of board cards, ex. ('4s', 4d', '4c', '5h')
    preflop actions -- tuple of action lines in str
    flop_actions    -- tuple of flop action lines
    turn_actions
    river_actions
    total_pot       -- total pot after end of actions
    show_down       -- There was showd_down or wasn't (bool)
    winners         -- tuple of winner names, even when there is only one winner. ex. ('W2lkm2n')

Testing
-------

From project folder::

    $ py.test

Py.test will automatically pick up unit tests.

Requirements
------------

|  Python 2.7 and ``pytz``.
|  ``pytest`` for testing.

LICENSE
-------

The MIT License (MIT)

Copyright (c) 2013 Kiss György

Me
--

|  `@Walkman_ <https://twitter.com/Walkman_>`_ on twitter
|  or you can reach me on my `public Github e-mail <https://github.com/Walkman>`_.
