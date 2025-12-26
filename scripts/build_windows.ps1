param(
    [string]$OutputName = 'ai_notepad'
)

$ErrorActionPreference = 'Stop'

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $RepoRoot

try {
    $VenvDir = Join-Path $RepoRoot '.venv'
    $VenvPython = Join-Path $VenvDir 'Scripts\python.exe'
    $VenvUv = Join-Path $VenvDir 'Scripts\uv.exe'

    # 1) Ensure .venv exists.
    if (-not (Test-Path $VenvPython)) {
        Write-Host "Creating venv at $VenvDir"
        python -m venv $VenvDir
    }

    # 2) Ensure uv exists in the venv (so we always use the same environment).
    if (-not (Test-Path $VenvUv)) {
        Write-Host "Installing uv into .venv"
        & $VenvPython -m pip install --upgrade pip
        & $VenvPython -m pip install uv
    }

    # 3) Install app + tooling deps into the venv.
    Write-Host "Installing dependencies into .venv"
    & $VenvUv pip install -r requirements.txt
    & $VenvUv pip install pyinstaller

    # 4) Remove any prior exe with this name.
    $DistExe = Join-Path $RepoRoot ("dist\\{0}.exe" -f $OutputName)
    if (Test-Path $DistExe) {
        Write-Host "Removing existing build: $DistExe"
        Remove-Item $DistExe -Force
    }

    # 5) Build using the spec (so hooks/hidden imports apply).
    $env:AI_NOTEPAD_EXE_NAME = $OutputName
    Write-Host "Building $OutputName.exe via PyInstaller spec"
    & $VenvPython -m PyInstaller --noconfirm --clean ai_notepad.spec
}
finally {
    Pop-Location
}
