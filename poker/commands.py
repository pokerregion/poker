import sys
import collections
import contextlib
import datetime as dt
from dateutil import tz
import click


LOCALTIMEZONE = tz.tzlocal()


def _print_header(title):
    click.echo(title)
    click.echo("-" * len(title))


def _print_values(*args):
    for what, value in args:
        valueformat = "{!s}"
        if not value:
            value = "-"
        elif isinstance(value, int):
            valueformat = "{:,}"
        elif isinstance(value, dt.datetime):
            value = value.astimezone(LOCALTIMEZONE)
            valueformat = "{:%Y-%m-%d (%A) %H:%M (%Z)}"
        elif isinstance(value, dt.date):
            valueformat = "{:%Y-%m-%d}"
        elif isinstance(value, collections.Sequence) and not isinstance(value, str):
            value = ", ".join(value)
        click.echo(("{:<20}" + valueformat).format(what + ": ", value))


@click.group()
def poker():
    """Main command for the poker framework."""


@poker.command(
    "range", short_help="Prints the range in a formatted table in ASCII or HTML."
)
@click.argument("range")
@click.option("--no-border", is_flag=True, help="Don't show border.")
@click.option(
    "--html", is_flag=True, help="Output html, so you can paste it on a website."
)
def range_(range, no_border, html):
    """Prints the given range in a formatted table either in a plain ASCII or HTML.
    The only required argument is the range definition, e.g. "A2s+ A5o+ 55+"
    """
    from .hand import Range

    border = not no_border
    result = Range(range).to_html() if html else Range(range).to_ascii(border)
    click.echo(result)


@poker.command(
    "2p2player", short_help="Get profile information about a Two plus Two member."
)
@click.argument("username")
def twoplustwo_player(username):
    """Get profile information about a Two plus Two Forum member given the username."""

    from .website.twoplustwo import (
        ForumMember,
        AmbiguousUserNameError,
        UserNotFoundError,
    )

    try:
        member = ForumMember(username)
    except UserNotFoundError:
        raise click.ClickException('User "%s" not found!' % username)
    except AmbiguousUserNameError as e:
        click.echo("Got multiple users with similar names!", err=True)

        for ind, user in enumerate(e.users):
            click.echo(f"{ind + 1}. {user.name}", err=True)

        number = click.prompt(
            f"Which would you like to see [1-{len(e.users)}]",
            prompt_suffix="? ",
            type=click.IntRange(1, len(e.users)),
            err=True,
        )

        userid = e.users[int(number) - 1].id
        member = ForumMember.from_userid(userid)

        click.echo(err=True)  # empty line after input

    _print_header("Two plus two forum member")
    _print_values(
        ("Username", member.username),
        ("Forum id", member.id),
        ("Location", member.location),
        ("Total posts", member.total_posts),
        ("Posts per day", member.posts_per_day),
        ("Rank", member.rank),
        ("Last activity", member.last_activity),
        ("Join date", member.join_date),
        ("Usergroups", member.public_usergroups),
        ("Profile picture", member.profile_picture),
        ("Avatar", member.avatar),
    )


@poker.command(short_help="List pocketfives ranked players (1-100).")
@click.argument("num", type=click.IntRange(1, 100), default=100)
def p5list(num):
    """List pocketfives ranked players, max 100 if no NUM, or NUM if specified."""

    from .website.pocketfives import get_ranked_players

    format_str = (
        "{:>4.4}   {!s:<15.13}{!s:<18.15}{!s:<9.6}{!s:<10.7}"
        "{!s:<14.11}{!s:<12.9}{!s:<12.9}{!s:<12.9}{!s:<4.4}"
    )

    click.echo(
        format_str.format(
            "Rank",
            "Player name",
            "Country",
            "Triple",
            "Monthly",
            "Biggest cash",
            "PLB score",
            "Biggest s",
            "Average s",
            "Prev",
        )
    )
    # just generate the appropriate number of underlines and cut them with format_str
    underlines = ["-" * 20] * 10
    click.echo(format_str.format(*underlines))

    for ind, player in enumerate(get_ranked_players()):
        click.echo(format_str.format(str(ind + 1) + ".", *player))
        if ind == num - 1:
            break


@poker.command(short_help="Show PokerStars status like active players.")
def psstatus():
    """Shows PokerStars status such as number of players, tournaments."""
    from .website.pokerstars import get_status

    _print_header("PokerStars status")

    status = get_status()
    _print_values(
        ("Info updated", status.updated),
        ("Tables", status.tables),
        ("Players", status.players),
        ("Active tournaments", status.active_tournaments),
        ("Total tournaments", status.total_tournaments),
        ("Clubs", status.clubs),
        ("Club members", status.club_members),
    )

    site_format_str = (
        "{0.id:<12}  {0.tables:<7,}  {0.players:<8,}  {0.active_tournaments:,}"
    )
    click.echo("\nSite          Tables   Players   Tournaments")
    click.echo("-----------   ------   -------   -----------")

    for site in status.sites:
        click.echo(site_format_str.format(site))
