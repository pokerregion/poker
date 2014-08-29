from collections import namedtuple
import requests
from lxml import etree
from .._common import _make_float


__all__ = ['get_ranked_players', 'WEBSITE_URL', 'RANKINGS_URL']


WEBSITE_URL = 'http://www.pocketfives.com'
RANKINGS_URL = WEBSITE_URL + '/rankings/'


_Player = namedtuple('_Player',
    'name '
    'country '
    'triple_crowns '
    'monthly_win '
    'biggest_cash '
    'plb_score '
    'biggest_score '
    'average_score '
    'previous_rank '
)
"""Named tuple for Pocketfives player data."""


def get_ranked_players():
    """Get the list of the first 100 ranked players."""

    rankings_page = requests.get(RANKINGS_URL)
    root = etree.HTML(rankings_page.text)
    player_rows = root.xpath('//div[@id="ranked"]//tr')

    for row in player_rows[1:]:
        player_row = row.xpath('td[@class!="country"]//text()')
        yield _Player(
            name = player_row[1],
            country = row[1][0].get('title'),
            triple_crowns = int(player_row[3]),
            monthly_win = int(player_row[4]),
            biggest_cash = player_row[5],
            plb_score = _make_float(player_row[6]),
            biggest_score = _make_float(player_row[7]),
            average_score = _make_float(player_row[8]),
            previous_rank = player_row[9],
        )
