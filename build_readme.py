import html
import pathlib
import re
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
RUST_BLOG_FEED = "https://rsbit.es/atom.xml"
RUST_EXERCISES_URL = "https://rustplatform.com/api/"
NUMBER_BLUESKY_POSTS = 3
NUM_ITEMS_PER_TYPE = 2
SNIPPET_MAX_LENGTH = 100


class ContentPiece(typing.NamedTuple):
    url: str
    title: str
    date: str = ""
    content_type: str = ""
    snippet: str = ""


def _make_snippet(text: str, max_length: int = SNIPPET_MAX_LENGTH) -> str:
    """Strip HTML tags and entities, then truncate to max_length."""
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = " ".join(text.split())
    if len(text) > max_length:
        text = text[:max_length].rsplit(" ", 1)[0] + "..."
    return text


def _fetch_json(url: str) -> list[dict[str, str]]:
    resp = httpx.get(url)
    resp.raise_for_status()
    return resp.json()


def get_latest_pybites_content(
    num_items: int = NUM_ITEMS_PER_TYPE,
) -> list[ContentPiece]:
    """Get the latest Pybites articles, bites, Rust blog posts, and Rust exercises."""
    pieces: list[ContentPiece] = []

    articles = [
        i for i in _fetch_json(PYBITES_ARTICLES_URL) if i["content_type"] == "article"
    ]
    for item in articles[:num_items]:
        pieces.append(
            ContentPiece(
                url=item["link"],
                title=item["title"],
                content_type="Article",
                snippet=_make_snippet(item.get("summary", "")),
            )
        )

    bites = list(reversed(_fetch_json(PYBITES_BITES_URL)))
    base_url = PYBITES_BITES_URL.replace("/api", "")
    for item in bites[:num_items]:
        url = f"{base_url}{item['slug']}/"
        pieces.append(
            ContentPiece(
                url=url,
                title=item["title"],
                content_type="Bite",
                snippet=_make_snippet(item.get("description", "")),
            )
        )

    rust_posts = feedparser.parse(RUST_BLOG_FEED).entries
    for entry in rust_posts[:num_items]:
        snippet = _make_snippet(entry.get("content", [{}])[0].get("value", ""))
        pieces.append(
            ContentPiece(
                url=entry.link,
                title=entry.title,
                content_type="Rust article",
                snippet=snippet,
            )
        )

    rust_exercises = sorted(
        _fetch_json(RUST_EXERCISES_URL),
        key=lambda x: x.get("created_at", ""),
        reverse=True,
    )
    for item in rust_exercises[:num_items]:
        url = f"https://rustplatform.com/exercises/{item['slug']}/"
        pieces.append(
            ContentPiece(
                url=url,
                title=item["name"],
                content_type="Rust exercise",
                snippet=_make_snippet(item.get("description", "")),
            )
        )

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
