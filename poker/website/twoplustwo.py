# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function

import re
from datetime import datetime, timedelta
from collections import namedtuple
from lxml import etree
import requests
import parsedatetime
from dateutil.tz import tzoffset
from pytz import UTC
from .._common import _make_float, _make_int


__all__ = ['search_userid', 'ForumMember', 'FORUM_URL', 'FORUM_MEMBER_URL', 'AJAX_USERSEARCH_URL']


FORUM_URL = 'http://forumserver.twoplustwo.com'
FORUM_MEMBER_URL = FORUM_URL + '/members'
AJAX_USERSEARCH_URL = FORUM_URL + '/ajax.php?do=usersearch'


class AmbiguousUserNameError(Exception):
    """Exception when username is not unique, there are more starting with the same."""

class UserNotFoundError(Exception):
    """User cannot be found."""


def search_userid(username):
    headers = {'X-Requested-With': 'XMLHttpRequest',
               'Origin': FORUM_URL,
               'Referer': FORUM_URL + '/search.php'
               }

    data = {'securitytoken': 'guest',
            'do': 'usersearch',
            'fragment': username
            }

    response = requests.post(AJAX_USERSEARCH_URL, data, headers=headers)
    root = etree.fromstring(response.content)

    try:
        found_name = root[0].text
    except IndexError:
        raise UserNotFoundError(username)

    # The request is basically a search, can return multiple userids
    # for users starting with username. Make sure we got the right one!
    if found_name.upper() != username.upper():
        exc = AmbiguousUserNameError(username)
        # attach the extra users to the exception
        ExtraUser = namedtuple('ExtraUser', 'name, id')
        exc.users = tuple(ExtraUser(name=child.text, id=child.attrib['userid']) for child in root)
        raise exc

    userid = root[0].attrib['userid']
    # userid is str on Python2, we need to decode to make it unicode
    return userid.decode('utf-8')


class ForumMember(object):
    """Download and store a member data from the Two Plus Two forum."""

    _tz_re = re.compile('GMT (.*?)\.')
    _attributes = (
        ('username', '//td[@id="username_box"]/h1/text()', unicode),
        ('rank', '//td[@id="username_box"]/h2/text()', unicode),
        ('profile_picture', '//td[@id="profilepic_cell"]/img/@src', unicode),
        ('location', '//div[@id="collapseobj_aboutme"]/div/ul/li/dl/dd[1]/text()', unicode),
        ('total_posts', '//div[@id="collapseobj_stats"]/div/fieldset[1]/ul/li[1]/text()', _make_int),
        ('posts_per_day', '//div[@id="collapseobj_stats"]/div/fieldset[1]/ul/li[2]/text()', float),
        ('public_usergroups', '//ul[@id="public_usergroup_list"]/li/text()', tuple),
        ('avatar', '//img[@id="user_avatar"]/@src', unicode),
    )

    def __init__(self, username):
        self.id = search_userid(username)
        self._download_and_parse()

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.username).encode('utf-8')

    @classmethod
    def from_userid(cls, userid):
        self = super(ForumMember, cls).__new__(cls)
        # we need unicode for consistency
        self.id = userid.decode('utf-8')
        self._download_and_parse()
        return self

    def _download_and_parse(self):
        root = self._download_page()
        self._parse_attributes(root)
        tz = self._get_timezone(root)
        self._parse_last_activity(root, tz)
        self._parse_join_date(root)

    @property
    def profile_url(self):
        return '{}/{}/'.format(FORUM_MEMBER_URL, self.id)

    def _download_page(self):
        stats_page = requests.get(self.profile_url)
        self.download_date = datetime.now(UTC)
        return etree.HTML(stats_page.text)

    def _parse_attributes(self, root):
        for attname, xpath, type_ in self._attributes:
            if type_ != tuple:
                try:
                    setattr(self, attname, type_(root.xpath(xpath)[0]))
                except IndexError:
                    setattr(self, attname, None)
            else:
                setattr(self, attname, type_(root.xpath(xpath)))


    def _get_timezone(self, root):
        """Find timezone informatation on bottom of the page."""
        tz_str = root.xpath('//div[@class="smallfont" and @align="center"]')[0].text
        hours = int(self._tz_re.search(tz_str).group(1))
        return tzoffset(tz_str, hours * 60)

    def _parse_last_activity(self, root, tz):
        try:
            li = root.xpath('//div[@id="collapseobj_stats"]/div/fieldset[2]/ul/li[1]')[0]
            date_str = li[0].tail.strip()
            time_str = li[1].text.strip()
            self.last_activity = self._parse_date(date_str + ' ' + time_str, tz)
        except IndexError:
            self.last_activity = None

    def _parse_join_date(self, root):
        ul = root.xpath('//div[@id="collapseobj_stats"]/div/fieldset[2]/ul')[0]
        try:
            join_date = ul.xpath('li[2]/text()')[0]
        except IndexError:
            # not everybody has a last activity field.
            # in this case, it's the first li element, not the second
            join_date = ul.xpath('li[1]/text()')[0]
        join_date = join_date.strip()
        self.join_date = datetime.strptime(join_date, '%m-%d-%Y').date()

    @staticmethod
    def _parse_date(date_str, tz):
        try:
            dt = datetime.strptime(date_str.strip(), '%m-%d-%Y %I:%M %p')
            return dt.replace(tzinfo=tz).astimezone(UTC)

        except ValueError:
            # in case like "Yesterday 3:30 PM" or dates like that.

            # calculates based on sourceTime. tz is 2p2 forum timezone
            source = datetime.now(UTC).astimezone(tz)
            dt, pt = parsedatetime.Calendar().parseDT(date_str, tzinfo=tz, sourceTime=source)

            # parsed as a C{datetime}, means that parsing was successful
            if pt == 3:
                return dt.astimezone(UTC)
            raise ValueError('Could not parse date: {}'.format(date_str))
