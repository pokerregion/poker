Poker framework for Python
==========================

|travis| |coveralls| |pythons| |release| |license| |wheel| |downloads|

A Python framework for poker related operations.

It contains classes for parsing card Suits, Cards, Hand combinations (called Combos),
construct hand Ranges and check for syntax, parse Hand histories.

It can get information from poker related websites like
Pocketfives, TwoplusTwo Forum, or PokerStars website by scraping them.
In the long term, it will have a fast hand evaluator and an equity calculator.

It uses the MIT license, so its code can be used in any product without legal consequences.

It aims for quality, fully tested code and easy usability with nice APIs, suitable for beginners
to play with.


Documentation
-------------

https://poker.readthedocs.org/

State of the project
--------------------

As you can see, there is not much activity from me, because I don't play poker anymore and 
I don't have motivation to develop this library. The PokerStars parser is broken because 
a small change in PokerStars hand history format. A serious investment/donation would be
required to allow me to work on this library.


License
-------

The MIT License (MIT)

Copyright (c) 2013-2019 Kiss György


Repo and contact
----------------

| Repo: https://github.com/pokerregion/poker
| `@kissgyorgy <https://twitter.com/kissgyorgy>`_ on twitter
| or you can reach me on my `public Github e-mail <https://github.com/kissgyorgy>`_.


.. |travis| image:: https://travis-ci.org/pokerregion/poker.svg?branch=master
   :target: https://travis-ci.org/pokerregion/poker

.. |coveralls| image:: https://coveralls.io/repos/pokerregion/poker/badge.png?branch=master
  :target: https://coveralls.io/r/pokerregion/poker?branch=master

.. |pythons| image:: https://img.shields.io/pypi/pyversions/poker.svg
   :target: https://pypi.python.org/pypi/poker/
   :alt: Supported Python versions

.. |release| image:: https://img.shields.io/pypi/v/poker.svg
   :target: https://pypi.python.org/pypi/poker/
   :alt: Latest Version

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/pokerregion/poker/blob/master/LICENSE
   :alt: MIT License

.. |downloads| image:: https://img.shields.io/pypi/dm/poker.svg
   :target: https://pypi.python.org/pypi/poker/
   :alt: Downloads

.. |wheel| image:: https://img.shields.io/pypi/wheel/poker.svg
   :target: https://pypi.python.org/pypi/poker/
   :alt: Wheel package
