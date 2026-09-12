<#
.SYNOPSIS
    Legt eine neue Newsmeldung mit fertigem Kopf an.
.DESCRIPTION
    Bequemlichkeit, kein Muss: Eine Meldung ist eine Datei in _posts/ und laesst
    sich genauso gut von Hand oder in der Weboberflaeche von GitHub anlegen.
.EXAMPLE
    powershell -File werkzeug/neue-news.ps1 "Der Godot-Client ist da"
#>
param([Parameter(Mandatory)][string]$Titel)

$ErrorActionPreference = "Stop"
$wurzel = Split-Path $PSScriptRoot -Parent
$datum  = Get-Date -Format "yyyy-MM-dd"

# Kuerzel aus dem Titel: Umlaute aufloesen, alles andere zu Bindestrichen.
#
# Die Umlaute stehen bewusst als Codepunkte da, damit diese Datei reines ASCII
# bleibt. Steht ein echtes "ue" im Skript, liest Windows PowerShell 5.1 die
# BOM-lose UTF-8-Datei als ANSI, macht daraus zwei Zeichen - und die Ersetzung
# trifft nie zu. Genau so ist es beim ersten Versuch passiert: Aus "Uemlaut"
# wurde "mlaut", weil der Umlaut ungetroffen durch den naechsten Filter fiel.
$umlaute = [ordered]@{
    ([char]0x00E4) = "ae"   # a-Umlaut
    ([char]0x00F6) = "oe"   # o-Umlaut
    ([char]0x00FC) = "ue"   # u-Umlaut
    ([char]0x00DF) = "ss"   # scharfes s
}

$kuerzel = $Titel.ToLower()
foreach ($umlaut in $umlaute.GetEnumerator()) {
    # [string] erzwingt die (string, string)-Ueberladung; mit einem [char] als
    # erstem Argument verlangt .NET auch als Ersatz genau ein Zeichen.
    $kuerzel = $kuerzel.Replace([string]$umlaut.Key, $umlaut.Value)
}
$kuerzel = ($kuerzel -replace "[^a-z0-9]+", "-").Trim("-")
if (-not $kuerzel) { throw "Aus dem Titel laesst sich kein Kuerzel bilden." }

$datei = Join-Path $wurzel "_posts/$datum-$kuerzel.md"
if (Test-Path $datei) { throw "Gibt es schon: $datei" }

$inhalt = @"
---
title: "$Titel"
excerpt: ""
---

Werte Spieler,


"@

# UTF-8 ohne BOM: Jekyll erwartet die Datei so.
[System.IO.File]::WriteAllText($datei, $inhalt, [System.Text.UTF8Encoding]::new($false))

Write-Host "Angelegt: $datei"
