---
title: Bilder
permalink: /bilder/
redirect_from:
  - /bilder.html
---

Einige Eindrücke aus dem Spiel. Ein Klick öffnet das Bild in voller Größe.

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

<p class="hinweis">
  Weitere Ansichten kommen mit der ersten Fassung des neuen Clients hinzu.
</p>

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

Bewegte Bilder gibt es auf dem
[YouTube-Kanal](https://www.youtube.com/channel/UCBNIo4SB2c2GkgL7f_dMN_w).
