Glossary
========


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

    Combo
        Exact two cards with suits specified like "2s2c", "7s6c". There are total of 1326 Combos.

    Range
        A range of hands with either in :term:`Hand` form or :term:`Combo`.
        e.g. "55+ AJo+ 7c6h 8s6s", "66-33 76o-73o AsJc 2s2h" or with other speical notation.
        (See above.)

    Range percent
        Compared to the total of 1326 hand :term:`Combo`\ s, how many are in the range?

    Range length
    Range size
        How many concrete hand :term:`Combo`\ s are in the range?

    Range is "bigger" than another
        If there are more hand :term:`Combo`\ s in it. (Equity vs each other doesn't matter here.)

    Token
        Denote one part of a range. In a "66-33 76o-73o AsJc 2s2h" range, there are 4 tokens:
        - "66-33" meaning 33, 44, 55, 66
        - "AsJc"  specific :term:`Combo`
        - "2s2h" a specific pair of deuces
        - "76o-73o"  several offsuit :term:`Hand`\ s

    Broadway card
        T, J, Q, K, A

    Face card
        Only: J, Q, K.

        .. warning:: Ace is not a face card!


.. |ranks| replace:: '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'
.. |suits| replace:: 'c', 'd', 'h', or 's'

.. _pypoker-eval: http://pokersource.sourceforge.net/
