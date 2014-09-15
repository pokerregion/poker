Room specific operations
========================


Manipulating PokerStars player notes
------------------------------------

:class:`poker.room.pokerstars.Notes` class is capable of handling PokerStars Players notes.

You can add and delete labels, and notes, save the modifications to a new file or just print
the object instance and get the full XML.


.. code-block:: python

   >>> from poker.room.pokerstars import Notes
   >>> notes = Notes.from_file('notes.W2lkm2n.xml')
   >>> notes.players
   ('regplayer', 'sharkplayer', 'fishplayer', '"htmlchar"', '$dollarsign', 'nonoteforplayer',
    '-=strangename=-', '//ÄMGS', '0bullmarket0', 'CarlGardner', 'µ (x+t)', 'Walkman')

   >>> notes.labels
   (_Label(id='0', color='30DBFF', name='FISH'),
    _Label(id='1', color='30FF97', name='SHARK'),
    _Label(id='2', color='E1FF80', name='REG'),
    _Label(id='3', color='E1FF80', name='GENERAL'))

   >>> notes.add_label('NIT', 'FF0000')
   >>> notes.labels
   (_Label(id='0', color='30DBFF', name='FISH'),
    _Label(id='1', color='30FF97', name='SHARK'),
    _Label(id='2', color='E1FF80', name='REG'),
    _Label(id='3', color='E1FF80', name='GENERAL'))
    _Label(id='4', color='FF0000', name='NIT'))


For the full API, see the :doc:`api/room`.
