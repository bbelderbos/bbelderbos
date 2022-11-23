import datetime
import operator
import pathlib
import re
import typing

import feedparser
import httpx
import jinja2

ROOT_DIR = pathlib.Path(__file__).parent.resolve()
README_FILE = ROOT_DIR / "README.md"
TEMPLATE_FILE = ROOT_DIR / "TEMPLATE.md"
NOTE_URL = "https://github.com/bbelderbos/bobcodesit/blob/main/{note_filename}"
NOTES_INDEX = "https://raw.githubusercontent.com/bbelderbos/bobcodesit/main/index.md"
ARTICLE_FEED = "https://codechalleng.es/api/articles/"
FOSSTODON_USER = "bbelderbos"


class ContentPiece(typing.NamedTuple):
    url: str
    title: str
    date: str


ContentPieces = list[ContentPiece]


def _parse_notes_index() -> set[tuple[str, str]]:
    """
    Parse bobcodesit tips index to get tuples of
    (title, note_file)
    """
    resp = httpx.get(NOTES_INDEX)
    notes = re.findall(r'notes/\d+\.md', resp.text)
    pat = re.compile(r'\[(.*?)\]\((notes/\d+\.md)')
    notes = re.findall(pat, resp.text)
    return set(notes)


def get_latest_tips(num_items: int = 8) -> ContentPieces:
    """
    Get the last tips from bobcodesit tips GitHub repo
    """
    notes = _parse_notes_index()
    last_notes = sorted(
        notes, key=operator.itemgetter(1), reverse=True
    )[:num_items]

    content_pieces = []
    for note in last_notes:
        title, md_file = note

        url = NOTE_URL.format(note_filename=md_file)

        tstamp_number = re.sub(r"notes/(\d+)\.md", r"\1", md_file)
        tstamp_dt = datetime.datetime.strptime(
            tstamp_number, "%Y%m%d%H%M%S")
        date_readable = tstamp_dt.strftime("%Y-%m-%d")

        content_pieces.append(
            ContentPiece(url=url, title=title, date=date_readable)
        )
    return content_pieces


def get_latest_articles(num_items: int = 5) -> ContentPieces:
    """
    Get the last articles from Pybites blog
    """
    resp = httpx.get(ARTICLE_FEED)
    return [
        ContentPiece(
            url=row["link"], title=row["title"], date=row["publish_date"].split()[0]
        )
        for row in resp.json()
    ][:num_items]


def _parse_fosstodon_feed(username: str) -> list[feedparser.util.FeedParserDict]:
    url = f"https://fosstodon.org/@{FOSSTODON_USER}.rss"
    entries = feedparser.parse(url).entries
    return entries


def get_latest_toots(num_items: int = 3) -> ContentPieces:
    """
    Get latest toots from Fosstodon.
    I was using the local cached db first, but let's use RSS = always up2date.
    """
    entries = _parse_fosstodon_feed(FOSSTODON_USER)

    data = []
    for entry in entries[:num_items]:  # should have newest first
        if entry.summary.count("<p>") > 1:
            # if multiple paragraphs extract the first one
            summary = re.sub(
                r"^(<p>.*?)</p>.*$", r"\1 ...</p>", entry.summary
            )
        else:
            summary = entry.summary

        date = datetime.datetime(
            *entry.published_parsed[:6]
        ).strftime("%Y-%m-%d")

        data.append(
            ContentPiece(url=entry.id, title=summary, date=date)
        )

    return data


def generate_readme(content: dict[str, list[ContentPiece]]) -> None:
    """
    Generate Readme file from template file
    """
    template_content = TEMPLATE_FILE.read_text()
    jinja_template = jinja2.Template(template_content)
    updated_content = jinja_template.render(**content)
    README_FILE.write_text(updated_content)


if __name__ == "__main__":
    content = dict(
        articles=get_latest_articles(),
        tips=get_latest_tips(),
        toots=get_latest_toots(),
    )
    generate_readme(content)
