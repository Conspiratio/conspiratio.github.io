#!/usr/bin/env python3
"""Prueft die gebaute Seite in _site/ gegen feste Zusagen.

Aufruf: python werkzeug/pruefe_ausgabe.py
Exit 0 = alles in Ordnung, Exit 1 = mindestens eine Zusage verletzt.

Dieses Skript tritt an die Stelle einer Testsuite, die es fuer eine statische
Seite sonst nicht gaebe. Jede Aufgabe des Implementierungsplans ergaenzt hier
ihre Zusagen, bevor sie sie erfuellt.
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
