# Umstellung von conspiratio.net auf GitHub Pages

Diese Schritte kann nur ausführen, wer Zugriff auf die Domainverwaltung und auf die
Repo-Einstellungen hat. **Die Reihenfolge ist zwingend** — andernfalls ist das Forum
zwischen zwei Schritten nicht erreichbar.

## 1. Forum auf eine eigene Subdomain

Beim DNS-Anbieter einen A-Record `forum.conspiratio.net` auf die bisherige Hostgator-IP
setzen und im Forum selbst die Basis-URL auf `https://forum.conspiratio.net/` umstellen.

Erst weitermachen, wenn das Forum über die neue Adresse erreichbar ist. Die neue Seite
verweist bereits ausschließlich dorthin.

## 2. Neue Seite unter github.io abnehmen

In `Settings → Pages → Build and deployment → Source` auf **„GitHub Actions"** stellen.
Nach dem nächsten Push auf `main` läuft der Workflow und veröffentlicht unter
`https://conspiratio.github.io/`.

Dort abnehmen: alle zehn Seiten, in hell und dunkel, mit Zier- und Lesbarkeitsschrift,
in Telefonbreite und mit abgeschaltetem JavaScript.

## 3. Impressum ausfüllen

`impressum.md` trägt Platzhalter (`BITTE-AUSFUELLEN-NAME`, `BITTE-AUSFUELLEN-ANSCHRIFT`).
**Vor** der Domainumstellung ersetzen.

## 4. Apex auf GitHub umstellen

Beim DNS-Anbieter eintragen:

| Typ | Name | Wert |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| AAAA | `@` | `2606:50c0:8000::153` |
| AAAA | `@` | `2606:50c0:8001::153` |
| AAAA | `@` | `2606:50c0:8002::153` |
| AAAA | `@` | `2606:50c0:8003::153` |
| CNAME | `www` | `conspiratio.github.io` |

Dann im Repo eine Datei `CNAME` mit dem einzigen Inhalt `conspiratio.net` anlegen und
pushen (oder in `Settings → Pages → Custom domain` eintragen, was dieselbe Datei erzeugt).

## 5. HTTPS erzwingen — erst danach

GitHub stellt das Zertifikat selbst aus (Let's Encrypt). Das dauert bis zu 24 Stunden.

**„Enforce HTTPS" erst anhaken, wenn GitHub das Zertifikat ausgestellt hat.** Vorher
gesetzt, ist die Seite in der Zwischenzeit nicht erreichbar.

## 6. Nachkontrolle

- `https://conspiratio.net` und `https://www.conspiratio.net` erreichbar, gültiges Zertifikat.
- `https://conspiratio.net/geschichte.html` landet auf `/spiel/` — ebenso die fünf anderen
  alten Adressen (`download.html`, `bilder.html`, `ueber.html`, `links.html`, `kontakt.html`).
- `https://forum.conspiratio.net/` erreichbar.
- `https://conspiratio.net/feed.xml` liefert den Newsfeed.

## Was danach entfällt

Der Hostgator-Webspeicher wird nur noch vom Forum gebraucht. Bevor er ganz abgeschaltet
wird: **Die Installationsprogramme von 1.4.1 und 1.4.2 liegen ausschließlich dort**
(`/downloads/Conspiratio.1.4.1.0.msi` und `.1.4.2.0.msi`). Es gibt für beide kein
GitHub-Release. Wer sie erhalten will, lädt sie vorher herunter und legt sie als Release
im Repo `Conspiratio.WinForms` ab; danach können die Einträge in `_data/downloads.yml`
ihre `msi:`-Zeile bekommen und der Hinweis auf der Downloadseite entfallen.
