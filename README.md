### Hi there! 👋

- 🐍 Python software developer
- 💻 Co-Founder of PyBites
- 📚 Love books/reading

<table><tr><td valign="top" width="50%">

### Latest Bluesky posts

<ul>

  <li>
    #Django has many great template filters, I just used `intcomma` (requires `humanize`) and `pluralize` :)

And you can roll your own as well:

1. create a [your_app]/templatetags/tags.py

2.
from django import template
register = template.Library()

3.
@register.filter
... write your function ... (15 Jan 2025) - <a href="https://bsky.app/profile/bbelderbos.bsky.social/post/3lfs6r6g4422u" target="_blank">link</a>
  </li>

  <li>
    You can use zfill or an f-string to add leading zeros:

>>> var = 1
>>> str(var).zfill(2)
'01'
>>> f"{var:2}"
' 1'
>>> f"{var:02}"
'01'
>>> f"{var:03}"
'001'

#python (15 Jan 2025) - <a href="https://bsky.app/profile/bbelderbos.bsky.social/post/3lfrlaiz6os27" target="_blank">link</a>
  </li>

  <li>
    You can use SequenceMatcher (#python difflib module) to analyze similarity between strings. 🐍 😍

Django's manage.py uses this for example:

$ uv run python manage.py migra
Unknown command: 'migra'. Did you mean migrate?
Type 'manage.py help' for usage. (15 Jan 2025) - <a href="https://bsky.app/profile/bbelderbos.bsky.social/post/3lfrfqhk6ss2x" target="_blank">link</a>
  </li>

</ul>

> <a href="https://bsky.app/profile/bbelderbos.bsky.social" target="_blank">Follow me &raquo;</a>


</td><td valign="top" width="50%">

### Latest Python tips

<ul>

  <li>
    Timing code in Python: Using `timeit` to compare merging dictionaries in #Python: Old way with `**` unpacking vs. new way with `|`. ... (26 Jul 2024) - <a href="https://github.com/bbelderbos/bobcodesit/blob/main/notes/20240726111622.md" target="_blank">link</a>
  </li>

  <li>
    Merging dictionaries: Old way: `{**dict1, **dict2}` ... (26 Jul 2024) - <a href="https://github.com/bbelderbos/bobcodesit/blob/main/notes/20240726111507.md" target="_blank">link</a>
  </li>

  <li>
    You can now use | for typing: `|` got added to type hints >= 3.10, not needing the `typing` import anymore for these: ... (26 Jul 2024) - <a href="https://github.com/bbelderbos/bobcodesit/blob/main/notes/20240726111223.md" target="_blank">link</a>
  </li>

  <li>
    dict dispatch pattern: Tired of long and unmaintainable `if-elif-elif-else` chains? 😱 ... (13 Jul 2024) - <a href="https://github.com/bbelderbos/bobcodesit/blob/main/notes/20240713105037.md" target="_blank">link</a>
  </li>

  <li>
    split file name and extension: `pathlib` has you covered, just make a `Path` object and access the `stem` and `suffix` attributes: ... (11 Jul 2024) - <a href="https://github.com/bbelderbos/bobcodesit/blob/main/notes/20240711112258.md" target="_blank">link</a>
  </li>

</ul>

> <a href="https://github.com/bbelderbos/bobcodesit" target="_blank">More Python tips &raquo;</a>

</td>
</tr></table>

<a href="https://github.com/bbelderbos/bbelderbos/actions" target="_blank"><img src="https://github.com/bbelderbos/bbelderbos/workflows/Daily%20Update/badge.svg" align="right" alt="Build README"></a>Roll your own: <a href="https://pybit.es/articles/how-to-create-a-self-updating-github-readme/" target="_blank">How to create a self updating GitHub Readme</a>.