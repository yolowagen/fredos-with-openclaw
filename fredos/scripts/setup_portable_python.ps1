$ErrorActionPreference = "Stop"

$PYTHON_URL = "https://github.com/indygreg/python-build-standalone/releases/download/20240224/cpython-3.11.8+20240224-x86_64-pc-windows-msvc-shared-install_only.tar.gz"
$DOWNLOAD_DEST = ".\cpython-3.11.8.tar.gz"
$PYTHON_DIR = ".\.python"

Write-Host "Downloading Portable Python 3.11.8..."
Invoke-WebRequest -Uri $PYTHON_URL -OutFile $DOWNLOAD_DEST

Write-Host "Extracting..."
# Windows 10+ includes tar
tar -xzf $DOWNLOAD_DEST

Write-Host "Moving to $PYTHON_DIR..."
if (Test-Path $PYTHON_DIR) {
    Remove-Item -Recurse -Force $PYTHON_DIR
}
# The tarball extracts to a folder named "python"
Rename-Item -Path "python" -NewName ".python"

Write-Host "Cleaning up tarball..."
Remove-Item $DOWNLOAD_DEST

$PYTHON_EXE = ".\.python\python.exe"

Write-Host "Verifying Python installation..."
& $PYTHON_EXE --version

Write-Host "Installing dependencies from requirements.txt..."
& $PYTHON_EXE -m pip install -r requirements.txt

Write-Host "Portable Python setup complete!"
Write-Host "You can now run FredOS using: .\.python\python.exe app\main.py"
Write-Host "Or just use '.\fredos.bat run'"
