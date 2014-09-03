Range parsing
=============

The :class:`poker.hand.Range` class parses human readable (text) ranges like ``"22+ 54s 76s 98s AQo+"`` to a set of :term:`Hand`\ s and
hand :term:`Combo`\ s.

| Can parse ranges and compose parsed ranges into human readable form again.
| It's very fault-tolerant, so it's easy and fast to write ranges manually.
| Can normalize unprecise human readable ranges into a precise human readable form, like ``"22+ AQo+ 33 AKo"`` --> ``"22+ AQo+"``
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


Printing the range as an HTML table
-----------------------------------

Range has a method :meth:`to_html() <poker.hand.Range.to_html>`. When you print the result of that, you get a simple HTML table representation of it.

``Range('XX').to_html()`` looks like this:

.. raw:: html

   <table class="range"><tr><td class="pair">AA</td><td class="suited">AKs</td><td class="suited">AQs</td><td class="suited">AJs</td><td class="suited">ATs</td><td class="suited">A9s</td><td class="suited">A8s</td><td class="suited">A7s</td><td class="suited">A6s</td><td class="suited">A5s</td><td class="suited">A4s</td><td class="suited">A3s</td><td class="suited">A2s</td></tr><tr><td class="offsuit">AKo</td><td class="pair">KK</td><td class="suited">KQs</td><td class="suited">KJs</td><td class="suited">KTs</td><td class="suited">K9s</td><td class="suited">K8s</td><td class="suited">K7s</td><td class="suited">K6s</td><td class="suited">K5s</td><td class="suited">K4s</td><td class="suited">K3s</td><td class="suited">K2s</td></tr><tr><td class="offsuit">AQo</td><td class="offsuit">KQo</td><td class="pair">QQ</td><td class="suited">QJs</td><td class="suited">QTs</td><td class="suited">Q9s</td><td class="suited">Q8s</td><td class="suited">Q7s</td><td class="suited">Q6s</td><td class="suited">Q5s</td><td class="suited">Q4s</td><td class="suited">Q3s</td><td class="suited">Q2s</td></tr><tr><td class="offsuit">AJo</td><td class="offsuit">KJo</td><td class="offsuit">QJo</td><td class="pair">JJ</td><td class="suited">JTs</td><td class="suited">J9s</td><td class="suited">J8s</td><td class="suited">J7s</td><td class="suited">J6s</td><td class="suited">J5s</td><td class="suited">J4s</td><td class="suited">J3s</td><td class="suited">J2s</td></tr><tr><td class="offsuit">ATo</td><td class="offsuit">KTo</td><td class="offsuit">QTo</td><td class="offsuit">JTo</td><td class="pair">TT</td><td class="suited">T9s</td><td class="suited">T8s</td><td class="suited">T7s</td><td class="suited">T6s</td><td class="suited">T5s</td><td class="suited">T4s</td><td class="suited">T3s</td><td class="suited">T2s</td></tr><tr><td class="offsuit">A9o</td><td class="offsuit">K9o</td><td class="offsuit">Q9o</td><td class="offsuit">J9o</td><td class="offsuit">T9o</td><td class="pair">99</td><td class="suited">98s</td><td class="suited">97s</td><td class="suited">96s</td><td class="suited">95s</td><td class="suited">94s</td><td class="suited">93s</td><td class="suited">92s</td></tr><tr><td class="offsuit">A8o</td><td class="offsuit">K8o</td><td class="offsuit">Q8o</td><td class="offsuit">J8o</td><td class="offsuit">T8o</td><td class="offsuit">98o</td><td class="pair">88</td><td class="suited">87s</td><td class="suited">86s</td><td class="suited">85s</td><td class="suited">84s</td><td class="suited">83s</td><td class="suited">82s</td></tr><tr><td class="offsuit">A7o</td><td class="offsuit">K7o</td><td class="offsuit">Q7o</td><td class="offsuit">J7o</td><td class="offsuit">T7o</td><td class="offsuit">97o</td><td class="offsuit">87o</td><td class="pair">77</td><td class="suited">76s</td><td class="suited">75s</td><td class="suited">74s</td><td class="suited">73s</td><td class="suited">72s</td></tr><tr><td class="offsuit">A6o</td><td class="offsuit">K6o</td><td class="offsuit">Q6o</td><td class="offsuit">J6o</td><td class="offsuit">T6o</td><td class="offsuit">96o</td><td class="offsuit">86o</td><td class="offsuit">76o</td><td class="pair">66</td><td class="suited">65s</td><td class="suited">64s</td><td class="suited">63s</td><td class="suited">62s</td></tr><tr><td class="offsuit">A5o</td><td class="offsuit">K5o</td><td class="offsuit">Q5o</td><td class="offsuit">J5o</td><td class="offsuit">T5o</td><td class="offsuit">95o</td><td class="offsuit">85o</td><td class="offsuit">75o</td><td class="offsuit">65o</td><td class="pair">55</td><td class="suited">54s</td><td class="suited">53s</td><td class="suited">52s</td></tr><tr><td class="offsuit">A4o</td><td class="offsuit">K4o</td><td class="offsuit">Q4o</td><td class="offsuit">J4o</td><td class="offsuit">T4o</td><td class="offsuit">94o</td><td class="offsuit">84o</td><td class="offsuit">74o</td><td class="offsuit">64o</td><td class="offsuit">54o</td><td class="pair">44</td><td class="suited">43s</td><td class="suited">42s</td></tr><tr><td class="offsuit">A3o</td><td class="offsuit">K3o</td><td class="offsuit">Q3o</td><td class="offsuit">J3o</td><td class="offsuit">T3o</td><td class="offsuit">93o</td><td class="offsuit">83o</td><td class="offsuit">73o</td><td class="offsuit">63o</td><td class="offsuit">53o</td><td class="offsuit">43o</td><td class="pair">33</td><td class="suited">32s</td></tr><tr><td class="offsuit">A2o</td><td class="offsuit">K2o</td><td class="offsuit">Q2o</td><td class="offsuit">J2o</td><td class="offsuit">T2o</td><td class="offsuit">92o</td><td class="offsuit">82o</td><td class="offsuit">72o</td><td class="offsuit">62o</td><td class="offsuit">52o</td><td class="offsuit">42o</td><td class="offsuit">32o</td><td class="pair">22</td></tr></table>


You can format it with CSS, you only need to define ``td.pair``, ``td.offsuit`` and ``td.suited`` selectors.
It's easy to recreate PokerStove style colors:

.. code-block:: html

   <style>
      td {
         /* Make cells same width and height and centered */
         width: 30px;
         height: 30px;
         text-align: center;
         vertical-align: middle;
      }
      td.pair {
         background: #aaff9f;
      }
      td.offsuit {
         background: #bbced3;
      }
      td.suited {
         background: #e37f7d;
      }
   </style>

.. raw:: html

   <style>
      #styled_range td {
         width: 30px;
         height: 30px;
         text-align: center;
         vertical-align: middle;
      }
      #styled_range td.pair {
         background: #aaff9f;
      }
      #styled_range td.offsuit {
         background: #bbced3;
      }
      #styled_range td.suited {
         background: #e37f7d;
      }
   </style>
   <table id="styled_range" class="range"><tr><td class="pair">AA</td><td class="suited">AKs</td><td class="suited">AQs</td><td class="suited">AJs</td><td class="suited">ATs</td><td class="suited">A9s</td><td class="suited">A8s</td><td class="suited">A7s</td><td class="suited">A6s</td><td class="suited">A5s</td><td class="suited">A4s</td><td class="suited">A3s</td><td class="suited">A2s</td></tr><tr><td class="offsuit">AKo</td><td class="pair">KK</td><td class="suited">KQs</td><td class="suited">KJs</td><td class="suited">KTs</td><td class="suited">K9s</td><td class="suited">K8s</td><td class="suited">K7s</td><td class="suited">K6s</td><td class="suited">K5s</td><td class="suited">K4s</td><td class="suited">K3s</td><td class="suited">K2s</td></tr><tr><td class="offsuit">AQo</td><td class="offsuit">KQo</td><td class="pair">QQ</td><td class="suited">QJs</td><td class="suited">QTs</td><td class="suited">Q9s</td><td class="suited">Q8s</td><td class="suited">Q7s</td><td class="suited">Q6s</td><td class="suited">Q5s</td><td class="suited">Q4s</td><td class="suited">Q3s</td><td class="suited">Q2s</td></tr><tr><td class="offsuit">AJo</td><td class="offsuit">KJo</td><td class="offsuit">QJo</td><td class="pair">JJ</td><td class="suited">JTs</td><td class="suited">J9s</td><td class="suited">J8s</td><td class="suited">J7s</td><td class="suited">J6s</td><td class="suited">J5s</td><td class="suited">J4s</td><td class="suited">J3s</td><td class="suited">J2s</td></tr><tr><td class="offsuit">ATo</td><td class="offsuit">KTo</td><td class="offsuit">QTo</td><td class="offsuit">JTo</td><td class="pair">TT</td><td class="suited">T9s</td><td class="suited">T8s</td><td class="suited">T7s</td><td class="suited">T6s</td><td class="suited">T5s</td><td class="suited">T4s</td><td class="suited">T3s</td><td class="suited">T2s</td></tr><tr><td class="offsuit">A9o</td><td class="offsuit">K9o</td><td class="offsuit">Q9o</td><td class="offsuit">J9o</td><td class="offsuit">T9o</td><td class="pair">99</td><td class="suited">98s</td><td class="suited">97s</td><td class="suited">96s</td><td class="suited">95s</td><td class="suited">94s</td><td class="suited">93s</td><td class="suited">92s</td></tr><tr><td class="offsuit">A8o</td><td class="offsuit">K8o</td><td class="offsuit">Q8o</td><td class="offsuit">J8o</td><td class="offsuit">T8o</td><td class="offsuit">98o</td><td class="pair">88</td><td class="suited">87s</td><td class="suited">86s</td><td class="suited">85s</td><td class="suited">84s</td><td class="suited">83s</td><td class="suited">82s</td></tr><tr><td class="offsuit">A7o</td><td class="offsuit">K7o</td><td class="offsuit">Q7o</td><td class="offsuit">J7o</td><td class="offsuit">T7o</td><td class="offsuit">97o</td><td class="offsuit">87o</td><td class="pair">77</td><td class="suited">76s</td><td class="suited">75s</td><td class="suited">74s</td><td class="suited">73s</td><td class="suited">72s</td></tr><tr><td class="offsuit">A6o</td><td class="offsuit">K6o</td><td class="offsuit">Q6o</td><td class="offsuit">J6o</td><td class="offsuit">T6o</td><td class="offsuit">96o</td><td class="offsuit">86o</td><td class="offsuit">76o</td><td class="pair">66</td><td class="suited">65s</td><td class="suited">64s</td><td class="suited">63s</td><td class="suited">62s</td></tr><tr><td class="offsuit">A5o</td><td class="offsuit">K5o</td><td class="offsuit">Q5o</td><td class="offsuit">J5o</td><td class="offsuit">T5o</td><td class="offsuit">95o</td><td class="offsuit">85o</td><td class="offsuit">75o</td><td class="offsuit">65o</td><td class="pair">55</td><td class="suited">54s</td><td class="suited">53s</td><td class="suited">52s</td></tr><tr><td class="offsuit">A4o</td><td class="offsuit">K4o</td><td class="offsuit">Q4o</td><td class="offsuit">J4o</td><td class="offsuit">T4o</td><td class="offsuit">94o</td><td class="offsuit">84o</td><td class="offsuit">74o</td><td class="offsuit">64o</td><td class="offsuit">54o</td><td class="pair">44</td><td class="suited">43s</td><td class="suited">42s</td></tr><tr><td class="offsuit">A3o</td><td class="offsuit">K3o</td><td class="offsuit">Q3o</td><td class="offsuit">J3o</td><td class="offsuit">T3o</td><td class="offsuit">93o</td><td class="offsuit">83o</td><td class="offsuit">73o</td><td class="offsuit">63o</td><td class="offsuit">53o</td><td class="offsuit">43o</td><td class="pair">33</td><td class="suited">32s</td></tr><tr><td class="offsuit">A2o</td><td class="offsuit">K2o</td><td class="offsuit">Q2o</td><td class="offsuit">J2o</td><td class="offsuit">T2o</td><td class="offsuit">92o</td><td class="offsuit">82o</td><td class="offsuit">72o</td><td class="offsuit">62o</td><td class="offsuit">52o</td><td class="offsuit">42o</td><td class="offsuit">32o</td><td class="pair">22</td></tr></table>


Printing the range as an ASCII table
------------------------------------

:meth:`to_ascii() <poker.hand.Range.to_ascii>` can print a nicely formatted ASCII table to the
terminal:

.. code-block:: python

   >>> print(Range('22+ A2+ KT+ QJ+ 32 42 52 62 72').to_ascii())
   AA  AKs AQs AJs ATs A9s A8s A7s A6s A5s A4s A3s A2s
   AKo KK  KQs KJs KTs
   AQo KQo QQ  QJs
   AJo KJo QJo JJ
   ATo KTo         TT
   A9o                 99
   A8o                     88
   A7o                         77                  72s
   A6o                             66              62s
   A5o                                 55          52s
   A4o                                     44      42s
   A3o                                         33  32s
   A2o                         72o 62o 52o 42o 32o 22
