import pathlib
import typing

import feedparser
import httpx
import jinja2

ROOT_DIR = pathlib.Path(__file__).parent.resolve()
README_FILE = ROOT_DIR / "README.md"
TEMPLATE_FILE = ROOT_DIR / "TEMPLATE.md"
BLUESKY_FEED = "https://bsky.app/profile/did:plc:uay2bzai5qhnwqcqz7ivsvzg/rss"
PYBITES_ARTICLES_URL = "https://codechalleng.es/api/content/"
PYBITES_BITES_URL = "https://pybitesplatform.com/api/bites/"
PYBITES_TIPS_URL = "https://pybitesplatform.com/api/tips/"
NUMBER_BLUESKY_POSTS = 3
NUM_ITEMS_PER_TYPE = 2


class ContentPiece(typing.NamedTuple):
    url: str
    title: str
    date: str = ""
    content_type: str = ""


def _fetch_json(url: str) -> list[dict[str, str]]:
    resp = httpx.get(url)
    resp.raise_for_status()
    return resp.json()


def get_latest_pybites_content(
    num_items: int = NUM_ITEMS_PER_TYPE,
) -> list[ContentPiece]:
    """Get the latest Pybites articles, bites, and tips."""
    pieces: list[ContentPiece] = []

    articles = [
        i for i in _fetch_json(PYBITES_ARTICLES_URL) if i["content_type"] == "article"
    ]
    for item in articles[:num_items]:
        pieces.append(
            ContentPiece(url=item["link"], title=item["title"], content_type="Article")
        )

    for item in _fetch_json(PYBITES_BITES_URL)[:num_items]:
        url = f"https://pybitesplatform.com/bites/{item['slug']}/"
        pieces.append(ContentPiece(url=url, title=item["title"], content_type="Bite"))

    for item in _fetch_json(PYBITES_TIPS_URL)[:num_items]:
        url = f"https://pybitesplatform.com/tips/{item['slug']}/"
        pieces.append(ContentPiece(url=url, title=item["title"], content_type="Tip"))

    return pieces


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
