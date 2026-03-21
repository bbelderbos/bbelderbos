from unittest.mock import patch, MagicMock

import build_readme as br


FAKE_FEED_ENTRIES = [
    MagicMock(link="https://belderbos.dev/post-one/", title="Post One"),
    MagicMock(link="https://belderbos.dev/post-two/", title="Post Two"),
    MagicMock(link="https://belderbos.dev/post-three/", title="Post Three"),
    MagicMock(link="https://belderbos.dev/post-four/", title="Post Four"),
    MagicMock(link="https://belderbos.dev/post-five/", title="Post Five"),
    MagicMock(link="https://belderbos.dev/post-six/", title="Post Six"),
]


@patch("build_readme.feedparser.parse")
def test_get_latest_posts_default(mock_parse):
    mock_parse.return_value.entries = FAKE_FEED_ENTRIES

    posts = br.get_latest_posts()

    assert len(posts) == 5
    assert all(isinstance(p, br.Post) for p in posts)
    assert posts[0].title == "Post One"
    assert posts[0].url == "https://belderbos.dev/post-one/"
    mock_parse.assert_called_once_with(br.BELDERBOS_FEED)


@patch("build_readme.feedparser.parse")
def test_get_latest_posts_custom_count(mock_parse):
    mock_parse.return_value.entries = FAKE_FEED_ENTRIES

    posts = br.get_latest_posts(num_items=2)

    assert len(posts) == 2
    assert posts[0].title == "Post One"
    assert posts[1].title == "Post Two"


@patch("build_readme.feedparser.parse")
def test_get_latest_posts_empty_feed(mock_parse):
    mock_parse.return_value.entries = []

    posts = br.get_latest_posts()

    assert posts == []


def test_generate_readme(tmp_path):
    template = tmp_path / "TEMPLATE.md"
    readme = tmp_path / "README.md"
    template.write_text("{% for p in posts %}{{ p.title }}\n{% endfor %}")

    posts = [br.Post(url="https://example.com", title="Hello")]

    with patch.object(br, "TEMPLATE_FILE", template), patch.object(
        br, "README_FILE", readme
    ):
        br.generate_readme(posts)

    assert "Hello" in readme.read_text()
