import attr
from dateutil.parser import parse as parse_date
import requests
from lxml import etree


__all__ = [
    "get_current_tournaments",
    "get_status",
    "WEBSITE_URL",
    "TOURNAMENTS_XML_URL",
    "STATUS_URL",
]


WEBSITE_URL = "http://www.pokerstars.eu"
TOURNAMENTS_XML_URL = WEBSITE_URL + "/datafeed_global/tournaments/all.xml"
STATUS_URL = "http://www.psimg.com/datafeed/dyn_banners/summary.json.js"


@attr.s(slots=True)
class _Tournament:
    """Upcoming pokerstars tournament."""

    start_date = attr.ib(convert=parse_date)
    name = attr.ib()
    game = attr.ib()
    buyin = attr.ib()
    players = attr.ib(convert=int)


def get_current_tournaments():
    """Get the next 200 tournaments from pokerstars."""

    schedule_page = requests.get(TOURNAMENTS_XML_URL)
    root = etree.XML(schedule_page.content)

    for tour in root.iter("{*}tournament"):
        yield _Tournament(
            start_date=tour.findtext("{*}start_date"),
            name=tour.findtext("{*}name"),
            game=tour.findtext("{*}game"),
            buyin=tour.findtext("{*}buy_in_fee"),
            players=tour.get("players"),
        )


@attr.s(slots=True)
class _Status:
    """PokerStars status."""

    updated = attr.ib(convert=parse_date)
    tables = attr.ib()
    next_update = attr.ib()
    players = attr.ib()
    clubs = attr.ib()
    active_tournaments = attr.ib()
    total_tournaments = attr.ib()
    sites = attr.ib()  # list of sites, including Play Money
    club_members = attr.ib()


@attr.s(slots=True)
class _SiteStatus:
    """PokerStars status on different subsites like FR, ES IT or Play Money."""

    id = attr.ib()  # ".FR", ".ES", ".IT" or 'Play Money'
    tables = attr.ib()
    players = attr.ib()
    active_tournaments = attr.ib()


def get_status():
    """Get pokerstars status: players online, number of tables, etc."""

    res = requests.get(STATUS_URL)
    status = res.json()["tournaments"]["summary"]

    # move all sites under sites attribute, including play money
    sites = status.pop("site")
    play_money = status.pop("play_money")
    play_money["id"] = "Play Money"
    sites.append(play_money)
    sites = tuple(_SiteStatus(**site) for site in sites)

    return _Status(sites=sites, updated=status.pop("updated"), **status)
