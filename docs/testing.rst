Testing
=======

The framework contains a lot of tests (over 400). The basic elements like Card, Hand, Range, etc.
are fully tested.

All the unit tests are written in `pytest`_. I choose it because it offers very nice funcionality,
and no-boilerplate code for tests. No need to sublass anything, just prefix classes with ``Test``
and methods with ``test_``.

All assertion use the default python ``assert`` keyword.

To run the tests, just invoke::

    $ python setup.py test

Or alternatively you need to install the pacakge itself::

    $ python setup.py develop

or::

    $ pip install -e .

and install `pytest`_ and run it directly::

    $ pip install pytest
    $ cd poker
    $ py.test

from the poker module directory and `pytest`_ will automatically pick up all unit tests.

.. _pytest: http://pytest.org/
