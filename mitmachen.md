---
title: Mitmachen
permalink: /mitmachen/
redirect_from:
  - /ueber.html
---

Conspiratio ist ein Freizeitprojekt und quelloffen unter der GPL-3.0. Unterstützung wird in
allen Bereichen gesucht — am dringendsten in diesen:

- **Spielen und berichten.** Was sich unrund anfühlt, was unklar ist, was fehlt. Das ist die
  Hilfe, die am meisten bringt und am wenigsten kostet.
- **Grafik.** Der neue Client übernimmt die Bilder des alten; vieles davon ist zwanzig Jahre
  alt.
- **Übersetzung.** Das Spiel gibt es bisher nur auf Deutsch.
- **Programmierung.** C# und Godot 4.7. Die Spielregeln liegen in einer eigenen Bibliothek mit
  Tests, der Client setzt nur die Oberfläche darauf.

Am einfachsten geht das über [Discord](https://discord.gg/dxkC5DPgRY) oder direkt auf
[GitHub](https://github.com/Conspiratio/).

## Das Team

Das Projekt ins Leben gerufen und maßgeblich daran mitgewirkt haben:

{% for person in site.data.team -%}
**{{ person.name }}**
{{ person.rolle }}
{% endfor %}
