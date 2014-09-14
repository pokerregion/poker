Room specific classes API
=========================


Pokerstars player notes
-----------------------

.. currentmodule:: poker.room.pokerstars


.. autoclass:: Notes
   :members:
   :exclude-members: get_note, add_note, del_note

   .. automethod:: get_note

      :raises poker.room.pokerstars.NoteNotFoundError:

   .. automethod:: add_note

      :raises poker.room.pokerstars.LabelNotFoundError: if there is no such label name


   .. automethod:: del_note

      :raises poker.room.pokerstars.NoteNotFoundError:


.. autoclass:: _Label

   :ivar str id:     numeric id for the label. ``None`` when no label ('``-1``' in XML)
   :ivar str color:  color code for note
   :ivar str name:   name of the note

.. autoclass:: _Note

   :ivar str player:                player name
   :ivar str label:                 Label name of note
   :ivar datetime.datetime update:  when was the note last updated
   :ivar str text:                  Note text


.. autoexception:: NoteNotFoundError

.. autoexception:: LabelNotFoundError
