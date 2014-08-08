Testing
=======

All the unit tests are written in `pytest`_. I choose it because it offers very nice funcionality,
and no-boilerplate code for tests. No need to sublass anything, just prefix classes with ``Test``
and methods with ``test_``.

All assertion use the default python ``assert`` keyword.

To run the tests, just invoke::

    $ python setup.py test

Or alternatively install pytest and run it directly::

    $ pip install pytest
    $ py.test

from the module directory and `pytest`_ will automatically pick up all unit tests.

.. _pytest: http://pytest.org/
