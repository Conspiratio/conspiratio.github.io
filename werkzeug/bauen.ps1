<#
.SYNOPSIS
    Baut die Seite im Docker-Container - ohne lokale Ruby-Installation.
.DESCRIPTION
    Benutzt dasselbe Gemfile.lock wie CI, weil der Container Linux ist wie der Runner.
    Die Gems liegen in einem benannten Volume und ueberleben den Lauf.
.PARAMETER Vorschau
    Startet statt eines einmaligen Builds den Entwicklungsserver auf http://localhost:4000.
#>
param([switch]$Vorschau)

$ErrorActionPreference = "Stop"
$wurzel = Split-Path $PSScriptRoot -Parent

# --force_polling: Dateiaenderungen auf einem Windows-Bind-Mount erreichen den
# Container nicht als Ereignis, nur durch Nachsehen.
$befehl = if ($Vorschau) {
    "bundle install --quiet && bundle exec jekyll serve --host 0.0.0.0 --force_polling"
} else {
    "bundle install --quiet && bundle exec jekyll build"
}

docker run --rm `
    -v "${wurzel}:/srv" -w /srv `
    -v conspiratio-gems:/usr/local/bundle `
    -p 4000:4000 `
    ruby:3.3 bash -lc $befehl

if ($LASTEXITCODE -ne 0) { throw "Build fehlgeschlagen (Exit $LASTEXITCODE)" }
