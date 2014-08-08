import requests
from bs4 import BeautifulSoup


POCKETFIVES_URL = 'http://www.pocketfives.com'
RANKINGS_URL = POCKETFIVES_URL + '/rankings/'


def _make_float(tag):
    return float(tag.string.replace(',', ''))


def get_ranked_players():
    rankings_page = requests.get(RANKINGS_URL)
    soup = BeautifulSoup(rankings_page.text, 'lxml')  # use lxml parser

    player_rows = soup.find(id='ranked').find_all('tr')
    players = []

    for row in player_rows[1:]:
        player_row = row.find_all('td')
        player = dict(
            name = player_row[0].img['alt'],
            # some players doesn't have a Country set, this would throw TypeError
            country = player_row[1].img['title'] if player_row[1].img else None
            triple_crowns = int(player_row[2].string)
            monthly_win = int(player_row[3].string)
            biggest_cash = player_row[4].string
            plb_score = _make_float(player_row[5])
            biggest_score = _make_float(player_row[6])
            average_score = _make_float(player_row[7])
            previous_rank = player_row[8].string
        )
        players.append(player)

    return players
