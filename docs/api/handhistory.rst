Hand history parsing API
========================


.. note:: Hand history parsing API will change for sure until 1.0 is done.


Constant values
---------------

These enumerations are used to identify common values like limit types, game, etc.
By unifying these into groups of enumeration classes, it's possible to have common values
accross the whole framework, even when parsing totally different kind of hand histories, which
uses different values. (`Data normalization`_)
It's recommended to use keys (name property) to save in database, and print them to the user.
(E.g. in a web application template, ``{{ PokerRoom.STARS }}`` will be converted to ``'PokerStars'``.)

.. automodule:: poker.constants
   :members:
   :undoc-members:


Base classes
------------

.. autoclass:: poker.handhistory._BaseHandHistory
   :members:
   :exclude-members: board

   :param str hand_text:  poker hand text

   | The attributes can be iterated.
   | The class can read like a dictionary.
   | Every attribute default value is ``None``.

   :ivar str date_format:                  default date format for the given poker room
   :ivar str ident:                        hand id
   :ivar poker.constants.GameType game_type:  ``"TOUR"`` for tournaments or ``"SNG"`` for Sit&Go-s
   :ivar str tournament_ident:             tournament id
   :ivar str tournament_level:             level of tournament blinds
   :ivar poker.constants.Currency currency:  3 letter iso code ``"USD"``, ``"HUF"``, ``"EUR"``, etc.
   :ivar decimal.Decimal buyin:            buyin **without** rake
   :ivar decimal.Decimal rake:             if game_type is ``"TOUR"`` it's buyin rake, if ``"CASH"`` it's rake from pot
   :ivar poker.constants.Game game:        ``"HOLDEM"``, ``"OMAHA"``, ``"STUD"``, ``"RAZZ"``, etc.
   :ivar poker.constants.Limit limit:      ``"NL"``, ``"PL"`` or ``"FL"``
   :ivar decimal.Decimal sb:               amount of small blind
   :ivar decimal.Decimal bb:               amount of big blind
   :ivar datetime date:                    hand date in UTC
   :ivar str table_name:                   name of the table. it's ``"tournament_number table_number"``
   :ivar int max_players:                   maximum players can sit on the table, 2, 4, 6, 7, 8, 9
   :ivar poker.handhistory._Player button: player on the button
   :ivar poker.handhistory._Player hero:   hero player
   :ivar list players:                     list of :class:`poker.handhistory._Player`.
                                           the sequence is the seating order at the table at the start of the hand
   :ivar _Flop flop:                       room specific Flop object
   :ivar poker.card.Card turn:             turn card, e.g. ``Card('Ah')``
   :ivar poker.card.Card river:            river card, e.g. ``Card('2d')``
   :ivar tuple board:                      board cards, e.g. ``(Card('4s'), Card('4d'), Card('4c'), Card('5h'))``
   :ivar tuple preflop_actions:            action lines in str
   :ivar tuple turn_actions:               turn action lines
   :ivar decimal.Decimal turn_pot:         pot size before turn
   :ivar int turn_num_players:             number of players seen the turn
   :ivar tuple river_actions:              river action lines
   :ivar decimal.Decimal river_pot:        pot size before river
   :ivar int river_num_players:            number of players seen the river
   :ivar str tournament_name:              e.g. ``"$750 Guarantee"``, ``"$5 Sit & Go (Super Turbo)"``
   :ivar decimal.Decimal total_pot:        total pot after end of actions (rake included)
   :ivar bool show_down:                   There was show_down or wasn't
   :ivar tuple winners:                    winner names, tuple if even when there is only one winner. e.g. ``('W2lkm2n',)``
   :ivar dict extra:                       Contains information which are specific to a concrete hand history
                                           and not common accross all. When iterating through the instance,
                                           this extra attribute will not be included. default value is None

.. autoclass:: poker.handhistory._Player

   :ivar str name:            Player name
   :ivar int stack:           Stack size (sometimes called as chips)
   :ivar int seat:            Seat number
   :ivar Combo,None combo:    If the player revealed his/her hand, this property hold's it.
                              None for players didn't show... autoclass:: poker.handhistory._Player


Every hand history has an attribute ``flop`` which is an instance of the room specific :class:`_Flop`
object which has the following attributes:

.. currentmodule:: None

.. class:: _Flop

   :ivar tuple cards:          tuple of :class:`poker.card.Card`\ s
   :ivar decimal.Decimal pot:  pot size after actions
   :ivar tuple players:        tuple of player names
   :ivar tuple actions:        | tuple of :class:`poker.constants.Action` in the order of happening.
                              | Form:
                              | (Player name, Action, Amount) or
                              | (Player name, Action) if no amount needed (e.g. in case of Check)

   It also has properties about flop texture like:

   :ivar bool is_rainbow:
   :ivar bool is_monotone:
   :ivar bool is_triplet:
   :ivar bool has_pair:
   :ivar bool has_straightdraw:
   :ivar bool has_gutshot:
   :ivar bool has_flushdraw:

PokerStars
----------

.. autoclass:: poker.room.pokerstars.PokerStarsHandHistory


Full Tilt Poker
---------------

.. autoclass:: poker.room.fulltiltpoker.FullTiltPokerHandHistory

   PokerStars and Full Tilt hand histories are very similar, so parsing them is almost identical.
   There are small differences though.

   **Class specific**

   :ivar tournament_level:  ``None``
   :ivar buyin:             ``None``: it's not in the hand history, but the filename
   :ivar rake:              ``None``: also
   :ivar currency:          ``None``
   :ivar str table_name:    just a number, but str type

   **Extra**

   :ivar Decimal turn_pot:        pot size before turn
   :ivar int turn_num_players:    number of players seen the turn
   :ivar Decimal river_pot:       pot size before river
   :ivar int river_num_players:   number of players seen the river
   :ivar str tournament_name:     e.g. ``"$750 Guarantee"``, ``"$5 Sit & Go (Super Turbo)"``


PKR
---

.. autoclass:: poker.room.pkr.PKRHandHistory

  **Class specific**

  :ivar str table_name:   "#table_number - name_of_the_table"

  **Extra**

  :ivar str last_ident:    last hand id
  :ivar str money_type:    ``"R"`` for real money, ``"P"`` for play money


.. _data normalization: http://en.wikipedia.org/wiki/Data_normalization
