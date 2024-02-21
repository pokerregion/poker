import attr
import requests
from dateutil.parser import parse as parse_date
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

    start_date = attr.ib(converter=parse_date)
    name = attr.ib()
    game = attr.ib()
    buyin = attr.ib()
    players = attr.ib(converter=int)


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

    updated = attr.ib(converter=parse_date)
    next_update = attr.ib()
    sites = attr.ib()  # list of sites, including Play Money


@attr.s(slots=True)
class _SiteStatus:
    """PokerStars status on different subsites like FR, ES IT or Play Money."""

    id = attr.ib()  # "COM", "FR", "ES", "IT"
    tables = attr.ib()
    players = attr.ib()
    active_tournaments = attr.ib(converter=int)
    total_tournaments = attr.ib(converter=int, default=0)
    play_money = attr.ib(default=0)
    clubs = attr.ib(default=0)
    club_members = attr.ib(default=0)


def get_status():
    """Get pokerstars status: players online, number of tables, etc."""

    res = requests.get(STATUS_URL)
    # breakpoint()
    status = res.json()["tournaments"]["host"]
    sites = status.pop("site")
    sites = tuple(_SiteStatus(**site) for site in sites)

    return _Status(
        sites=sites, updated=status["updated"], next_update=status["next_update"]
    )
