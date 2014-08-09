Deck
====

Making a new deck is easy:

.. code-block:: python

    from poker.card import DECK
    import random

    newdeck = list(DECK)
    random.shuffle(newdeck)

    flop = [newdeck.pop() for __ in range(3)]
    turn = newdeck.pop()
    river = newdeck.pop()
