# Modernisierung von conspiratio.net auf GitHub Pages

Stand: 2026-09-12

## 1. Ziel und Abgrenzung

Die Projektseite (Repo `Conspiratio/conspiratio.github.io`) wird heute von Hand per FTP zu Hostgator
hochgeladen und ist unter `conspiratio.net` erreichbar. Sie besteht aus sieben HTML-Dateien in
HTML 4.01 mit fester Breite von 1000 px, einer gemeinsamen `cons.css` und einer siebenfach kopierten
Navigation.

Dieses Vorhaben stellt sie auf **GitHub Pages** um und modernisiert sie dabei:

- responsiv, auf dem Telefon benutzbar (heute nicht der Fall),
- helles und dunkles Thema, umschaltbar,
- ein Schalter für eine gut lesbare Schriftart,
- Newsmeldungen, die sich mit einer einzigen Markdown-Datei anlegen lassen,
- inhaltlich auf den Stand des Godot-Clients gebracht.

Kein CMS, keine Datenbank, kein JavaScript-Framework. Ausgeliefert wird statisches HTML.

**Nicht Gegenstand dieses Spec:**

- Das Forum. Es zieht lediglich auf eine Subdomain um und bleibt technisch, wie es ist. Ob es
  langfristig durch Discord ersetzt wird, ist eine spätere Entscheidung.
- Die beiden Handbücher. Das WinForms-Wiki und das Godot-Handbuch
  (siehe `2026-09-12-godot-handbuch-pages-design.md`) bleiben eigenständig; diese Seite verlinkt sie.
- Eine vollständige englische Fassung. Es entsteht **eine** englische Seite.
- Der Godot-Release selbst. Die Seite wird so gebaut, dass sie ihn ohne Umbau aufnehmen kann.

## 2. Entscheidungen im Überblick

| Frage | Entscheidung |
|---|---|
| Hosting | GitHub Pages, Quelle: GitHub Actions |
| Domain | `conspiratio.net` als Apex auf Pages; Forum auf `forum.conspiratio.net` |
| Generator | Jekyll (der von Pages nativ unterstützte Weg) |
| Newsmeldung | eine Markdown-Datei in `_posts/` |
| Sprache | deutsch, dazu eine einzelne englische Seite unter `/en/` |
| Godot-Client | steht vorn als kommender Hauptclient; WinForms 1.4.8 bleibt daneben herunterladbar |
| Themen | hell (Pergament) und dunkel (Kontor bei Kerzenlicht), umschaltbar |
| Schrift | Grenze Gotisch / EB Garamond, umschaltbar auf Atkinson Hyperlegible |

### Warum Jekyll und nicht handgeschriebenes HTML

Die heutige Seite hat zwei Schmerzpunkte, und beide haben dieselbe Ursache: Kopf, Navigation und
Fußzeile stehen siebenmal im Repo. Der Git-Verlauf zeigt es wörtlich — *„Jahreszahl auf jeder Seite
aktualisiert"*. Ein Generator löst das und bringt das News-Archiv, den RSS-Feed und die Sitemap
nebenbei mit. Das Ergebnis bleibt schlankes statisches HTML; die Seite wird nicht schwerer, sondern
leichter.

Verworfen wurden: ein selbst geschriebener Generator in Python (Eigenbau für Paginierung, Feed und
Sitemap, ohne Gegenwert bei sieben Seiten) und ein reines Laufzeit-Rendern der News per JavaScript aus
einer `news.json` (die Meldungen stünden nicht im Quelltext — für Suchmaschinen und Feedreader wäre
die Seite leer, und die duplizierte Navigation bliebe bestehen).

## 3. Domain, Forum und Umschaltung

### Zielzustand

| Name | Ziel |
|---|---|
| `conspiratio.net` | GitHub Pages (vier A-Records und vier AAAA-Records) |
| `www.conspiratio.net` | `CNAME` auf `conspiratio.github.io` |
| `forum.conspiratio.net` | A-Record auf die bisherige Hostgator-IP |

A-Records: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
AAAA-Records: `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`,
`2606:50c0:8003::153`.

Im Repo liegt eine Datei `CNAME` mit dem einen Inhalt `conspiratio.net`. Das Zertifikat stellt Pages
selbst aus (Let's Encrypt); „Enforce HTTPS" wird danach aktiviert.

### Reihenfolge der Umstellung

Diese Reihenfolge ist zwingend, sonst ist das Forum zwischen zwei Schritten nicht erreichbar:

1. `forum.conspiratio.net` anlegen und auf Hostgator einrichten, prüfen, dass das Forum darüber
   läuft.
2. Alle Verweise auf `conspiratio.net/forum/` im Forum selbst und in der neuen Seite auf die
   Subdomain umstellen.
3. Die neue Seite unter `conspiratio.github.io` fertigstellen und dort prüfen.
4. Erst dann die A-/AAAA-Records des Apex auf GitHub umstellen und die `CNAME`-Datei einchecken.
5. Nach erfolgreicher Zertifikatsausstellung „Enforce HTTPS" setzen.

### Manuelle Voraussetzungen

Zwei Schritte kann nur der Repo- bzw. Domaineigentümer ausführen:

1. In `conspiratio.github.io` → Settings → Pages → Source auf **„GitHub Actions"** stellen und unter
   „Custom domain" `conspiratio.net` eintragen.
2. Die DNS-Einträge beim Anbieter setzen (Abschnitt oben).

### Alte URLs

Die Domain bleibt dieselbe, also bleiben alle je verlinkten Adressen bestehen. `geschichte.html`,
`download.html`, `bilder.html`, `ueber.html`, `links.html` und `kontakt.html` werden über
`jekyll-redirect-from` als Weiterleitungen auf die neuen Adressen geführt. Das betrifft unter anderem
externe Verweise aus dem Wikipedia-Artikel zu *Die Fugger II* und aus den Foren befreundeter
Projekte.

## 4. Technik

### Verzeichnisstruktur

```
_config.yml              Titel, URL, Sammlungen, Plugins, Standard-Frontmatter
_layouts/
  basis.html             <head>, Themenattribut, Kopf, Fuß
  seite.html             Inhaltsseite
  news.html              eine Newsmeldung
  start.html             Startseite mit Aufmacher und News-Anrissen
_includes/
  navigation.html        einmal, nicht siebenmal
  fuss.html
  schalter.html          Thema, Schrift, EN
_posts/
  2026-01-01-conspiratio-1-4-8.md
_data/
  downloads.yml          Version, Datum, Dateigröße, Links je Release
  team.yml
  links.yml
  bilder.yml             Bild, Alternativtext, Client (godot|winforms)
assets/
  css/conspiratio.css
  js/einstellungen.js
  schriften/*.woff2
  bilder/
CNAME
*.html                   Weiterleitungsstümpfe der alten Adressen
.github/workflows/pages.yml
werkzeug/neue-news.ps1
```

### Bauen und Ausliefern

Ein Actions-Workflow auf Push nach `main`: `actions/checkout` → `ruby/setup-ruby` (mit
Bundler-Zwischenspeicher) → `bundle exec jekyll build` → `actions/upload-pages-artifact` →
`actions/deploy-pages`. Berechtigungen `pages: write` und `id-token: write`.

Nicht die eingebaute Pages-Jekyll-Automatik, sondern Actions — aus demselben Grund wie beim
Handbuch-Spec: Die Versionen stehen in `Gemfile.lock` und sind damit gepinnt, und die Plugin-Auswahl
ist frei. Bei Pull Requests läuft derselbe Build ohne den Deploy-Schritt, so dass ein Fehler vor dem
Merge auffällt.

**Plugins, abschließend:** `jekyll-feed` (RSS), `jekyll-seo-tag` (Meta- und OpenGraph-Angaben),
`jekyll-sitemap`, `jekyll-redirect-from`. Mehr nicht.

### Lokale Vorschau

`bundle exec jekyll serve` braucht Ruby. Auf Windows ist das die unangenehmste Stelle des Vorhabens;
der RubyInstaller mit DevKit genügt. Wer das nicht einrichten will, arbeitet über Pull Requests und
prüft das Ergebnis nach dem Merge — für Textänderungen und Newsmeldungen reicht das, weil deren
Layout sich nicht ändert.

## 5. Seiten und Navigation

Kopfzeile: **Das Spiel · Bilder · Downloads · News · Handbuch ↗ · Mitmachen · Kontakt**, rechts
daneben die Schalter für Thema und Schrift sowie `EN`. Fußzeile: Links, Datenschutz, GitHub, Lizenz,
Jahreszahl (aus `site.time`, also nie wieder von Hand). Das Team steht auf `/mitmachen/` und bekommt
daher keinen eigenen Fußzeileneintrag.

| Adresse | Inhalt | Herkunft |
|---|---|---|
| `/` | Aufmacher, Download-Knopf, die drei neuesten Meldungen als Anrisse, Discord-Hinweis | `index.html`, `geschichte.html` |
| `/spiel/` | Spielbeschreibung, die Kernschleife in vier bis fünf Absätzen mit Bildern; die Ämtergrafiken aus `bilder/` bekommen hier einen Platz | `geschichte.html`, erweitert |
| `/bilder/` | Galerie, getrennt nach Godot- und WinForms-Client, Godot zuerst | `bilder.html` + neue Bilder |
| `/downloads/` | Godot-Client oben (Stand, Changelog, Repo, Platz für den Release-Knopf), darunter WinForms 1.4.8 und das Archiv, darunter Systemvoraussetzungen je Client | `download.html` |
| `/news/` | Archiv, jahrweise gruppiert, mit RSS-Verweis | neu |
| `/news/<jahr>/<monat>/<tag>/<kürzel>/` | eine Meldung | neu |
| `/mitmachen/` | was gebraucht wird (Grafik, Testen, Übersetzung, Code), wie man anfängt, dazu das Team | `ueber.html`, erweitert |
| `/kontakt/` | Discord, Mail, Forum (neue Subdomain) | `kontakt.html` |
| `/links/` | unverändert übernommen, über die Fußzeile erreichbar | `links.html` |
| `/en/` | eine englische Seite: Was das Spiel ist, Download, GitHub, Discord | neu |
| `/datenschutz/` | was GitHub Pages beim Ausliefern verarbeitet und was die Seite selbst erhebt (nichts) | neu |

**Kein Impressum, nur Datenschutz.** Erwogen war zunächst eine Anbieterkennzeichnung nach § 5 DDG.
Der Projekteigentümer hat entschieden, keine zu führen und wie bisher keine Anschrift zu
hinterlegen: Das Projekt ist ein nicht-kommerzielles Open-Source-Fanprojekt ohne finanzielle Ziele,
und die Pflicht greift in dieser Konstellation nach seiner Einschätzung nicht.

Angelegt wird deshalb allein eine **Datenschutzerklärung**. Sie ist auch die inhaltlich
begründetere der beiden: Der Wechsel zu GitHub Pages verlagert die Auslieferung zu einem
US-Anbieter, der dabei IP-Adressen verarbeitet, und genau das erfährt der Besucher sonst nirgends.
Sie hält außerdem fest, was die Seite *nicht* tut — keine Cookies, keine Zählung, keine fremden
Inhalte, keine Formulare —, was nach dem Selbst-Ausliefern der Schriften eine sehr kurze und
ungewöhnlich vollständige Aufzählung ist.

**Inhaltliche Aktualisierungen**, die dabei anfallen: Die Kompatibilitätsangabe nennt heute
Windows 7/8/10; sie wird je Client richtiggestellt (WinForms: .NET Framework 4.6.2; Godot: .NET 8).
Die Spielbeschreibung nennt den Godot-Client und seine Neuerungen. Der Verweis auf das
Forums-Newsarchiv wird durch `/news/` ersetzt und bleibt nur als Fußnote im Archiv stehen.

## 6. Das News-System

### Format

Eine Meldung ist eine Datei `_posts/JJJJ-MM-TT-kuerzel.md`:

```markdown
---
title:   "Der Godot-Client ist da"
date:    2026-09-12
excerpt: "Nach vier Jahren Umbau steht die erste Fassung des neuen Clients bereit."
bild:    /assets/bilder/news/godot-1-0-0.png     # optional
---

Werte Spieler,

… Fließtext in Markdown …
```

Datum und URL-Kürzel stammen aus dem Dateinamen, das Layout aus dem Standard-Frontmatter in
`_config.yml`. Die Schlüssel sind Jekylls eigene (`title`, `date`, `excerpt`) und bleiben daher
englisch, während alles Inhaltliche deutsch ist — das ist eine technische Schnittstelle, kein
Domänenbegriff. Fehlt `excerpt`, nimmt Jekyll den ersten Absatz.

### Drei Wege, eine Meldung anzulegen

1. **Im Browser auf github.com:** „Add file" → Dateiname → Text → „Commit". Nach ein bis zwei
   Minuten ist die Meldung online. Kein lokales Repo, kein Ruby, kein Editor; das geht auch vom
   Telefon.
2. Lokal anlegen und pushen.
3. `werkzeug/neue-news.ps1 "Titel der Meldung"` legt die Datei mit fertigem Kopf und heutigem Datum
   an.

### Was automatisch entsteht

Die Anrisse auf der Startseite, die Archivseite, die Einzelseite je Meldung, `/feed.xml` und die
Sitemap-Einträge.

### Übernahme des Bestands

Die vorhandenen Texte gehen nicht verloren. `Massenmail_2021.txt`, `Massenmail_2022.txt`,
`massenmails/Massenmail_2024.txt` und die aktuelle Startseitenmeldung (1.4.8, 01.01.2026) werden zu
vier Meldungen mit Originaltext und Originaldatum. Für die übrigen Releases (1.4.1 bis 1.4.6)
entstehen kurze Einträge aus Datum, Version und Changelog-Link, so dass das Archiv eine durchgehende
Linie von 2018 bis heute zeigt. Die Rohtexte bleiben als Dateien im Repo erhalten.

### Bewusst nicht gebaut

Eine Automatik, die aus einem veröffentlichten GitHub-Release eine Newsmeldung erzeugt. Die
Meldungen sind Briefe an die Spieler („Werte Spieler, frohe Weihnachten…"), keine
Changelog-Auszüge; ein Generat davon wäre schlechter als ein selbst geschriebener Absatz.
Nachrüstbar bleibt es.

## 7. Aussehen

### Zwei Themen, beide aus dem Spielmaterial

Die Vorlage liefert beide Stimmungen bereits: `pergament3.png` ist das helle Thema,
`hintIntro.png` (Kontor bei Kerzenlicht) das dunkle.

| | hell | dunkel |
|---|---|---|
| Grund | Pergament, warmes Creme | tiefes Braunschwarz |
| Schrift | dunkles Braun | warmes Cremeweiß |
| Akzent | Bernstein-Gold der Kerzenflamme | dasselbe Gold, etwas heller |

Kein blaugraues Standard-Dunkelthema — das Spiel hat eine eigene Palette und die trägt. Damit
entfällt zugleich der auffälligste Altbestand: Links stehen heute in `#0000FF` und werden beim
Überfahren weiß.

Umgesetzt über CSS-Variablen auf `:root`; das dunkle Thema definiert nur die Variablen neu. Ein
`data-thema`-Attribut am Wurzelelement gewinnt gegen `prefers-color-scheme`, so dass die
Voreinstellung des Systems gilt, bis der Besucher selbst wählt.

### Schrift

Hier liegt das eigentliche Lesbarkeitsproblem: Heute steht der *gesamte* Fließtext in Old English
Text MT bei 22 px.

| | Standard | Schalter „gut lesbar" |
|---|---|---|
| Überschriften | Grenze Gotisch | wie der Fließtext |
| Fließtext | EB Garamond | Atkinson Hyperlegible |
| Zeilen-/Buchstabenabstand | normal | leicht erhöht |

Gebrochene Schrift nur noch als Auszeichnung (Seitentitel, H1, H2), nie im Fließtext. Atkinson
Hyperlegible ist eigens für Menschen mit Sehschwäche entworfen und frei lizenziert — der Schalter
ist damit eine Hilfe und keine Geste.

Alle Schriften werden als `woff2` **selbst ausgeliefert**, nicht von Google geladen: schneller, und
der Datenschutzabsatz bleibt kurz.

**Lizenzfehler, der dabei behoben wird:** `OLDENGL.TTF` liegt im Repo und wird per `@font-face`
ausgeliefert. Das ist eine Microsoft-Systemschrift und dafür nicht lizenziert. Sie wird entfernt.

### Layout

Das feste `width: 1000px` entfällt. Eine Spalte, Zeilenlänge auf etwa 70 Zeichen begrenzt,
Schriftgrößen über `clamp()`, Galerie als CSS-Grid (`repeat(auto-fill, minmax(240px, 1fr))`).
Unterhalb von etwa 700 px klappt die Navigation über ein `<details>`-Element auf — ohne JavaScript.

Kein CSS-Framework. Eine Datei, CSS-Variablen als einzige Schaltstelle.

### Zierrat

Der Holzbalken mit den Symbolen (`header4.png` — Fachwerkhaus, Kreuz, Hammer, Truhe, Schwert,
Wagenrad) bleibt als schmales Band unter dem Seitentitel; die Holztextur kachelt waagerecht. Das
Introbild wird zum Aufmacher der Startseite statt zum festen Vollbildhintergrund hinter jedem Text.
Das Pergament wird zur wiederholbaren Kachel statt zum Einzelbild von 192 KB.

### Skript

`assets/js/einstellungen.js`, etwa 40 Zeilen: Voreinstellung aus `prefers-color-scheme`, ein Klick
überschreibt und merkt sich das im `localStorage`, dasselbe für die Schrift. Ein winziges Skript im
`<head>` setzt die Attribute **vor** dem ersten Zeichnen — sonst blitzt beim Laden kurz das falsche
Thema auf. Ohne JavaScript ist die Seite vollständig benutzbar, nur ohne Umschalter.

### Barrierefreiheit und Ladezeit

Feste Vorgaben, gegen die abgenommen wird: Kontrast mindestens 4,5:1 in beiden Themen, sichtbarer
Fokusrahmen, `alt`-Texte für alle Screenshots, `prefers-reduced-motion` beachtet, Sprache über
`lang` ausgezeichnet. Bilder als WebP mit Rückfall, `loading="lazy"`, feste `width`/`height` gegen
das Umspringen beim Laden.

## 8. Bilder und Altlasten

- **Godot-Screenshots** kommen aus derselben Quelle wie die des Handbuchs: der `--bilder`-Ernte des
  E2E-Treibers im Repo `Conspiratio.Godot` (siehe `2026-09-12-godot-handbuch-pages-design.md`,
  Kapitel 6). Für die Galerie genügt eine Handvoll — Kontor, Stadt, Schreibstube, Weltkarte,
  Gerichtsverhandlung, Ämterübersicht. Aufbereitung wie dort beschrieben.
- **WinForms-Screenshots** werden aus `screenshots/` übernommen; die getrennten `_thumb`-Dateien
  entfallen, die Galerie skaliert selbst.
- `Jurist_aufsuchen.png` (2,1 MB im Wurzelverzeichnis) wird von keiner Seite eingebunden und
  entfällt.
- Die Ämtergrafiken aus `bilder/` (Stadt-, Land-, Reichsämter je politisch/kirchlich/militärisch)
  sind heute unverlinkt und bekommen auf `/spiel/` einen Platz.

## 9. Umsetzung und Prüfung

### Reihenfolge

Die Seite entsteht **neben** dem Alten im selben Repo, damit die laufende Seite bis zur Umschaltung
unangetastet bleibt.

1. Gerüst: `_config.yml`, Layouts, Includes, Workflow, Build grün unter `conspiratio.github.io`.
2. CSS: Themen, Schriften, Layout, Schalter — an einer Beispielseite abgenommen.
3. Inhaltsseiten übernehmen und aktualisieren.
4. News-System samt Übernahme des Bestands.
5. Bilder aufbereiten, Galerie.
6. Weiterleitungen, Datenschutzerklärung, englische Seite.
7. Altdateien entfernen: `cons.css`, `OLDENGL.TTF`, `Jurist_aufsuchen.png`, die `_thumb`-Dateien und
   die nicht mehr eingebundenen Hintergrundbilder. Die alten `*.html` bleiben als
   Weiterleitungsstümpfe, die `Massenmail_*.txt` als Quellen der übernommenen Meldungen.
8. Forum auf die Subdomain, dann Apex-Umstellung (Kapitel 3).

### Womit geprüft wird

Es gibt hier keine Testsuite und braucht auch keine; geprüft wird gegen eine feste Liste:

- **Build:** Der Actions-Lauf ist grün. Er läuft auch bei Pull Requests, ohne zu deployen.
- **Tote Links:** `lychee` als eigener Schritt im Workflow über die gebaute Seite. Das fängt genau
  den Fehler, den der Git-Verlauf zweimal zeigt (*„Korrigiere Versionsnummer im Link"*,
  *„Changeloglink angepasst"*). Externe Links werden gewarnt, nicht als Fehler gewertet — fremde
  Seiten verschwinden, ohne dass die eigene Veröffentlichung daran scheitern soll.
- **Darstellung:** Jede Seite in vier Kombinationen gesichtet — hell/dunkel × Standardschrift/gut
  lesbar —, dazu in Telefonbreite (375 px) und auf dem Schreibtisch.
- **Ohne JavaScript:** Jede Seite ist vollständig lesbar und bedienbar.
- **Kontrast:** Stichprobe je Thema gegen 4,5:1.
- **Weiterleitungen:** Jede der sechs alten Adressen landet auf der richtigen neuen Seite.

### Fehlerfälle, die bedacht sind

- **Zertifikat nach der DNS-Umstellung nicht sofort da.** Pages braucht bis zu 24 Stunden; bis
  dahin kein „Enforce HTTPS" setzen, sonst ist die Seite vorübergehend nicht erreichbar.
- **Jekyll-Build bricht bei einer fehlerhaften Newsmeldung ab** (unbalanciertes Frontmatter). Da der
  Deploy nur bei grünem Build läuft, bleibt die alte Fassung online; der Fehler steht im
  Actions-Protokoll.
- **Die Seite wird im Browser ohne lokale Vorschau bearbeitet.** Genau dafür läuft der Build bei
  Pull Requests.

## 10. Bewusst nicht Gegenstand

- Suche über die Seite (sieben Seiten brauchen keine).
- Kommentare unter Newsmeldungen (dafür gibt es Discord und das Forum).
- Besucherstatistik oder Analyse-Werkzeuge.
- Cookie-Banner — es werden keine Cookies gesetzt; `localStorage` für Thema und Schrift ist eine
  vom Besucher ausgelöste Einstellung und nicht einwilligungspflichtig.
- Eine automatische Kopplung zwischen dieser Seite und den Handbuch- oder Client-Repos.

## 11. Erfolgskriterien

1. `https://conspiratio.net` wird von GitHub Pages ausgeliefert, mit gültigem Zertifikat, und
   `www` leitet dorthin.
2. `https://forum.conspiratio.net` erreicht das Forum; die sechs alten Seitenadressen leiten auf
   ihre neuen Ziele.
3. Eine neue Newsmeldung entsteht durch das Anlegen einer einzigen Markdown-Datei — nachgewiesen,
   indem eine Meldung vollständig über die GitHub-Weboberfläche veröffentlicht wird.
4. Das News-Archiv enthält die Meldungen von 2018 bis heute; `/feed.xml` ist gültiges RSS.
5. Jede Seite ist in 375 px Breite ohne waagerechtes Scrollen lesbar.
6. Thema und Schriftart lassen sich umschalten, die Wahl überlebt einen Seitenwechsel, und beim
   Laden blitzt kein falsches Thema auf.
7. Ohne JavaScript bleibt jede Seite vollständig lesbar.
8. Der Godot-Client steht auf Startseite und Downloadseite vorn; WinForms 1.4.8 ist weiterhin
   herunterladbar.
9. `lychee` meldet keine toten internen Links.
10. `OLDENGL.TTF` ist aus dem Repo entfernt.

## 12. Offene Punkte

- ~~**Impressumsangaben** muss der Eigentümer beisteuern.~~ Entschieden: kein Impressum, nur eine
  Datenschutzerklärung (siehe Kapitel 5). Damit hängt die Veröffentlichung nicht mehr daran.
- **Der Godot-Release-Termin** ist offen. Die Downloadseite trägt bis dahin „erscheint demnächst"
  mit Verweis auf Repo und Changelog; der Release-Knopf ist vorbereitet und braucht dann nur einen
  Eintrag in `_data/downloads.yml`.
- **Die Zukunft des Forums** (Bestand oder Ablösung durch Discord) bleibt offen und berührt dieses
  Vorhaben nur über den Namen der Subdomain.
- **Die Aufteilung der Umsetzung** in Arbeitsschritte legt der Implementierungsplan fest.
