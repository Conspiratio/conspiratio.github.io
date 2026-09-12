# Umstellung von conspiratio.net auf GitHub Pages

> **Durchgeführt am 12.09.2026.** Die Seite wird seitdem von GitHub Pages ausgeliefert, das
> Forum läuft unter `forum.conspiratio.net`, die Mail unverändert bei Hostgator. Dieses
> Dokument bleibt als Protokoll stehen — es beschreibt den tatsächlichen Ablauf samt der
> Stellen, an denen es anders kam als geplant.

## Wo die Zone liegt

Die Domain ist bei **United-Domains** registriert, aber dort sind Hostgators Nameserver
eingetragen (`ns8353.hostgator.com`, `ns8354.hostgator.com`). Autoritativ ist damit Hostgator:
**Alle DNS-Einträge werden in cPanel unter „Domains → Zone Editor" geändert**, nicht bei
United-Domains. Dort steht nur die Registrierung und der Verweis auf diese Nameserver.

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

AAAA-Einträge gab es **keine** — IPv6 ist nicht in Gebrauch, und GitHub Pages ist über IPv4
vollständig erreichbar. Ein `_dmarc`-Eintrag fehlt ebenfalls; das ist unabhängig von dieser
Umstellung.

## 1. Forum auf eine eigene Subdomain

**Reihenfolge beachten — hier ging es beim ersten Versuch schief:** Wer den A-Eintrag für
`forum` von Hand im Zone Editor anlegt, kann die Subdomain danach nicht mehr erstellen. cPanel
bricht ab mit

```
Error: (XID …) A DNS entry for "forum.conspiratio.net" already exists.
```

Richtig ist deshalb: **erst die Subdomain in cPanel anlegen, den DNS-Eintrag macht cPanel
selbst.** Steht dort schon einer, vorher im Zone Editor löschen.

In cPanel unter **Domains → Create A New Domain** (ältere Fassungen: **Subdomains**) `forum`
anlegen. Beim Dokumentenstamm aufpassen: Er muss auf den **vorhandenen** Forenordner zeigen —
hier `public_html/forum` —, nicht auf das von cPanel vorgeschlagene
`public_html/forum.conspiratio.net`.

**Eine Änderung am Dokumentenstamm wirkt nicht sofort.** Nach dem Speichern vergehen einige
Minuten, bis der vHost neu gebaut ist; bis dahin liefert die Subdomain weiterhin eine
Fehlerseite. Das ist kein Grund, an der Einstellung zu zweifeln — erst nach ein paar Minuten
erneut nachsehen.

Im Forum selbst (phpBB) umstellen:

- **ACP → Allgemein → Server-Einstellungen:** Domain-Name `forum.conspiratio.net`, Skript-Pfad
  `/` (vorher `/forum`), Protokoll `https://`, Port 443, „Server-URL erzwingen" ein.
- **ACP → Allgemein → Cookie-Einstellungen:** Cookie-Domain auf `forum.conspiratio.net`. Ohne
  das funktioniert die Anmeldung nicht. Alle Nutzer werden dabei einmal abgemeldet.
- Falls der Zugang zum ACP danach klemmt: Dieselben Werte stehen in der Tabelle `phpbb_config`
  unter `server_name`, `script_path`, `server_protocol` und `cookie_domain` und lassen sich in
  phpMyAdmin geradeziehen.

**Sobald „Server-URL erzwingen" gesetzt ist, ist das Forum unter der alten Adresse nicht mehr
bedienbar** — es leitet dann auf die Subdomain, und wenn die noch nicht steht, ist es
vorübergehend nirgends erreichbar. Diesen Schritt also erst machen, wenn die Subdomain
antwortet.

### Zertifikat für die Subdomain

AutoSSL war auf diesem Konto nicht verfügbar („because my server is not configured to support
it"). **Das war kein Hindernis:** Auf dem Konto lag bereits ein Wildcard-Zertifikat

```
CN = *.conspiratio.net      Let's Encrypt
SAN: *.conspiratio.net, conspiratio.net
```

Ein Wildcard deckt genau eine Ebene ab, also auch `forum.conspiratio.net`. Hostgators eigene
Automatik hat es dem neuen vHost von selbst zugewiesen, kurz nachdem er stand. Falls das einmal
nicht geschieht, lässt es sich unter **SSL/TLS → „Zertifikate installieren und verwalten"** von
Hand zuweisen („Autofill by Domain").

> **Im Blick behalten:** Das Wildcard läuft alle 90 Tage ab. Dass es bisher erneuert wurde,
> spricht dafür, dass es weiterhin geschieht — ein Blick vor dem jeweiligen Ablaufdatum schadet
> nicht.

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

Ein bis zwei Tage vor der Umstellung die TTL des A-Eintrags für `@` auf **300 Sekunden** setzen.
Dann ist eine Rücknahme in Minuten statt in Stunden wirksam. Nach der geglückten Umstellung
wieder auf den üblichen Wert erhöhen.

## 5. Apex auf GitHub umstellen

Im Zone Editor den A-Eintrag für `@` durch diese vier ersetzen:

| Typ | Name | Wert |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `conspiratio.github.io` |

**Alle vier A-Einträge**, nicht einer — sie sind Ausfallsicherheit, kein Auswahlmenü. Der alte
Eintrag `108.167.142.87` wird dabei ersetzt, nicht ergänzt.

**`www` muss auf `conspiratio.github.io` zeigen, nicht auf den Apex.** Zeigt es auf
`conspiratio.net`, nimmt GitHub den Namen nicht mit ins Zertifikat, und `https://www…` wirft
eine Zertifikatswarnung — auch wenn die Seite selbst erreichbar ist.

AAAA ist nicht nötig (siehe oben). Wer sie doch will: `2606:50c0:8000::153` bis
`2606:50c0:8003::153`.

**Nicht anfassen:** `MX`, den A-Eintrag für `mail` (der darf **nicht** mit umziehen), und das
DKIM-TXT. Sie stören sich nicht mit den A-Einträgen des Apex — das ist der Grund, warum der
Umzug der Webseite die Mail nicht berührt.

## 6. Custom Domain und HTTPS

In **Settings → Pages → Custom domain** `conspiratio.net` eintragen und speichern. Das genügt;
eine `CNAME`-Datei im Repo ist derselbe Schalter über einen zweiten Weg und nicht zusätzlich
nötig.

GitHub stellt das Zertifikat selbst aus (Let's Encrypt), in der Regel in unter 15 Minuten.
**„Enforce HTTPS" erst anhaken, wenn es steht.**

**Ändert sich danach etwas am DNS, zieht GitHub von selbst nach.** Im Pages-Reiter erscheint
dann „Detected a change to DNS settings. Requesting a new certificate." — in diesem Fall genügt
Warten; die Domain muss nicht gelöscht und neu eingetragen werden. So kam auch `www` ins
Zertifikat, nachdem der CNAME korrigiert war.

## 7. SPF nachziehen

Der Eintrag lautete:

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

- `https://conspiratio.net` und `https://www.conspiratio.net` erreichbar, gültiges Zertifikat —
  im Zertifikat müssen **beide** Namen stehen (`subjectAltName`).
- `https://conspiratio.net/geschichte.html` landet auf `/spiel/` — ebenso die fünf anderen alten
  Adressen (`download.html`, `bilder.html`, `ueber.html`, `links.html`, `kontakt.html`).
- `https://conspiratio.net/forum/` leitet auf die Subdomain; ein Tiefenlink wie
  `/forum/viewtopic.php?p=204` ebenfalls (über die 404-Seite).
- `https://forum.conspiratio.net/` zeigt **direkt** die Forenübersicht, nicht erst unter
  `/forum/`. Anmeldung prüfen.
- `https://conspiratio.net/feed.xml` liefert den Newsfeed.
- **Eine Testmail an `mail@conspiratio.net` senden und eine von dort verschicken.**

## Beim Nachmessen zu beachten

- **Zwischenspeicher hinken hinterher.** Direkt nach der Umstellung liefern öffentliche
  Auflöser und der eigene Rechner noch die alte Adresse — teils stundenlang. Autoritativ
  nachsehen statt sich beirren zu lassen:
  `nslookup -type=A conspiratio.net ns8353.hostgator.com`
- **Mod_Security weist nackte Abrufe ab.** `curl` ohne browserartige Kopfzeilen bekommt vom
  Hostgator ein `406 Not Acceptable` oder eine Weiterleitung auf eine Fehlerseite. Zum Prüfen
  `User-Agent`, `Accept` und `Accept-Language` mitschicken, sonst misst man den Schutzmechanismus
  statt der Seite.
- **Das ausgelieferte Zertifikat hängt an der SNI.** Wer mit dem Browser oder `openssl` prüft,
  muss den richtigen Namen mitschicken (`-servername www.conspiratio.net`), sonst sieht man ein
  anderes Zertifikat als das, um das es geht.

## Was danach noch offen ist

Der Hostgator-Webspeicher wird nur noch vom Forum und von der Mail gebraucht. cPanel betrachtet
den A-Eintrag der Hauptdomain als „seinen" — nach größeren Kontoaktionen prüfen, ob er noch auf
GitHub zeigt.
