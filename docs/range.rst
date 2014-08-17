Range parsing
=============

The :class:`poker.hand.Range` class parses human readable (text) ranges like ``"22+ 54s 76s 98s AQo+"`` to a set of :term:`Hand`\ s and
hand :term:`Combo`\ s.

| Can parse ranges and compose parsed ranges into human readable form again.
| It's very fault-tolerant, so it's easy and fast to write ranges manually.
| Can normalize unprecise human readable ranges into a precise human readable form, like "22+ AQo+ 33 AKo" --> "22+ AQo+"
| Can tell how big a range is by :term:`Percentage <Range percent>` or number of :term:`Combo`\ s.


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
    | 2s2h, AsKc | exact hand :term:`Combo`\ s                                       |
    +------------+-------------------------------------------------------------------+

    .. note::
        "Q+" and "Q-" are invalid ranges, because in Hold'em, there are two hands to start with not one.

Ranges are case insensitive, so ``"AKs"`` and ``"aks"`` and ``"aKS"`` means the same.
Also the order of the cards doesn't matter. ``"AK"`` is the same as ``"KA"``.
Hands can be separated by space (even multiple), comma, colon or semicolon, and Combo of them (multiple spaces, etc.).


Normalization
-------------

Ranges should be rearranged and parsed according to these rules:

- hands separated with one space only in repr, with ", " in str representation
- in any given hand the first card is bigger than second (except pairs of course)
- pairs first, if hyphened, bigger first
- suited hands after pairs, descending by rank
- offsuited hands at the end
