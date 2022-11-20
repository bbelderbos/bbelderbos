import datetime
import operator
import pathlib
import re
import typing

import httpx
import jinja2

ROOT_DIR = pathlib.Path(__file__).parent.resolve()
README_FILE = ROOT_DIR / "README.md"
TEMPLATE_FILE = ROOT_DIR / "TEMPLATE.md"
NOTE_URL = "https://github.com/bbelderbos/bobcodesit/blob/main/{note_filename}"
NOTES_INDEX = "https://raw.githubusercontent.com/bbelderbos/bobcodesit/main/index.md"
ARTICLE_FEED = "https://codechalleng.es/api/articles/"
NUM_LATEST_ITEMS = 5


class ContentPiece(typing.NamedTuple):
    url: str
    title: str
    date: str


ContentPieces = typing.Iterable[ContentPiece]


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


def get_last_tip_notes(num_items: int = NUM_LATEST_ITEMS) -> ContentPieces:
    """
    Get the last tips from bobcodesit
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


def get_latest_articles(num_items: int = NUM_LATEST_ITEMS) -> ContentPieces:
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


def generate_readme(content: dict[str, typing.Iterable[ContentPiece]]) -> None:
    """
    Generate Readme file from template file
    """
    template_content = TEMPLATE_FILE.read_text()
    jinja_template = jinja2.Template(template_content)
    updated_content = jinja_template.render(**content)
    README_FILE.write_text(updated_content)


if __name__ == "__main__":
    content = dict(articles=get_latest_articles(), tips=get_last_tip_notes())
    generate_readme(content)
