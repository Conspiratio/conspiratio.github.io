# Umstellung von conspiratio.net auf GitHub Pages

Diese Schritte kann nur ausführen, wer Zugriff auf cPanel und auf die Repo-Einstellungen hat.
**Die Reihenfolge ist zwingend** — andernfalls ist das Forum zwischen zwei Schritten nicht
erreichbar.

## Wo die Zone liegt

Die Domain ist bei **United-Domains** registriert, aber dort sind Hostgators Nameserver
eingetragen (gemessen: `ns8353.hostgator.com`, `ns8354.hostgator.com`). Autoritativ ist damit
Hostgator: **Alle DNS-Einträge werden in cPanel unter „Domains → Zone Editor" geändert**, nicht
bei United-Domains. Dort steht nur die Registrierung und der Verweis auf diese Nameserver.

Das ist auch die risikoärmste Variante, weil MX, SPF und DKIM unangetastet an Ort und Stelle
bleiben und nur die A-Einträge angefasst werden.

### Bestand vor der Umstellung

| Typ | Name | Wert |
|---|---|---|
| A | `@` | `108.167.142.87` |
| CNAME | `www` | `conspiratio.net` |
| A | `mail` | `108.167.142.87` |
| MX | `@` | `0 mail.conspiratio.net` |
| TXT | `@` | `v=spf1 a mx include:websitewelcome.com ~all` |
| TXT | `default._domainkey` | DKIM-Schlüssel |

AAAA-Einträge gibt es **keine** — IPv6 ist nicht in Gebrauch. Ein `_dmarc`-Eintrag fehlt
ebenfalls; das ist unabhängig von dieser Umstellung.

## 1. Forum auf eine eigene Subdomain

In cPanel unter **Subdomains** `forum` anlegen. Beim Dokumentenstamm aufpassen: Er muss auf den
**vorhandenen** Forenordner zeigen (meist `public_html/forum`), nicht auf einen neuen leeren.
cPanel legt dabei in der Regel den A-Eintrag `forum` → `108.167.142.87` selbst an; falls nicht,
von Hand im Zone Editor nachtragen.

Danach AutoSSL für die Subdomain laufen lassen, sonst gibt es Zertifikatswarnungen.

Im Forum selbst (phpBB) umstellen:

- **ACP → Allgemein → Server-Einstellungen:** Domain-Name `forum.conspiratio.net`, Skript-Pfad `/`
  (vorher vermutlich `/forum`), Protokoll `https://`, Port 443, „Server-URL erzwingen" ein.
- **ACP → Allgemein → Cookie-Einstellungen:** Cookie-Domain auf `forum.conspiratio.net`. Ohne das
  funktioniert die Anmeldung nicht. Alle Nutzer werden dabei einmal abgemeldet — das ist normal.
- Falls der Zugang zum ACP danach klemmt: Dieselben Werte stehen in der Tabelle `phpbb_config`
  unter `server_name`, `script_path`, `server_protocol` und `cookie_domain` und lassen sich in
  phpMyAdmin geradeziehen.

Erst weitermachen, wenn das Forum über die neue Adresse erreichbar ist. Die neue Seite verweist
bereits ausschließlich dorthin — die übernommenen Newsmeldungen enthalten Dutzende solcher Links.

Solange die Subdomain fehlt, meldet der lychee-Schritt in CI sie zu Recht als nicht erreichbar.
Das ist erwartet und blockiert nichts (`fail: false`); nach diesem Schritt verschwindet die
Meldung von selbst.

## 2. E-Mail-Routing festnageln

In cPanel unter **E-Mail → E-Mail-Routing** ausdrücklich auf **„Local Mail Exchanger"** stellen.

Steht dort „Automatisch", entscheidet cPanel anhand des DNS, ob es Mail selbst zustellt. Sobald
der A-Eintrag des Apex auf GitHub zeigt, kann es auf „Remote Mail Exchanger" umspringen und die
lokale Zustellung einstellen — die Mail geht dann ins Nichts, obwohl der MX stimmt.

## 3. Neue Seite unter github.io abnehmen

In `Settings → Pages → Build and deployment → Source` auf **„GitHub Actions"** stellen. Nach dem
nächsten Push auf `main` läuft der Workflow und veröffentlicht unter
`https://conspiratio.github.io/`.

Dort abnehmen: alle Seiten, in hell und dunkel, mit Zier- und Lesbarkeitsschrift, in
Telefonbreite und mit abgeschaltetem JavaScript.

## 4. TTL senken

Ein bis zwei Tage vor der Umstellung die TTL des A-Eintrags für `@` auf **300 Sekunden**
setzen. Dann ist eine Rücknahme in Minuten statt in Stunden wirksam. Nach der geglückten
Umstellung wieder auf den üblichen Wert erhöhen.

## 5. Apex auf GitHub umstellen

Im Zone Editor den A-Eintrag für `@` durch diese vier ersetzen:

| Typ | Name | Wert |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `conspiratio.github.io` |

AAAA-Einträge sind **nicht nötig** — die Zone hat heute keine, IPv6 ist nicht in Gebrauch. Wer
sie doch will: `2606:50c0:8000::153` bis `2606:50c0:8003::153`. Bietet Hostgators Zone Editor
keine AAAA an, einfach weglassen; über IPv4 ist die Seite vollständig erreichbar.

**Nicht anfassen:** `MX`, den A-Eintrag für `mail` (der darf **nicht** mit umziehen), und das
DKIM-TXT. Sie stören sich nicht mit den A-Einträgen des Apex — das ist der Grund, warum der
Umzug der Webseite die Mail nicht berührt.

Dann im Repo eine Datei `CNAME` mit dem einzigen Inhalt `conspiratio.net` anlegen und pushen
(oder in `Settings → Pages → Custom domain` eintragen, was dieselbe Datei erzeugt).

## 6. HTTPS erzwingen — erst danach

GitHub stellt das Zertifikat selbst aus (Let's Encrypt). Das dauert bis zu 24 Stunden.

**„Enforce HTTPS" erst anhaken, wenn GitHub das Zertifikat ausgestellt hat.** Vorher gesetzt,
ist die Seite in der Zwischenzeit nicht erreichbar.

## 7. SPF nachziehen

Der bestehende Eintrag lautet:

```
v=spf1 a mx include:websitewelcome.com ~all
```

Das `a` bedeutet „der Server hinter dem A-Eintrag von conspiratio.net darf senden". Nach der
Umstellung zeigt dieser A-Eintrag auf GitHub — das `a` autorisiert also Webserver, die niemals
Mail versenden, und nicht mehr den Mailserver.

**Die Zustellung bricht dadurch nicht**, weil `mx` den tatsächlichen Absender weiterhin abdeckt
(`mail.conspiratio.net` zeigt auf dieselbe IP). Richtig ist danach trotzdem:

```
v=spf1 mx include:websitewelcome.com ~all
```

Nur das `a` streichen, sonst nichts.

## 8. Nachkontrolle

- `https://conspiratio.net` und `https://www.conspiratio.net` erreichbar, gültiges Zertifikat.
- `https://conspiratio.net/geschichte.html` landet auf `/spiel/` — ebenso die fünf anderen alten
  Adressen (`download.html`, `bilder.html`, `ueber.html`, `links.html`, `kontakt.html`).
- `https://conspiratio.net/forum/` leitet auf die Subdomain; ein Tiefenlink wie
  `/forum/viewtopic.php?p=204` ebenfalls (über die 404-Seite).
- `https://forum.conspiratio.net/` erreichbar, Anmeldung funktioniert.
- `https://conspiratio.net/feed.xml` liefert den Newsfeed.
- **Eine Testmail an `mail@conspiratio.net` senden und eine von dort verschicken.**

## Was danach noch offen ist

Der Hostgator-Webspeicher wird nur noch vom Forum und von der Mail gebraucht. cPanel betrachtet
den A-Eintrag der Hauptdomain als „seinen" — nach größeren Kontoaktionen prüfen, ob er noch auf
GitHub zeigt.
