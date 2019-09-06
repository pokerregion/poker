import attr
import requests
from lxml import etree
from .._common import _make_float


__all__ = ["get_ranked_players", "WEBSITE_URL", "RANKINGS_URL"]


WEBSITE_URL = "http://www.pocketfives.com"
RANKINGS_URL = WEBSITE_URL + "/rankings/"


@attr.s(slots=True)
class _Player:
    """Pocketfives player data."""

    name = attr.ib()
    country = attr.ib()
    triple_crowns = attr.ib(convert=int)
    monthly_win = attr.ib(convert=int)
    biggest_cash = attr.ib()
    plb_score = attr.ib(convert=_make_float)
    biggest_score = attr.ib(convert=_make_float)
    average_score = attr.ib(convert=_make_float)
    previous_rank = attr.ib(convert=_make_float)


def get_ranked_players():
    """Get the list of the first 100 ranked players."""

    rankings_page = requests.get(RANKINGS_URL)
    root = etree.HTML(rankings_page.text)
    player_rows = root.xpath('//div[@id="ranked"]//tr')

    for row in player_rows[1:]:
        player_row = row.xpath('td[@class!="country"]//text()')
        yield _Player(
            name=player_row[1],
            country=row[1][0].get("title"),
            triple_crowns=player_row[3],
            monthly_win=player_row[4],
            biggest_cash=player_row[5],
            plb_score=player_row[6],
            biggest_score=player_row[7],
            average_score=player_row[8],
            previous_rank=player_row[9],
        )
