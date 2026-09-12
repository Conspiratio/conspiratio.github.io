---
title: Links
permalink: /links/
redirect_from:
  - /links.html
---

Hier findet Ihr Verweise auf andere lesenswerte Seiten.

<ul class="linkliste">
{%- for eintrag in site.data.links %}
  <li>
    <a href="{{ eintrag.ziel }}" target="_blank" rel="noopener">{{ eintrag.titel }}</a>
    <span class="linkliste-text">{{ eintrag.beschreibung }}</span>
  </li>
{%- endfor %}
</ul>
