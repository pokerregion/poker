Card API
========

The :mod:`poker.card` module has three basic classes for dealing with card suits, card ranks
and cards. It also has a DECK, which is just a tuple of Cards.

.. currentmodule:: poker.card



Suit
----

.. autoclass:: poker.card.Suit

   Enumeration of the four :term:`Suit`\ s.



Rank
----

.. autoclass:: poker.card.Rank

   Enumeration of the 13 :term:`Rank`\ s.

   .. automethod:: difference

      :param str,Rank first:
      :param str,Rank second:
      :return: value of the difference (always positive)
      :rtype: int


.. data:: FACE_RANKS

   See :term:`Face card`


.. data:: BROADWAY_RANKS

   See :term:`Broadway card`



Card
----

.. autoclass:: poker.card.Card

   .. automethod:: make_random

      :rtype: :class:`Card`

   .. autoattribute:: is_face

      :type: bool

   .. autoattribute:: is_broadway

      :type: bool

   .. autoattribute:: rank

      :type: :class:`Rank`

   .. autoattribute:: suit

      :type: :class:`Suit`

