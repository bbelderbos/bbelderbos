import pathlib
import typing

import feedparser
import httpx
import jinja2

ROOT_DIR = pathlib.Path(__file__).parent.resolve()
README_FILE = ROOT_DIR / "README.md"
TEMPLATE_FILE = ROOT_DIR / "TEMPLATE.md"
BLUESKY_FEED = "https://bsky.app/profile/did:plc:uay2bzai5qhnwqcqz7ivsvzg/rss"
PYBITES_CONTENT_URL = "https://codechalleng.es/api/content/"
NUMBER_BLUESKY_POSTS = 3
CONTENT_PER_TYPE = 2
CONTENT_TYPES = ("article", "bite", "tip")


class ContentPiece(typing.NamedTuple):
    url: str
    title: str
    date: str = ""
    content_type: str = ""


def get_latest_pybites_content(
    per_type: int = CONTENT_PER_TYPE,
) -> list[ContentPiece]:
    """Get the latest Pybites articles and podcasts from the content API."""
    resp = httpx.get(PYBITES_CONTENT_URL)
    resp.raise_for_status()
    items = resp.json()

    content_pieces: list[ContentPiece] = []
    for ct in CONTENT_TYPES:
        type_items = [i for i in items if i["content_type"] == ct]
        for item in type_items[:per_type]:
            content_pieces.append(
                ContentPiece(
                    url=item["link"],
                    title=item["title"],
                    content_type=ct.capitalize(),
                )
            )
    return content_pieces


def get_latest_bluesky_posts(
    num_items: int = NUMBER_BLUESKY_POSTS,
) -> list[ContentPiece]:
    """Get the latest Bluesky posts from feed."""
    entries = feedparser.parse(BLUESKY_FEED).entries
    data = []
    for entry in entries[:num_items]:
        data.append(
            ContentPiece(
                url=entry.link, title=entry.description, date=entry.published[:11]
            )
        )
    return data


def generate_readme(content: dict[str, list[ContentPiece]]) -> None:
    """Generate README file from template file."""
    template_content = TEMPLATE_FILE.read_text()
    jinja_template = jinja2.Template(template_content)
    updated_content = jinja_template.render(**content)
    README_FILE.write_text(updated_content)


if __name__ == "__main__":
    content = dict(
        posts=get_latest_bluesky_posts(),
        pybites_content=get_latest_pybites_content(),
    )
    generate_readme(content)
