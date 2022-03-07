import os
import shutil
import subprocess
import sys
import webbrowser

import ads
import requests
import rich
from rich import prompt
from rich import progress


def fuzzy_search_results(papers):
    """Launch fzf subprocess and prompt selection of article by user.

    Parameters
    ----------
    papers : ads.search.SearchQuery
        The executed search query containing the article responses from ads.

    Returns
    -------
    str
        The bibcode of the selected article.
    """

    # Open fzf subprocess
    process = subprocess.Popen(
        [shutil.which("fzf"), *FZF_OPTIONS],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=None,
    )

    # Populate fzf dialogue
    for paper in papers:

        # Articles which are not open access are dimmed
        OPENACCESS = "OPENACCESS" in paper.property

        PREFIX = COLOUR_NO_OPENACCESS if not OPENACCESS else ""
        POSTFIX = COLOUR_RESET if not OPENACCESS else ""

        # Append the title out-of-view: it is cut into the preview window
        HIDDEN_TITLE = ":".join([" " * shutil.get_terminal_size()[0], paper.title[0]])

        # Flush article line to fzf choices
        process.stdin.write(
            f"{PREFIX}{FZF_LINE_FORMAT(paper)}{POSTFIX}{HIDDEN_TITLE}".encode(
                sys.getdefaultencoding()
            )
            + b"\n"
        )
        process.stdin.flush()

    # Run process and wait for user selection
    process.stdin.close()
    process.wait()

    # Extract bibcode of selected article and return
    try:
        choice = [line for line in process.stdout][0].decode()
    except IndexError:  # no choice was made, c-c c-c
        sys.exit()
    return choice.split(":")[0]


def present_choice(article):
    """Query user for action on selected article.

    Parameters
    ----------
    article : ads.search.Article
        The user-selected article instance from ADS.
    """

    # Boilerplate
    rich.print(
        "\n".join(["", " and ".join(article.author), f"[i]{article.title[0]}[/i]", ""])
    )

    options = "  ".join(
        [f"[blue][{i}][/blue] {option}" for i, option in enumerate(article.esources)]
        + [f"\n[green]\[o][/green] Open on ADS"]
        + [f"[green]\[e][/green] Export bibtex"]
        + [f"[green]\[n][/green] Do Nothing"]
    )

    decision = prompt.Prompt.ask(
        "\n".join([options, "Choose article source or action:"]),
        choices=[f"{i}" for i in range(len(options))] + ["o", "e", "n"],
        show_choices=False,
        default="0",
    )

    try:
        source = article.esources[int(decision)]
    except ValueError:
        if decision == "e":
            rich.print("")
            rich.print(
                ads.export.ExportQuery(
                    bibcodes=article.bibcode, format="bibtex"
                ).execute()
            )
        elif decision == "o":  # open page on ADS
            webbrowser.open(f"https://ui.adsabs.harvard.edu/abs/{article.bibcode}")
        sys.exit()

    # Retrieve article
    URL = f"https://ui.adsabs.harvard.edu/link_gateway/{article.bibcode}/{source}"
    FILENAME = f"/tmp/{article.bibcode}.pdf"

    if "HTML" in source:
        webbrowser.open(URL)
        sys.exit()

    if not os.path.isfile(FILENAME):
        rich.print(f"\nRetrieving article from {source}..")
        download_article(URL, FILENAME)
    webbrowser.open(FILENAME)


def download_article(URL, FILENAME):
    """Download article to file, displaying a progressbar.

    Parameters
    ----------
    URL : str
        The URl to the article PDF.
    FILENAME : str
        The filename under which to save the PDF.
    """

    # Send GET request
    response = requests.get(URL, stream=True)

    # Get total filesize for progressbar
    total = int(response.headers.get("content-length", 0))

    # Save to file
    with open(FILENAME, "wb") as file, progress.Progress(
        progress.BarColumn(), progress.DownloadColumn()
    ) as bar:

        task = bar.add_task("", total=total)

        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(task, advance=size)


# ------
# Settings

# Options passed to fzf executable
FZF_OPTIONS = [
    "--ansi",
    r"--preview=/usr/bin/echo $(echo {} | cut -d':' -f3)",
    "--no-hscroll",
    "--preview-window",
    "up,1",
]
FZF_LINE_FORMAT = lambda paper: f"{paper.bibcode}: {'& '.join(paper.author[:3])}"

# Colours for fzf lines
COLOUR_NO_OPENACCESS = "\033[2m"
COLOUR_RESET = "\033[0m"

# Article fields to query from ADS
QUERY_FIELDS = ["author", "bibcode", "year", "title", "property", "esources"]

# A subjective selection of search fields from
# https://ui.adsabs.harvard.edu/help/search/search-syntax
QUERY_KWS = {
    "abs": {
        "short": "",
        "help": "search for word or phrase in abstract, title and keywords",
    },
    "abstract": {
        "short": "",
        "help": "search for a word or phrase in an abstract only",
    },
    "arxiv": {"short": "", "help": "finds a specific record using its arXiv id"},
    "author": {
        "short": "a",
        "help": "author name may include just lastname and initial",
    },
    "bibcode": {
        "short": "",
        "help": "adsbib  finds a specific record using the ADS bibcode",
    },
    "bibstem": {
        "short": "",
        "help": "adsbibstem  find records that contain a specific bibstem in their bibcode",
    },
    "body": {
        "short": "",
        "help": "search for a word or phrase in (only) the full text",
    },
    "database": {
        "short": "",
        "help": "limit search to either astronomy or physics or general",
    },
    "doi": {"short": "", "help": "finds a specific record using its digital object id"},
    "first-author": {"short": "fa", "help": "limit the search to first-author papers"},
    "full": {
        "short": "",
        "help": "search for word or phrase in fulltext, help= acknowledgements, abstract, title and keywords",
    },
    "identifier": {
        "short": "",
        "help": "finds a paper using any of its identifiers, arXiv, bibcode, doi, etc.",
    },
    "keyword": {"short": "", "help": "search publisher- or author-supplied keywords"},
    "property": {
        "short": "",
        "help": "limit search to article with specific attributes",
    },
    "query": {"short": "q", "help": "search using a generic query term"},
    "title": {"short": "", "help": "search for word or phrase in title field"},
    "year": {
        "short": "y",
        "help": "require specific publication year or range of years",
    },
}
