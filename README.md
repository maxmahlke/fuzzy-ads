An unofficial command line interface for the SAO/NASA Astrophysics Data System.

Make queries from the command line as in the webbrowser:

    $ ads -q "author:^livingston year:2010-2022"
 
Common query elements are implemented as short-hands such as `-y|--year`,`-fa|--first-author`, `-a|--author`:

    $ ads -fa jenkins -y 2020


Then fuzzy-search the results based on year, author, and title and open the selected article as PDF:

<img src="https://github.com/maxmahlke/ads-cli/blob/main/gfx/fuzzy_ads_preview.gif?raw=true" width="900" height="540"/>

Note that entries without open-access PDFs available are dimmed. 
See `ads --help` more information.

# Prerequisites

1. A command-line fuzzy-finder: [fzf](https://github.com/junegunn/fzf)
2. An account at the [astrophysics data system](https://ui.adsabs.harvard.edu/) and an API token, stored either in `~/.ads/dev_key` or in the `ADS_DEV_KEY` shell environment variable as per the [ads python package's instructions](https://ads.readthedocs.io/en/latest/#getting-started)

# Install

The package is available on PyPI as `fuzzy-ads`:

     $ pip install fuzzy-ads
