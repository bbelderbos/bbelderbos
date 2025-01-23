### Hi there! 👋

- 🐍 Python software developer
- 💻 Co-Founder of PyBites
- 📚 Love books/reading

<table><tr><td valign="top" width="50%">

### Latest Bluesky posts

<ul>

  <li>
    TIL there is a #uv buildpack for #Heroku, nice!

https://github.com/dropseed/heroku-buildpack-uv

This saves me the manual step of generating the requirements.txt from an updated pyproject.toml with git-based (not Docker) deployments 😍 📈 (22 Jan 2025) - <a href="https://bsky.app/profile/bbelderbos.bsky.social/post/3lgdnto2ges2d" target="_blank">link</a>
  </li>

  <li>
    #Python regex tip: 

Use groupdict() to extract groups as a dict!

• Tuple: r"(\d{4})-(\d{2})-(\d{2})" 
→ match.groups() → ('2025', '01', '22')

• Dict: r"(?P\d{4})-(?P\d{2})-(?P\d{2})" 
→ match.groupdict() → {'year': '2025', 'month': '01', 'day': '22'} (22 Jan 2025) - <a href="https://bsky.app/profile/bbelderbos.bsky.social/post/3lgd4nd7obs2i" target="_blank">link</a>
  </li>

  <li>
    Interesting learning today: Tahoe-LAFS (Tahoe Least-Authority File Store), a free and open, secure, decentralized, fault-tolerant, distributed data store and distributed file system.

Have you used this for anything? (21 Jan 2025) - <a href="https://bsky.app/profile/bbelderbos.bsky.social/post/3lgbdwcfhik2f" target="_blank">link</a>
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