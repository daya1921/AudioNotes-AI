$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $project

python -m PyInstaller --noconfirm --clean --distpath dist-updated AudioNotesAI.spec

Write-Host "Build complete: $project\dist\AudioNotesAI\AudioNotesAI.exe"
