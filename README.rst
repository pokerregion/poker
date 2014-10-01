Poker framework for Python
==========================

|travis| |coveralls| |pythons| |release| |license| |wheel| |downloads|

A Python framework for poker related operations.

It contains classes for parsing card Suits, Cards, Hand combinations (called Combos),
construct hand Ranges and check for syntax, parse Hand histories.

It can get information from poker related websites like
Pocketfives, TwoplusTwo Forum, or PokerStars website by scraping them.
In the long term, it will have a fast hand evaluator and an equity calculator.

It uses the MIT license, soo it's code can be used in any product without legal consequences.

It aims quality, fully tested code and easy usability with nice APIs, suitable for beginners
to play with.


Documentation
-------------

https://poker.readthedocs.org/


Requirements
------------

* Python 2.7
* pytz
* requests
* lxml
* python-dateutil
* parsedatetime
* cacheed-property
* click
* enum34
* pathlib
* configparser

License
-------

The MIT License (MIT)

Copyright (c) 2013-2014 Kiss György


Repo and contact
----------------

| Repo: https://github.com/pokerregion/poker
| Issues: https://github.com/pokerregion/poker/issues
| `@Walkman_ <https://twitter.com/Walkman_>`_ on twitter
| or you can reach me on my `public Github e-mail <https://github.com/Walkman>`_.


.. |travis| image:: https://travis-ci.org/pokerregion/poker.svg?branch=master
   :target: https://travis-ci.org/pokerregion/poker

.. |coveralls| image:: https://coveralls.io/repos/pokerregion/poker/badge.png?branch=master
  :target: https://coveralls.io/r/pokerregion/poker?branch=master

.. |pythons| image:: https://pypip.in/py_versions/poker/badge.svg?style=flat
   :target: https://pypi.python.org/pypi/poker/
   :alt: Supported Python versions

.. |release| image:: https://pypip.in/version/poker/badge.svg?style=flat
   :target: https://pypi.python.org/pypi/poker/
   :alt: Latest Version

.. |license| image:: https://pypip.in/license/poker/badge.svg?style=flat
   :target: https://github.com/pokerregion/poker/blob/master/LICENSE
   :alt: MIT License

.. |downloads| image:: https://pypip.in/download/poker/badge.svg?style=flat
   :target: https://pypi.python.org/pypi/poker/
   :alt: Downloads

.. |wheel| image:: https://pypip.in/wheel/poker/badge.svg?style=flat
   :target: https://pypi.python.org/pypi/poker/
   :alt: Wheel package
