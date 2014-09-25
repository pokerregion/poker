Getting information from poker related websites
===============================================

PokerStars status
-----------------

You can get information about PokerStars online players, active tournaments,
number of tables currently running::

   >>> from poker.website.pokerstars import get_status
   >>> status = get_status()
   >>> status.players, status.tables
   (110430, 16427)

See the possible attributes in the :class:`API documentation <poker.website.pokerstars._Status>`.


List of upcoming tournaments from PokerStars
--------------------------------------------

.. code-block:: python

   >>> from poker.website.pokerstars import get_current_tournaments
   # get_current_tournaments is a generator, so if you want a list, you need to cast it
   # otherwise, you can iterate over it
   >>> list(get_current_tournaments())
   [_Tournament(start_date=datetime.datetime(2014, 8, 16, 8, 2, tzinfo=tzoffset(None, -14400)), name="Copernicus' FL Omaha H/L Freeroll", game='Omaha', buyin='$0 + $0', players=2509),
   _Tournament(start_date=datetime.datetime(2014, 8, 16, 8, 2, tzinfo=tzoffset(None, -14400)), name='500 Cap: $0.55 NLHE', game="Hold'em", buyin='$0.50 + $0.05', players=80),
   _Tournament(start_date=datetime.datetime(2014, 8, 16, 8, 2, tzinfo=tzoffset(None, -14400)), name='Sunday Million Sat [Rd 1]: $0.55+R NLHE [2x-Turbo], 3 Seats Gtd', game="Hold'em", buyin='$0.50 + $0.05', players=14),
   _Tournament(start_date=datetime.datetime(2014, 8, 16, 8, 2, tzinfo=tzoffset(None, -14400)), name='$11 NLHE [Phase 1] Sat: 5+R FPP NLHE [2x-Turbo], 2 Seats Gtd', game="Hold'em", buyin='$0 + $0', players=45),
   ...
   ]

Or you can iterate over it and use specific data::

   >>> from poker.website.pokerstars import get_current_tournaments
   >>> for tournament in get_current_tournaments():
   ...     print(tournament.name)
   Play Money, No Limit Hold'em + Knockout (5,000)
   Sunday Million Sat [Rd 1]: $2.20 NLHE [Turbo]
   Play Money, No Limit Omaha (100k)
   Play Money, Hourly 1K, NLHE
   $11 NL Hold'em [Time: 15 Minutes]
   $2.20 NL Hold'em [Heads-Up,128 Cap, Winner-Take-All]
   $2.20 NL Hold'em [4-Max, Turbo,5x-Shootout]
   $11+R NL Hold'em [Action Hour], $5K Gtd
   ...


Information about a Two plus two forum member
---------------------------------------------

If you want to download all the available public information about a forum member
(e.g. http://forumserver.twoplustwo.com/members/115014/) all you need to do is::

   >>> from poker.website.twoplustwo import ForumMember
   >>> forum_member = ForumMember('Walkman_')
   >>> vars(forum_member)
   {'public_usergroups': ('Marketplace Approved',),
    'username': 'Walkman_ ',
    'location': 'Hungary',
    'download_date': datetime.datetime(2014, 8, 29, 16, 30, 45, 64197, tzinfo=datetime.timezone.utc),
    'rank': 'enthusiast',
    'total_posts': 92,
    'id': '115014',
    'join_date': datetime.date(2008, 3, 10),
    'posts_per_day': 0.04,
    'profile_picture': 'http://forumserver.twoplustwo.com/customprofilepics/profilepic115014_1.gif',
    'avatar': 'http://forumserver.twoplustwo.com/customavatars/thumbs/avatar115014_1.gif',
    'last_activity': datetime.datetime(2014, 8, 26, 2, 49, tzinfo=<UTC>)}


Getting the top 100 players from Pocketfives
--------------------------------------------

   >>> from poker.website.pocketfives import get_ranked_players
   >>> list(get_ranked_players())
   [_Player(name='pleno1', country='United Kingdom', triple_crowns=1, monthly_win=0, biggest_cash='$110,874.68', plb_score=7740.52, biggest_score=817.0, average_score=42.93, previous_rank='2nd'),
   _Player(name='p0cket00', country='Canada', triple_crowns=6, monthly_win=0, biggest_cash='$213,000.00', plb_score=7705.61, biggest_score=1000.0, average_score=47.23, previous_rank='1st'),
   _Player(name='r4ndomr4gs', country='Sweden', triple_crowns=2, monthly_win=1, biggest_cash='$174,150.00', plb_score=7583.38, biggest_score=803.0, average_score=46.59, previous_rank='3rd'),
   _Player(name='huiiiiiiiiii', country='Austria', triple_crowns=1, monthly_win=0, biggest_cash='$126,096.00', plb_score=7276.52, biggest_score=676.0, average_score=39.26, previous_rank='11th'),
   _Player(name='TheClaimeer', country='United Kingdom', triple_crowns=1, monthly_win=0, biggest_cash='$102,296.00', plb_score=6909.56, biggest_score=505.0, average_score=41.68, previous_rank='4th'),


:class:`poker.website.pocketfives._Player` is a named tuple, so you can look up attributes on it:

   >>> for player in get_ranked_players():
   ...     print(player.name, player.country)
   pleno1 United Kingdom
   p0cket00 Canada
   r4ndomr4gs Sweden
   huiiiiiiiiii Austria
   TheClaimeer United Kingdom
   Romeopro Ukraine
   PokerKaiser Chile
   dipthrong Canad
   ...
