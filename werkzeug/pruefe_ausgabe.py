#!/usr/bin/env python3
"""Prueft die gebaute Seite in _site/ gegen feste Zusagen.

Aufruf: python werkzeug/pruefe_ausgabe.py
Exit 0 = alles in Ordnung, Exit 1 = mindestens eine Zusage verletzt.

Dieses Skript tritt an die Stelle einer Testsuite, die es fuer eine statische
Seite sonst nicht gaebe. Jede Aufgabe des Implementierungsplans ergaenzt hier
ihre Zusagen, bevor sie sie erfuellt.

Die Fehlermeldungen sind bewusst ASCII: Die Windows-Konsole zerlegt Umlaute,
und wer den Lauf nach einem Wort durchsuchen will, soll das tun koennen.
"""
from __future__ import annotations

import datetime
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
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


@pruefung
def jede_seite_traegt_navigation_und_fuss() -> None:
    for seite in seiten():
        text = seite.read_text(encoding="utf-8")
        if ist_weiterleitung(text):
            continue
        pfad = seite.relative_to(SITE)
        pruefe('class="hauptnavigation"' in text, f"{pfad}: Hauptnavigation fehlt")
        pruefe('class="fuss"' in text, f"{pfad}: Fusszeile fehlt")


@pruefung
def die_navigation_markiert_die_aktuelle_seite() -> None:
    text = lies("spiel/index.html")
    pruefe('aria-current="page"' in text,
           "spiel/index.html: aktiver Menuepunkt ist nicht als aria-current markiert")


@pruefung
def die_jahreszahl_kommt_aus_der_konfiguration() -> None:
    # Der Fuss nennt das laufende Jahr; es darf in keiner Inhaltsdatei hart stehen.
    text = lies("index.html")
    pruefe(str(datetime.date.today().year) in text,
           "index.html: das laufende Jahr steht nicht im Fuss")


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
    pruefe("#0000FF" not in css.upper(), "conspiratio.css: enthaelt noch das alte Linkblau #0000FF")
    pruefe("OLDENGL" not in css.upper(),
           "conspiratio.css: verweist noch auf die nicht lizenzierte Schrift")


def _leuchtdichte(hex_farbe: str) -> float:
    """Relative Leuchtdichte nach WCAG 2.1."""
    hex_farbe = hex_farbe.lstrip("#")
    werte = []
    for i in (0, 2, 4):
        anteil = int(hex_farbe[i:i + 2], 16) / 255
        werte.append(anteil / 12.92 if anteil <= 0.03928
                     else ((anteil + 0.055) / 1.055) ** 2.4)
    return 0.2126 * werte[0] + 0.7152 * werte[1] + 0.0722 * werte[2]


def _kontrast(vorne: str, hinten: str) -> float:
    hell, dunkel = sorted((_leuchtdichte(vorne), _leuchtdichte(hinten)), reverse=True)
    return (hell + 0.05) / (dunkel + 0.05)


@pruefung
def die_farben_haben_genug_kontrast() -> None:
    """Jede Schriftfarbe muss auf jedem Grund 4,5:1 erreichen - in beiden Themen.

    Die Werte werden aus dem gebauten CSS gelesen, nicht hier wiederholt: So
    faellt eine spaetere Farbaenderung auf, statt nur hier gepflegt zu werden.
    """
    css = lies("assets/css/conspiratio.css")
    if not css:
        pruefe(False, "conspiratio.css fehlt - Kontrast nicht pruefbar")
        return

    # Der erste :root-Block ist das helle Thema, der [data-thema="dunkel"]-Block
    # das dunkle. Beide tragen denselben Satz Variablen.
    def farben_aus(block: str) -> dict[str, str]:
        return dict(re.findall(r"--([a-z-]+):\s*(#[0-9a-fA-F]{6})", block))

    hell_block = css.split(":root {", 1)[-1].split("}", 1)[0]
    dunkel_block = css.split(':root[data-thema="dunkel"] {', 1)[-1].split("}", 1)[0]

    for name, block in (("hell", hell_block), ("dunkel", dunkel_block)):
        farben = farben_aus(block)
        fehlend = {"grund", "grund-erhoben", "schrift", "schrift-leise", "akzent"} - farben.keys()
        pruefe(not fehlend, f"Thema {name}: Farben fehlen: {sorted(fehlend)}")
        if fehlend:
            continue
        for vorne in ("schrift", "schrift-leise", "akzent"):
            for hinten in ("grund", "grund-erhoben"):
                wert = _kontrast(farben[vorne], farben[hinten])
                pruefe(wert >= 4.5,
                       f"Thema {name}: {vorne} auf {hinten} nur {wert:.2f}:1 (noetig 4.5)")
        # Der Knopf traegt die Grundfarbe als Schrift auf dem Akzent.
        wert = _kontrast(farben["grund"], farben["akzent"])
        pruefe(wert >= 4.5,
               f"Thema {name}: Knopftext auf Akzent nur {wert:.2f}:1 (noetig 4.5)")


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


def meldungen() -> list[pathlib.Path]:
    """Alle gebauten Newsmeldungen (Permalink /news/JJJJ/MM/TT/kuerzel/)."""
    return sorted(SITE.rglob("news/*/*/*/*/index.html"))


@pruefung
def das_newsarchiv_listet_jede_meldung() -> None:
    archiv = lies("news/index.html")
    pruefe(archiv != "", "news/index.html fehlt")
    pruefe(len(meldungen()) > 0, "es wurde keine einzige Meldung gebaut")
    for meldung in meldungen():
        adresse = "/" + meldung.parent.relative_to(SITE).as_posix() + "/"
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
        pruefe(False, f"feed.xml ist kein gueltiges XML: {fehler}")
        return
    eintraege = baum.findall("{http://www.w3.org/2005/Atom}entry")
    pruefe(len(eintraege) == len(meldungen()),
           f"feed.xml hat {len(eintraege)} Eintraege, gebaut wurden {len(meldungen())} Meldungen")


@pruefung
def jede_meldung_nennt_ihr_datum() -> None:
    for meldung in meldungen():
        text = meldung.read_text(encoding="utf-8")
        pruefe("<time" in text, f"{meldung.relative_to(SITE)}: kein <time>-Element")


@pruefung
def das_archiv_reicht_bis_2018_zurueck() -> None:
    jahre = {meldung.parts[-5] for meldung in meldungen()}
    for jahr in ("2018", "2019", "2020", "2021", "2022", "2023", "2024", "2026"):
        pruefe(jahr in jahre, f"im Archiv fehlt eine Meldung aus {jahr}")
    archiv = lies("news/index.html")
    for version in ("1.4.1", "1.4.8"):
        pruefe(version in archiv, f"das Archiv nennt Version {version} nicht")


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
