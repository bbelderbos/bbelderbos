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
    {
        "content_type": "video",
        "title": "Video One",
        "link": "https://youtube.com/watch?v=1",
        "summary": "A video.",
    },
]

FAKE_BITES_RESPONSE = [
    {
        "title": "Sum n numbers",
        "slug": "sum-n-numbers",
        "description": "...",
        "level": "beginner",
        "tags": [],
    },
    {
        "title": "Regex fun",
        "slug": "regex-fun",
        "description": "...",
        "level": "intermediate",
        "tags": [],
    },
    {
        "title": "Word values",
        "slug": "word-values",
        "description": "...",
        "level": "advanced",
        "tags": [],
    },
]

FAKE_TIPS_RESPONSE = [
    {
        "title": "swap 2 variables",
        "slug": "swap-2-variables",
        "description": "...",
        "code": "...",
        "explanation": "...",
    },
    {
        "title": "f-strings",
        "slug": "f-strings",
        "description": "...",
        "code": "...",
        "explanation": "...",
    },
    {
        "title": "walrus operator",
        "slug": "walrus-operator",
        "description": "...",
        "code": "...",
        "explanation": "...",
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
    if url == br.PYBITES_TIPS_URL:
        return FAKE_TIPS_RESPONSE
    raise ValueError(f"Unexpected URL: {url}")


@patch("build_readme._fetch_json", side_effect=_mock_fetch_json)
def test_get_latest_pybites_content_default(mock_fetch):
    pieces = br.get_latest_pybites_content()

    assert len(pieces) == 6
    assert all(isinstance(p, br.ContentPiece) for p in pieces)

    articles = [p for p in pieces if p.content_type == "Article"]
    bites = [p for p in pieces if p.content_type == "Bite"]
    tips = [p for p in pieces if p.content_type == "Tip"]
    assert len(articles) == 2
    assert len(bites) == 2
    assert len(tips) == 2


@patch("build_readme._fetch_json", side_effect=_mock_fetch_json)
def test_get_latest_pybites_content_num_items(mock_fetch):
    pieces = br.get_latest_pybites_content(num_items=1)
    assert len(pieces) == 3
    assert [p.content_type for p in pieces] == ["Article", "Bite", "Tip"]


@patch("build_readme._fetch_json", side_effect=_mock_fetch_json)
def test_articles_filter_non_article_types(mock_fetch):
    pieces = br.get_latest_pybites_content(num_items=10)

    articles = [p for p in pieces if p.content_type == "Article"]
    assert len(articles) == 3
    assert all("pybit.es/articles" in a.url for a in articles)


@patch("build_readme._fetch_json", side_effect=_mock_fetch_json)
def test_bite_urls_use_platform_domain(mock_fetch):
    pieces = br.get_latest_pybites_content()
    bites = [p for p in pieces if p.content_type == "Bite"]

    assert bites[0].url == "https://pybitesplatform.com/bites/sum-n-numbers/"
    assert bites[1].url == "https://pybitesplatform.com/bites/regex-fun/"


@patch("build_readme._fetch_json", side_effect=_mock_fetch_json)
def test_tip_urls_use_platform_domain(mock_fetch):
    pieces = br.get_latest_pybites_content()
    tips = [p for p in pieces if p.content_type == "Tip"]

    assert tips[0].url == "https://pybitesplatform.com/tips/swap-2-variables/"
    assert tips[1].url == "https://pybitesplatform.com/tips/f-strings/"


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


@patch("build_readme._fetch_json", side_effect=_mock_fetch_json)
def test_content_pieces_have_snippets(mock_fetch):
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
