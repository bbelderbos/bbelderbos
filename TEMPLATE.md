Software developer passionate about building useful tools and helping people grow their Python + programming skills through [Pybites](https://pybit.es).

<table><tr><td valign="top" width="50%">

### Latest Pybites articles

<ul>
{% for article in articles %}
  <li><a href="{{ article.url }}">{{ article.title }}</a> - {{ article.date }}</li>
{% endfor %}
</ul>

More on [pybit.es](https://pybit.es/articles/)

</td><td valign="top" width="50%">

### Latest Python tips

<ul>
{% for tip in tips %}
  <li><a href="{{ tip.url }}">{{ tip.title }}</a> - {{ tip.date }}</li>
{% endfor %}
</ul>

More on [bobcodesit](https://github.com/bbelderbos/bobcodesit)

</td></tr></table>

<a href="https://github.com/bbelderbos/bbelderbos/actions"><img src="https://github.com/bbelderbos/bbelderbos/workflows/Daily%20Update/badge.svg" align="right" alt="Build README"></a> - Inspired by <a href="https://pybit.es/articles/how-to-create-a-self-updating-github-readme/">How to create a self updating GitHub Readme</a>.
