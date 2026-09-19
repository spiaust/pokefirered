param([switch]$Compare)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
Push-Location $projectRoot
try {
    New-Item -ItemType Directory -Force -Path .local-tools | Out-Null
    $allInputs = @(git -c core.quotepath=false ls-files --cached --others --exclude-standard)
    if ($LASTEXITCODE -ne 0) { throw 'Could not list source files.' }
    $dirtyInputs = @(git -c core.quotepath=false diff --name-only HEAD)
    if ($LASTEXITCODE -ne 0) { throw 'Could not inspect changed source files.' }
    $dirtyInputs += @(git -c core.quotepath=false ls-files --others --exclude-standard)
    if ($LASTEXITCODE -ne 0) { throw 'Could not list new source files.' }
    $encoding = [Text.UTF8Encoding]::new($false)
    [IO.File]::WriteAllText((Join-Path $projectRoot '.local-tools/build-inputs.txt'), ($allInputs -join "`0") + "`0", $encoding)
    [IO.File]::WriteAllText((Join-Path $projectRoot '.local-tools/dirty-inputs.txt'), ($dirtyInputs -join "`0") + "`0", $encoding)
    & tar -cf .local-tools/source-inputs.tar --null -T .local-tools/build-inputs.txt
    if ($LASTEXITCODE -ne 0) { throw 'Could not package build inputs.' }
} finally {
    Pop-Location
}
$linuxRoot = (& wsl -d Ubuntu -- wslpath -a ($projectRoot.Replace('\', '/')))
if ($LASTEXITCODE -ne 0) { throw 'Could not locate the project in Ubuntu.' }
$linuxRoot = ($linuxRoot -join '').Trim()
if (-not $linuxRoot) { throw 'Ubuntu returned an empty project path.' }
$target = if ($Compare) { 'compare' } else { 'all' }
& wsl -d Ubuntu --cd $linuxRoot -- bash scripts/build-linux.sh $target --windows-manifests
if ($LASTEXITCODE -ne 0) { throw 'ROM build failed. See the errors above.' }
