# Conspiratio.Website

Die Website von <https://conspiratio.net> — eine statische Jekyll-Seite, die über GitHub
Actions nach GitHub Pages veröffentlicht wird.

## Eine Newsmeldung schreiben

Eine Meldung ist **eine Datei** in `_posts/`, benannt `JJJJ-MM-TT-kuerzel.md`:

```markdown
---
title: "Der Godot-Client ist da"
excerpt: "Ein Satz, der auf der Startseite und im Archiv steht."
---

Werte Spieler,

… Fließtext in Markdown …
```

Drei Wege, sie anzulegen:

1. **Auf github.com**, ganz ohne lokales Repo: „Add file" → Dateiname eintippen → schreiben
   → „Commit". Nach ein bis zwei Minuten ist sie online. Das geht auch vom Telefon.
2. Lokal anlegen und pushen.
3. `powershell -File werkzeug/neue-news.ps1 "Titel der Meldung"` legt die Datei mit
   fertigem Kopf und heutigem Datum an.

Archiv, Anrisse auf der Startseite, Einzelseite und RSS-Feed entstehen daraus von selbst.

## Ein neues Release eintragen

Einen Eintrag oben in `_data/downloads.yml` ergänzen. Die Downloadseite nimmt den obersten
Eintrag als aktuelle Fassung, alle weiteren als Archiv.

## Lokal bauen

Braucht **kein Ruby**, nur Docker:

```powershell
powershell -File werkzeug/bauen.ps1              # einmalig bauen nach _site/
powershell -File werkzeug/bauen.ps1 -Vorschau    # Server auf http://localhost:4000
python werkzeug/pruefe_ausgabe.py                # prueft die gebaute Seite
```

`pruefe_ausgabe.py` tritt an die Stelle einer Testsuite: Es prüft Sprache, Navigation,
Kontrast in beiden Themen, tote interne Verweise, Alternativtexte, die Weiterleitungen der
alten Adressen und die Vollständigkeit des Newsarchivs. Es läuft auch in CI; ein Fehler
verhindert die Veröffentlichung.

## Bilder

`python werkzeug/bilder_aufbereiten.py` skaliert die Vorlagen aus `quellen/` und
`rohbilder/` nach `assets/bilder/` (WebP, 1000 px) und schreibt `_data/bilder.yml`.
Die Alternativtexte stehen in diesem Skript; ein Motiv ohne Alternativtext wird nicht
aufbereitet.

## Aufbau

| Ort | Inhalt |
|---|---|
| `_layouts/`, `_includes/` | Seitengerüst, Navigation, Fußzeile, Schalter |
| `_data/` | Navigation, Downloads, Team, Links, Bilder |
| `_posts/` | Newsmeldungen |
| `assets/` | CSS, JavaScript, Schriften, fertige Bilder |
| `quellen/` | unbearbeitete Bildvorlagen (nicht veröffentlicht) |
| `werkzeug/` | Bau-, Prüf- und Hilfsskripte |
| `docs/` | Spec, Implementierungsplan, Anleitung zur DNS-Umstellung |

Die Umstellung der Domain auf GitHub Pages beschreibt
[`docs/umstellung-dns.md`](docs/umstellung-dns.md).

## Lizenz

GNU General Public License v3.0. Die Schriftarten unter `assets/schriften/` stehen unter
der SIL Open Font License; ihre Lizenztexte liegen daneben.
