Deck
====

Making a new deck is easy:

.. code-block:: python

    from poker.rangeparser import DECK
    import random

    newdeck = list(DECK)
    random.shuffle(newdeck)

    flop = newdeck.pop()
    turn = newdeck.pop()
    river = newdeck.pop()
