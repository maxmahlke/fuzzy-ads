An unofficial command line interface for the SAO/NASA Astrophysics Data System.

Query ADS as in the webbrowser, fuzzy-search through the results, and download
the PDF or export the bibtex entry.

<img src="https://github.com/maxmahlke/ads-cli/blob/main/gfx/fuzzy_ads_preview.gif?raw=true" width="480" height="270"/>
          
Note that entries without open-access PDFs available are dimmed.

# Prerequisites

1. The command-line fuzzy-finder [fzf](https://github.com/junegunn/fzf)
2. An account at the [astrophysics data system](https://ui.adsabs.harvard.edu/) and an API token, saved as per the [ads python package's instructions](https://ads.readthedocs.io/en/latest/#getting-started) either in `~/.ads/dev_key` or in the `ADS_DEV_KEY` shell environment variable

# Install

Unfortunately, the `ads-cli` name was already reserved on PyPI. Instead, the package is now name

     $ pip install fuzzy-ads
