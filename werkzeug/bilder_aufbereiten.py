#!/usr/bin/env python3
"""Bereitet Rohbilder fuer die Galerie auf: skalieren, WebP, Masse nach _data/bilder.yml.

Quellen (beide nicht im Repo bzw. nicht veroeffentlicht):
  rohbilder/godot/*.png       Aufnahmen aus dem E2E-Treiber des Godot-Clients,
                              entnommen aus Conspiratio.Godot/docs/ansichten/ und
                              nach Motiv umbenannt. Der Ordner ist in .gitignore.
  quellen/screenshots/*.jpg   Die alten WinForms-Aufnahmen der bisherigen Seite.

Veroeffentlicht werden nur die fertigen WebP unter assets/bilder/; quellen/
steht in der exclude-Liste von _config.yml.

Aufruf: python werkzeug/bilder_aufbereiten.py

Ein Motiv ohne Alternativtext wird absichtlich NICHT aufbereitet: Ein Bild ohne
Alternativtext hat auf der Seite nichts verloren, und das Pruefskript wuerde es
ohnehin bemaengeln.
"""
from __future__ import annotations

import pathlib

from PIL import Image

WURZEL = pathlib.Path(__file__).resolve().parent.parent
ZIEL = WURZEL / "assets" / "bilder"
BREITE = 1000

GODOT = {
    "kontor": "Das Kontor: der Schreibtisch, von dem aus alle Bereiche eines Zuges angesteuert werden",
    "weltkarte": "Die Weltkarte mit den vierzehn Städten zwischen Wattern, Meadowvalley und Redcoast",
    "schreibstube": "Die Schreibstube: Kreditbuch, Gesetze und Akten auf dem Tisch",
    "hinterzimmer": "Das Hinterzimmer: Gift, Würfel, eine Bombe und ein versiegelter Brief im Kerzenlicht",
    "gesetze": "Die Strafgesetze einer Stadt - Spionage verboten, Anschwärzen erlaubt",
}

WINFORMS = {
    "Conspiratio_Kontor": "Das Kontor im bisherigen Client",
    "Conspiratio_Schreibstube_Gesetze": "Die Gesetzestafel in der Schreibstube",
    "Conspiratio_Amtsuebersicht": "Die Ämterübersicht mit Amtsinhabern und Bewerbungen",
    "Conspiratio_Beziehungen_Kontrahenten": "Die Beziehungen zu den Kontrahenten",
    "Conspiratio_Kirche": "Die Kirche",
    "Conspiratio_Produktion": "Die Produktion einer Werkstätte",
    "Conspiratio_Stadtinfos": "Die Stadtinformationen mit Lagerbeständen und Preisen",
    "Conspiratio_Zollburg_verwalten": "Eine Zollburg verwalten",
}


def bereite_auf(quelle: pathlib.Path, zielname: str, breite: int = BREITE) -> tuple[int, int]:
    """Skaliert auf die Zielbreite, schreibt WebP, gibt die Zielmasse zurueck."""
    with Image.open(quelle) as bild:
        bild = bild.convert("RGB")
        hoehe = round(bild.height * breite / bild.width)
        bild = bild.resize((breite, hoehe), Image.LANCZOS)
        ZIEL.mkdir(parents=True, exist_ok=True)
        bild.save(ZIEL / f"{zielname}.webp", "WEBP", quality=82, method=6)
    return breite, hoehe


def main() -> int:
    eintraege: list[str] = []
    fehlend: list[str] = []

    quellen = (
        ("godot", WURZEL / "rohbilder" / "godot", ".png", GODOT),
        ("winforms", WURZEL / "quellen" / "screenshots", ".jpg", WINFORMS),
    )

    for client, verzeichnis, endung, motive in quellen:
        for motiv, alt in motive.items():
            quelle = verzeichnis / f"{motiv}{endung}"
            if not quelle.is_file():
                fehlend.append(str(quelle.relative_to(WURZEL)))
                continue
            kurz = motiv.lower().replace("conspiratio_", "").replace("_", "-")
            zielname = f"{client}-{kurz}"
            breite, hoehe = bereite_auf(quelle, zielname)
            eintraege.append(
                f"- datei: {zielname}.webp\n"
                f'  alt: "{alt}"\n'
                f"  client: {client}\n"
                f"  breite: {breite}\n"
                f"  hoehe: {hoehe}\n"
            )

    kopf = (
        "# Erzeugt von werkzeug/bilder_aufbereiten.py - nicht von Hand pflegen.\n"
        "# Alternativtexte stehen in jenem Skript.\n\n"
    )
    ziel_yaml = WURZEL / "_data" / "bilder.yml"
    ziel_yaml.parent.mkdir(parents=True, exist_ok=True)
    ziel_yaml.write_text(kopf + "\n".join(eintraege), encoding="utf-8", newline="\n")
    print(f"{len(eintraege)} Bild(er) aufbereitet -> {ziel_yaml.relative_to(WURZEL)}")

    if fehlend:
        print("\nNicht gefunden (uebersprungen):")
        for pfad in fehlend:
            print(f"  - {pfad}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
