from collections import namedtuple
import dateutil.parser
import requests
from bs4 import BeautifulSoup


__all__ = ['get_current_tournaments', 'PokerStarsTournament',
           'POKERSTARS_URL', 'TOURNAMENTS_XML_URL']


POKERSTARS_URL = 'http://www.pokerstars.eu'
TOURNAMENTS_XML_URL = POKERSTARS_URL + '/datafeed_global/tournaments/all.xml'


class PokerStarsTournament(namedtuple('PokerStarsTournament',
                           'start_date name game buyin players')):
    """Named tuple for upcoming pokerstars tournaments."""


def get_current_tournaments():
    """Get the next 200 tournaments from pokerstars."""

    schedule_page = requests.get(TOURNAMENTS_XML_URL)
    soup = BeautifulSoup(schedule_page.text, 'xml')

    tournament_nodes = soup.find_all('tournament')
    tournaments = []

    for tour in tournament_nodes:
        tournament = PokerStarsTournament(
            start_date = dateutil.parser.parse(tour.start_date.string),
            name = tour.find('name').string,
            game = tour.game.string,
            buyin = tour.buy_in_fee.string,
            players = int(tour['players'])
        )

        yield tournament
