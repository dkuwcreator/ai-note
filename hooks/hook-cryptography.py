from PyInstaller.utils.hooks import collect_all

# cryptography includes native extensions and indirect imports that static
# analysis can miss; collecting the whole package is the most reliable.
datas, binaries, hiddenimports = collect_all("cryptography")
