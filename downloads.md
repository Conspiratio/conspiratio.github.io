---
title: Downloads
permalink: /downloads/
redirect_from:
  - /download.html
---

## Der neue Client (Godot)

Conspiratio wird von Grund auf neu gebaut: derselbe Spielinhalt, neue Oberfläche, Godot 4.7
statt WinForms. Der neue Client ist inhaltlich vollständig und wird derzeit geprüft — eine
erste Fassung erscheint demnächst.

<p class="hinweis">
  Bis dahin ist die WinForms-Fassung darunter die spielbare Version.
</p>

- [Entwicklungsstand und Quellcode](https://github.com/Conspiratio/Conspiratio.Godot)
- [Was neu sein wird](https://github.com/Conspiratio/Conspiratio.Godot/blob/main/CHANGELOG.md)

Ein eigenes Handbuch zum neuen Client entsteht gerade; bis dahin gilt das
[bestehende Wiki](https://github.com/Conspiratio/Conspiratio.Wiki/wiki), dessen Spielregeln
für beide Clients dieselben sind.

**Systemvoraussetzungen:** Windows 10 oder Windows 11, .NET 8.

## Der bisherige Client (WinForms)

{%- assign aktuell = site.data.downloads | first %}

<p><a class="knopf" href="{{ aktuell.msi }}">Version {{ aktuell.version }} herunterladen</a></p>

<p>
  {{ aktuell.datum | date: "%d.%m.%Y" }} · {{ aktuell.groesse }} ·
  <a href="{{ aktuell.changelog }}">Changelog</a>
</p>

**Systemvoraussetzungen:** Windows 7 bis Windows 11,
[.NET Framework 4.6.2](https://www.microsoft.com/de-de/download/details.aspx?id=53344),
Administratorrechte für die Installation.

### Installation

1. Auf den Downloadknopf klicken.
2. Die heruntergeladene MSI-Datei ausführen.
3. Den Installationsanweisungen folgen.

### Ältere Fassungen

<ul>
{%- for eintrag in site.data.downloads offset: 1 %}
  <li>
    Version {{ eintrag.version }} ({{ eintrag.datum | date: "%d.%m.%Y" }}, {{ eintrag.groesse }}) —
    {% if eintrag.msi %}<a href="{{ eintrag.msi }}">MSI</a> · {% endif %}
    <a href="{{ eintrag.changelog }}">Changelog</a>
  </li>
{%- endfor %}
</ul>

<p class="hinweis">
  Von 1.4.1 und 1.4.2 gibt es kein Installationsprogramm mehr: Beide wurden nie als
  GitHub-Release veröffentlicht und lagen nur auf dem alten Webspeicher. Ihr Changelog ist
  erhalten.
</p>

## Hinweise zum Spiel

Nähere Informationen stehen im [Wiki](https://github.com/Conspiratio/Conspiratio.Wiki/wiki),
im [Forum](https://forum.conspiratio.net/) oder im beigelegten ReadMe.
