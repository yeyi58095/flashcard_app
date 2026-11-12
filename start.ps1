$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$appPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $appPython)) {
    $basePython = Get-Command python -ErrorAction SilentlyContinue |
        Where-Object Source -NotLike '*\Microsoft\WindowsApps\*' |
        Select-Object -ExpandProperty Source -First 1
    if (-not $basePython) {
        $basePython = Get-ChildItem -Path 'C:\Program Files\WindowsApps\OpenAI.CodexPrimaryRuntime*\dependencies\python\python.exe' -ErrorAction SilentlyContinue |
            Sort-Object FullName -Descending | Select-Object -ExpandProperty FullName -First 1
    }
    if (-not $basePython) { throw 'Python not found. Install Python 3.10+ and run this launcher again.' }
    & $basePython -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Could not create the Python environment.' }
}
& $appPython -c "import importlib.util, sys; sys.exit(0 if importlib.util.find_spec('streamlit') else 1)"
if ($LASTEXITCODE -ne 0) {
    & $appPython -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw 'Installation failed. Check your internet connection and retry.' }
}
& $appPython -m streamlit run avionics_flashcard_app.py --server.address 127.0.0.1 --browser.gatherUsageStats false
