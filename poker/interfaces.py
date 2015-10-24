# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function

from zope.interface import Interface, Attribute


class IStreet(Interface):
    actions = Attribute('_StreetAction instances.')
    cards = Attribute('Cards.')
    pot = Attribute('Pot size after actions.')


class IHandHistory(Interface):
    """Interface for all hand histories. Not all attributes are available in all room's hand
    histories, missing attributes are always None. This contains the most properties, available in
    any pokerroom hand history, so you always have to deal with None values.
    """
    # parsing information
    header_parsed = Attribute('Shows wheter header is parsed already or not.')
    parsed = Attribute('Shows wheter the whole hand history is parsed already or not.')
    date = Attribute('Date of the hand history.')

    # Street informations
    preflop = Attribute('_Street instance for preflop actions.')
    flop = Attribute('_Street instance for flop actions.')
    turn = Attribute('_Street instance for turn actions.')
    river = Attribute('_Street instance for river actions.')
    show_down = Attribute('_Street instance for showdown.')

    # Player informations
    table_name = Attribute('Name of')
    max_players = Attribute('Maximum number of players can sit on the table.')
    players = Attribute('Tuple of player instances.')
    hero = Attribute('_Player instance with hero data.')
    button = Attribute('_Player instance of button.')
    winners = Attribute('Tuple of _Player instances with winners.')

    # Game informations
    game_type = Attribute('GameType enum value (CASH, TOUR or SNG)')
    sb = Attribute('Small blind size.')
    bb = Attribute('Big blind size.')
    buyin = Attribute('Buyin with rake.')
    rake = Attribute('Rake only.')
    game = Attribute('Game enum value (HOLDEM, OMAHA? OHILO, RAZZ or STUD)')
    limit = Attribute('Limit enum value (NL, PL or FL)')
    ident = Attribute('Unique id of the hand history.')
    currency = Attribute('Currency of the hand history.')
    total_pot = Attribute('Total pot Decimal.')

    tournament_ident = Attribute('Unique tournament id.')
    tournament_name = Attribute('Name of the tournament.')
    tournament_level = Attribute('Tournament level.')

    def parse_header():
        """Parses only the header of a hand history. It is used for quick looking into the hand
        history for basic informations:
            ident, date, game, game_type, limit, money_type, sb, bb, buyin, rake, currency
        by parsing the least lines possible to get these.
        """

    def parse():
        """Parses the body of the hand history, but first parse header if not yet parsed."""

