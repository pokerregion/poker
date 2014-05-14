Rangeparser
===========

About
-----

Parses human readable ranges like "22+ 54s 76s 98s AQo+" to a set of hands.

Contains functions for parsing, composing ranges, and checking for syntax.
Can parse ranges and compose parsed ranges into human readable form again.
It's very fault-tolerant, so it's easy to write ranges manually.
Can normalize unprecise human readable ranges into a precise human readable
form, like "22+ AQo+ 33 AKo" --> "22+ AQo+"

Can tell how big a range is by percentage or number of hand combinations.
(Hand combination: AhKs or 2c2d)


Signs
-----

X
    jolly joker, means "any card"

A K Q J T 9 8 7 6 5 4 3 2
    Ace, King, Queen, Jack, Ten, 9, ...

"s" or "o" after hands like AKo or 76s
    suited and offsuit

-
    hands worse down to deuces

+
    hands better, up to pairs


Defining ranges
---------------

Available formats for defining ranges:
    XX      - every hand (100% range)

    22      - one pair
    44+     - all pairs better than 33
    66-     - all pairs worse than 77
    55-33   - 55, 44, 33

    None of these below select pairs (unambiguity):

    64s, 72s - specific hands with suits

    AKo, J9o - offsuit hands
    AKs, 72s - suited hands

    AJo+    - offsuit hands above this: AJo, AQo, AKo
    AJs+    - same as offsuit
    Q8o+    - Q8o, Q9o, QTo, QJo
    A5o-    - offsuit hands; A5o-A2o
    A5s-    - suited hands; A5s-A2s

    J8o-J4o - J8o, J7o, J6o, J5o, J4o
    76s-74s - 76s, 75s, 74s

    A5+     - either suited or offsuited hands that contains an Ace and the other is bigger than 5
              same as "A5o+ A5s+"
    A5-     - downward, same as above

    AX      - Any hand that contains an ace
    AXo     - Any offsuit hand that contains an Ace
    AXs     - Any suited hand that contains an Ace

    QX+     - Any hand that contains a card bigger than a King; Q2+, K2+, A2+
    KXs+    - Any suited hand that contains a card bigger than a Queen
    KXo+    - same as above with offsuit hands
    5X-     - any hand that contains a card lower than 6
    7Xs-    - see above
    8Xo-    - see above

    76s+    - this is valid, although "+" not neccessary, because there are no suited cards above 76s

    .. note::
        "Q+" and "Q-" are invalid ranges, because in Hold'em, there are two hands to start with not one.

Ranges are case insensitive, so ``"AKs"`` and ``"aks"`` and ``"aKS"`` means the same.
Also the order of the cards doesn't matter. ``"AK"`` is the same as ``"KA"``.
Hands can be separated by space (even multiple), comma, colon or semicolon, and combination of them.


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


Glossary
--------

Hand
    Two cards without precise suits like "AKo", "22".

Combination
    Exact two cards with suits specified like "2s2c", "7s6c".

Range
    A range of hands with either in Hand (general) form or Combination.
    e.g. "55+ AJo+ 7c6h 8s6s", "66-33 76o-73o AsJc 2s2h"

Range syntax error
    A given range cannot be parsed because of bad format

Range percent
    Compared to the total of 1326 hand combinations, how many are in the range?

Range "length" or range size
    How many concreta hands combinations are in the range?
