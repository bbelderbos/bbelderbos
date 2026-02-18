from unittest.mock import patch, MagicMock

import build_readme as br


FAKE_ARTICLES_RESPONSE = [
    {
        "content_type": "article",
        "title": "Article One",
        "link": "https://pybit.es/articles/one/",
        "summary": "This is a <b>great</b> article about Python&#8230; and more.",
    },
    {
        "content_type": "article",
        "title": "Article Two",
        "link": "https://pybit.es/articles/two/",
        "summary": "Another article.",
    },
    {
        "content_type": "article",
        "title": "Article Three",
        "link": "https://pybit.es/articles/three/",
        "summary": "Third one.",
    },
    {
        "content_type": "podcast",
        "title": "Podcast One",
        "link": "https://podcast.example.com/1",
        "summary": "A podcast.",
    },
]

FAKE_BITES_RESPONSE = [
    {
        "title": "Sum n numbers",
        "slug": "sum-n-numbers",
        "description": "Old bite.",
        "level": "beginner",
        "tags": [],
    },
    {
        "title": "Regex fun",
        "slug": "regex-fun",
        "description": "Middle bite.",
        "level": "intermediate",
        "tags": [],
    },
    {
        "title": "FastAPI Endpoints",
        "slug": "fastapi-endpoints",
        "description": "Newest bite.",
        "level": "advanced",
        "tags": [],
    },
]


def _make_rust_blog_entry(link: str, title: str, content_html: str) -> MagicMock:
    entry = MagicMock()
    entry.link = link
    entry.title = title
    entry.get.return_value = [{"value": content_html}]
    return entry


FAKE_RUST_BLOG_ENTRIES = [
    _make_rust_blog_entry(
        "https://rsbit.es/iterators/", "Rust iterators", "<p>Iterators are great.</p>"
    ),
    _make_rust_blog_entry(
        "https://rsbit.es/functions/", "Rust functions", "<p>Functions in Rust.</p>"
    ),
]

FAKE_RUST_EXERCISES_RESPONSE = [
    {
        "name": "Old Exercise",
        "slug": "old-exercise",
        "description": "An old one.",
        "created_at": "2024-09-04T17:24:48.017369Z",
    },
    {
        "name": "Newest Exercise",
        "slug": "newest-exercise",
        "description": "Brand new.",
        "created_at": "2026-02-14T13:30:55.788849Z",
    },
    {
        "name": "Second Newest",
        "slug": "second-newest",
        "description": "Pretty new.",
        "created_at": "2026-02-14T13:30:54.408364Z",
    },
]

FAKE_BLUESKY_ENTRIES = [
    MagicMock(
        link="https://bsky.app/post/1",
        description="Post one",
        published="09 Feb 2026 12:00",
    ),
    MagicMock(
        link="https://bsky.app/post/2",
        description="Post two",
        published="08 Feb 2026 12:00",
    ),
    MagicMock(
        link="https://bsky.app/post/3",
        description="Post three",
        published="07 Feb 2026 12:00",
    ),
]


def _mock_fetch_json(url: str) -> list[dict]:
    if url == br.PYBITES_ARTICLES_URL:
        return FAKE_ARTICLES_RESPONSE
    if url == br.PYBITES_BITES_URL:
        return FAKE_BITES_RESPONSE
    if url == br.RUST_EXERCISES_URL:
        return FAKE_RUST_EXERCISES_RESPONSE
    raise ValueError(f"Unexpected URL: {url}")


def _mock_feedparser_parse(url: str) -> MagicMock:
    result = MagicMock()
    if url == br.RUST_BLOG_FEED:
        result.entries = FAKE_RUST_BLOG_ENTRIES
    elif url == br.BLUESKY_FEED:
        result.entries = FAKE_BLUESKY_ENTRIES
    else:
        result.entries = []
    return result


@patch("build_readme.feedparser.parse", side_effect=_mock_feedparser_parse)
@patch("build_readme._fetch_json", side_effect=_mock_fetch_json)
def test_get_latest_pybites_content_default(mock_fetch, mock_feed):
    pieces = br.get_latest_pybites_content()

    assert len(pieces) == 8
    assert all(isinstance(p, br.ContentPiece) for p in pieces)

    articles = [p for p in pieces if p.content_type == "Article"]
    bites = [p for p in pieces if p.content_type == "Bite"]
    rust_articles = [p for p in pieces if p.content_type == "Rust article"]
    rust_exercises = [p for p in pieces if p.content_type == "Rust exercise"]
    assert len(articles) == 2
    assert len(bites) == 2
    assert len(rust_articles) == 2
    assert len(rust_exercises) == 2


@patch("build_readme.feedparser.parse", side_effect=_mock_feedparser_parse)
@patch("build_readme._fetch_json", side_effect=_mock_fetch_json)
def test_get_latest_pybites_content_num_items(mock_fetch, mock_feed):
    pieces = br.get_latest_pybites_content(num_items=1)
    assert len(pieces) == 4
    types = [p.content_type for p in pieces]
    assert types == ["Article", "Bite", "Rust article", "Rust exercise"]


@patch("build_readme.feedparser.parse", side_effect=_mock_feedparser_parse)
@patch("build_readme._fetch_json", side_effect=_mock_fetch_json)
def test_articles_filter_non_article_types(mock_fetch, mock_feed):
    pieces = br.get_latest_pybites_content(num_items=10)

    articles = [p for p in pieces if p.content_type == "Article"]
    assert len(articles) == 3
    assert all("pybit.es/articles" in a.url for a in articles)


@patch("build_readme.feedparser.parse", side_effect=_mock_feedparser_parse)
@patch("build_readme._fetch_json", side_effect=_mock_fetch_json)
def test_bites_are_reversed_newest_first(mock_fetch, mock_feed):
    pieces = br.get_latest_pybites_content()
    bites = [p for p in pieces if p.content_type == "Bite"]

    assert bites[0].title == "FastAPI Endpoints"
    assert bites[0].url == "https://pybitesplatform.com/bites/fastapi-endpoints/"
    assert bites[1].title == "Regex fun"


@patch("build_readme.feedparser.parse", side_effect=_mock_feedparser_parse)
@patch("build_readme._fetch_json", side_effect=_mock_fetch_json)
def test_rust_blog_entries(mock_fetch, mock_feed):
    pieces = br.get_latest_pybites_content()
    rust_articles = [p for p in pieces if p.content_type == "Rust article"]

    assert rust_articles[0].url == "https://rsbit.es/iterators/"
    assert rust_articles[0].title == "Rust iterators"


@patch("build_readme.feedparser.parse", side_effect=_mock_feedparser_parse)
@patch("build_readme._fetch_json", side_effect=_mock_fetch_json)
def test_rust_exercises_sorted_newest_first(mock_fetch, mock_feed):
    pieces = br.get_latest_pybites_content()
    rust_exercises = [p for p in pieces if p.content_type == "Rust exercise"]

    assert rust_exercises[0].title == "Newest Exercise"
    assert (
        rust_exercises[0].url == "https://rustplatform.com/exercises/newest-exercise/"
    )
    assert rust_exercises[1].title == "Second Newest"


@patch("build_readme.feedparser")
def test_get_latest_bluesky_posts(mock_feedparser):
    mock_feedparser.parse.return_value.entries = FAKE_BLUESKY_ENTRIES

    posts = br.get_latest_bluesky_posts(num_items=2)

    assert len(posts) == 2
    assert posts[0].url == "https://bsky.app/post/1"
    assert posts[0].title == "Post one"
    assert posts[0].date == "09 Feb 2026"
    assert posts[1].date == "08 Feb 2026"


@patch("build_readme.feedparser")
def test_get_latest_bluesky_posts_default_count(mock_feedparser):
    mock_feedparser.parse.return_value.entries = FAKE_BLUESKY_ENTRIES

    posts = br.get_latest_bluesky_posts()
    assert len(posts) == 3


def test_make_snippet_strips_html_and_entities():
    raw = "<p>This is a <b>great</b> article&#8230;</p>"
    result = br._make_snippet(raw)
    assert "<" not in result
    assert ">" not in result
    assert "\u2026" in result or "..." in result


def test_make_snippet_truncates_long_text():
    long_text = "word " * 50
    result = br._make_snippet(long_text, max_length=20)
    assert len(result) <= 24  # 20 + "..."
    assert result.endswith("...")


def test_make_snippet_preserves_short_text():
    assert br._make_snippet("Hello world") == "Hello world"


@patch("build_readme.feedparser.parse", side_effect=_mock_feedparser_parse)
@patch("build_readme._fetch_json", side_effect=_mock_fetch_json)
def test_content_pieces_have_snippets(mock_fetch, mock_feed):
    pieces = br.get_latest_pybites_content()
    assert all(p.snippet for p in pieces)

    article = pieces[0]
    assert "great" in article.snippet
    assert "<b>" not in article.snippet


def test_generate_readme(tmp_path):
    template = tmp_path / "TEMPLATE.md"
    readme = tmp_path / "README.md"
    template.write_text("{% for p in posts %}{{ p.title }}\n{% endfor %}")

    content = {
        "posts": [br.ContentPiece(url="https://example.com", title="Hello")],
    }

    with patch.object(br, "TEMPLATE_FILE", template), patch.object(
        br, "README_FILE", readme
    ):
        br.generate_readme(content)

    assert "Hello" in readme.read_text()
