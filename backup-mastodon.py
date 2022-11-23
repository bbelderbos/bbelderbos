import datetime
import sys

import feedparser
import sqlite_utils

FOSSTODON = "https://fosstodon.org/@{username}.rss"
DB = "toots.db"
ME = "bbelderbos"


def main(username):
    url = FOSSTODON.format(username=username)
    entries = feedparser.parse(url).entries

    db = sqlite_utils.Database(DB)
    rows = [
        {
            "id": int(entry.id.split("/")[-1]),
            "published": datetime.datetime(*entry.published_parsed[:6]),
            "summary": entry.summary,
            # could normalize, but KISS for now:
            "tags": ", ".join(t.term for t in getattr(entry, "tags", [])),
            "media": (
                entry.media_content[0]["url"]
                if getattr(entry, "media_content", False)
                else ""
            )
        } for entry in entries
    ]
    db[username].upsert_all(
        rows, pk="id", column_order=("id", "twitter", "name")
    )


if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) == 2 else ME
    main(username)
