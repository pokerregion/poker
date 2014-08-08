import dateutil.parser
import requests
from bs4 import BeautifulSoup


POKERSTARS_URL = 'http://www.pokerstars.eu'
TOURNAMENTS_XML_URL = POKERSTARS_URL + '/datafeed_global/tournaments/all.xml'


def get_current_tournaments():
    schedule_page = requests.get(TOURNAMENTS_XML_URL)
    soup = BeautifulSoup(schedule_page.text, 'xml')

    tournament_nodes = soup.find_all('tournament')
    tournaments = []

    for tour in tournament_nodes:
        tournament = dict(
            start_date = dateutil.parser.parse(tour.start_date.string),
            name = tour.find('name').string,
            game = tour.game.string,
            buy_in = tour.buy_in_fee.string,
            players = int(tour['players'])
        )

        yield tournament
