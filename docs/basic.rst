Basic operations
================


Card suits
----------

Enumeration of suits::

   >>> from poker import Suit
   >>> list(Suit)
   [Suit('♣'), Suit('♦'), Suit('♥'), Suit('♠')]

Suits are comparable::

    >>> Suit.CLUBS < Suit.DIAMONDS
    True


Card ranks
----------

Enumeration of ranks::

   >>> from poker import Rank
   >>> list(Rank)
   [Rank('2'), Rank('3'), Rank('4'), Rank('5'), Rank('6'), Rank('7'), Rank('8'), Rank('9'), Rank('T'), Rank('J'), Rank('Q'), Rank('K'), Rank('A')]

Ranks are comparable::

    >>> Rank('2') < Rank('A')
    True

Making a random Rank::

   >> Rank.make_random()
   Rank('2')


Cards
-----

Making a random Card::

   >>> Card.make_random()
   Card('As')

Comparing Cards::

   >>> Card('As') > Card('Ks')
   True
   >>> Card('Tc') < Card('Td')
   True


Implementing a deck
-------------------

A deck is just a list of :class:`poker.card.Card`\ s.
Making a new deck and simulating shuffling is easy::

    import random
    from poker import Card

    deck = list(Card)
    random.shuffle(deck)

    flop = [deck.pop() for __ in range(3)]
    turn = deck.pop()
    river = deck.pop()


Operations with Hands and Combos
--------------------------------

.. code-block:: python

    >>> from poker.hand import Hand, Combo


List of all hands::

   >>> list(Hand)
   [Hand('32o'), Hand('32s'), Hand('42o'), Hand('42s'), Hand('43o'), Hand('43s'), Hand('52o'),
    ..., Hand('JJ'), Hand('QQ'), Hand('KK'), Hand('AA')]


Comparing::

    >>> Hand('AAd') > Hand('KK')
    True
    >>> Combo('7s6s') > Combo('6d5d')
    True

Sorting::

    >>> sorted([Hand('22'), Hand('66'), Hand('76o')])
    [Hand('76o'), Hand('22'), Hand('66')]

Making a random hand::

    >>> Hand.make_random()
    Hand('AJs')
