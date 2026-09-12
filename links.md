---
title: Links
permalink: /links/
redirect_from:
  - /links.html
---

Hier findet Ihr Verweise auf andere lesenswerte Seiten.

{% for eintrag in site.data.links -%}
**[{{ eintrag.titel }}]({{ eintrag.ziel }})**
{{ eintrag.beschreibung }}
{% endfor %}
