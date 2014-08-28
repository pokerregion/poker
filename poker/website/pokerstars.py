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


_PokerStarsStatus = namedtuple('PokerStarsStatus',
    'updated '
    'tables '
    'next_update '
    'players '
    'clubs '
    'active_tournaments '
    'total_tournaments '
    'sites '                # list of sites, including Play Money
    'club_members '
)


_PokerStarsSiteStatus = namedtuple('PokerStarsSiteStatus',
    'id '       # ".FR", ".ES", ".IT" or 'Play Money'
    'tables '
    'players '
    'active_tournaments '
)


def get_status():
    """Get pokerstars status: players online, number of tables, etc."""

    res = requests.get(STATUS_URL)
    status = res.json()['tournaments']['summary']

    # move all sites under sites attribute, including play money
    sites = status.pop('site')
    play_money = status.pop('play_money')
    play_money['id'] = 'Play Money'
    sites.append(play_money)
    sites = tuple(_PokerStarsSiteStatus(**site) for site in sites)

    updated = parse_date(status.pop('updated'))

    return _PokerStarsStatus(sites=sites, updated=updated, **status)
