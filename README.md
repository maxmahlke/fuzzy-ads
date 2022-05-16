![PyPI](https://img.shields.io/pypi/v/fuzzy-ads) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# fuzzy-ads

An unofficial command line interface for the SAO/NASA Astrophysics Data System.

<img src="https://github.com/maxmahlke/ads-cli/blob/main/gfx/fuzzy_ads_preview.gif?raw=true" width="900" height="540"/>

Make queries from the command line as in the webbrowser

    $ ads -q "author:^livingston year:2010-2022"

or use ADS abbreviations such as `-y|--year`,`-fa|--first-author`, `-a|--author`:

    $ ads -fa jenkins -y 2020

Then fuzzy-search the results based on year, author, and title. Use `<c-r>` to get only refereed articles and `<c-f>` to get non-refereed results only.
Results without open-access PDFs available are dimmed in the search prompt. See `ads --help` more information.

# Install

## Prerequisites

1. A command-line fuzzy-finder: [fzf](https://github.com/junegunn/fzf), version 0.27 or higher.
   Likely installed with a command like
   
       $ sudo [brew|apt|pacman|dnf] install fzf
       
2. An account at the [astrophysics data system](https://ui.adsabs.harvard.edu/) and an API token, stored either in `~/.ads/dev_key` or in the `ADS_DEV_KEY` shell environment variable as per the [ads python package's instructions](https://ads.readthedocs.io/en/latest/#getting-started)

## From PyPI

The package is available on PyPI as `fuzzy-ads`:

     $ pip install fuzzy-ads
     
## Bleeding edge

Clone the repository and run

     $ pip install .
     
in its root directory.
