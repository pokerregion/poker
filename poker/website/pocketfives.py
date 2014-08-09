import requests
from bs4 import BeautifulSoup
from .._common import _make_float


POCKETFIVES_URL = 'http://www.pocketfives.com'
RANKINGS_URL = POCKETFIVES_URL + '/rankings/'


def get_ranked_players():
    """Get the list of ranked players. (Generator)"""

    rankings_page = requests.get(RANKINGS_URL)
    soup = BeautifulSoup(rankings_page.text, 'lxml')  # use lxml parser

    player_rows = soup.find(id='ranked').find_all('tr')
    players = []

    for row in player_rows[1:]:
        player_row = row.find_all('td')
        player = dict(
            name = player_row[0].img['alt'],
            # some players doesn't have a Country set, this would throw TypeError
            country = player_row[1].img['title'] if player_row[1].img else None,
            triple_crowns = int(player_row[2].string),
            monthly_win = int(player_row[3].string),
            biggest_cash = player_row[4].string,
            plb_score = _make_float(player_row[5].string),
            biggest_score = _make_float(player_row[6].string),
            average_score = _make_float(player_row[7].string),
            previous_rank = player_row[8].string,
        )

        yield player
