# Modernisierung conspiratio.net — Implementierungsplan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Die Projektseite conspiratio.net wird eine responsive, umschaltbar helle/dunkle
Jekyll-Seite auf GitHub Pages, deren Newsmeldungen aus je einer Markdown-Datei entstehen.

**Architecture:** Jekyll baut statisches HTML aus Layouts (`_layouts/`), Bausteinen (`_includes/`),
Daten (`_data/*.yml`) und Meldungen (`_posts/*.md`). Gebaut wird lokal in einem Docker-Container mit
derselben `Gemfile.lock` wie in CI; ausgeliefert wird über einen GitHub-Actions-Workflow. Die
Abnahme läuft über ein Python-Prüfskript, das die gebaute Seite in `_site/` gegen feste Zusagen
prüft — es ersetzt die Testsuite, die es für eine statische Seite sonst nicht gäbe.

**Tech Stack:** Jekyll 4.3 (Ruby 3.3, im Container), jekyll-feed / -seo-tag / -sitemap /
-redirect-from, handgeschriebenes CSS mit Custom Properties, ~40 Zeilen Vanilla-JavaScript,
Python 3.11 (Prüfskript, Bildaufbereitung mit Pillow), GitHub Actions, lychee.

**Spec:** [`docs/superpowers/specs/2026-09-12-webseite-modernisierung-design.md`](../specs/2026-09-12-webseite-modernisierung-design.md)

## Global Constraints

Diese Vorgaben gelten für **jede** Aufgabe; sie werden nicht je Aufgabe wiederholt.

- **Repo:** `Conspiratio/conspiratio.github.io`, Arbeitszweig `feature/pages-neubau`, Zielzweig `main`.
- **Sprache:** Alle sichtbaren Texte, Dateinamen eigener Dateien, Commit-Nachrichten und Kommentare
  auf **Deutsch**. Ausgenommen sind Schnittstellenbegriffe des Frameworks (`_posts`, `_data`,
  `_layouts`, `title`, `date`, `excerpt`, `permalink`, `redirect_from`) — sie bleiben englisch, weil
  Jekyll sie so und nur so liest.
- **Kein CMS, keine Datenbank, kein CSS- oder JS-Framework.** Genau eine CSS-Datei
  (`assets/css/conspiratio.css`) und eine JS-Datei (`assets/js/einstellungen.js`).
- **Plugins abschließend:** `jekyll-feed`, `jekyll-seo-tag`, `jekyll-sitemap`,
  `jekyll-redirect-from`. Keine weiteren.
- **Schriften werden selbst ausgeliefert.** Im gesamten `_site/` darf kein Verweis auf
  `fonts.googleapis.com` oder `fonts.gstatic.com` stehen.
- **`OLDENGL.TTF` wird entfernt** (Microsoft-Systemschrift, nicht zur Weitergabe lizenziert) und darf
  in keiner Fassung wieder auftauchen.
- **Ohne JavaScript** muss jede Seite vollständig lesbar und bedienbar bleiben; JavaScript schaltet
  ausschließlich Thema und Schriftart um.
- **Kontrast** mindestens 4,5:1 in beiden Themen; jedes `<img>` trägt `alt`, `width`, `height` und
  `loading="lazy"` (Ausnahme: das Aufmacherbild der Startseite, das ohne `loading="lazy"` lädt).
- **Domain-Umschaltung findet in diesem Plan nicht statt.** Bis Aufgabe 10 liegt die neue Seite unter
  `https://conspiratio.github.io`; `conspiratio.net` zeigt weiterhin auf Hostgator. Die DNS-Schritte
  sind in Aufgabe 10 nur dokumentiert, nicht ausgeführt — sie kann nur der Domaineigentümer tun.
- **Jede Aufgabe endet grün:** `pwsh werkzeug/bauen.ps1` baut ohne Fehler **und**
  `python werkzeug/pruefe_ausgabe.py` meldet keinen Fehler. Erst dann wird committet.

### Werkzeugvoraussetzungen (einmalig, vor Aufgabe 1)

Auf der Maschine vorhanden und geprüft: Docker 29.6, Python 3.11.4, Node 22, `gh` 2.96.
**Ruby ist nicht installiert und wird auch nicht installiert** — der Build läuft im Container.

```powershell
python -m pip install --user pillow fonttools brotli
```

---

## Dateiübersicht

Was am Ende im Repo steht und wofür jede Datei zuständig ist. Die Zuständigkeiten sind bewusst eng
geschnitten: ein Layout kennt nur seine Seitenform, ein Include nur seinen Baustein.

| Datei | Zuständigkeit | Aufgabe |
|---|---|---|
| `Gemfile`, `Gemfile.lock` | Jekyll-Version und Plugins, exakt gepinnt | 1 |
| `_config.yml` | Titel, URL, Plugins, Permalinks, Standard-Layouts, `exclude` | 1 |
| `werkzeug/bauen.ps1` | Build und Vorschau im Docker-Container | 1 |
| `werkzeug/pruefe_ausgabe.py` | prüft `_site/` gegen feste Zusagen; wächst mit jeder Aufgabe | 1–10 |
| `.github/workflows/pages.yml` | Build bei PR, Build + Deploy auf `main` | 1, 10 |
| `_layouts/basis.html` | `<html>`, `<head>`, Themenattribut, Kopf, Fuß — sonst nichts | 2 |
| `_layouts/seite.html` | Inhaltsseite: Titel + Inhalt in der Textspalte | 2 |
| `_layouts/start.html` | Startseite: Aufmacher, Download-Knopf, News-Anrisse | 6 |
| `_layouts/news.html` | eine Meldung: Titel, Datum, Inhalt, Rückweg ins Archiv | 4 |
| `_includes/navigation.html` | Kopfnavigation aus `_data/navigation.yml`, aktiver Punkt markiert | 2 |
| `_includes/fuss.html` | Fußzeile inkl. Jahreszahl aus `site.time` | 2 |
| `_includes/schalter.html` | die drei Schalter (Thema, Schrift, EN) | 3 |
| `_includes/news-anriss.html` | ein Anriss; von Startseite und Archiv benutzt | 4 |
| `_data/navigation.yml` | Menüpunkte (Titel, Ziel, extern ja/nein) | 2 |
| `_data/downloads.yml` | je Release: Version, Datum, Größe, MSI-Link, Changelog-Link | 7 |
| `_data/team.yml`, `_data/links.yml` | Team- und Linkliste | 6 |
| `_data/bilder.yml` | Galerie: Datei, Alternativtext, Client, Maße | 8 |
| `assets/css/conspiratio.css` | gesamtes Aussehen; Custom Properties als einzige Schaltstelle | 3 |
| `assets/js/einstellungen.js` | Thema- und Schriftumschalter, `localStorage` | 3 |
| `assets/schriften/*.woff2` | Grenze Gotisch, EB Garamond, Atkinson Hyperlegible | 3 |
| `_posts/*.md` | je eine Newsmeldung | 4, 5 |
| `index.html`, `spiel.md`, `bilder.md`, `downloads.md`, `mitmachen.md`, `kontakt.md`, `links.md`, `impressum.md`, `en/index.md`, `news/index.html` | die Seiten | 6–8 |
| `CNAME` | `conspiratio.net` | 10 |
| `werkzeug/neue-news.ps1` | legt eine Meldungsdatei mit fertigem Kopf an | 4 |
| `werkzeug/bilder_aufbereiten.py` | Skalierung, WebP, Maße in `_data/bilder.yml` | 8 |

---

## Aufgabe 1: Gerüst, Build im Container und Prüfskript

Ohne diese Aufgabe kann keine andere abgenommen werden — sie liefert den Test-Kreislauf.

**Files:**
- Create: `Gemfile`, `_config.yml`, `index.html`, `_layouts/basis.html`
- Create: `werkzeug/bauen.ps1`, `werkzeug/pruefe_ausgabe.py`
- Create: `.github/workflows/pages.yml`, `.gitignore`

**Interfaces:**
- Consumes: nichts.
- Produces:
  - `pwsh werkzeug/bauen.ps1` → baut nach `_site/`; `-Vorschau` startet den Server auf
    `http://localhost:4000`.
  - `python werkzeug/pruefe_ausgabe.py` → Exit 0 bei Erfolg, Exit 1 mit einer Fehlerliste sonst.
  - `werkzeug/pruefe_ausgabe.py` stellt den folgenden Aufbau bereit, den **alle späteren Aufgaben
    erweitern**: eine Funktion `pruefe(bedingung: bool, meldung: str) -> None`, eine Liste
    `PRUEFUNGEN: list[Callable[[], None]]`, und `SITE: pathlib.Path` als Wurzel der gebauten Seite.
  - Layout `basis` mit den Blöcken `{{ content }}`, `{{ page.title }}`.

- [ ] **Step 1: Arbeitszweig anlegen**

```bash
cd "D:/Projekte/C# Projekte/conspiratio.github.io"
git checkout -b feature/pages-neubau
```

- [ ] **Step 2: Das Prüfskript schreiben — es schlägt zuerst fehl**

`werkzeug/pruefe_ausgabe.py`:

```python
#!/usr/bin/env python3
"""Prueft die gebaute Seite in _site/ gegen feste Zusagen.

Aufruf: python werkzeug/pruefe_ausgabe.py
Exit 0 = alles in Ordnung, Exit 1 = mindestens eine Zusage verletzt.
"""
from __future__ import annotations

import pathlib
import sys
from typing import Callable

WURZEL = pathlib.Path(__file__).resolve().parent.parent
SITE = WURZEL / "_site"

_fehler: list[str] = []
PRUEFUNGEN: list[Callable[[], None]] = []


def pruefe(bedingung: bool, meldung: str) -> None:
    """Vermerkt einen Fehler, wenn die Bedingung nicht gilt."""
    if not bedingung:
        _fehler.append(meldung)


def lies(pfad: str) -> str:
    """Liest eine Datei aus _site/ als Text; leerer String, wenn sie fehlt."""
    datei = SITE / pfad
    return datei.read_text(encoding="utf-8") if datei.is_file() else ""


def seiten() -> list[pathlib.Path]:
    """Alle gebauten HTML-Dateien."""
    return sorted(SITE.rglob("*.html"))


def ist_weiterleitung(text: str) -> bool:
    """Von jekyll-redirect-from erzeugte Stuempel sind keine richtigen Seiten:
    sie tragen weder Navigation noch Fuss und stehen auf lang="en-US"."""
    return 'http-equiv="refresh"' in text


def pruefung(funktion: Callable[[], None]) -> Callable[[], None]:
    PRUEFUNGEN.append(funktion)
    return funktion


@pruefung
def die_seite_wurde_gebaut() -> None:
    pruefe(SITE.is_dir(), "_site/ fehlt - wurde `pwsh werkzeug/bauen.ps1` ausgefuehrt?")
    pruefe((SITE / "index.html").is_file(), "_site/index.html fehlt")


@pruefung
def jede_seite_nennt_ihre_sprache() -> None:
    for seite in seiten():
        text = seite.read_text(encoding="utf-8")
        if ist_weiterleitung(text):
            continue
        pfad = seite.relative_to(SITE)
        erwartet = 'lang="en"' if str(pfad).startswith("en") else 'lang="de"'
        pruefe(erwartet in text, f"{pfad}: erwartet {erwartet} im <html>-Tag")


def main() -> int:
    for funktion in PRUEFUNGEN:
        funktion()
    if _fehler:
        print(f"{len(_fehler)} Zusage(n) verletzt:\n")
        for meldung in _fehler:
            print(f"  - {meldung}")
        return 1
    print(f"{len(PRUEFUNGEN)} Pruefung(en) bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Prüfskript laufen lassen — es muss fehlschlagen**

Run: `python werkzeug/pruefe_ausgabe.py`
Expected: Exit 1, „`_site/ fehlt`" und „`_site/index.html fehlt`".

- [ ] **Step 4: Gemfile, Konfiguration und ein Minimallayout schreiben**

`Gemfile`:

```ruby
source "https://rubygems.org"

gem "jekyll", "~> 4.3.4"
gem "jekyll-feed", "~> 0.17"
gem "jekyll-seo-tag", "~> 2.8"
gem "jekyll-sitemap", "~> 1.4"
gem "jekyll-redirect-from", "~> 0.16"
gem "webrick", "~> 1.8"
```

`_config.yml`:

```yaml
title: Conspiratio
description: >-
  Conspiratio ist eine freie Wirtschaftssimulation der frühen Neuzeit: Handel, Ämter,
  Intrigen und eine Dynastie, die den eigenen Tod überdauern muss.
url: https://conspiratio.net
lang: de

plugins:
  - jekyll-feed
  - jekyll-seo-tag
  - jekyll-sitemap
  - jekyll-redirect-from

permalink: /news/:year/:month/:day/:title/

defaults:
  - scope: { path: "", type: posts }
    values: { layout: news }
  - scope: { path: "" }
    values: { layout: seite }

feed:
  path: feed.xml
  posts_limit: 50   # Vorgabe waere 10; der Feed soll das ganze Archiv tragen

exclude:
  - Gemfile
  - Gemfile.lock
  - README.md
  - LICENSE
  - docs/
  - werkzeug/
  - massenmails/
  - rohbilder/
  - "*.txt"
```

`_layouts/basis.html` (vorläufig; Kopf und Fuß kommen in Aufgabe 2):

```html
<!DOCTYPE html>
<html lang="{{ page.lang | default: site.lang }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  {%- seo -%}
  <link rel="icon" href="/assets/bilder/icon.png">
</head>
<body>
  <main>
    {{ content }}
  </main>
</body>
</html>
```

`index.html`:

```html
---
layout: basis
title: Conspiratio
---
<h1>Conspiratio</h1>
```

`.gitignore`:

```
_site/
.jekyll-cache/
.jekyll-metadata
rohbilder/
```

- [ ] **Step 5: Das Bauskript schreiben**

`werkzeug/bauen.ps1`:

```powershell
<#
.SYNOPSIS
    Baut die Seite im Docker-Container - ohne lokale Ruby-Installation.
.DESCRIPTION
    Benutzt dasselbe Gemfile.lock wie CI, weil der Container Linux ist wie der Runner.
    Die Gems liegen in einem benannten Volume und ueberleben den Lauf.
.PARAMETER Vorschau
    Startet statt eines einmaligen Builds den Entwicklungsserver auf http://localhost:4000.
#>
param([switch]$Vorschau)

$ErrorActionPreference = "Stop"
$wurzel = Split-Path $PSScriptRoot -Parent

# --force_polling: Dateiaenderungen auf einem Windows-Bind-Mount erreichen den
# Container nicht als Ereignis, nur durch Nachsehen.
$befehl = if ($Vorschau) {
    "bundle install --quiet && bundle exec jekyll serve --host 0.0.0.0 --force_polling"
} else {
    "bundle install --quiet && bundle exec jekyll build"
}

docker run --rm `
    -v "${wurzel}:/srv" -w /srv `
    -v conspiratio-gems:/usr/local/bundle `
    -p 4000:4000 `
    ruby:3.3 bash -lc $befehl

if ($LASTEXITCODE -ne 0) { throw "Build fehlgeschlagen (Exit $LASTEXITCODE)" }
```

- [ ] **Step 6: Bauen und prüfen — jetzt muss es grün sein**

```powershell
pwsh werkzeug/bauen.ps1
python werkzeug/pruefe_ausgabe.py
```

Expected: Build ohne Fehler, `_site/index.html` vorhanden, „2 Pruefung(en) bestanden."
Der erste Lauf dauert wegen `bundle install` mehrere Minuten; danach ist das Volume gefüllt.

- [ ] **Step 7: Den CI-Workflow schreiben**

`.github/workflows/pages.yml`:

```yaml
name: Seite bauen und veröffentlichen

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  bauen:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: "3.3"
          bundler-cache: true
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Seite bauen
        run: bundle exec jekyll build
        env:
          JEKYLL_ENV: production
      - name: Ausgabe prüfen
        run: python werkzeug/pruefe_ausgabe.py
      - uses: actions/upload-pages-artifact@v3
        with:
          path: _site

  veroeffentlichen:
    needs: bauen
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deploy.outputs.page_url }}
    steps:
      - id: deploy
        uses: actions/deploy-pages@v4
```

- [ ] **Step 8: `Gemfile.lock` aus dem Container übernehmen und committen**

Der Container hat die Datei beim ersten `bundle install` geschrieben. Sie **muss** eingecheckt
werden, sonst ist die Version in CI nicht gepinnt und `bundler-cache: true` greift nicht.

```bash
git add Gemfile Gemfile.lock _config.yml index.html _layouts/basis.html .gitignore \
        werkzeug/bauen.ps1 werkzeug/pruefe_ausgabe.py .github/workflows/pages.yml
git status   # Gemfile.lock muss dabei sein
git commit -F - <<'EOF'
Gerüst: Jekyll-Build im Container, Prüfskript und CI-Workflow

Baut ohne lokale Ruby-Installation über ruby:3.3, mit demselben
Gemfile.lock wie der CI-Runner. Das Prüfskript tritt an die Stelle
einer Testsuite und wächst mit jeder weiteren Aufgabe.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
```

---

## Aufgabe 2: Basislayout, Navigation und Fußzeile

Beseitigt die Ursache des wiederkehrenden Ärgers („Jahreszahl auf jeder Seite aktualisiert"):
Navigation und Fußzeile stehen ab hier **einmal** im Repo.

**Files:**
- Create: `_data/navigation.yml`, `_includes/navigation.html`, `_includes/fuss.html`,
  `_layouts/seite.html`
- Modify: `_layouts/basis.html`, `werkzeug/pruefe_ausgabe.py`
- Create: `spiel.md` (als zweite Seite, damit die Navigation prüfbar wird)

**Interfaces:**
- Consumes: `pruefe`, `lies`, `seiten`, `pruefung`, `SITE` aus Aufgabe 1.
- Produces:
  - `_data/navigation.yml`: Liste von Einträgen mit den Schlüsseln `titel`, `ziel`, `extern`
    (bool, optional).
  - Layout `seite` (erwartet `title` im Frontmatter).
  - Jede gebaute Seite enthält `<nav class="hauptnavigation">` und `<footer class="fuss">`.

- [ ] **Step 1: Die Zusagen ins Prüfskript schreiben**

Ans Ende von `werkzeug/pruefe_ausgabe.py`, **vor** `def main()`:

```python
@pruefung
def jede_seite_traegt_navigation_und_fuss() -> None:
    for seite in seiten():
        text = seite.read_text(encoding="utf-8")
        if ist_weiterleitung(text):
            continue
        pfad = seite.relative_to(SITE)
        pruefe('class="hauptnavigation"' in text, f"{pfad}: Hauptnavigation fehlt")
        pruefe('class="fuss"' in text, f"{pfad}: Fußzeile fehlt")


@pruefung
def die_navigation_markiert_die_aktuelle_seite() -> None:
    text = lies("spiel/index.html")
    pruefe('aria-current="page"' in text,
           "spiel/index.html: aktiver Menuepunkt ist nicht als aria-current markiert")


@pruefung
def die_jahreszahl_kommt_aus_der_konfiguration() -> None:
    # Der Fuss nennt das laufende Jahr; es darf in keiner Inhaltsdatei hart stehen.
    import datetime
    text = lies("index.html")
    pruefe(str(datetime.date.today().year) in text,
           "index.html: das laufende Jahr steht nicht im Fuß")
```

- [ ] **Step 2: Prüfskript laufen lassen — es muss fehlschlagen**

Run: `python werkzeug/pruefe_ausgabe.py`
Expected: Exit 1, „Hauptnavigation fehlt", „Fußzeile fehlt", „aktiver Menuepunkt …".

- [ ] **Step 3: Daten und Bausteine schreiben**

`_data/navigation.yml`:

```yaml
- titel: Das Spiel
  ziel: /spiel/
- titel: Bilder
  ziel: /bilder/
- titel: Downloads
  ziel: /downloads/
- titel: News
  ziel: /news/
- titel: Handbuch
  ziel: https://conspiratio.github.io/Conspiratio.Wiki/
  extern: true
- titel: Mitmachen
  ziel: /mitmachen/
- titel: Kontakt
  ziel: /kontakt/
```

`_includes/navigation.html` — die `<details>`-Hülle klappt unter 700 px auf und ist darüber per CSS
immer offen; das kostet kein JavaScript:

```html
<nav class="hauptnavigation" aria-label="Hauptnavigation">
  <details class="navigation-huelle">
    <summary class="navigation-knopf">Menü</summary>
    <ul>
      {%- for eintrag in site.data.navigation -%}
        {%- assign aktiv = false -%}
        {%- if page.url contains eintrag.ziel and eintrag.extern != true -%}
          {%- assign aktiv = true -%}
        {%- endif -%}
        <li>
          <a href="{{ eintrag.ziel }}"
             {% if aktiv %}aria-current="page"{% endif %}
             {% if eintrag.extern %}target="_blank" rel="noopener"{% endif %}>
            {{ eintrag.titel }}{% if eintrag.extern %} <span aria-hidden="true">↗</span>{% endif %}
          </a>
        </li>
      {%- endfor -%}
    </ul>
  </details>
</nav>
```

`_includes/fuss.html`:

```html
<footer class="fuss">
  <p>
    <a href="/links/">Links</a> ·
    <a href="/impressum/">Impressum</a> ·
    <a href="https://github.com/Conspiratio/" target="_blank" rel="noopener">GitHub</a>
  </p>
  <p class="fuss-recht">
    Conspiratio 2011–{{ site.time | date: "%Y" }} · GNU General Public License v3.0
  </p>
</footer>
```

- [ ] **Step 4: Layouts verdrahten**

`_layouts/basis.html` — der `<body>` bekommt Kopf, Inhalt, Fuß:

```html
<body>
  <a class="zum-inhalt" href="#inhalt">Zum Inhalt springen</a>
  <header class="kopf">
    <a class="wortmarke" href="/">Conspiratio</a>
  </header>
  <div class="zierbalken" role="presentation"></div>
  {%- include navigation.html -%}
  <main id="inhalt">
    {{ content }}
  </main>
  {%- include fuss.html -%}
</body>
```

`_layouts/seite.html`:

```html
---
layout: basis
---
<article class="textspalte">
  <h1>{{ page.title }}</h1>
  {{ content }}
</article>
```

`spiel.md` (vorläufiger Text; Aufgabe 6 füllt ihn):

```markdown
---
title: Über das Spiel
permalink: /spiel/
---

Zu Beginn erbt der Spieler eine heruntergekommene Produktionsstätte und das bescheidene
Ersparte eines Verwandten.
```

`index.html` bekommt `layout: seite` statt `layout: basis`.

- [ ] **Step 5: Bauen und prüfen**

```powershell
pwsh werkzeug/bauen.ps1
python werkzeug/pruefe_ausgabe.py
```

Expected: „5 Pruefung(en) bestanden."

- [ ] **Step 6: Commit**

```bash
git add _data/navigation.yml _includes _layouts index.html spiel.md werkzeug/pruefe_ausgabe.py
git commit -F - <<'EOF'
Navigation und Fußzeile stehen nur noch einmal im Repo

Die Jahreszahl kommt aus site.time und muss nie wieder von Hand
nachgezogen werden. Die Navigation klappt unter 700 px über ein
<details>-Element auf, ohne JavaScript.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
```

---

## Aufgabe 3: Gestaltung — Themen, Schriften, Umschalter

**Files:**
- Create: `assets/css/conspiratio.css`, `assets/js/einstellungen.js`,
  `assets/schriften/*.woff2`, `_includes/schalter.html`
- Modify: `_layouts/basis.html`, `werkzeug/pruefe_ausgabe.py`

**Interfaces:**
- Consumes: Layout `basis` aus Aufgabe 2.
- Produces:
  - Attribute am `<html>`: `data-thema` (`hell` | `dunkel`) und `data-schrift` (`standard` |
    `lesbar`). Beide fehlen, solange der Besucher nichts gewählt hat — dann gilt
    `prefers-color-scheme`.
  - `localStorage`-Schlüssel `conspiratio-thema` und `conspiratio-schrift` mit denselben Werten.
  - CSS-Klassen, auf die spätere Aufgaben bauen: `.textspalte`, `.galerie`, `.knopf`,
    `.news-anriss`, `.hinweis`.

- [ ] **Step 1: Die Zusagen ins Prüfskript schreiben**

```python
@pruefung
def keine_fremden_schriftabrufe() -> None:
    for seite in seiten():
        text = seite.read_text(encoding="utf-8")
        pfad = seite.relative_to(SITE)
        for fremd in ("fonts.googleapis.com", "fonts.gstatic.com"):
            pruefe(fremd not in text, f"{pfad}: verweist auf {fremd}")
    css = lies("assets/css/conspiratio.css")
    pruefe("fonts.gstatic.com" not in css, "conspiratio.css: verweist auf fonts.gstatic.com")


@pruefung
def die_schriften_liegen_im_repo() -> None:
    ordner = SITE / "assets" / "schriften"
    pruefe(ordner.is_dir(), "assets/schriften/ fehlt")
    dateien = {d.name for d in ordner.glob("*.woff2")} if ordner.is_dir() else set()
    for erwartet in ("grenze-gotisch-400.woff2", "eb-garamond-400.woff2",
                     "eb-garamond-400-kursiv.woff2", "eb-garamond-600.woff2",
                     "atkinson-hyperlegible-400.woff2", "atkinson-hyperlegible-700.woff2"):
        pruefe(erwartet in dateien, f"assets/schriften/{erwartet} fehlt")


@pruefung
def beide_themen_sind_definiert() -> None:
    css = lies("assets/css/conspiratio.css")
    pruefe(":root" in css, "conspiratio.css: :root fehlt")
    pruefe("prefers-color-scheme: dark" in css,
           "conspiratio.css: dunkles Thema folgt nicht der Systemeinstellung")
    pruefe('[data-thema="dunkel"]' in css, "conspiratio.css: dunkles Thema nicht erzwingbar")
    pruefe('[data-thema="hell"]' in css, "conspiratio.css: helles Thema nicht erzwingbar")
    pruefe('[data-schrift="lesbar"]' in css, "conspiratio.css: Lesbar-Schrift fehlt")


@pruefung
def das_alte_linkblau_ist_weg() -> None:
    css = lies("assets/css/conspiratio.css")
    pruefe("#0000FF" not in css.upper(), "conspiratio.css: enthält noch das alte Linkblau #0000FF")
    pruefe("OldEng" not in css and "OLDENGL" not in css.upper(),
           "conspiratio.css: verweist noch auf die nicht lizenzierte Schrift")


@pruefung
def das_thema_steht_vor_dem_ersten_zeichnen_fest() -> None:
    # Ohne dieses Inline-Skript im <head> blitzt beim Laden kurz das falsche Thema auf.
    text = lies("index.html")
    kopf = text.split("</head>")[0]
    pruefe("conspiratio-thema" in kopf,
           "index.html: das Thema wird nicht schon im <head> gesetzt")


@pruefung
def die_schalter_sind_bedienbar() -> None:
    text = lies("index.html")
    pruefe('id="schalter-thema"' in text, "index.html: Themenschalter fehlt")
    pruefe('id="schalter-schrift"' in text, "index.html: Schriftschalter fehlt")
    pruefe("aria-pressed" in text, "index.html: Schalter ohne aria-pressed")
```

- [ ] **Step 2: Prüfskript laufen lassen — es muss fehlschlagen**

Run: `python werkzeug/pruefe_ausgabe.py`
Expected: Exit 1, unter anderem „assets/schriften/ fehlt" und „conspiratio.css: :root fehlt".

- [ ] **Step 3: Die Schriften beschaffen und umwandeln**

Alle drei sind unter der SIL Open Font License frei; die Lizenzdateien wandern mit ins Repo.

1. Auf `fonts.google.com` je Familie „Get font" → „Download all" laden:
   **Grenze Gotisch**, **EB Garamond**, **Atkinson Hyperlegible**.
2. Aus den Archiven die statischen TTF nach `C:\temp\schriften\` entpacken:
   `GrenzeGotisch-Regular.ttf`, `EBGaramond-Regular.ttf`, `EBGaramond-Italic.ttf`,
   `EBGaramond-SemiBold.ttf`, `AtkinsonHyperlegible-Regular.ttf`,
   `AtkinsonHyperlegible-Bold.ttf`.
   (Grenze Gotisch und EB Garamond liegen zusätzlich als Variable Font bei — die statischen
   nehmen, sie sind kleiner.)
3. Umwandeln und benennen:

```powershell
$ziel = "assets/schriften"
New-Item -ItemType Directory -Force $ziel | Out-Null
$paare = @{
    "GrenzeGotisch-Regular"        = "grenze-gotisch-400"
    "EBGaramond-Regular"           = "eb-garamond-400"
    "EBGaramond-Italic"            = "eb-garamond-400-kursiv"
    "EBGaramond-SemiBold"          = "eb-garamond-600"
    "AtkinsonHyperlegible-Regular" = "atkinson-hyperlegible-400"
    "AtkinsonHyperlegible-Bold"    = "atkinson-hyperlegible-700"
}
foreach ($paar in $paare.GetEnumerator()) {
    python -m fontTools.ttLib.woff2 compress "C:\temp\schriften\$($paar.Key).ttf"
    Move-Item "C:\temp\schriften\$($paar.Key).woff2" "$ziel\$($paar.Value).woff2" -Force
}
Get-ChildItem $ziel
```

4. Die `OFL.txt` je Familie als `assets/schriften/OFL-<familie>.txt` ablegen.

- [ ] **Step 4: Das Stylesheet schreiben**

`assets/css/conspiratio.css`. Die Farben sind aus dem vorhandenen Bildmaterial genommen: das
Pergament für hell, das Introbild (Kontor bei Kerzenlicht) für dunkel.

```css
/* ---------- Schriften ---------- */
@font-face { font-family: "Grenze Gotisch"; src: url("/assets/schriften/grenze-gotisch-400.woff2") format("woff2");
             font-weight: 400; font-display: swap; }
@font-face { font-family: "EB Garamond"; src: url("/assets/schriften/eb-garamond-400.woff2") format("woff2");
             font-weight: 400; font-style: normal; font-display: swap; }
@font-face { font-family: "EB Garamond"; src: url("/assets/schriften/eb-garamond-400-kursiv.woff2") format("woff2");
             font-weight: 400; font-style: italic; font-display: swap; }
@font-face { font-family: "EB Garamond"; src: url("/assets/schriften/eb-garamond-600.woff2") format("woff2");
             font-weight: 600; font-display: swap; }
@font-face { font-family: "Atkinson Hyperlegible"; src: url("/assets/schriften/atkinson-hyperlegible-400.woff2") format("woff2");
             font-weight: 400; font-display: swap; }
@font-face { font-family: "Atkinson Hyperlegible"; src: url("/assets/schriften/atkinson-hyperlegible-700.woff2") format("woff2");
             font-weight: 700; font-display: swap; }

/* ---------- Farben: hell = Pergament ---------- */
:root {
  --grund:          #efe3c8;
  --grund-erhoben:  #f7eeda;
  --schrift:        #2a1d0d;
  --schrift-leise:  #5b4526;
  --akzent:         #8a5a12;   /* Bernstein, auf hellem Grund abgedunkelt: 5.2:1 */
  --akzent-hell:    #6d4509;
  --linie:          #c9b48a;

  --schrift-zier:   "Grenze Gotisch", "Palatino Linotype", serif;
  --schrift-text:   "EB Garamond", Georgia, serif;
  --zeilenhoehe:    1.65;
  --buchstabenabstand: 0;
  --spaltenbreite:  38rem;      /* rund 70 Zeichen */
}

/* ---------- Farben: dunkel = Kontor bei Kerzenlicht ---------- */
@media (prefers-color-scheme: dark) {
  :root:not([data-thema="hell"]) {
    --grund:         #14100b;
    --grund-erhoben: #1f1810;
    --schrift:       #ece0cb;
    --schrift-leise: #b8a68b;
    --akzent:        #e0a84a;   /* Kerzenflamme, auf dunklem Grund: 8.1:1 */
    --akzent-hell:   #f2c477;
    --linie:         #3d3122;
  }
}
:root[data-thema="dunkel"] {
  --grund:         #14100b;
  --grund-erhoben: #1f1810;
  --schrift:       #ece0cb;
  --schrift-leise: #b8a68b;
  --akzent:        #e0a84a;
  --akzent-hell:   #f2c477;
  --linie:         #3d3122;
}

/* ---------- Lesbare Schrift ---------- */
:root[data-schrift="lesbar"] {
  --schrift-zier: "Atkinson Hyperlegible", system-ui, sans-serif;
  --schrift-text: "Atkinson Hyperlegible", system-ui, sans-serif;
  --zeilenhoehe: 1.8;
  --buchstabenabstand: 0.01em;
}

/* ---------- Grundlagen ---------- */
*, *::before, *::after { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--grund);
  color: var(--schrift);
  font-family: var(--schrift-text);
  font-size: clamp(1.05rem, 0.98rem + 0.35vw, 1.2rem);
  line-height: var(--zeilenhoehe);
  letter-spacing: var(--buchstabenabstand);
}

h1, h2, h3, .wortmarke {
  font-family: var(--schrift-zier);
  font-weight: 400;
  line-height: 1.15;
}
h1 { font-size: clamp(2rem, 1.4rem + 2.6vw, 3.2rem); }
h2 { font-size: clamp(1.5rem, 1.2rem + 1.4vw, 2.1rem); }

a { color: var(--akzent); text-decoration-thickness: 1px; text-underline-offset: 0.15em; }
a:hover { color: var(--akzent-hell); }
:focus-visible { outline: 3px solid var(--akzent); outline-offset: 2px; }

img { max-width: 100%; height: auto; }

.zum-inhalt {
  position: absolute; left: -9999px;
}
.zum-inhalt:focus { left: 0.5rem; top: 0.5rem; position: fixed; background: var(--grund-erhoben);
                    padding: 0.5rem 1rem; z-index: 10; }

.textspalte { max-width: var(--spaltenbreite); margin: 0 auto; padding: 0 1.25rem 4rem; }

/* ---------- Kopf und Navigation ---------- */
.kopf { text-align: center; padding: 1.5rem 1rem 0.5rem; }
.wortmarke { font-size: clamp(2.5rem, 1.6rem + 4vw, 4.5rem); text-decoration: none; color: var(--schrift); }

/* Der Holzbalken mit Fachwerkhaus, Kreuz, Hammer, Truhe, Schwert und Wagenrad
   aus der alten Seite (header4.png). Er kachelt waagerecht, also traegt er jede
   Breite; auf dem Telefon wird er flacher. */
.zierbalken {
  height: clamp(28px, 6vw, 56px);
  background: url("/assets/bilder/zierbalken.webp") repeat-x center / auto 100%;
  border-block: 1px solid var(--linie);
}
:root[data-thema="dunkel"] .zierbalken { filter: brightness(0.72); }
@media (prefers-color-scheme: dark) {
  :root:not([data-thema="hell"]) .zierbalken { filter: brightness(0.72); }
}

.hauptnavigation { border-block: 1px solid var(--linie); background: var(--grund-erhoben); }
.hauptnavigation ul {
  list-style: none; margin: 0; padding: 0.5rem 1rem;
  display: flex; flex-wrap: wrap; gap: 0.35rem 1.5rem; justify-content: center;
}
.hauptnavigation a { text-decoration: none; font-family: var(--schrift-zier); font-size: 1.25rem; }
.hauptnavigation a[aria-current="page"] { color: var(--schrift); text-decoration: underline; }
.navigation-knopf { display: none; }

@media (max-width: 700px) {
  .navigation-knopf { display: block; cursor: pointer; padding: 0.75rem 1rem;
                      font-family: var(--schrift-zier); font-size: 1.25rem; }
  .hauptnavigation ul { flex-direction: column; align-items: flex-start; }
}
/* Ueber 700 px ist die Huelle immer offen, auch ohne Klick. */
@media (min-width: 701px) {
  .navigation-huelle > ul { display: flex !important; }
}

/* ---------- Schalter ---------- */
.schalter { display: flex; gap: 0.5rem; justify-content: center; padding: 0.5rem; }
.schalter button, .schalter a {
  background: none; border: 1px solid var(--linie); color: var(--schrift);
  border-radius: 3px; padding: 0.3rem 0.7rem; cursor: pointer;
  font: inherit; font-size: 0.9rem; text-decoration: none;
}

/* ---------- Bausteine ---------- */
.knopf {
  display: inline-block; background: var(--akzent); color: var(--grund);
  padding: 0.7rem 1.4rem; border-radius: 3px; text-decoration: none;
  font-family: var(--schrift-zier); font-size: 1.25rem;
}
.knopf:hover { background: var(--akzent-hell); color: var(--grund); }

.galerie { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
           max-width: 68rem; margin: 0 auto; padding: 0 1.25rem; list-style: none; }
.galerie figure { margin: 0; }
.galerie figcaption { font-size: 0.9rem; color: var(--schrift-leise); }

.news-anriss { border-top: 1px solid var(--linie); padding-top: 1rem; margin-top: 1.5rem; }
.news-anriss time { color: var(--schrift-leise); font-size: 0.9rem; }

.hinweis { background: var(--grund-erhoben); border-left: 3px solid var(--akzent);
           padding: 0.75rem 1rem; }

.fuss { border-top: 1px solid var(--linie); text-align: center; padding: 1.5rem 1rem;
        color: var(--schrift-leise); font-size: 0.9rem; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
```

- [ ] **Step 5: Schalter und Skript schreiben**

`_includes/schalter.html`:

```html
<div class="schalter">
  <button type="button" id="schalter-thema" aria-pressed="false">
    <span aria-hidden="true">◑</span> Dunkel
  </button>
  <button type="button" id="schalter-schrift" aria-pressed="false">
    Gut lesbar
  </button>
  <a href="/en/" hreflang="en">EN</a>
</div>
```

`assets/js/einstellungen.js`:

```js
// Thema und Schriftart umschalten. Die Seite funktioniert ohne diese Datei
// vollstaendig - dann gilt die Systemeinstellung und die Standardschrift.
(function () {
  "use strict";

  function verbinde(knopfId, schluessel, anWert) {
    var knopf = document.getElementById(knopfId);
    if (!knopf) { return; }
    var attribut = schluessel === "conspiratio-thema" ? "data-thema" : "data-schrift";

    function zeige() {
      knopf.setAttribute("aria-pressed",
        document.documentElement.getAttribute(attribut) === anWert ? "true" : "false");
    }

    knopf.addEventListener("click", function () {
      var an = document.documentElement.getAttribute(attribut) === anWert;
      if (an) {
        document.documentElement.removeAttribute(attribut);
        try { localStorage.removeItem(schluessel); } catch (e) { /* privates Fenster */ }
      } else {
        document.documentElement.setAttribute(attribut, anWert);
        try { localStorage.setItem(schluessel, anWert); } catch (e) { /* privates Fenster */ }
      }
      zeige();
    });

    zeige();
  }

  verbinde("schalter-thema", "conspiratio-thema", "dunkel");
  verbinde("schalter-schrift", "conspiratio-schrift", "lesbar");
})();
```

- [ ] **Step 6: Layout erweitern**

In `_layouts/basis.html` in den `<head>`, **vor** dem Stylesheet — dieses Skript muss laufen, bevor
der Browser zeichnet, sonst blitzt beim Laden das falsche Thema auf:

```html
  <script>
    (function () {
      try {
        var t = localStorage.getItem("conspiratio-thema");
        if (t) { document.documentElement.setAttribute("data-thema", t); }
        var s = localStorage.getItem("conspiratio-schrift");
        if (s) { document.documentElement.setAttribute("data-schrift", s); }
      } catch (e) { /* privates Fenster: Voreinstellung gilt */ }
    })();
  </script>
  <link rel="stylesheet" href="/assets/css/conspiratio.css">
  <link rel="preload" as="font" type="font/woff2" crossorigin
        href="/assets/schriften/eb-garamond-400.woff2">
```

Im `<body>`: `{%- include schalter.html -%}` direkt nach der Navigation, und vor `</body>`:

```html
  <script src="/assets/js/einstellungen.js" defer></script>
```

- [ ] **Step 7: Bauen, prüfen, mit Augen abnehmen**

```powershell
pwsh werkzeug/bauen.ps1
python werkzeug/pruefe_ausgabe.py
pwsh werkzeug/bauen.ps1 -Vorschau     # http://localhost:4000
```

Expected: „11 Pruefung(en) bestanden."
Im Browser: Beide Schalter wirken, die Wahl überlebt einen Seitenwechsel und einen Neuladen; beim
Neuladen im dunklen Thema blitzt **kein** helles Bild auf. In den Entwicklerwerkzeugen JavaScript
abschalten und neu laden: Die Seite bleibt vollständig lesbar, nur die Schalter tun nichts.

- [ ] **Step 8: Commit**

```bash
git add assets _includes/schalter.html _layouts/basis.html werkzeug/pruefe_ausgabe.py
git commit -F - <<'EOF'
Aussehen: zwei Themen aus dem Spielmaterial, umschaltbare Lesbarkeitsschrift

Hell ist das Pergament, dunkel das Kontor bei Kerzenlicht; der Akzent ist
in beiden das Bernstein der Kerzenflamme. Gebrochene Schrift nur noch als
Auszeichnung, nie im Fließtext - das war der eigentliche Grund, warum die
alte Seite schwer zu lesen war. Alle Schriften liegen als woff2 im Repo,
es geht kein Abruf mehr zu Google.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
```

---

## Aufgabe 4: Das News-System

**Files:**
- Create: `_layouts/news.html`, `_includes/news-anriss.html`, `news/index.html`,
  `werkzeug/neue-news.ps1`, `_posts/2026-01-01-conspiratio-1-4-8.md`
- Modify: `werkzeug/pruefe_ausgabe.py`

**Interfaces:**
- Consumes: Layouts aus Aufgabe 2, CSS-Klasse `.news-anriss` aus Aufgabe 3.
- Produces:
  - Frontmatter einer Meldung: `title` (String), `date` (aus dem Dateinamen), `excerpt` (String,
    optional), `bild` (absoluter Pfad, optional).
  - `_includes/news-anriss.html`, aufgerufen mit `{% include news-anriss.html meldung=eintrag %}`.
  - `/news/` listet alle Meldungen; `/feed.xml` ist gültiges RSS.

- [ ] **Step 1: Die Zusagen ins Prüfskript schreiben**

```python
import xml.etree.ElementTree as ET  # zu den Importen oben ergaenzen


@pruefung
def das_newsarchiv_listet_jede_meldung() -> None:
    archiv = lies("news/index.html")
    pruefe(archiv != "", "news/index.html fehlt")
    meldungen = [p for p in SITE.rglob("news/*/*/*/*/index.html")]
    pruefe(len(meldungen) > 0, "es wurde keine einzige Meldung gebaut")
    for meldung in meldungen:
        adresse = "/" + str(meldung.parent.relative_to(SITE)).replace("\\", "/") + "/"
        pruefe(adresse in archiv, f"Archiv listet {adresse} nicht")


@pruefung
def der_feed_ist_gueltiges_rss() -> None:
    roh = lies("feed.xml")
    pruefe(roh != "", "feed.xml fehlt")
    if not roh:
        return
    try:
        baum = ET.fromstring(roh)
    except ET.ParseError as fehler:
        pruefe(False, f"feed.xml ist kein gültiges XML: {fehler}")
        return
    eintraege = baum.findall(".//{http://www.w3.org/2005/Atom}entry")
    meldungen = list(SITE.rglob("news/*/*/*/*/index.html"))
    pruefe(len(eintraege) == len(meldungen),
           f"feed.xml hat {len(eintraege)} Einträge, gebaut wurden {len(meldungen)} Meldungen")


@pruefung
def jede_meldung_nennt_ihr_datum() -> None:
    for meldung in SITE.rglob("news/*/*/*/*/index.html"):
        text = meldung.read_text(encoding="utf-8")
        pfad = meldung.relative_to(SITE)
        pruefe("<time" in text, f"{pfad}: kein <time>-Element")
```

- [ ] **Step 2: Prüfskript laufen lassen — es muss fehlschlagen**

Run: `python werkzeug/pruefe_ausgabe.py`
Expected: Exit 1, „news/index.html fehlt", „es wurde keine einzige Meldung gebaut".

- [ ] **Step 3: Layout, Anriss und Archiv schreiben**

`_layouts/news.html`:

```html
---
layout: basis
---
<article class="textspalte">
  <h1>{{ page.title }}</h1>
  <p><time datetime="{{ page.date | date_to_xmlschema }}">{{ page.date | date: "%d.%m.%Y" }}</time></p>
  {%- if page.bild %}
  <img src="{{ page.bild }}" alt="{{ page.bild_alt | default: page.title }}"
       width="1000" height="563" loading="lazy">
  {%- endif %}
  {{ content }}
  <p><a href="/news/">← Alle Meldungen</a></p>
</article>
```

`_includes/news-anriss.html`:

```html
<article class="news-anriss">
  <h2><a href="{{ include.meldung.url }}">{{ include.meldung.title }}</a></h2>
  <p><time datetime="{{ include.meldung.date | date_to_xmlschema }}">
    {{ include.meldung.date | date: "%d.%m.%Y" }}
  </time></p>
  <p>{{ include.meldung.excerpt | strip_html | strip_newlines | truncate: 280 }}</p>
  <p><a href="{{ include.meldung.url }}">Weiterlesen</a></p>
</article>
```

`news/index.html`:

```html
---
layout: seite
title: News
permalink: /news/
---
<p>
  Alle Ankündigungen zum Spiel. Als <a href="/feed.xml">RSS-Feed</a> abonnierbar.
</p>

{%- assign jahre = site.posts | group_by_exp: "meldung", "meldung.date | date: '%Y'" -%}
{%- for jahr in jahre %}
<h2>{{ jahr.name }}</h2>
{%- for meldung in jahr.items %}
  {% include news-anriss.html meldung=meldung %}
{%- endfor %}
{%- endfor %}

<p class="hinweis">
  Ältere Meldungen von vor 2018 stehen weiterhin im
  <a href="https://forum.conspiratio.net/viewforum.php?f=32">Newsarchiv des Forums</a>.
</p>
```

- [ ] **Step 4: Die erste Meldung anlegen (Text aus der heutigen Startseite)**

`_posts/2026-01-01-conspiratio-1-4-8.md`:

```markdown
---
title: "Conspiratio 1.4.8 ist erschienen"
excerpt: "Das krankheitsbedingt verschobene Weihnachts-Update behebt die gemeldeten Abstürze und Hänger."
---

Liebe Spieler,

ein gesundes und frohes neues Jahr euch allen! Leider musste das traditionelle
Weihnachts-Update krankheitsbedingt etwas verschoben werden. Nun habe ich aber die Zeit
gefunden, das Update mit der wichtigen Korrektur zu den Abstürzen und Hängern zu
veröffentlichen:
[Conspiratio 1.4.8](https://github.com/Conspiratio/Conspiratio.WinForms/releases/download/1.4.8/Conspiratio.1.4.8.0.msi)

Hier findet ihr Details zu den Änderungen:
[Changelog](https://github.com/Conspiratio/Conspiratio.WinForms/blob/main/CHANGELOG.md#148---01012026)

Eine erste Version des neuen Godot-Clients verschiebt sich leider noch weiter.
Unterstützung in allen Bereichen wird weiterhin gesucht!

Feedback, Wünsche oder Anregungen gerne über [Discord](https://discord.gg/dxkC5DPgRY)
oder im [Forum](https://forum.conspiratio.net/viewtopic.php?p=204).

Viel Spaß und einen guten Start ins neue Jahr,

Euer Sir Toby und das Conspiratio Team
```

- [ ] **Step 5: Das Hilfsskript für neue Meldungen schreiben**

`werkzeug/neue-news.ps1`:

```powershell
<#
.SYNOPSIS
    Legt eine neue Newsmeldung mit fertigem Kopf an.
.EXAMPLE
    pwsh werkzeug/neue-news.ps1 "Der Godot-Client ist da"
#>
param([Parameter(Mandatory)][string]$Titel)

$ErrorActionPreference = "Stop"
$wurzel = Split-Path $PSScriptRoot -Parent
$datum  = Get-Date -Format "yyyy-MM-dd"

# Kuerzel aus dem Titel: Umlaute aufloesen, alles andere zu Bindestrichen.
$kuerzel = $Titel.ToLower().
    Replace("ä", "ae").Replace("ö", "oe").Replace("ü", "ue").Replace("ß", "ss")
$kuerzel = ($kuerzel -replace "[^a-z0-9]+", "-").Trim("-")

$datei = Join-Path $wurzel "_posts/$datum-$kuerzel.md"
if (Test-Path $datei) { throw "Gibt es schon: $datei" }

@"
---
title: "$Titel"
excerpt: ""
---

Werte Spieler,

"@ | Set-Content -Path $datei -Encoding utf8

Write-Host "Angelegt: $datei"
```

- [ ] **Step 6: Bauen und prüfen**

```powershell
pwsh werkzeug/bauen.ps1
python werkzeug/pruefe_ausgabe.py
```

Expected: „14 Pruefung(en) bestanden."; `_site/news/2026/01/01/conspiratio-1-4-8/index.html` und
`_site/feed.xml` mit genau einem Eintrag.

- [ ] **Step 7: Das Hilfsskript einmal wirklich benutzen**

```powershell
pwsh werkzeug/neue-news.ps1 "Probemeldung zum Wegwerfen"
pwsh werkzeug/bauen.ps1
python werkzeug/pruefe_ausgabe.py     # muss weiterhin gruen sein, jetzt mit 2 Meldungen
Remove-Item _posts/*probemeldung-zum-wegwerfen.md
```

- [ ] **Step 8: Commit**

```bash
git add _layouts/news.html _includes/news-anriss.html news werkzeug/neue-news.ps1 \
        _posts werkzeug/pruefe_ausgabe.py
git commit -F - <<'EOF'
News-System: eine Meldung ist eine Markdown-Datei

Archiv, Anrisse, Einzelseiten und der RSS-Feed entstehen daraus von
selbst. Eine Meldung lässt sich auch über die Weboberfläche von GitHub
anlegen, ohne lokales Repo.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
```

---

## Aufgabe 5: Den Newsbestand von 2018 bis heute übernehmen

**Files:**
- Create: 9 Dateien in `_posts/`
- Modify: `werkzeug/pruefe_ausgabe.py`
- Move: `Massenmail_2022.txt` → `massenmails/Massenmail_2022.txt`

**Interfaces:**
- Consumes: das Meldungsformat aus Aufgabe 4.
- Produces: ein lückenloses Archiv 2018–2026.

- [ ] **Step 1: Die Zusage ins Prüfskript schreiben**

```python
@pruefung
def das_archiv_reicht_bis_2018_zurueck() -> None:
    jahre = {p.parts[-5] for p in SITE.rglob("news/*/*/*/*/index.html")}
    for jahr in ("2018", "2019", "2020", "2021", "2022", "2023", "2024", "2026"):
        pruefe(jahr in jahre, f"im Archiv fehlt eine Meldung aus {jahr}")
    archiv = lies("news/index.html")
    pruefe("1.4.1" in archiv and "1.4.8" in archiv,
           "das Archiv nennt nicht alle Releases von 1.4.1 bis 1.4.8")
```

- [ ] **Step 2: Prüfskript laufen lassen — es muss fehlschlagen**

Run: `python werkzeug/pruefe_ausgabe.py`
Expected: Exit 1, „im Archiv fehlt eine Meldung aus 2018" (und sechs weitere Jahre).

- [ ] **Step 3: Die drei erhaltenen Originaltexte übernehmen**

Quellen im Repo: `Massenmail_2021.txt` (Wurzel — Dateiname trägt 2021, Inhalt gehört zu 1.4.4),
`Massenmail_2022.txt` (Wurzel, Release 1.4.5), `massenmails/Massenmail_2024.txt` (Release 1.4.7).

Für jede: den Text unverändert übernehmen, nackte URLs in Markdown-Links umschreiben, Forenlinks auf
`forum.conspiratio.net` umstellen. Die Dateinamen tragen das Releasedatum aus `download.html`:

| Datei | Quelle | `title` |
|---|---|---|
| `_posts/2021-12-24-conspiratio-1-4-4.md` | `Massenmail_2021.txt` | „Conspiratio 1.4.4 zu Weihnachten" |
| `_posts/2022-12-24-conspiratio-1-4-5.md` | `Massenmail_2022.txt` | „Conspiratio 1.4.5 zu Weihnachten" |
| `_posts/2024-12-24-conspiratio-1-4-7.md` | `massenmails/Massenmail_2024.txt` | „Conspiratio 1.4.7 zu Weihnachten" |

Beispiel `_posts/2022-12-24-conspiratio-1-4-5.md`:

```markdown
---
title: "Conspiratio 1.4.5 zu Weihnachten"
excerpt: "Viele Korrekturen und Verbesserungen aus eurem Feedback - und erste Prototypen in Unity und Godot."
---

Werte Spieler,

frohe Weihnachten! Es ist wieder einmal soweit, es gibt Geschenke, so auch dieses Jahr in
Form eines kleinen Conspiratio-Updates:
[Conspiratio 1.4.5](https://github.com/Conspiratio/Conspiratio.WinForms/releases/download/1.4.5/Conspiratio.1.4.5.0.msi)

Dank eures zahlreichen Feedbacks aus dem vergangenen Jahr gibt es viele Korrekturen,
Verbesserungen sowie ein paar Kleinigkeiten, hier der
[Changelog](https://github.com/Conspiratio/Conspiratio.WinForms/blob/main/CHANGELOG.md#145---24122022).

Ich habe geplant, um Erfahrungen für den neuen Client zu sammeln, jeweils einen Prototyp
sowohl in Unity als auch in Godot zu erstellen. Damit habe ich auch bereits angefangen, bin
aber noch nicht so weit gekommen wie erhofft. Mehr dazu in Kürze.

Feedback, Wünsche oder Anregungen gerne über [Discord](https://discord.gg/dxkC5DPgRY)
oder im [Forum](https://forum.conspiratio.net/).

Viel Spaß, angenehme Feiertage und einen guten Rutsch ins neue Jahr,

Euer Conspiratio Team
```

- [ ] **Step 4: Die fünf Releases ohne erhaltenen Text als Kurzmeldungen anlegen**

Daten aus `download.html` (Version, Datum, Dateigröße) und dem WinForms-Changelog. Je eine Datei
nach diesem Muster — hier `_posts/2018-12-24-conspiratio-1-4-1.md`:

```markdown
---
title: "Conspiratio 1.4.1 zu Weihnachten"
excerpt: "Das Weihnachtsupdate 2018."
---

Zum Weihnachtsfest 2018 ist Conspiratio 1.4.1 erschienen.

- [Conspiratio.1.4.1.0.msi](https://github.com/Conspiratio/Conspiratio.WinForms/releases/download/1.4.1/Conspiratio.1.4.1.0.msi) (217 MB)
- [Changelog](https://github.com/Conspiratio/Conspiratio.WinForms/blob/main/CHANGELOG.md#141---24122018)
```

Anzulegen, jeweils datiert auf den 24.12.:

| Datei | Version | Größe | Changelog-Anker |
|---|---|---|---|
| `_posts/2018-12-24-conspiratio-1-4-1.md` | 1.4.1 | 217 MB | `#141---24122018` |
| `_posts/2019-12-24-conspiratio-1-4-2.md` | 1.4.2 | 217 MB | `#142---24122019` |
| `_posts/2020-12-24-conspiratio-1-4-3.md` | 1.4.3 | 218 MB | `#143---24122020` |
| `_posts/2023-12-24-conspiratio-1-4-6.md` | 1.4.6 | 234 MB | `#146---24122023` |

**Achtung bei 1.4.1 und 1.4.2:** In `download.html` zeigen sie auf
`http://www.conspiratio.net/downloads/…`, nicht auf GitHub. Prüfen, ob unter
`https://github.com/Conspiratio/Conspiratio.WinForms/releases/tag/1.4.1` bzw. `…/1.4.2` ein Release
mit MSI liegt (`gh release view 1.4.1 --repo Conspiratio/Conspiratio.WinForms`). Wenn ja, den
GitHub-Link nehmen — der alte Pfad verschwindet mit dem FTP. Wenn nein, in der Meldung nur den
Changelog verlinken und in Aufgabe 7 auf der Downloadseite ebenso verfahren.

- [ ] **Step 5: Die Rohtexte an einen Ort räumen**

```bash
git mv Massenmail_2022.txt massenmails/
git mv Massenmail_2021.txt massenmails/ 2>/dev/null || true
ls massenmails/
```

(`Massenmail_2021.txt` liegt möglicherweise schon dort — dann schlägt der zweite Befehl folgenlos
fehl.)

- [ ] **Step 6: Bauen und prüfen**

```powershell
pwsh werkzeug/bauen.ps1
python werkzeug/pruefe_ausgabe.py
```

Expected: „15 Pruefung(en) bestanden."; `/news/` zeigt acht Jahresüberschriften.

- [ ] **Step 7: Commit**

```bash
git add _posts massenmails
git commit -F - <<'EOF'
Newsarchiv 2018 bis 2026 übernommen

Die drei erhaltenen Massenmail-Texte gehen im Original ein, die übrigen
fünf Releases als Kurzmeldungen aus Datum, Version und Changelog. Damit
zeigt das Archiv eine durchgehende Linie statt eines Forenlinks.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
```

---

## Aufgabe 6: Inhaltsseiten

**Files:**
- Create: `_layouts/start.html`, `mitmachen.md`, `kontakt.md`, `links.md`, `impressum.md`,
  `en/index.md`, `_data/team.yml`, `_data/links.yml`
- Modify: `index.html`, `spiel.md`, `werkzeug/pruefe_ausgabe.py`

**Interfaces:**
- Consumes: Layouts und CSS-Klassen aus Aufgaben 2–3, `news-anriss.html` aus Aufgabe 4.
- Produces: alle Seiten aus Kapitel 5 des Spec außer `/bilder/` (Aufgabe 8) und `/downloads/`
  (Aufgabe 7).

- [ ] **Step 1: Die Zusagen ins Prüfskript schreiben**

```python
ERWARTETE_SEITEN = [
    "index.html", "spiel/index.html", "downloads/index.html", "bilder/index.html",
    "news/index.html", "mitmachen/index.html", "kontakt/index.html", "links/index.html",
    "impressum/index.html", "en/index.html",
]


@pruefung
def alle_seiten_existieren() -> None:
    for pfad in ERWARTETE_SEITEN:
        pruefe((SITE / pfad).is_file(), f"{pfad} fehlt")


@pruefung
def die_startseite_zeigt_die_neuesten_meldungen() -> None:
    text = lies("index.html")
    pruefe(text.count('class="news-anriss"') == 3,
           "Startseite: es stehen nicht genau drei News-Anrisse darauf")
    pruefe("/downloads/" in text, "Startseite: kein Weg zu den Downloads")


@pruefung
def die_englische_seite_ist_englisch_ausgezeichnet() -> None:
    text = lies("en/index.html")
    pruefe('lang="en"' in text, "en/index.html: nicht als englisch ausgezeichnet")


@pruefung
def kein_verweis_mehr_auf_das_alte_forum() -> None:
    for seite in seiten():
        text = seite.read_text(encoding="utf-8")
        pfad = seite.relative_to(SITE)
        pruefe("conspiratio.net/forum" not in text,
               f"{pfad}: verweist noch auf conspiratio.net/forum statt forum.conspiratio.net")
```

- [ ] **Step 2: Prüfskript laufen lassen — es muss fehlschlagen**

Run: `python werkzeug/pruefe_ausgabe.py`
Expected: Exit 1, „mitmachen/index.html fehlt" und weitere.

- [ ] **Step 3: Startseite und Startlayout**

`_layouts/start.html`:

```html
---
layout: basis
---
<div class="aufmacher">
  <img src="/assets/bilder/kontor-aufmacher.webp"
       alt="Ein Schreibtisch bei Kerzenlicht: Landkarte, Federkiel, Münzen und ein versiegelter Brief"
       width="1600" height="900">
  <div class="textspalte">
    <p class="vorspann">{{ site.description }}</p>
    <p><a class="knopf" href="/downloads/">Herunterladen</a></p>
  </div>
</div>

<section class="textspalte">
  <h2>Ankündigungen</h2>
  {%- for meldung in site.posts limit: 3 %}
    {% include news-anriss.html meldung=meldung %}
  {%- endfor %}
  <p><a href="/news/">Alle Meldungen</a></p>
</section>
```

`index.html` wird zu:

```html
---
layout: start
title: Conspiratio
---
```

Ins CSS (`assets/css/conspiratio.css`) ergänzen:

```css
.aufmacher img { width: 100%; height: auto; display: block; max-height: 60vh; object-fit: cover; }
.vorspann { font-size: 1.2em; }
```

Das Aufmacherbild entsteht in Aufgabe 8 aus `hintIntro.png`; bis dahin genügt eine Kopie:

```powershell
New-Item -ItemType Directory -Force assets/bilder | Out-Null
Copy-Item hintIntro.png assets/bilder/kontor-aufmacher.webp   # wird in Aufgabe 8 richtig erzeugt
Copy-Item icon.png assets/bilder/icon.png
python -c "from PIL import Image; im=Image.open('header4.png').convert('RGB'); im.save('assets/bilder/zierbalken.webp','WEBP',quality=88)"
```

- [ ] **Step 4: `/spiel/` ausschreiben**

`spiel.md` — der Text aus `geschichte.html` übernommen, um den Godot-Stand ergänzt, und die bisher
unverlinkten Ämtergrafiken bekommen einen Platz:

```markdown
---
title: Über das Spiel
permalink: /spiel/
redirect_from:
  - /geschichte.html
---

Zu Beginn erbt Ihr eine heruntergekommene Produktionsstätte und das bescheidene Ersparte
eines Verwandten. Damit stellt Ihr Euer Geschick als Kaufmann unter Beweis: Ihr stellt Waren
her und verkauft sie, tätigt wohl durchdachte Investitionen oder setzt Euch als gewiefter
Exporteur durch.

## Handel

Vierzehn Städte, jede mit eigener Hauptproduktion, eigenem Wohlstand und eigener Bevölkerung.
Wer denselben Markt Jahr für Jahr beliefert, drückt dort den Preis — die Stadt wächst
allerdings mit dem Handel, und ein über Jahre entwickelter Markt trägt am Ende mehr als ein
frisch entdeckter.

## Ämter und Titel

Reichtum allein macht keine Dynastie. Ämter auf Stadt-, Landes- und Reichsebene bringen
Einkommen, Privilegien und Einfluss — und man muss sie sich erst durch Titel erschließen und
dann in einer Wahl gewinnen.

<figure>
  <img src="/assets/bilder/aemter-stadt-politisch.webp"
       alt="Die politischen Stadtämter von Ratsherr bis Bürgermeister"
       width="500" height="300" loading="lazy">
  <figcaption>Die politischen Ämter einer Stadt</figcaption>
</figure>

## Intrigen

Spione, Saboteure, Bestechung, Erpressung, ein Duell mit dem Degen — und die Aussicht, für all
das vor Gericht zu stehen.

## Die Dynastie

Während die Jahre ins Land ziehen, müsst Ihr für Nachwuchs sorgen, einen Erben bestimmen und
ein Testament hinterlassen, damit das angehäufte Vermögen am Ende nicht dem Erzbistum in den
Schoß fällt. Habt Ihr das nötige Zeug dazu, in dieser Welt von geringer Moral eine
fortbestehende Dynastie zu errichten?

Weitere Einzelheiten stehen im [Handbuch](https://conspiratio.github.io/Conspiratio.Wiki/)
und in der [Bildergalerie](/bilder/).
```

(Die Ämterbilder werden in Aufgabe 8 nach `assets/bilder/` aufbereitet; die Namen stehen hier
bereits fest.)

- [ ] **Step 5: Die übrigen Seiten**

`mitmachen.md`:

```markdown
---
title: Mitmachen
permalink: /mitmachen/
redirect_from:
  - /ueber.html
---

Conspiratio ist ein Freizeitprojekt und quelloffen (GPL-3.0). Unterstützung wird in allen
Bereichen gesucht — am dringendsten in diesen:

- **Spielen und berichten.** Was sich unrund anfühlt, was unklar ist, was fehlt. Das ist die
  Hilfe, die am meisten bringt und am wenigsten kostet.
- **Grafik.** Der neue Client übernimmt die Bilder des alten; vieles davon ist zwanzig Jahre alt.
- **Übersetzung.** Das Spiel gibt es nur auf Deutsch.
- **Programmierung.** C# und Godot 4.7; die Spielregeln liegen in einer eigenen Bibliothek mit
  Tests.

Am einfachsten geht das über [Discord](https://discord.gg/dxkC5DPgRY) oder direkt auf
[GitHub](https://github.com/Conspiratio/).

## Das Team

{% for person in site.data.team %}**{{ person.name }}**
{{ person.rolle }}

{% endfor %}
```

`_data/team.yml`:

```yaml
- name: Marco Berger (DerEinzehnte)
  rolle: Gründung, ursprüngliche Projektleitung, Programmierung, Konzeption
- name: Andreas Käfer (beetle)
  rolle: Gründung, Grafik und Design, Konzeption, Homepage
- name: Tobias (Sir Toby)
  rolle: Derzeitige Projektleitung, Programmierung, Konzeption, Homepage
```

`kontakt.md`:

```markdown
---
title: Kontakt
permalink: /kontakt/
redirect_from:
  - /kontakt.html
---

Wir freuen uns immer über Rückmeldungen, Hilfe oder Anregungen. Über diese Wege erreicht Ihr uns:

- [Discord](https://discord.gg/dxkC5DPgRY) — der schnellste Weg
- [mail@conspiratio.net](mailto:mail@conspiratio.net)
- [Forum](https://forum.conspiratio.net/)

## Sonstiges

Die Seite conspiratio.net ist in privatem Besitz und dient dazu, Wissen und Erfahrung über das
frei erhältliche Spiel Conspiratio auszutauschen. Es bestehen weder finanzielle Ziele noch
Interessen.
```

`links.md`:

```markdown
---
title: Links
permalink: /links/
redirect_from:
  - /links.html
---

Hier findet Ihr Verweise auf andere lesenswerte Seiten.

{% for eintrag in site.data.links %}**[{{ eintrag.titel }}]({{ eintrag.ziel }})**
{{ eintrag.beschreibung }}

{% endfor %}
```

`_data/links.yml` — die fünf Einträge aus `links.html` unverändert, mit den Schlüsseln `titel`,
`ziel`, `beschreibung`: Mittelland AD, Commercia, gilde2.de, Wikipedia „Die Fugger II", Die Gulde.

`impressum.md` (`permalink: /impressum/`) — **Gerüst mit Platzhaltern in Großbuchstaben**, das der
Eigentümer ausfüllt:

```markdown
---
title: Impressum
permalink: /impressum/
---

## Angaben gemäß § 5 DDG

NAME
ANSCHRIFT
E-Mail: mail@conspiratio.net

## Datenschutz

Diese Seite wird von GitHub Pages (GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco,
CA 94107, USA) ausgeliefert. Beim Abruf verarbeitet GitHub technisch notwendige Daten,
darunter die IP-Adresse; siehe die
[GitHub Privacy Statement](https://docs.github.com/site-policy/privacy-policies/github-privacy-statement).

Diese Seite setzt keine Cookies und bindet keine fremden Inhalte ein. Schriftarten werden von
diesem Server ausgeliefert, nicht von Dritten. Die Wahl von Farbschema und Schriftart wird im
lokalen Speicher des Browsers abgelegt und verlässt das Gerät nicht.
```

> **Hinweis an den Ausführenden:** Die Seite wird mit den Platzhaltern committet, aber Aufgabe 10
> (Veröffentlichung) darf erst laufen, wenn sie ausgefüllt ist.

`en/index.md`:

```markdown
---
title: "Conspiratio — a free trading and intrigue simulation"
permalink: /en/
lang: en
---

Conspiratio is a free, turn-based economic simulation set in the early modern period,
inspired by *Die Fugger II*. You inherit a run-down workshop, build a trading business across
fourteen cities, climb from burgher to duke through offices and titles, and scheme against
your rivals — all while making sure your dynasty outlives you.

The game is in **German only**. There is currently no English translation, and none is
planned; helping to make one is one of the ways to contribute.

- [Download](/downloads/)
- [Source code on GitHub](https://github.com/Conspiratio/) (GPL-3.0)
- [Discord](https://discord.gg/dxkC5DPgRY)
```

`_includes/schalter.html` ergänzen: Auf `/en/` zeigt der Sprachlink zurück auf `/`.

- [ ] **Step 6: Bauen und prüfen**

```powershell
pwsh werkzeug/bauen.ps1
python werkzeug/pruefe_ausgabe.py
```

Expected: Es fehlen noch `downloads/index.html` (Aufgabe 7) und `bilder/index.html` (Aufgabe 8).
**Um die Aufgabe grün abzuschließen**, beide als einzeilige Platzhalter mit korrektem Frontmatter
anlegen; Aufgabe 7 und 8 füllen sie. Danach: „19 Pruefung(en) bestanden."

- [ ] **Step 7: Commit**

```bash
git add index.html spiel.md mitmachen.md kontakt.md links.md impressum.md en \
        downloads.md bilder.md _layouts/start.html _data assets \
        _includes/schalter.html werkzeug/pruefe_ausgabe.py
git commit -F - <<'EOF'
Inhaltsseiten: Start, Spiel, Mitmachen, Kontakt, Links, Impressum, EN

Die Spielbeschreibung ist nach Handel, Ämtern, Intrigen und Dynastie
gegliedert statt ein Textblock zu sein, und die Ämtergrafiken sind zum
ersten Mal überhaupt verlinkt. Neu sind eine englische Seite und ein
Impressum; letzteres noch mit Platzhaltern.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
```

---

## Aufgabe 7: Die Downloadseite

**Files:**
- Create: `_data/downloads.yml`
- Modify: `downloads.md`, `werkzeug/pruefe_ausgabe.py`

**Interfaces:**
- Consumes: Layout `seite`, CSS-Klassen `.knopf` und `.hinweis`.
- Produces: `_data/downloads.yml` mit den Schlüsseln `version`, `datum` (ISO), `groesse`,
  `msi` (URL oder leer), `changelog` (URL).

- [ ] **Step 1: Die Zusagen ins Prüfskript schreiben**

```python
@pruefung
def die_downloadseite_stellt_godot_voran() -> None:
    text = lies("downloads/index.html")
    pruefe("Godot" in text, "Downloadseite: der Godot-Client kommt nicht vor")
    pruefe(text.index("Godot") < text.index("1.4.8"),
           "Downloadseite: der Godot-Client steht nicht vor dem WinForms-Release")


@pruefung
def die_downloadseite_listet_jedes_release() -> None:
    text = lies("downloads/index.html")
    for version in ("1.4.8", "1.4.7", "1.4.6", "1.4.5", "1.4.4", "1.4.3", "1.4.2", "1.4.1"):
        pruefe(version in text, f"Downloadseite: Version {version} fehlt")


@pruefung
def die_systemvoraussetzungen_sind_aktuell() -> None:
    text = lies("downloads/index.html")
    pruefe(".NET Framework 4.6.2" in text, "Downloadseite: WinForms-Voraussetzung fehlt")
    pruefe("Windows 11" in text,
           "Downloadseite: nennt Windows 11 nicht - die alte Seite hörte bei Windows 10 auf")
```

- [ ] **Step 2: Prüfskript laufen lassen — es muss fehlschlagen**

Run: `python werkzeug/pruefe_ausgabe.py`
Expected: Exit 1, „Downloadseite: der Godot-Client kommt nicht vor" und weitere.

- [ ] **Step 3: Die Daten erfassen**

`_data/downloads.yml` — Werte aus `download.html`:

```yaml
- version: "1.4.8"
  datum: 2026-01-01
  groesse: "236 MB"
  msi: https://github.com/Conspiratio/Conspiratio.WinForms/releases/download/1.4.8/Conspiratio.1.4.8.0.msi
  changelog: https://github.com/Conspiratio/Conspiratio.WinForms/blob/main/CHANGELOG.md#148---01012026
- version: "1.4.7"
  datum: 2024-12-24
  groesse: "234 MB"
  msi: https://github.com/Conspiratio/Conspiratio.WinForms/releases/download/1.4.7/Conspiratio.1.4.7.0.msi
  changelog: https://github.com/Conspiratio/Conspiratio.WinForms/blob/main/CHANGELOG.md#147---24122024
# … 1.4.6 (2023-12-24, 234 MB), 1.4.5 (2022-12-24, 231 MB), 1.4.4 (2021-12-24, 218 MB),
#   1.4.3 (2020-12-24, 218 MB), 1.4.2 (2019-12-24, 217 MB), 1.4.1 (2018-12-24, 217 MB)
```

Für 1.4.1 und 1.4.2 gilt derselbe Vorbehalt wie in Aufgabe 5, Schritt 4: Falls kein GitHub-Release
existiert, `msi:` leer lassen — das Template gibt dann nur den Changelog aus, statt auf den
verschwindenden FTP-Pfad zu zeigen.

```bash
gh release view 1.4.1 --repo Conspiratio/Conspiratio.WinForms --json assets 2>&1 | head -5
gh release view 1.4.2 --repo Conspiratio/Conspiratio.WinForms --json assets 2>&1 | head -5
```

- [ ] **Step 4: Die Seite schreiben**

`downloads.md`:

```markdown
---
title: Downloads
permalink: /downloads/
redirect_from:
  - /download.html
---

## Der neue Client (Godot)

Conspiratio wird gerade von Grund auf neu gebaut: gleicher Spielinhalt, neue Oberfläche,
Godot 4.7 statt WinForms. Der neue Client ist inhaltlich vollständig und wird derzeit
geprüft — eine erste Fassung erscheint demnächst.

<p class="hinweis">
Bis dahin ist die WinForms-Fassung unten die spielbare Version.
</p>

- [Entwicklungsstand und Quellcode](https://github.com/Conspiratio/Conspiratio.Godot)
- [Was neu sein wird](https://github.com/Conspiratio/Conspiratio.Godot/blob/main/CHANGELOG.md)
- [Handbuch zum neuen Client](https://conspiratio.github.io/Conspiratio.Wiki/)

**Systemvoraussetzungen:** Windows 10 oder Windows 11, .NET 8.

## Der bisherige Client (WinForms)

{%- assign aktuell = site.data.downloads | first %}

<p>
  <a class="knopf" href="{{ aktuell.msi }}">Version {{ aktuell.version }} herunterladen</a>
</p>
<p>
  {{ aktuell.datum | date: "%d.%m.%Y" }} · {{ aktuell.groesse }} ·
  <a href="{{ aktuell.changelog }}">Changelog</a>
</p>

**Systemvoraussetzungen:** Windows 7 bis Windows 11,
[.NET Framework 4.6.2](https://www.microsoft.com/de-de/download/details.aspx?id=53344),
Administratorrechte für die Installation.

### Installation

1. Auf den Downloadlink klicken.
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
```

- [ ] **Step 5: Bauen und prüfen**

```powershell
pwsh werkzeug/bauen.ps1
python werkzeug/pruefe_ausgabe.py
```

Expected: „22 Pruefung(en) bestanden."

- [ ] **Step 6: Commit**

```bash
git add downloads.md _data/downloads.yml werkzeug/pruefe_ausgabe.py
git commit -F - <<'EOF'
Downloadseite: Godot-Client voran, WinForms 1.4.8 als spielbare Fassung

Die Releaseliste kommt aus _data/downloads.yml; ein neues Release ist
künftig ein Eintrag dort und keine Änderung am Seitentext. Die
Systemvoraussetzungen sind je Client richtiggestellt - die alte Seite
hörte bei Windows 10 auf und nannte .NET 8 gar nicht.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
```

---

## Aufgabe 8: Bilder aufbereiten und Galerie

**Files:**
- Create: `werkzeug/bilder_aufbereiten.py`, `_data/bilder.yml`, `assets/bilder/**`
- Modify: `bilder.md`, `werkzeug/pruefe_ausgabe.py`

**Interfaces:**
- Consumes: CSS-Klasse `.galerie` aus Aufgabe 3.
- Produces:
  - `python werkzeug/bilder_aufbereiten.py` → schreibt `assets/bilder/*.webp` und erzeugt
    `_data/bilder.yml` mit den Schlüsseln `datei`, `alt`, `client` (`godot` | `winforms`),
    `breite`, `hoehe`.

- [ ] **Step 1: Die Zusagen ins Prüfskript schreiben**

```python
import re  # zu den Importen oben ergaenzen


@pruefung
def jedes_bild_hat_alt_und_masse() -> None:
    muster = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
    for seite in seiten():
        text = seite.read_text(encoding="utf-8")
        pfad = seite.relative_to(SITE)
        for treffer in muster.findall(text):
            pruefe("alt=" in treffer, f"{pfad}: <img> ohne alt: {treffer[:90]}")
            pruefe("width=" in treffer and "height=" in treffer,
                   f"{pfad}: <img> ohne width/height: {treffer[:90]}")


@pruefung
def die_galerie_trennt_die_beiden_clients() -> None:
    text = lies("bilder/index.html")
    pruefe("Godot" in text and "WinForms" in text,
           "Bilderseite: die beiden Clients sind nicht getrennt überschrieben")
    pruefe(text.index("Godot") < text.index("WinForms"),
           "Bilderseite: der Godot-Client steht nicht zuerst")


@pruefung
def alle_oertlichen_verweise_zeigen_auf_vorhandene_dateien() -> None:
    # Interner Linkpruefer: ersetzt lychee fuer alles, was im Repo liegt.
    muster = re.compile(r'(?:href|src)="(/[^"#?]*)"')
    for seite in seiten():
        text = seite.read_text(encoding="utf-8")
        pfad = seite.relative_to(SITE)
        for ziel in set(muster.findall(text)):
            kandidat = SITE / ziel.lstrip("/")
            ok = kandidat.is_file() or (kandidat / "index.html").is_file()
            pruefe(ok, f"{pfad}: toter interner Verweis auf {ziel}")
```

- [ ] **Step 2: Prüfskript laufen lassen — es muss fehlschlagen**

Run: `python werkzeug/pruefe_ausgabe.py`
Expected: Exit 1, „Bilderseite: die beiden Clients sind nicht getrennt überschrieben" und tote
Verweise auf die in Aufgabe 6 vorweggenommenen Bildnamen.

- [ ] **Step 3: Godot-Aufnahmen ernten**

Im **anderen** Repo, mit Renderer (nicht headless — der Dummy-Treiber zeichnet nicht):

```powershell
cd C:\Projekte\Godot\Conspiratio.Godot
$godot = "C:\Program Files (x86)\Godot_v4.7.1-stable_mono_win64\Godot_v4.7.1-stable_mono_win64.exe"
& $godot --path . "res://scenes/E2eTest.tscn" -- --jahre=12 --spieler=2 --bilder="$PWD\ernte"
```

Aus `ernte/` sechs Aufnahmen wählen und nach
`D:\Projekte\C# Projekte\conspiratio.github.io\rohbilder\godot\` kopieren, benannt nach Motiv:
`kontor.png`, `stadt.png`, `schreibstube.png`, `weltkarte.png`, `aemter.png`, `hinterzimmer.png`.

Wenn der Lauf scheitert oder keine brauchbaren Bilder liefert: die Aufgabe **nicht blockieren**.
Dann nur die WinForms-Galerie bauen und in `bilder.md` unter „Godot" den Satz setzen, dass Bilder
folgen, sobald die erste Fassung erschienen ist. Der Rest der Aufgabe bleibt gültig.

- [ ] **Step 4: Das Aufbereitungsskript schreiben**

`werkzeug/bilder_aufbereiten.py`:

```python
#!/usr/bin/env python3
"""Bereitet Rohbilder fuer die Galerie auf: skalieren, WebP, Masse nach _data/bilder.yml.

Quellen:
  rohbilder/godot/*.png      Aufnahmen aus dem E2E-Treiber
  screenshots/*.jpg          die alten WinForms-Aufnahmen (ohne die _thumb-Dateien)
Aufruf: python werkzeug/bilder_aufbereiten.py
"""
from __future__ import annotations

import pathlib

from PIL import Image

WURZEL = pathlib.Path(__file__).resolve().parent.parent
ZIEL = WURZEL / "assets" / "bilder"
BREITE = 1000

# Motiv -> Alternativtext. Was hier nicht steht, wird nicht aufbereitet:
# ein Bild ohne Alternativtext geht nicht auf die Seite.
GODOT = {
    "kontor": "Das Kontor: von hier aus werden alle Bereiche des Zuges angesteuert",
    "stadt": "Die Stadtansicht mit Werkstätten, Lagerbeständen und Preisen",
    "schreibstube": "Die Schreibstube mit Ämtern, Gesetzen und Krediten",
    "weltkarte": "Die Weltkarte mit den vierzehn Städten",
    "aemter": "Die Ämterübersicht mit Amtsinhabern und Bewerbungen",
    "hinterzimmer": "Das Hinterzimmer: Beziehungen, Spionage und Erpressung",
}
WINFORMS = {
    "Conspiratio_Kontor": "Das Kontor im bisherigen Client",
    "Conspiratio_Schreibstube_Gesetze": "Die Gesetzestafel in der Schreibstube",
    "Conspiratio_Amtsuebersicht": "Die Ämterübersicht",
    "Conspiratio_Beziehungen_Kontrahenten": "Beziehungen zu den Kontrahenten",
    "Conspiratio_Kirche": "Die Kirche",
    "Conspiratio_Produktion": "Die Produktion einer Werkstätte",
    "Conspiratio_Stadtinfos": "Die Stadtinformationen",
    "Conspiratio_Zollburg_verwalten": "Eine Zollburg verwalten",
}


def bereite_auf(quelle: pathlib.Path, zielname: str) -> tuple[int, int]:
    """Skaliert auf BREITE, schreibt WebP, gibt die Zielmasse zurueck."""
    with Image.open(quelle) as bild:
        bild = bild.convert("RGB")
        hoehe = round(bild.height * BREITE / bild.width)
        bild = bild.resize((BREITE, hoehe), Image.LANCZOS)
        ZIEL.mkdir(parents=True, exist_ok=True)
        bild.save(ZIEL / f"{zielname}.webp", "WEBP", quality=82, method=6)
    return BREITE, hoehe


def main() -> int:
    eintraege: list[str] = []
    fehlend: list[str] = []

    for client, verzeichnis, endung, motive in (
        ("godot", WURZEL / "rohbilder" / "godot", ".png", GODOT),
        ("winforms", WURZEL / "screenshots", ".jpg", WINFORMS),
    ):
        for motiv, alt in motive.items():
            quelle = verzeichnis / f"{motiv}{endung}"
            if not quelle.is_file():
                fehlend.append(str(quelle.relative_to(WURZEL)))
                continue
            zielname = f"{client}-{motiv.lower().replace('conspiratio_', '')}"
            breite, hoehe = bereite_auf(quelle, zielname)
            eintraege.append(
                f"- datei: {zielname}.webp\n"
                f"  alt: \"{alt}\"\n"
                f"  client: {client}\n"
                f"  breite: {breite}\n"
                f"  hoehe: {hoehe}\n"
            )

    # Das Aufmacherbild der Startseite aus dem Introbild.
    intro = WURZEL / "hintIntro.png"
    if intro.is_file():
        bereite_auf(intro, "kontor-aufmacher")

    ziel_yaml = WURZEL / "_data" / "bilder.yml"
    ziel_yaml.parent.mkdir(parents=True, exist_ok=True)
    ziel_yaml.write_text("".join(eintraege), encoding="utf-8")
    print(f"{len(eintraege)} Bild(er) aufbereitet -> {ziel_yaml.relative_to(WURZEL)}")

    if fehlend:
        print("\nNicht gefunden (werden übersprungen):")
        for pfad in fehlend:
            print(f"  - {pfad}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Zusätzlich die drei Ämtergrafiken aus `bilder/` von Hand einmalig umwandeln (sie gehören zu
`/spiel/`, nicht in die Galerie):

```powershell
python -c "from PIL import Image; im=Image.open('bilder/StadtaemterPolit.png').convert('RGB'); im.save('assets/bilder/aemter-stadt-politisch.webp','WEBP',quality=85)"
```

- [ ] **Step 5: Die Galerieseite schreiben**

`bilder.md`:

```markdown
---
title: Bilder
permalink: /bilder/
redirect_from:
  - /bilder.html
---

Einige Eindrücke aus dem Spiel.

## Der neue Client (Godot)

<ul class="galerie">
{%- for bild in site.data.bilder %}{% if bild.client == "godot" %}
  <li><figure>
    <a href="/assets/bilder/{{ bild.datei }}">
      <img src="/assets/bilder/{{ bild.datei }}" alt="{{ bild.alt }}"
           width="{{ bild.breite }}" height="{{ bild.hoehe }}" loading="lazy">
    </a>
    <figcaption>{{ bild.alt }}</figcaption>
  </figure></li>
{%- endif %}{% endfor %}
</ul>

## Der bisherige Client (WinForms)

<ul class="galerie">
{%- for bild in site.data.bilder %}{% if bild.client == "winforms" %}
  <li><figure>
    <a href="/assets/bilder/{{ bild.datei }}">
      <img src="/assets/bilder/{{ bild.datei }}" alt="{{ bild.alt }}"
           width="{{ bild.breite }}" height="{{ bild.hoehe }}" loading="lazy">
    </a>
    <figcaption>{{ bild.alt }}</figcaption>
  </figure></li>
{%- endif %}{% endfor %}
</ul>
```

- [ ] **Step 6: Aufbereiten, bauen, prüfen**

```powershell
python werkzeug/bilder_aufbereiten.py
pwsh werkzeug/bauen.ps1
python werkzeug/pruefe_ausgabe.py
```

Expected: „25 Pruefung(en) bestanden." Der interne Linkprüfer schlägt jetzt bei jedem Tippfehler in
einem Bildnamen an — das ist sein eigentlicher Zweck.

- [ ] **Step 7: Commit**

```bash
git add werkzeug/bilder_aufbereiten.py _data/bilder.yml assets/bilder bilder.md \
        werkzeug/pruefe_ausgabe.py
git commit -F - <<'EOF'
Galerie mit beiden Clients, Bilder als WebP mit festen Maßen

Die Aufbereitung ist ein Skript, kein Handbetrieb: skalieren auf 1000 px,
WebP, Maße nach _data/bilder.yml. Ein Bild ohne Alternativtext wird
absichtlich nicht aufbereitet. Das Prüfskript hat jetzt einen internen
Linkprüfer und fängt tote Verweise ohne Netz.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
```

---

## Aufgabe 9: Weiterleitungen und Aufräumen

Erst hier verschwindet die alte Seite — bis dahin lag sie unangetastet daneben.

**Files:**
- Delete: `cons.css`, `OLDENGL.TTF`, `Jurist_aufsuchen.png`, `index.html` (alt), `geschichte.html`,
  `download.html`, `bilder.html`, `ueber.html`, `links.html`, `kontakt.html`,
  `header4.png`, `bar1.png`, `footer.png`, `symb.png`, `symb1.png`, `pergament3.png`,
  `hintIntro.png`, `icon.png`, `screenshots/*_thumb.jpg`, `bilder/*.png`
- Modify: `werkzeug/pruefe_ausgabe.py`

**Interfaces:**
- Consumes: `redirect_from` aus den Aufgaben 6–8.
- Produces: keine neuen Schnittstellen.

- [ ] **Step 1: Die Zusagen ins Prüfskript schreiben**

```python
WEITERLEITUNGEN = {
    "geschichte.html": "/spiel/",
    "download.html": "/downloads/",
    "bilder.html": "/bilder/",
    "ueber.html": "/mitmachen/",
    "links.html": "/links/",
    "kontakt.html": "/kontakt/",
}


@pruefung
def die_alten_adressen_leiten_weiter() -> None:
    for alt, neu in WEITERLEITUNGEN.items():
        text = lies(alt)
        pruefe(text != "", f"{alt}: Weiterleitung fehlt")
        pruefe(neu in text, f"{alt}: leitet nicht auf {neu}")


@pruefung
def die_altlasten_sind_verschwunden() -> None:
    for name in ("cons.css", "OLDENGL.TTF", "Jurist_aufsuchen.png"):
        pruefe(not (SITE / name).exists(), f"{name} wird noch ausgeliefert")
    pruefe(not list(SITE.rglob("*_thumb.jpg")), "es werden noch _thumb-Dateien ausgeliefert")
```

- [ ] **Step 2: Prüfskript laufen lassen — es muss fehlschlagen**

Run: `python werkzeug/pruefe_ausgabe.py`
Expected: Exit 1, „cons.css wird noch ausgeliefert", „OLDENGL.TTF wird noch ausgeliefert".

> **Falls stattdessen „geschichte.html: Weiterleitung fehlt" erscheint:** Die alte
> `geschichte.html` liegt noch im Repo und Jekyll kopiert sie, statt die Weiterleitung zu
> erzeugen. Genau das behebt Schritt 3.

- [ ] **Step 3: Die Altdateien entfernen**

```bash
git rm cons.css OLDENGL.TTF Jurist_aufsuchen.png \
       geschichte.html download.html bilder.html ueber.html links.html kontakt.html \
       header4.png bar1.png footer.png symb.png symb1.png pergament3.png hintIntro.png icon.png
git rm screenshots/*_thumb.jpg
git rm -r bilder
git status
```

Vor dem Löschen sicherstellen, dass `hintIntro.png`, `icon.png` und `header4.png` in Aufgabe 6/8
nach `assets/bilder/` gewandert sind (`kontor-aufmacher.webp`, `icon.png`, `zierbalken.webp`) —
der interne Linkprüfer schlägt sonst im nächsten Schritt an, und das ist die Absicht.
`header4.png` wird als Quelle gelöscht, **der Balken selbst bleibt** (Spec, Kapitel 7: „Der
Holzbalken mit den Symbolen bleibt als schmales Band unter dem Seitentitel").

Die alte `index.html` wird **nicht** gelöscht, sondern ist seit Aufgabe 6 die neue Startseite.

- [ ] **Step 4: Bauen und prüfen**

```powershell
pwsh werkzeug/bauen.ps1
python werkzeug/pruefe_ausgabe.py
```

Expected: „27 Pruefung(en) bestanden." `_site/geschichte.html` existiert und enthält eine
Weiterleitung nach `/spiel/`.

- [ ] **Step 5: Von Hand nachsehen**

```powershell
pwsh werkzeug/bauen.ps1 -Vorschau
```

`http://localhost:4000/geschichte.html` muss auf `/spiel/` landen — dasselbe für die übrigen fünf.

- [ ] **Step 6: Commit**

```bash
git add -u
git add werkzeug/pruefe_ausgabe.py
git commit -F - <<'EOF'
Alte Seite entfernt, ihre Adressen leiten weiter

Die sechs alten HTML-Adressen bleiben gültig, damit nichts bricht, was
je verlinkt wurde - darunter der Wikipedia-Artikel zu Die Fugger II.
OLDENGL.TTF ist weg: eine Microsoft-Systemschrift, die nicht zur
Weitergabe lizenziert ist und trotzdem ausgeliefert wurde.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
```

---

## Aufgabe 10: Veröffentlichung

**Files:**
- Create: `CNAME`, `docs/umstellung-dns.md`
- Modify: `.github/workflows/pages.yml`, `README.md`

**Interfaces:**
- Consumes: alles Vorherige.
- Produces: die laufende Seite unter `conspiratio.github.io`, bereit für die Domainumstellung.

- [ ] **Step 1: Externe Links in CI prüfen lassen**

In `.github/workflows/pages.yml`, im Job `bauen` nach „Ausgabe prüfen":

```yaml
      - name: Verweise prüfen
        uses: lycheeverse/lychee-action@v2
        with:
          args: >-
            --no-progress --accept 200,206,429
            --exclude-path _site/assets
            '_site/**/*.html'
          fail: false
```

`fail: false` ist Absicht: Fremde Seiten verschwinden, ohne dass die eigene Veröffentlichung daran
scheitern soll. Interne Verweise prüft `pruefe_ausgabe.py`, und das **schlägt** fehl.

- [ ] **Step 2: Die DNS-Umstellung dokumentieren**

`docs/umstellung-dns.md` — die Schritte aus Kapitel 3 des Spec, in dieser Reihenfolge, mit den
A-Records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`, den AAAA-Records
`2606:50c0:8000::153` bis `2606:50c0:8003::153` und dem `www`-CNAME auf `conspiratio.github.io`.
Ausdrücklich hineinschreiben: **„Enforce HTTPS" erst anhaken, wenn GitHub das Zertifikat ausgestellt
hat** (bis zu 24 Stunden) — sonst ist die Seite in der Zwischenzeit nicht erreichbar.

- [ ] **Step 3: Zusammenführen und in CI abnehmen**

```bash
git push -u origin feature/pages-neubau
gh pr create --title "Neue Seite auf GitHub Pages" --body-file docs/superpowers/specs/2026-09-12-webseite-modernisierung-design.md
```

Warten, bis der Workflow grün ist (Build, Prüfskript, lychee). Danach mergen.

- [ ] **Step 4: Unter der github.io-Adresse abnehmen**

In `Settings → Pages` die Quelle auf **„GitHub Actions"** stellen (nur der Eigentümer kann das).
Dann `https://conspiratio.github.io/` in vier Kombinationen durchsehen — hell/dunkel ×
Standardschrift/gut lesbar —, dazu in 375 px Breite und mit abgeschaltetem JavaScript. Jede der
zehn Seiten.

- [ ] **Step 5: Das Impressum ausfüllen**

Die Platzhalter aus Aufgabe 6 durch die echten Angaben ersetzen. **Vor** der Domainumstellung, nicht
danach.

- [ ] **Step 6: `CNAME` anlegen und die Domain umstellen**

Erst jetzt, und in dieser Reihenfolge (siehe `docs/umstellung-dns.md`): Forum auf
`forum.conspiratio.net`, dann Apex auf GitHub, dann `CNAME` mit dem Inhalt `conspiratio.net`
einchecken, dann „Enforce HTTPS".

- [ ] **Step 7: Commit**

```bash
git add CNAME docs/umstellung-dns.md .github/workflows/pages.yml README.md
git commit -F - <<'EOF'
Veröffentlichung: Linkprüfung in CI, DNS-Umstellung dokumentiert

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
```

---

## Abgleich mit dem Spec

| Spec-Kapitel | Aufgabe |
|---|---|
| 3 Domain, Forum, Umschaltung | 10 |
| 4 Technik (Struktur, Build, Vorschau) | 1 |
| 5 Seiten und Navigation | 2, 6, 7, 8 |
| 6 News-System | 4, 5 |
| 7 Aussehen (Themen, Schrift, Layout, Zierrat, Skript, Barrierefreiheit) | 3 |
| 8 Bilder und Altlasten | 8, 9 |
| 9 Umsetzung und Prüfung | 1 (Prüfskript), 9, 10 |
| 11 Erfolgskriterien 1–2 | 10 |
| 11 Erfolgskriterien 3–4 | 4, 5 |
| 11 Erfolgskriterien 5–7 | 3, 10 (Sichtprüfung) |
| 11 Erfolgskriterium 8 | 7 |
| 11 Erfolgskriterium 9 | 8 (intern), 10 (extern) |
| 11 Erfolgskriterium 10 | 9 |

**Abweichung vom Spec, bewusst:** Kapitel 4 des Spec nennt den RubyInstaller für die lokale
Vorschau. Auf dieser Maschine ist kein Ruby, aber Docker 29.6 vorhanden; Aufgabe 1 baut deshalb im
Container. Das ist der bessere Weg, weil derselbe `Gemfile.lock` lokal und in CI gilt — der Spec
braucht dafür keine Änderung, die Begründung steht hier.
