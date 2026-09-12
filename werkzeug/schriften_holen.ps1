<#
.SYNOPSIS
    Holt die drei Schriftfamilien einmalig nach assets/schriften/ als woff2.
.DESCRIPTION
    Alle drei stehen unter der SIL Open Font License und duerfen mit ausgeliefert
    werden. Ausgeliefert wird von unserem Server, nicht von Google - deshalb
    dieses Skript und nicht ein <link> auf fonts.googleapis.com.

    Google gibt je Anfrage mehrere @font-face zurueck, eines je Zeichensatz-
    Ausschnitt. Genommen wird das mit U+0000-00FF: Es traegt ASCII, die deutschen
    Umlaute und die typografischen Anfuehrungszeichen - mehr braucht die Seite nicht.

    Einmalig auszufuehren. Die Dateien liegen danach im Repo.
#>
$ErrorActionPreference = "Stop"
$wurzel = Split-Path $PSScriptRoot -Parent
$ziel = Join-Path $wurzel "assets\schriften"
New-Item -ItemType Directory -Force $ziel | Out-Null

# Ein moderner User-Agent ist noetig, sonst liefert Google ttf statt woff2.
$browser = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

$schriften = @(
    @{ anfrage = "Grenze+Gotisch:wght@400";        datei = "grenze-gotisch-400" },
    @{ anfrage = "EB+Garamond:ital,wght@0,400";    datei = "eb-garamond-400" },
    @{ anfrage = "EB+Garamond:ital,wght@1,400";    datei = "eb-garamond-400-kursiv" },
    @{ anfrage = "EB+Garamond:ital,wght@0,600";    datei = "eb-garamond-600" },
    @{ anfrage = "Atkinson+Hyperlegible:wght@400"; datei = "atkinson-hyperlegible-400" },
    @{ anfrage = "Atkinson+Hyperlegible:wght@700"; datei = "atkinson-hyperlegible-700" }
)

foreach ($schrift in $schriften) {
    $url = "https://fonts.googleapis.com/css2?family=$($schrift.anfrage)&display=swap"
    $css = (Invoke-WebRequest -Uri $url -UserAgent $browser -UseBasicParsing).Content

    # @font-face-Bloecke trennen und den mit dem lateinischen Grundausschnitt nehmen.
    # Das @() ist noetig: Bei genau einem Treffer waere $bloecke eine Zeichenkette
    # und $bloecke[0] ihr erstes Zeichen.
    $bloecke = @($css -split "@font-face" | Where-Object { $_ -match "U\+0000-00FF" })
    if ($bloecke.Count -eq 0) { throw "Kein lateinischer Block fuer $($schrift.anfrage)" }

    if ($bloecke[0] -notmatch "url\((https://[^)]+\.woff2)\)") {
        throw "Keine woff2-Adresse fuer $($schrift.anfrage)"
    }
    $quelle = $Matches[1]

    $zieldatei = Join-Path $ziel "$($schrift.datei).woff2"
    Invoke-WebRequest -Uri $quelle -OutFile $zieldatei -UseBasicParsing
    $groesse = [math]::Round((Get-Item $zieldatei).Length / 1KB, 1)
    Write-Host "$($schrift.datei).woff2  ($groesse KB)"
}

# Die Lizenztexte gehoeren dazu.
$lizenzen = @{
    "OFL-grenze-gotisch.txt"        = "https://raw.githubusercontent.com/google/fonts/main/ofl/grenzegotisch/OFL.txt"
    "OFL-eb-garamond.txt"           = "https://raw.githubusercontent.com/google/fonts/main/ofl/ebgaramond/OFL.txt"
    "OFL-atkinson-hyperlegible.txt" = "https://raw.githubusercontent.com/google/fonts/main/ofl/atkinsonhyperlegible/OFL.txt"
}
foreach ($lizenz in $lizenzen.GetEnumerator()) {
    Invoke-WebRequest -Uri $lizenz.Value -OutFile (Join-Path $ziel $lizenz.Key) -UseBasicParsing
    Write-Host $lizenz.Key
}
