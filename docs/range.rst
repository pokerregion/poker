Range parsing
=============

About
-----

Parses human readable (text) ranges like ``"22+ 54s 76s 98s AQo+"`` to a set of :term:`Hand`\ s and
hand :term:`Combination`\ s.

| Contains classes for parsing, composing :term:`Suit`\ s, :term:`Hand`\ s, :term:`Card`\ s,
  :term:`Combination`\ s, :term:`Range`\ s, and checking for syntax.
| Can parse ranges and compose parsed ranges into human readable form again.
| It's very fault-tolerant, so it's easy and fast to write ranges manually.
| Can normalize unprecise human readable ranges into a precise human readable form, like "22+ AQo+ 33 AKo" --> "22+ AQo+"
| Can tell how big a range is by :term:`Percentage <Range percent>` or number of :term:`Combination`\ s.


Defining ranges
---------------

Atomic signs

    +----------------------------------------+-------------------------------------------------+
    |                   X                    |                 means "any card"                |
    +----------------------------------------+-------------------------------------------------+
    | A K Q J T 9 8 7 6 5 4 3 2              | Ace, King, Queen, Jack, Ten, 9, ..., deuce      |
    +----------------------------------------+-------------------------------------------------+
    | "s" or "o" after hands like AKo or 76s | suited and offsuit. Pairs have no suit (``''``) |
    +----------------------------------------+-------------------------------------------------+
    | `-`                                    | hands worse, down to deuces                     |
    +----------------------------------------+-------------------------------------------------+
    | `+`                                    | hands better, up to pairs                       |
    +----------------------------------------+-------------------------------------------------+

Available formats for defining ranges:

    +--------+--------------------------+
    | Format |       Parsed range       |
    +========+==========================+
    | 22     | one pair                 |
    +--------+--------------------------+
    | 44+    | all pairs better than 33 |
    +--------+--------------------------+
    | 66-    | all pairs worse than 77  |
    +--------+--------------------------+
    | 55-33  | 55, 44, 33               |
    +--------+--------------------------+

None of these below select pairs (for unambiguity):

    +------------+-------------------------------------------------------------------+
    |  AKo, J9o  |                           offsuit hands                           |
    +------------+-------------------------------------------------------------------+
    | AKs, 72s   | suited hands                                                      |
    +------------+-------------------------------------------------------------------+
    | AJo+       | offsuit hands above this: AJo, AQo, AKo                           |
    | Q8o+       | Q8o, Q9o, QTo, QJo                                                |
    +------------+-------------------------------------------------------------------+
    | AJs+       | same as offsuit                                                   |
    +------------+-------------------------------------------------------------------+
    |            | this is valid, although "+" is not neccessary,                    |
    | 76s+       | because there are no suited cards above 76s                       |
    +------------+-------------------------------------------------------------------+
    | A5o-       | offsuit hands; A5o-A2o                                            |
    +------------+-------------------------------------------------------------------+
    | A5s-       | suited hands; A5s-A2s                                             |
    +------------+-------------------------------------------------------------------+
    | K7         | suited and offsuited version of hand; K7o, K7s                    |
    +------------+-------------------------------------------------------------------+
    | J8o-J4o    | J8o, J7o, J6o, J5o, J4o                                           |
    +------------+-------------------------------------------------------------------+
    | 76s-74s    | 76s, 75s, 74s                                                     |
    +------------+-------------------------------------------------------------------+
    | J8-J4      | both ranges in suited an offsuited form;                          |
    |            | J8o, J7o, J6o, J5o, J4o, J8s, J7s, J6s, J5s, J4s                  |
    +------------+-------------------------------------------------------------------+
    | A5+        | either suited or offsuited hands that contains an Ace             |
    |            | and the other is bigger than 5. Same as "A5o+ A5s+".              |
    +------------+-------------------------------------------------------------------+
    | A5-        | downward, same as above                                           |
    +------------+-------------------------------------------------------------------+
    | XX         | every hand (100% range)                                           |
    |            | In this special case, pairs are also included (but only this)     |
    +------------+-------------------------------------------------------------------+
    | AX         | Any hand that contains an ace either suited or offsuit (no pairs) |
    +------------+-------------------------------------------------------------------+
    | AXo        | Any offsuit hand that contains an Ace (equivalent to A2o+)        |
    +------------+-------------------------------------------------------------------+
    | AXs        | Any suited hand that contains an Ace (equivalent to A2s+)         |
    +------------+-------------------------------------------------------------------+
    | QX+        | Any hand that contains a card bigger than a Jack; Q2+, K2+, A2+   |
    +------------+-------------------------------------------------------------------+
    | 5X-        | any hand that contains a card lower than 6                        |
    +------------+-------------------------------------------------------------------+
    | KXs+       | Any suited hand that contains a card bigger than a Queen          |
    +------------+-------------------------------------------------------------------+
    | KXo+       | same as above with offsuit hands                                  |
    +------------+-------------------------------------------------------------------+
    | 7Xs-       | same as above                                                     |
    +------------+-------------------------------------------------------------------+
    | 8Xo-       | same as above                                                     |
    +------------+-------------------------------------------------------------------+
    | 2s2h, AsKc | exact hand :term:`Combination`\ s                                 |
    +------------+-------------------------------------------------------------------+

    .. note::
        "Q+" and "Q-" are invalid ranges, because in Hold'em, there are two hands to start with not one.

Ranges are case insensitive, so ``"AKs"`` and ``"aks"`` and ``"aKS"`` means the same.
Also the order of the cards doesn't matter. ``"AK"`` is the same as ``"KA"``.
Hands can be separated by space (even multiple), comma, colon or semicolon, and combination of them (multiple spaces, etc.).


Normalization
-------------

Ranges should be rearranged and parsed according to these rules:

- hands separated with one space only in repr, with ", " in str representation
- in any given hand the first card is bigger than second (except pairs of course)
- pairs first, if hyphened, bigger first
- suited hands after pairs, descending by rank
- offsuited hands at the end


Range glossary
--------------

.. glossary::

    Suit
        One of |suits|. Alternatively '♣', '♦', '♥', '♠'.
        `According to Wikipedia <http://en.wikipedia.org/wiki/High_card_by_suit>`_, suits are ranked as:

        spades > hearts > diamonds > clubs

    Shape
        A hand can have three "Shapes" `according to Wikipedia <http://en.wikipedia.org/wiki/Texas_hold_'em_starting_hands#Essentials>`_.

        'o' for offsuit, 's' for suited hands '' for pairs.

    Rank
        One card without suit. One of |ranks|.

    Card
        One exact card with a suit. e.g. 'As', '2s'. It has a :term:`Rank` and a :term:`Suit`.

    Hand
        Consists two :term:`Rank`\ s without precise suits like "AKo", "22".

    Hand comparisons
        Comparisons in this library has nothing to do with equities or if a hand beats another.
        They are only defined so that a consistent ordering can be ensured when
        representing objects. If you want to compare hands by equity, use `pypoker-eval`_
        instead.

        Comparison rules:
            - pairs are 'better' than none-pairs
            - non-pairs are better if at least one of the cards are bigger
            - suited better than offsuit

    Combination
        Exact two cards with suits specified like "2s2c", "7s6c". There are total of 1326 Combinations.

    Range
        A range of hands with either in :term:`Hand` form or :term:`Combination`.
        e.g. "55+ AJo+ 7c6h 8s6s", "66-33 76o-73o AsJc 2s2h" or with other speical notation.
        (See above.)

    Range percent
        Compared to the total of 1326 hand :term:`Combination`\ s, how many are in the range?

    Range length
    Range size
        How many concrete hand :term:`Combination`\ s are in the range?

    Range is "bigger" than another
        If there are more hand :term:`Combination`\ s in it. (Equity vs each other doesn't matter here.)

    Token
        Denote one part of a range. In a "66-33 76o-73o AsJc 2s2h" range, there are 4 tokens:
        - "66-33" meaning 33, 44, 55, 66
        - "AsJc"  specific :term:`Combination`
        - "2s2h" a specific pair of deuces
        - "76o-73o"  several offsuit :term:`Hand`\ s

    Broadway Cards
        T, J, Q, K, A

    Face cards
        Only: J, Q, K.

        .. warning:: Ace is not a face card!


.. |ranks| replace:: '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'
.. |suits| replace:: 'c', 'd', 'h', or 's'

.. _pypoker-eval: http://pokersource.sourceforge.net/
