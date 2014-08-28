from collections import namedtuple
from dateutil.parser import parse as parse_date
import requests
from lxml import etree


__all__ = ['get_current_tournaments', 'get_status', 'POKERSTARS_URL', 'TOURNAMENTS_XML_URL']


POKERSTARS_URL = 'http://www.pokerstars.eu'
TOURNAMENTS_XML_URL = POKERSTARS_URL + '/datafeed_global/tournaments/all.xml'
STATUS_URL = 'http://www.psimg.com/datafeed/dyn_banners/summary.json.js'


_PokerStarsTournament = namedtuple('PokerStarsTournament',
    'start_date '
    'name '
    'game '
    'buyin '
    'players '
)
"""Named tuple for upcoming pokerstars tournaments."""


def _getvalue(parent, tagname):
    return parent.find('{*}' + tagname).text


def get_current_tournaments():
    """Get the next 200 tournaments from pokerstars."""
    schedule_page = requests.get(TOURNAMENTS_XML_URL)
    root = etree.XML(schedule_page.content)

    for tour in root.iter('{*}tournament'):
        yield _PokerStarsTournament(
            start_date = parse_date(_getvalue(tour, 'start_date')),
            name = _getvalue(tour, 'name'),
            game = _getvalue(tour, 'game'),
            buyin = _getvalue(tour, 'buy_in_fee'),
            players = int(tour.get('players'))
        )


