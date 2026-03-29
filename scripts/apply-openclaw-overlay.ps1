param(
  [Parameter(Mandatory = $true)]
  [string]$OpenClawRoot
)

$ErrorActionPreference = "Stop"

$overlayRoot = Split-Path $PSScriptRoot -Parent
$overlayRoot = Join-Path $overlayRoot "openclaw-overlay"

if (-not (Test-Path $OpenClawRoot)) {
  throw "OpenClaw root not found: $OpenClawRoot"
}

Write-Host "Applying OpenClaw overlay from $overlayRoot"
Copy-Item "$overlayRoot\\*" $OpenClawRoot -Recurse -Force
Write-Host "Overlay applied."
