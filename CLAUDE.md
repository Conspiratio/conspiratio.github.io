# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Überblick

Die Projektseite von **Conspiratio** (<https://conspiratio.net>), einem freien Wirtschaftssimulations-
spiel der frühen Neuzeit. Eine statische Jekyll-Seite, die über GitHub Actions nach GitHub Pages
veröffentlicht wird. Kein CMS, kein CSS- oder JS-Framework: genau **eine** CSS-Datei
(`assets/css/conspiratio.css`) und **eine** JS-Datei (`assets/js/einstellungen.js`, nur die beiden
Umschalter). Die ganze Seite wiegt rund 1,3 MB.

Alle sichtbaren Texte, eigenen Dateinamen, Kommentare und Commit-Nachrichten sind **deutsch**.
Ausgenommen sind Schnittstellenbegriffe des Frameworks (`_posts`, `_data`, `_layouts`, `title`,
`date`, `excerpt`, `permalink`, `redirect_from`) — Jekyll liest sie so und nur so.

Schwesterrepos: `Conspiratio.Godot` (der neue Client), `Conspiratio.WinForms` (der bisherige, dort
liegen die Releases), `Conspiratio.Wiki` (Spielerdokumentation).

## Bauen und prüfen

**Kein lokales Ruby nötig** — der Build läuft im Docker-Container mit derselben `Gemfile.lock` wie
der CI-Runner. Docker Desktop muss laufen.

```powershell
powershell -File werkzeug/bauen.ps1              # einmalig nach _site/
powershell -File werkzeug/bauen.ps1 -Vorschau    # Server auf http://localhost:4000
python werkzeug/pruefe_ausgabe.py                # prüft die gebaute Seite
```

Der Port wird nur bei `-Vorschau` veröffentlicht, damit ein Build neben einer laufenden Vorschau
nicht an „port is already allocated" scheitert.

### Das Prüfskript ist die Testsuite

`werkzeug/pruefe_ausgabe.py` tritt an die Stelle der Tests, die es für eine statische Seite sonst
nicht gäbe. Es prüft **die gebaute Ausgabe in `_site/`**, nicht die Quellen, und läuft auch in CI —
ein Fehler verhindert die Veröffentlichung. Derzeit 33 Zusagen, darunter: Sprache je Seite,
Navigation und Fußzeile, WCAG-Kontrast beider Themen (aus dem CSS gelesen, nicht dupliziert), tote
interne Verweise, Alternativtexte und Bildmaße, die Weiterleitungen der alten Adressen, die
Vollständigkeit des Newsarchivs, Titellänge, Platzhalter und englische Monatsnamen.

Eine neue Prüfung ist eine Funktion mit `@pruefung`-Dekorator; sie ruft `pruefe(bedingung, meldung)`
und nutzt die Helfer `lies()`, `seiten()`, `meldungen()`, `ist_weiterleitung()`.

**Zwei Regeln, die sich bewährt haben:**

- **Erst die Zusage schreiben, sie fehlschlagen sehen, dann erfüllen.** So ist geklärt, dass die
  Prüfung überhaupt greifen kann.
- **Eine neue Prüfung einmal absichtlich brechen.** Mehrere Prüfungen sind so gegengeprüft worden
  (Kontrast, interner Linkprüfer, `aria-label` der Schalter) — eine, die nicht fehlschlagen kann,
  ist wertlos.
- Fehlermeldungen bleiben **ASCII**: Die Windows-Konsole zerlegt Umlaute, und man will den Lauf nach
  einem Wort durchsuchen können.

## Wiederkehrende Aufgaben

| Aufgabe | Wie |
|---|---|
| Newsmeldung | **eine** Datei `_posts/JJJJ-MM-TT-kuerzel.md` mit `title` und `excerpt`. Geht auch über die Weboberfläche von GitHub, ohne lokales Repo. `werkzeug/neue-news.ps1 "Titel"` legt sie mit fertigem Kopf an. |
| Neues Release | ein Eintrag oben in `_data/downloads.yml`. Der oberste gilt als aktuelle Fassung, alle weiteren als Archiv. |
| Bilder | `python werkzeug/bilder_aufbereiten.py` — skaliert aus `quellen/` und `rohbilder/` nach `assets/bilder/` (WebP, 1000 px) und schreibt `_data/bilder.yml`. Die Alternativtexte stehen **im Skript**; ein Motiv ohne Alternativtext wird absichtlich nicht aufbereitet. |
| Schriften | `werkzeug/schriften_holen.ps1`, einmalig. Liegen als woff2 im Repo. |
| Navigation | `_data/navigation.yml` |

## Aufbau

`_layouts/basis.html` trägt Kopf, Zierbalken, Navigation, Schalter und Fuß; `seite`, `start` und
`news` bauen darauf auf. Inhalte, die sich wiederholen, stehen in `_data/*.yml` und werden in Liquid
durchlaufen — Navigation, Downloads, Team, Links, Bilder. Damit steht jede Angabe **einmal** im Repo;
die Jahreszahl im Fuß etwa kommt aus `site.time`.

**`quellen/` enthält das unbearbeitete Bildmaterial** und steht in der `exclude`-Liste von
`_config.yml`: Ausgeliefert werden nur die fertigen WebP unter `assets/bilder/`. `rohbilder/` ist
zusätzlich in `.gitignore` (große Aufnahmen aus dem E2E-Treiber des Godot-Clients).

### Gestaltung

Die Custom Properties auf `:root` sind die einzige Schaltstelle. Ein Thema wird an **drei** Stellen
gepflegt: `:root` (hell), die `prefers-color-scheme`-Abfrage und `:root[data-thema="dunkel"]` — die
letzten beiden identisch, damit sowohl die Systemeinstellung als auch die eigene Wahl greifen.
Dasselbe Muster beim Schriftschalter (`[data-schrift="lesbar"]`).

Ein Inline-Skript im `<head>` setzt `data-thema`/`data-schrift` aus `localStorage`, **bevor** der
Browser zeichnet; ohne das blitzt beim Laden das falsche Thema auf. `einstellungen.js` setzt danach
nur noch Attribute — **niemals `textContent`**, sonst verschwindet die SVG im Themenschalter. Welches
Symbol sichtbar ist, entscheidet das Stylesheet.

Ohne JavaScript muss jede Seite vollständig lesbar und bedienbar bleiben; JS schaltet ausschließlich
Thema und Schrift.

## Fallstricke, die in diesem Repo schon zugeschlagen haben

- **PowerShell-Here-Strings taugen nicht für `git commit -F -`.** Der Text landet als Argument statt
  auf stdin. Für Commit-Nachrichten den Bash-Heredoc nehmen: `git commit -F - <<'EOF' … EOF`.
- **Python-Skripte in eine Datei schreiben, nicht als Heredoc einspeisen.** Über den Heredoc kommen
  Umlaute zerlegt an; ein Anker mit „Änderung" trifft dann nie.
- **Zeilenenden messen, nie annehmen.** Der Arbeitsbaum ist gemischt (git wandelt beim Auschecken
  um). Mit `newline=""` lesen, das dominante Ende bestimmen und die Anker darauf umstellen — sonst
  trifft ein mit `\n` geschriebener Anker eine CRLF-Datei nie. Danach `git diff --stat` prüfen: Ein
  Diff über die ganze Datei heißt, die Zeilenenden sind umgekippt.
- **Vor jedem `replace` ein `assert alt in s`.** Hat hier mehrfach verhindert, dass eine Datei halb
  umgeschrieben wird.
- **`git add -A` ist durch einen Hook blockiert.** Geänderte Pfade einzeln stagen.
- **GitHub Pages kann keine HTTP-Weiterleitung.** Kein `.htaccess`, keine `_redirects`, keine 301.
  `jekyll-redirect-from` erzeugt HTML mit `<meta http-equiv="refresh">`. Gemessen: `.php`-Dateien
  liefert Pages mit Status 200, aber als `application/x-httpd-php` aus — der Browser lädt sie
  herunter. Weiterleitungsseiten unter alten `.php`-Pfaden scheiden damit aus; das fängt `404.html`
  per JavaScript ab.
- **`main` ist geschützt** (eine Freigabe nötig). Einen eigenen PR kann man nicht selbst freigeben;
  der Eigentümer steht auf der Ausnahmeliste, gemergt wird mit `gh pr merge <n> --merge --admin`.
- **Dateien über 100 MB weist GitHub beim Push ab.** Große Binärdateien gehören an ein Release, nicht
  ins Repo (die MSI von 1.4.1/1.4.2 hängen am Tag `archiv-2018-2019` im WinForms-Repo).
- **Jekylls `date`-Filter schreibt Monatsnamen englisch.** Für ausgeschriebene Daten
  `{% include datum-lang.html datum=… %}` benutzen; eine Prüfung schlägt sonst an.
- **`<details>` als Aufklappnavigation funktioniert nicht** wie erhofft: Ein geschlossenes `<details>`
  verbirgt seine Kinder über einen Mechanismus des Browsers, den eine Media Query nicht verlässlich
  aufhebt. Die Navigation war dadurch oberhalb von 700 px unsichtbar **und** nicht zu öffnen. Sie
  bricht jetzt schlicht um.
- **Wartebedingungen eindeutig wählen.** Eine Schleife, die auf das Wort „umgezogen" wartete, brach
  sofort ab — das Wort stand auch auf der 404-Seite.

## Veröffentlichung und Domain

`.github/workflows/pages.yml` baut bei jedem Pull Request und veröffentlicht zusätzlich auf `main`.
Der lychee-Schritt prüft externe Verweise **ohne fehlzuschlagen** (fremde Seiten verschwinden, ohne
dass die eigene Veröffentlichung daran scheitern soll); interne Verweise prüft `pruefe_ausgabe.py`,
und das schlägt sehr wohl fehl. lychee braucht `--root-dir`, sonst meldet es jeden wurzelrelativen
Pfad als Fehler.

Die Seite läuft unter `https://conspiratio.github.io/`. **Die Umstellung von `conspiratio.net` auf
Pages hat noch nicht stattgefunden** — Reihenfolge, DNS-Werte und Fallstricke stehen in
[`docs/umstellung-dns.md`](docs/umstellung-dns.md). Bis dahin melden CI-Läufe zwei Gruppen toter
Verweise, beide erwartet: `forum.conspiratio.net` (die Subdomain entsteht erst) und
`conspiratio.net/…` (kanonische Adressen, geprüft gegen die noch laufende alte Seite).

Entwurf und Plan des Neubaus liegen unter [`docs/superpowers/`](docs/superpowers/).
