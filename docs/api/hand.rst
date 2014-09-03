Hand API
========

.. currentmodule:: poker.hand

Shape
-----

.. autoclass:: Shape

   See: :term:`Shape`

.. warning:: This might be removed in future version for simplify API.



Hand
----

.. autoclass:: poker.hand.Hand(hand)
   :members:
   :exclude-members: rank_difference, first, second, shape
   :undoc-members:

   :param str hand:    e.g. 'AKo', '22'

   :ivar Rank first:   first Rank
   :ivar Rank second:  second Rank
   :ivar Shape shape:  Hand shape (pair, suited or offsuit)

   .. autoattribute:: rank_difference

      :type: int

   .. autoattribute:: first

      :type:   :class:`poker.card.Rank`

   .. autoattribute:: second

      :type:   :class:`poker.card.Rank`

   .. autoattribute:: shape

      :type:   :class:`Shape`


.. autodata:: PAIR_HANDS

.. autodata:: OFFSUIT_HANDS

.. autodata:: SUITED_HANDS


Combo
-----

.. autoclass:: poker.hand.Combo
   :members:
   :exclude-members: first, second, shape
   :undoc-members:

   See :term:`Combo`

   .. autoattribute:: first

      :type:   :class:`poker.card.Card`

   .. autoattribute:: second

      :type:   :class:`poker.card.Card`

   .. autoattribute:: shape

      :type:   :class:`Shape`


Range
-----

.. autoclass:: poker.hand.Range
   :members:
   :exclude-members: hands, combos, percent, rep_pieces, to_html, to_ascii
   :undoc-members:

   :param str range:    Readable range in unicode

   .. note::

      All of the properties below are `cached_property`_, so make sure you invalidate the cache if you manipulate them!


   .. autoattribute:: hands

      :type: tuple of :class:`poker.hand.Hand`\ s


   .. autoattribute:: combos

      :type: tuple of :class:`poker.hand.Combo`\ s


   .. autoattribute:: percent

      :type: float (1-100)


   .. autoattribute:: rep_pieces

      :type: list of str

   .. automethod:: to_html

      :rtype: str

   .. automethod:: to_ascii

      :rtype: str


.. _cached_property: https://pypi.python.org/pypi/cached-property/
