"""Unofficial Command Line Interface the SAO/NASA Astrophysics Data System"""
import shutil
import sys

import click

import ads
from . import query

if shutil.which("fzf") is None:
    click.echo(
        "Missing dependency: fzf. See https://github.com/junegunn/fzf for install instructions."
    )
    sys.exit()


def add_options(options):
    """Convenience decorator to add click options.

    See https://github.com/pallets/click/issues/108."""

    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


query_options = [
    click.option(f"--{kw}", f"-{prop['short']}", help=prop["help"])
    if prop["short"]
    else click.option(f"--{kw}", help=prop["help"])
    for kw, prop in query.QUERY_KWS.items()
]


@click.command()
@add_options(query_options)
def cli(*args, **kwargs):
    """Unofficial Command Line Interface the SAO/NASA Astrophysics Data System"""

    # Parse user-specified options
    if all([value is None for value in kwargs.values()]):
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit()

    # Filter non-specified query keys
    query_params = {kw: value for kw, value in kwargs.items() if value is not None}

    # Send query
    papers = ads.SearchQuery(
        **query_params, fl=query.QUERY_FIELDS, sort="year", rows=1000
    )

    # Explicitly call execute to catch errors before launching subprocess
    papers.execute()

    # Parse results in fzf
    choice = query.fuzzy_search_results(papers)

    # Launch choice dialogue
    query.present_choice(
        [article for article in papers._articles if article.bibcode == choice][0]
    )
