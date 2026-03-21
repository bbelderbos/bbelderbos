import pathlib
import typing

import feedparser
import jinja2

ROOT_DIR = pathlib.Path(__file__).parent.resolve()
README_FILE = ROOT_DIR / "README.md"
TEMPLATE_FILE = ROOT_DIR / "TEMPLATE.md"
BELDERBOS_FEED = "https://belderbos.dev/atom.xml"
MAX_POSTS = 5


class Post(typing.NamedTuple):
    url: str
    title: str


def get_latest_posts(num_items: int = MAX_POSTS) -> list[Post]:
    entries = feedparser.parse(BELDERBOS_FEED).entries
    return [Post(url=e.link, title=e.title) for e in entries[:num_items]]


def generate_readme(posts: list[Post]) -> None:
    template_content = TEMPLATE_FILE.read_text()
    jinja_template = jinja2.Template(template_content)
    updated_content = jinja_template.render(posts=posts)
    README_FILE.write_text(updated_content)


if __name__ == "__main__":
    generate_readme(get_latest_posts())
