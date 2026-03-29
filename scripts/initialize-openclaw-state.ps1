param(
  [Parameter(Mandatory = $true)]
  [string]$StateDir
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path $PSScriptRoot -Parent
$templateRoot = Join-Path $repoRoot "openclaw-state-template"

New-Item -ItemType Directory -Force -Path $StateDir | Out-Null
Copy-Item "$templateRoot\\*" $StateDir -Recurse -Force

Write-Host "State template copied to $StateDir"
Write-Host "Next: edit openclaw.template.json into openclaw.json and replace placeholders."
