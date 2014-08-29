Website API
===========

This package contains mostly scraping tools for well known websites like Two Plus Two forum,
Pocketsfives, etc...



Two Plus Two Forum API
----------------------

.. automodule:: poker.website.twoplustwo

   .. data:: FORUM_URL

      http://forumserver.twoplustwo.com

   .. data:: FORUM_MEMBER_URL

      http://forumserver.twoplustwo.com/members

   .. autoclass:: ForumMember

      :param int,str id:      | Forum id (last part of members URL, e.g. in case of
                              | http://forumserver.twoplustwo.com/members/407153/
                              | the id is 407153)

      :ivar str id:                         Forum id
      :ivar str username:                   Forum username
      :ivar str rank:                       Forum rank like ``'enthusiast'``
      :ivar str,None profile_picture:       URL of profile if set.
      :ivar str location:                   Location (country)
      :ivar int total_posts:                Total posts
      :ivar float posts_per_day:            Posts per day on account page
      :ivar datetime last_activity:         Last activity with the website timezone
      :ivar date join_date:                 Join date on account page
      :ivar tuple public_usergroups:        Public usergroup permission as in the box on the top right
      :ivar datetime donwload_date:         When were the data downloaded from TwoplusTwo



Pocketfives API
---------------

.. automodule:: poker.website.pocketfives

   .. autoclass:: _Player

      :ivar str name:             Player name
      :ivar str country:          Country name
      :ivar int triple_crowns:    Number of triple crowns won
      :ivar int monthly_win:
      :ivar str biggest_cash:
      :ivar float plb_score:
      :ivar float biggest_score:  Biggest Pocketfives score
      :ivar float average_score:  Average pocketfives score
      :ivar str previous_rank:    Previous pocketfives rank

   .. autofunction:: get_ranked_players

      :return:  generator of :class:`_Player`\ s

      .. note:: Downloading this list is a slow operation!



PokerStars website API
----------------------

.. automodule:: poker.website.pokerstars


   .. data:: WEBSITE_URL

      http://www.pokerstars.eu


   .. data:: TOURNAMENTS_XML_URL

      http://www.pokerstars.eu/datafeed_global/tournaments/all.xml

   .. data:: STATUS_URL

      http://www.psimg.com/datafeed/dyn_banners/summary.json.js


   .. autofunction:: get_current_tournaments

      :return:      generator of :class:`_Tournament`

      .. note:: Downloading this list is an extremly slow operation!


   .. autofunction:: get_status

      :return: :class:`_Status`


   .. autoclass:: _Tournament

      :ivar datetime start_date:
      :ivar str name:         Tournament name as seen in PokerStars Lobby
      :ivar str game:         Game Type
      :ivar str buyin:        Buy in with fee
      :ivar int players:      Number of players already registered


   .. autoclass:: _Status

      :ivar datetime updated:       Status last updated
      :ivar int tables:             Number of tournament tables
      :ivar int players:            Number of players logged in to PokerStars
      :ivar int clubs:              Total number of Home Game clubs created
      :ivar int club_members:       Total number of Home Game club members
      :ivar int active_tournaments:
      :ivar int total_tournaments:
      :ivar tuple sites:            Tuple of :class:`_SiteStatus`

   .. autoclass:: _SiteStatus

      :ivar str id:        ID of the site (``".IT"``, ``".FR"``, ``"Play Money"``)
      :ivar int tables:
      :ivar int player:
      :ivar int active_tournaments:

