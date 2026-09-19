param([switch]$SkipBuild)
$ErrorActionPreference = 'Stop'
if (-not $SkipBuild) { & "$PSScriptRoot\build-windows.ps1" }
$projectRoot = Split-Path $PSScriptRoot -Parent
$linuxRoot = (& wsl -d Ubuntu -- wslpath -a ($projectRoot.Replace('\', '/')))
if ($LASTEXITCODE -ne 0 -or -not $linuxRoot) { throw 'Could not locate the project in Ubuntu.' }
$linuxRoot = ($linuxRoot -join '').Trim()
& wsl -d Ubuntu --cd $linuxRoot -- python3 scripts/run-tests.py
if ($LASTEXITCODE -ne 0) { throw 'Prototype integration tests failed.' }
