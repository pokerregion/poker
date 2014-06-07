Rangeparser
===========

About
-----

Parses human readable (text) ranges like ``"22+ 54s 76s 98s AQo+"`` to a set of hands.

Contains classes for parsing, composing ranges, and checking for syntax.
Can parse ranges and compose parsed ranges into human readable form again.
It's very fault-tolerant, so it's easy to write ranges manually.
Can normalize unprecise human readable ranges into a precise human readable
form, like "22+ AQo+ 33 AKo" --> "22+ AQo+"

Can tell how big a range is by :term:`Percentage` or number of :term:`Combination`s.


Signs
-----

X
    means "any card"

2 3 4 5 6 7 8 9 T J Q K A
    Ace, King, Queen, Jack, Ten, 9, ...

"s" or "o" after hands like AKo or 76s
    suited and offsuit. Pairs have no suit (``''``)

-
    hands worse, down to deuces

+
    hands better, up to pairs


Defining ranges
---------------

Available formats for defining ranges:
    XX          - every hand (100% range)

    22          - one pair
    44+         - all pairs better than 33
    66-         - all pairs worse than 77
    55-33       - 55, 44, 33

    None of these below select pairs (for unambiguity):

    64s, 72s    - specific hands with suits

    AKo, J9o    - offsuit hands
    AKs, 72s    - suited hands

    AJo+        - offsuit hands above this: AJo, AQo, AKo
    AJs+        - same as offsuit
    Q8o+        - Q8o, Q9o, QTo, QJo
    A5o-        - offsuit hands; A5o-A2o
    A5s-        - suited hands; A5s-A2s
    K7          - suited and offsuited version of hand; K7o, K7s

    J8o-J4o     - J8o, J7o, J6o, J5o, J4o
    76s-74s     - 76s, 75s, 74s

    J8-J4       - both ranges in suited an offsuited form;
                  J8o, J7o, J6o, J5o, J4o, J8s, J7s, J6s, J5s, J4s

    A5+         - either suited or offsuited hands that contains an Ace
                  and the other is bigger than 5. Same as "A5o+ A5s+".
    A5-         - downward, same as above

    AX          - Any hand that contains an ace
    AXo         - Any offsuit hand that contains an Ace
    AXs         - Any suited hand that contains an Ace

    QX+         - Any hand that contains a card bigger than a King; Q2+, K2+, A2+
    KXs+        - Any suited hand that contains a card bigger than a Queen
    KXo+        - same as above with offsuit hands
    5X-         - any hand that contains a card lower than 6
    7Xs-        - see above
    8Xo-        - see above

    2s2h, AsKc  - exact hand :ref:`Combination`s

    76s+        - this is valid, although "+" is not neccessary,
                  because there are no suited cards above 76s

    .. note::
        "Q+" and "Q-" are invalid ranges, because in Hold'em, there are two hands to start with not one.

Ranges are case insensitive, so ``"AKs"`` and ``"aks"`` and ``"aKS"`` means the same.
Also the order of the cards doesn't matter. ``"AK"`` is the same as ``"KA"``.
Hands can be separated by space (even multiple), comma, colon or semicolon, and Combination of them.


Normalization
-------------

Ranges should be rearranged and parsed to the most succint possible according to these rules:
- hands separated with one space only
- in any given hand the first card is bigger than second (except pairs of course)
- pairs first, if hyphened, bigger first
- descending order by card value
- hands with X
- suited Hands
- offsuited hands at the end


Examples
--------

| Readable Range |                      Parsed range                      |
|----------------|--------------------------------------------------------|
| 88+            | {'AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88'}             |
| TT+ AKs        | {'AA', 'KK', 'QQ', 'JJ', 'TT', 'AKs'}                  |
| 22-33, 75s+    | {'22', '33', '75s', '76s'}                             |
| Kx             | {'K2s', 'K2o', 'K3s', 'K3o', ... , 'KK', 'KQo', 'KQs'} |
| Kxs or KXs     | {'K2s', 'K3s', 'K4s', ..., 'KQs', 'Aks'}               |


Suit ranking
------------

According to Wikipedia `High card by suit`_, suits are ranked as:
    spades > hearts > diamonds > clubs


.. glossary::

    Suit
        One of 'c', 'd', 'h', or 's'. Alternatively ♣, '♦', '♥', '♠'

    Rank
        One card without suit. One of |cards|.

    Card
        One exact card with a suit. e.g. 'As', '2s'. It has a :term:`Rank` and a :term:`Suit`.

    Hand
        Consists two :term:`Rank`s without precise suits like "AKo", "22".

    Hand equality
        -
        -
        - suited better than offsuit

    Combination
        Exact two cards with suits specified like "2s2c", "7s6c". There are total of 1326 Combinations.

    Range
        A range of hands with either in :term:`Hand` form or :term:`Combination`.
        e.g. "55+ AJo+ 7c6h 8s6s", "66-33 76o-73o AsJc 2s2h"

    Range syntax error
        A given :term:`Range` or :term:`Token` cannot be parsed because of bad format, non-card  symbol, invalid suit, etc.

    Range percent
        Compared to the total of 1326 hand :term:`Combination`s, how many are in the range?

    Range length
    Range size
        How many concrete hand :term:`Combination`s are in the range?

    Range is "bigger" than another
        If there are more hand :term:`Combination`s in it. (Equity vs each other doesn't matter here.)

    Token
        Denote one part of a range. In a "66-33 76o-73o AsJc 2s2h" there are 4 tokens:
        - "66-33" meaning 33, 44, 55, 66
        - "AsJc"  specific :term:`Combination`
        - "2s2h" a specific pair of deuces
        - "76o-73o"  several offsuit :term:`Hand`s

    Broadway Cards

    Face cards

    .. warning:: Ace is not a face card!

       Broadway cards are only: J, Q, K.
       If this confuses you, use is_broadway_card() instead!


.. _High card by suit: http://en.wikipedia.org/wiki/High_card_by_suit

.. |cards| replace:: ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
