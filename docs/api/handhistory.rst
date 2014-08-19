Hand history parsing API
========================


.. autofunction:: poker.handhistory.normalize

  | For example, PKR calls "Cash game" "ring game",
  | or there are multiple forms of holdem like "Hold'em", "holdem", "he", etc..

  :param value: the word to normalize like ``"No limit"``, ``"Hold'em"``, ``"Cash game"``
  :return: Normalized form of the word like ``"NL"``, ``"HOLDEM"``, ``"CASH"``, etc.


Base classes
------------

.. autoclass:: poker.handhistory.HandHistoryPlayer

   :ivar str name:            Player name
   :ivar int stack:           Stack size (sometimes called as chips)
   :ivar int seat:            Seat number
   :ivar Combo,None combo:    If the player revealed his/her hand, this property hold's it.
                              None for players didn't show... autoclass:: poker.handhistory.HandHistoryPlayer


.. autoclass:: poker.handhistory.HandHistory

  :param str hand_text:  poker hand text
  :param bool parse:     if ``False``, hand will not parsed immediately.
                         Useful if you just want to quickly check header first and maybe process it later.

  | The attributes can be iterated.
  | The class can read like a dictionary.
  | Every attribute default value is ``None``.

  :ivar str poker_room:         room ID (4 byte max) e.g. ``"STARS"``, ``"FTP"``
  :ivar str date_format:        default date format for the given poker_room
  :ivar str ident:              hand id
  :ivar str game_type:          ``"TOUR"`` for tournaments or ``"SNG"`` for Sit&Go-s
  :ivar str tournament_ident:   tournament id
  :ivar str tournament_level:   level of tournament blinds
  :ivar str currency:           3 letter iso code ``"USD"``, ``"HUF"``, ``"EUR"``, etc.
  :ivar Decimal buyin:          buyin **without** rake
  :ivar Decimal rake:           if game_type is ``"TOUR"`` it's buyin rake, if ``"CASH"`` it's rake from pot
  :ivar str game:               ``"HOLDEM"``, ``"OMAHA"``, ``"STUD"``, ``"RAZZ"``, etc.
                                you should call :func:`normalize` to generate the correct value
  :ivar str limit:              ``"NL"``, ``"PL"`` or ``"FL"``
  :ivar Decimal sb:             amount of small blind
  :ivar Decimal bb:             amount of big blind
  :ivar datetime date:          hand date in UTC
  :ivar str table_name:         name of the table. it's ``"tournament_number table_number"``
  :ivar int max_player:         maximum players can sit on the table, 2, 4, 6, 7, 8, 9
  :ivar HandHistoryPlayer button:   player on the button
  :ivar HandHistoryPlayer hero:     hero
  :ivar list players:           HandHistoryPlayer namedtuples
                                the sequence is the seating order at the table at the start of the hand
  :ivar tuple flop:             tuple of Cards e.g. ``(Card('Ah'), Card('2s'), Card('2h'))``
  :ivar Card turn:              turn card, e.g. ``Card('Ah')``
  :ivar Card river:             river card, e.g. ``Card('2d')``
  :ivar tuple board:            board cards, e.g. ``(Card('4s'), Card('4d'), Card('4c'), Card('5h'))``
  :ivar tuple preflop_actions:  action lines in str
  :ivar tuple flop_actions:     flop action lines
  :ivar tuple turn_actions:     turn action lines
  :ivar tuple river_actions:    river action lines
  :ivar Decimal total_pot:      total pot after end of actions (rake included)
  :ivar bool show_down:         There was show_down or wasn't
  :ivar tuple winners:          winner names, tuple if even when there is only one winner. e.g. ``('W2lkm2n',)``


PokerStars
----------

.. autoclass:: poker.room.pokerstars.PokerStarsHandHistory

  **Class specific**

  :ivar str poker_room:   always ``STARS`` in this class


Full Tilt Poker
---------------

.. autoclass:: poker.room.fulltiltpoker.FullTiltPokerHandHistory

   PokerStars and Full Tilt hand histories are very similar, so parsing them is almost identical.
   There are small differences though.

   **Class specific**

   :cvar str poker_room:    always ``FTP`` for this class
   :ivar tournament_level:  ``None``
   :ivar buyin:             ``None``: it's not in the hand history, but the filename
   :ivar rake:              ``None``: also
   :ivar currency:          ``None``
   :ivar str table_name:    just a number, but str type

   **Extra**

   :ivar Decimal flop_pot:        pot size on the flop, before actions
   :ivar int flop_num_players:    number of players seen the flop
   :ivar Decimal turn_pot:        pot size before turn
   :ivar int turn_num_players:    number of players seen the turn
   :ivar Decimal river_pot:       pot size before river
   :ivar int river_num_players:   number of players seen the river
   :ivar str tournament_name:     e.g. ``"$750 Guarantee"``, ``"$5 Sit & Go (Super Turbo)"``


PKR
---

.. autoclass:: poker.room.pkr.PKRHandHistory

  **Class specific**

  :cvar str poker_room:   ``"PKR"`` for this class
  :ivar str table_name:   "#table_number - name_of_the_table"

  **Extra**

  :ivar str last_ident:    last hand id
  :ivar str money_type:    ``"R"`` for real money, ``"P"`` for play money
