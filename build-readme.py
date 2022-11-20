import datetime
import pathlib
import re
import typing

import httpx
import jinja2

README_FILE = pathlib.Path(__file__).parent.resolve() / "README.md"
TIPS_REPO_TREE = (
    "https://api.github.com/repos/bbelderbos/bobcodesit/git/trees/main?recursive=1"
)
NOTE_URL = "https://github.com/bbelderbos/bobcodesit/blob/main/{note_filename}"
NOTE_RAW_URL = (
    "https://raw.githubusercontent.com/bbelderbos/bobcodesit/main/{note_filename}"
)
ARTICLE_FEED = "https://codechalleng.es/api/articles/"
NUM_LATEST_ITEMS = 5


class ContentPiece(typing.NamedTuple):
    url: str
    title: str
    date: str


ContentPieces = typing.Iterable[ContentPiece]


def get_last_tip_notes(num_items: int = NUM_LATEST_ITEMS) -> ContentPieces:
    with httpx.Client() as client:

        def _get_note_title(note_filename: str) -> str:
            url = NOTE_RAW_URL.format(note_filename=note_filename)
            resp = client.get(url)
            title = resp.text.splitlines()[0].lstrip("# ").capitalize()
            return title

        resp = client.get(TIPS_REPO_TREE)
        tree = resp.json()["tree"]

        notes = [row["path"] for row in tree if "notes/" in row["path"]]
        last_notes = sorted(notes, reverse=True)[:num_items]

        return [
            ContentPiece(
                url=NOTE_URL.format(note_filename=note),
                title=_get_note_title(note),
                date=datetime.datetime.strptime(
                    re.sub(r"notes/(\d+)\.md", r"\1", note), "%Y%m%d%H%M%S"
                ).strftime("%Y-%m-%d"),
            )
            for note in last_notes
        ]


def get_latest_articles(num_items: int = NUM_LATEST_ITEMS) -> ContentPieces:
    resp = httpx.get(ARTICLE_FEED).json()
    return [
        ContentPiece(
            url=row["link"], title=row["title"], date=row["publish_date"].split()[0]
        )
        for row in resp
    ][:num_items]


def generate_readme(content: dict[str, typing.Iterable[ContentPiece]]) -> None:
    with open("TEMPLATE.md", "r", encoding="utf-8") as file:
        template = jinja2.Template(file.read())
    new_content = template.render(**content)
    README_FILE.open("w").write(new_content)


if __name__ == "__main__":
    content = dict(articles=get_latest_articles(), tips=get_last_tip_notes())
    generate_readme(content)
