Contributing
============

Coding style
------------

PEP8 except for line length, which is 99 max (hard limit).
If your code exceeds 99 characters, you do something wrong anyway, you need to refactor it
(e.g. to deeply nested, harder to understand)


New hand history parser
-----------------------

If you want to support a new poker room, do this:

.. code-block:: python

    class PokerRoomHandHistory(HandHistory):
        """Implement PokerRoom specific parsing."""

        def parse_header(self):
            # Parse header only! Usually just first line. The whole purpose is to do it fast.
            # No need to call super()

        def parse(self):
            # base class method strips and saves raw hand history
            super(PokerRoomHand, self).parse()

            # ...


You **have to** provide all common attributes, and *may* provide PokerRoom specific extra
attributes described in the base :class:`poker.handhistory.HandHistory` class API documentation.
