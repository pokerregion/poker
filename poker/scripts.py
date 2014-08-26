from pathlib import Path
import click


@click.group()
def poker():
    """Main command for the poker framework."""


@poker.command()
@click.argument('range')
@click.option('--no-border', is_flag=True, help="Don't show border.")
@click.option('--html', is_flag=True, help="Output html, so you can paste it on a website.")
def range(range, no_border, html):
    """Prints the given range in a formatted table either in a plain ASCII or HTML.
    The only required argument is the range definition, e.g. "A2s+ A5o+ 55+"
    """
    from .hand import Range
    border = not no_border
    result = Range(range).as_html() if html else Range(range).as_table(border)
    click.echo(result)


@poker.command()
@click.argument('id')
def get2p2info(id):
    """Get profile information about a Two plus Two member given the id."""
    from .website.twoplustwo import TwoPlusTwoForumMember
    from dateutil.tz import tzlocal
    localtimezone = tzlocal()

    member = TwoPlusTwoForumMember(id)
    info = (
        ('Forum id', member.id),
        ('Username', member.username),
        ('Location', member.location),
        ('Total posts', member.total_posts),
        ('Posts per day', member.posts_per_day),
        ('Rank', member.rank),
        ('Last activity', member.last_activity.astimezone(localtimezone)
                                .strftime('%Y-%m-%d (%A) %H:%I:%S (%Z)')),
        ('Join date', member.join_date.strftime('%Y-%m-%d')),
        ('Usergroups', member.public_usergroups),
        ('Profile picture', member.profile_picture),
    )
    for what, value in info:
        if not value:
            value = '-'
        click.echo((what + ': ').ljust(20) + str(value))
