import re
from datetime import datetime, timezone, timedelta
import requests
from bs4 import BeautifulSoup
import parsedatetime
from .._common import _make_float


FORUM_URL = 'http://forumserver.twoplustwo.com'
FORUM_MEMBER_URL = FORUM_URL + '/members'
_tz_re = re.compile('GMT (.*?)\.')


class TwoPlusTwoForumMember:
    """Represents a Forum member data from the Two Plus Two forum."""

    def __init__(self, id):
        self.id = id

        soup = self._download_page()
        self._set_username_and_rank(soup)
        self._set_profile_picture(soup)
        self._set_location(soup)
        tz = self._get_timezone(soup)
        self._set_stats(soup, tz)
        self._set_group_memberships(soup)

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__qualname__, self.username)

    @property
    def profile_url(self):
        return '{}/{}/'.format(FORUM_MEMBER_URL, self.id)

    def _download_page(self):
        stats_page = requests.get(self.profile_url)
        self.download_date = datetime.now(timezone.utc)
        return BeautifulSoup(stats_page.text, 'lxml')

    def _set_username_and_rank(self, soup):
        username_td = soup.find(id='username_box')
        self.username = username_td.h1.text.strip()
        self.rank = username_td.h2.string

    def _set_profile_picture(self, soup):
        try:
            self.profile_picture = soup.find(id='profilepic_cell').img['src']
        except AttributeError:
            self.profile_picture = None

    def _set_location(self, soup):
        try:
            self.location = soup.find('li', 'profilefield_category').dl.dd.string
        except AttributeError:
            self.location = None

    @staticmethod
    def _get_timezone(soup):
        """Find timezone informatation on bottom of the page."""
        tz_str = soup.find('div', {'class': 'smallfont', 'align': 'center'}).text
        hours = int(_tz_re.search(tz_str).group(1))
        return timezone(timedelta(hours=hours))

    def _set_stats(self, soup, tz):
        #stats > span.shade
        statrows = soup.find(id='stats').find_all('span', 'shade')

        self.total_posts = int(statrows[0].next_sibling.strip().replace(',', ''))
        self.posts_per_day = _make_float(statrows[1].next_sibling)
        date_str = statrows[2].next_sibling
        time_str = statrows[2].next_sibling.next_sibling.string
        self.last_activity = self._parse_date(date_str + time_str, tz)
        self.join_date = datetime.strptime(statrows[3].next_sibling.strip(), '%m-%d-%Y').date()

    @staticmethod
    def _parse_date(date_str, tz):
        try:
            dt = datetime.strptime(date_str.strip(), '%m-%d-%Y %I:%M %p')
            return dt.replace(tzinfo=tz)
        except ValueError:
            # in case like "Yesterday 3:30 PM" or dates like that.
            dt, pt = parsedatetime.Calendar().parseDT(date_str)
            if pt == 3:
                return dt.replace(tzinfo=tz)
            raise ValueError('Could not parse date: {}'.format(date_str))

    def _set_group_memberships(self, soup):
        try:
            memberships = soup.find(id='public_usergroup_list').find_all('li')
            self.public_usergroups = tuple(ms.string for ms in memberships)
        except AttributeError:
            self.public_usergroups = ()
