from pathlib import Path
import click
from .hand import Range


@click.group()
def poker():
    """Main command for the poker framework."""


@poker.command()
@click.argument('range')
@click.option('--no-border', is_flag=True, help="Don't show border.")
@click.option('--html', is_flag=True, help="Output html, so you can paste it on a website.")
@click.option('--outfile', type=click.Path(writable=True), help="Save the result to a file.")
def range(range, no_border, html, outfile):
    """Prints the given range in a formatted table either in a plain ASCII or HTML.
    The only required argument is the range definition, e.g. "A2s+ A5o+ 55+"
    """
    border = not no_border

    result = Range(range).as_html() if html else Range(range).as_table(border)

    if not outfile:
        click.echo(result)
        return

    if Path(outfile).exists():
        confirmed = click.confirm(
            'The file "{}" already exists. Are you sure you want to overwrite?'
            .format(outfile), abort=True
        )
    with open(outfile, 'w') as fp:
        fp.write(result)
    click.echo('File "{}" saved.'.format(outfile))
