### Hi there! 👋

- 🐍 Python software developer
- 💻 Co-Founder of PyBites
- 📚 Love books/reading

<table><tr><td valign="top" width="50%">

### Latest Bluesky posts

<ul>

  <li>
    Another #python stdlib gem 💎 + context manager 😎

`tempfile.TemporaryDirectory()`

- Creates a real temp dir on disk (e.g. /tmp/...)
- Cleans up automatically after the with block, no need to delete manually.

Eg: 

with TemporaryDirectory() as tmpdir:
... do stuff

# dir removed here (01 Apr 2025) - <a href="https://bsky.app/profile/bbelderbos.bsky.social/post/3llqz4au4422c" target="_blank">link</a>
  </li>

  <li>
    Oh I have pillow in this env - how so?

$ pipdeptree -r -p pillow
pillow==10.4.0
└── newspaper3k==0.2.8 [requires: pillow>=3.3.0]

Ok, got it!

Turns out you can also just use (uv) pip:

$ pip show pillow
...
Requires:
Required-by: newspaper3k

#python (01 Apr 2025) - <a href="https://bsky.app/profile/bbelderbos.bsky.social/post/3llqwwsnqu22a" target="_blank">link</a>
  </li>

  <li>
    Stumbled upon this nice quote today = great reminder as well:

"Heroism doesn’t always have to consist of spectacular deeds. Someone who quietly, persistently does what needs to be done in his or her life is also a hero."
- Stephen Fry (01 Apr 2025) - <a href="https://bsky.app/profile/bbelderbos.bsky.social/post/3llqvbwyfbk2v" target="_blank">link</a>
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