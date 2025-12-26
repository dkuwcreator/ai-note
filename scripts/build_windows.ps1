param(
    [string]$OutputName = 'ai_notepad'
)

# Override existing build
if (Test-Path ".\dist\$OutputName.exe") {
    Write-Host "Removing existing build: .\dist\$OutputName.exe"
    Remove-Item ".\dist\$OutputName.exe" -Force
}

python -m pip install --upgrade pip
pip install pyinstaller
pyinstaller --noconfirm --clean --onefile -n $OutputName -p . desktop_app/main.py
