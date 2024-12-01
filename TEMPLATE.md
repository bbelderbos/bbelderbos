> 👋 Hi there, I am a software developer passionate about building useful tools and helping people grow their Python + programming skills through <a href="https://pybit.es" target="_blank">Pybites</a>.

<table><tr><td valign="top" width="33%">

### Latest Pybites articles

<ul>
{% for article in articles %}
  <li><a href="{{ article.url }}" target="_blank">{{ article.title }}</a> - {{ article.date }}</li>
{% endfor %}
</ul>

> <a href="https://pybit.es/articles/" target="_blank">More &raquo;</a>


</td><td valign="top" width="34%">

### Latest Python tips

<ul>
{% for tip in tips %}
  <li><a href="{{ tip.url }}" target="_blank">{{ tip.title }}</a> - {{ tip.date }}</li>
{% endfor %}
</ul>

> <a href="https://github.com/bbelderbos/bobcodesit" target="_blank">More &raquo;</a>


</td><td valign="top" width="33%">

### Latest Rust notes

<ul>
{% for note in notes %}
  <li><a href="{{ note.url }}" target="_blank">{{ note.title }}</a> - {{ note.date }}</li>
{% endfor %}
</ul>

> <a href="https://apythonistalearningrust.com/" target="_blank">More &raquo;</a>

</td></tr></table>

<a href="https://github.com/bbelderbos/bbelderbos/actions" target="_blank"><img src="https://github.com/bbelderbos/bbelderbos/workflows/Daily%20Update/badge.svg" align="right" alt="Build README"></a>Roll your own: <a href="https://pybit.es/articles/how-to-create-a-self-updating-github-readme/" target="_blank">How to create a self updating GitHub Readme</a>.
