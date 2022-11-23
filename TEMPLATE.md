> 👋 Hi there, I am a software developer passionate about building useful tools and helping people grow their Python + programming skills through <a href="https://pybit.es" target="_blank">Pybites</a>.

<table><tr><td valign="top" width="33%">

### Latest Pybites articles

<ul>
{% for article in articles %}
  <li><a href="{{ article.url }}" target="_blank">{{ article.title }}</a> - {{ article.date }}</li>
{% endfor %}
</ul>

> <a href="https://pybit.es/articles/" target="_blank">More articles</a>


</td><td valign="top" width="34%">

### Latest Python tips

<ul>
{% for tip in tips %}
  <li><a href="{{ tip.url }}" target="_blank">{{ tip.title }}</a> - {{ tip.date }}</li>
{% endfor %}
</ul>

> <a href="https://github.com/bbelderbos/bobcodesit" target="_blank">More tips</a>


</td><td valign="top" width="33%">

### Latest Fosstodon toots

{% for toot in toots %}
  <blockquote>
  {{toot.title}}
  - <a href="{{ toot.url }}" target="_blank">{{ toot.date }}</a>
  </blockquote>
{% endfor %}

<br>

> <a href="https://fosstodon.org/@bbelderbos" target="_blank">More toots</a>


</td></tr></table>

<a href="https://github.com/bbelderbos/bbelderbos/actions" target="_blank"><img src="https://github.com/bbelderbos/bbelderbos/workflows/Daily%20Update/badge.svg" align="right" alt="Build README"></a>Roll your own: <a href="https://pybit.es/articles/how-to-create-a-self-updating-github-readme/" target="_blank">How to create a self updating GitHub Readme</a>.
