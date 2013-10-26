-----------------
API documentation
-----------------

.. automodule:: handparser
   :members:
   :member-order: groupwise
   :exclude-members: PokerHand

   .. autoclass:: PokerHand(hand_text, [, parse=True])

      .. method:: __init__(self, hand_text [, parse=True])

         Save raw hand history

         :param str hand_text:  poker hand text
         :param bool parse:     if ``False``, hand will not parsed immediately.
                                Useful if you just want to quickly check header first and maybe process it later.
