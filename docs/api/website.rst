Website package
===============

This package contains mostly scraping tools for well known websites like Two Plus Two forum,
Pocketsfives, etc...


Two Plus Two Forum API
----------------------

.. automodule:: poker.website.twoplustwo

   .. autoclass:: ForumMember

      :param int id:   Forum id

      :ivar str id:                         Forum id (last part of members URL)
      :ivar str username:                   Forum username
      :ivar datetime donwload_date:         When were the data downloaded from TwoplusTwo
      :ivar tuple public_usergroups:        Public usergroup permission as in the box on the top right
      :ivar str/None profile_picture:    URL of profile if set.
      :ivar date join_date:                 Join date on account page
      :ivar float posts_per_day:            Posts per day on account page
      :ivar int total_posts:                Total posts
      :ivar str location:                   Location (country)
      :ivar datetime last_activity:         Last activity with the website timezone
      :ivar str rank:                       Forum rank like ``'enthusiast'``


Pocketfives API
---------------

.. automodule:: poker.website.pocketfives

   .. autofunction:: get_ranked_players

      :return:  generator of player data
      :rtype:   list of dicts

      Dictionary keys:

        :name: (`str`)              Pocketfives name
        :country: (`str`)           Country name
        :triple_crowns: (`int`)     Number of triple crowns won
        :monthly_win: (`int`)
        :biggest_cash: (`str`)
        :plb_score: (`float`)
        :biggest_score: (`float`)   Biggest Pocketfives score
        :average_score: (`float`)   Average pocketfives score
        :previous_rank: (`str`)     Previous pocketfives rank


PokerStars website API
----------------------


.. automodule:: poker.website.pokerstars

   .. autofunction:: get_current_tournaments

      :return:      generator of tournament data
      :rtype:       list of dicts

      Dictionary keys:

        :start_date:  (`datetime`)
        :name:  (`str`)         Tournament name as seen in PokerStars Lobby
        :game: (`str`)          Game Type
        :buy_in: (`str`)        Buy in with fee
        :player_num: (`int`)   Number of players already registered
