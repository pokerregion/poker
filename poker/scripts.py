import sys
from pathlib import Path
from contextlib import contextmanager
import click


# FIXME: This is a hack about click incapability to prompt to stderr.
# See: https://github.com/mitsuhiko/click/issues/211
@contextmanager
def redirect_stdout_to_stderr():
    """Redirect standard output to standard error and restore after the context is finished."""
    oldout = sys.stdout
    sys.stdout = sys.stderr
    yield
    sys.stdout = oldout


@click.group()
def poker():
    """Main command for the poker framework."""
    click.echo()


@poker.command('range', short_help="Prints the range in a formatted table in ASCII or HTML.")
@click.argument('range')
@click.option('--no-border', is_flag=True, help="Don't show border.")
@click.option('--html', is_flag=True, help="Output html, so you can paste it on a website.")
def range_(range, no_border, html):
    """Prints the given range in a formatted table either in a plain ASCII or HTML.
    The only required argument is the range definition, e.g. "A2s+ A5o+ 55+"
    """
    from .hand import Range
    border = not no_border
    result = Range(range).as_html() if html else Range(range).as_table(border)
    click.echo(result)


@poker.command(short_help="Get profile information about a Two plus Two member.")
@click.argument('username')
def twoplustwo(username):
    """Get profile information about a Two plus Two Forum member given the username."""

    from .website.twoplustwo import (
        TwoPlusTwoForumMember, AmbiguousUserNameError, UserNotFoundError
    )
    from dateutil.tz import tzlocal
    localtimezone = tzlocal()

    try:
        member = TwoPlusTwoForumMember(username)
    except UserNotFoundError:
        raise click.ClickException('User "{}" not found!'.format(username))
    except AmbiguousUserNameError as e:
        click.echo('Got multiple users with similar names!', err=True)

        for ind, user in enumerate(e.users):
            click.echo('{}. {}'.format(ind + 1, user.name), err=True)

        with redirect_stdout_to_stderr():
            number = click.prompt('Which would you like to see [{}-{}]'.format(1, len(e.users)),
                                  prompt_suffix='? ', type=click.IntRange(1, len(e.users)))

        userid = e.users[int(number) - 1].id
        member = TwoPlusTwoForumMember.from_userid(userid)

        click.echo(err=True)  # empty line after input

    click.echo('Two plus two forum member')
    click.echo('-------------------------')

    if member.last_activity:
        last_activity = member.last_activity.astimezone(localtimezone)\
                                            .strftime('%Y-%m-%d (%A) %H:%M:%S (%Z)')
    else:
        last_activity = None

    info = (
        ('Username', member.username),
        ('Forum id', member.id),
        ('Location', member.location),
        ('Total posts', member.total_posts),
        ('Posts per day', member.posts_per_day),
        ('Rank', member.rank),
        ('Last activity', last_activity),
        ('Join date', member.join_date.strftime('%Y-%m-%d')),
        ('Usergroups', ', '.join(member.public_usergroups)),
        ('Profile picture', member.profile_picture),
        ('Avatar', member.avatar),
    )

    for what, value in info:
        if not value:
            value = '-'
        click.echo('{:<20}{!s}'.format(what + ': ', value))


@poker.command(short_help="List pocketfives ranked players.")
@click.argument('num', type=click.IntRange(1, 100), default=100)
def p5_players(num):
    """List pocketfives ranked players, max 100 if no num, or num if specified."""
    from poker.website.pocketfives import get_ranked_players

    format_str = '{:>4.4}   {!s:<15.13}{!s:<18.15}{!s:<9.6}{!s:<10.7}'\
                 '{!s:<14.11}{!s:<12.9}{!s:<12.9}{!s:<12.9}{!s:<4.4}'
    click.echo(format_str.format(
        'Rank' , 'Player name', 'Country', 'Triple', 'Monthly', 'Biggest cash',
        'PLB score', 'Biggest s', 'Average s', 'Prev'
    ))
    # just generate the appropriate number of underlines and cut them with format_str
    underlines = tuple('-' * 20 for __ in range(10))
    click.echo(format_str.format(*underlines))

    for ind, player in enumerate(get_ranked_players()):
        click.echo(format_str.format(str(ind + 1) + '.', *player))
        if ind == num - 1:
            break
