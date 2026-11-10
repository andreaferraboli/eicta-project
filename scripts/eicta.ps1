# Thin PowerShell wrapper: .\scripts\eicta.ps1 <command> [args]
# Works from any directory and with paths containing spaces.
$ErrorActionPreference = "Stop"
$script = Join-Path $PSScriptRoot "eicta.py"
$python = if (Get-Command py -ErrorAction SilentlyContinue) { "py" } else { "python" }
if ($python -eq "py") { & py -3 $script @args } else { & python $script @args }
exit $LASTEXITCODE
