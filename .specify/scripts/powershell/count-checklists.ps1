#!/usr/bin/env pwsh

# Checklist Item Counter Script (PowerShell)
#
# This script counts checklist items in all checklist files within a feature directory.
# It provides a safe, reliable alternative to inline PowerShell commands that suffer
# from quoting/escaping issues when passed through shell/JSON/host layers.
#
# Usage: ./count-checklists.ps1 [-FeatureDir <path>] [-Json]
#
# OPTIONS:
#   -FeatureDir <path>  Path to feature directory (default: auto-detect from current branch)
#   -Json               Output in JSON format
#   -Help, -h           Show help message

[CmdletBinding()]
param(
    [string]$FeatureDir,
    [switch]$Json,
    [switch]$Help
)

$ErrorActionPreference = 'Stop'

# Show help if requested
if ($Help) {
    Write-Output @"
Usage: count-checklists.ps1 [OPTIONS]

Count checklist items across all checklist files in a feature directory.

OPTIONS:
  -FeatureDir <path>  Path to feature directory (default: auto-detect from current branch)
  -Json               Output in JSON format
  -Help, -h           Show this help message

EXAMPLES:
  # Count checklists in current feature (auto-detect)
  .\count-checklists.ps1

  # Count checklists with JSON output
  .\count-checklists.ps1 -Json

  # Count checklists in specific feature directory
  .\count-checklists.ps1 -FeatureDir "C:\repo\specs\001-my-feature"

OUTPUT (Text format):
  | Checklist   | Total | Completed | Incomplete | Status |
  |-------------|-------|-----------|------------|--------|
  | ux.md       | 12    | 12        | 0          | ✓ PASS |
  | test.md     | 8     | 5         | 3          | ✗ FAIL |

OUTPUT (JSON format):
  {
    "checklists": [
      {"name": "ux.md", "total": 12, "completed": 12, "incomplete": 0, "status": "PASS"},
      {"name": "test.md", "total": 8, "completed": 5, "incomplete": 3, "status": "FAIL"}
    ],
    "overall_status": "FAIL",
    "total_incomplete": 3
  }

"@
    exit 0
}

# Source common functions if we need to auto-detect feature directory
if (-not $FeatureDir) {
    . "$PSScriptRoot/common.ps1"
    $paths = Get-FeaturePathsEnv
    $FeatureDir = $paths.FEATURE_DIR
}

# Validate and normalize path
if (-not (Test-Path $FeatureDir -PathType Container)) {
    Write-Output "ERROR: Feature directory not found: $FeatureDir"
    exit 1
}
$FeatureDir = (Resolve-Path $FeatureDir).Path

# Check if checklists directory exists
$checklistsDir = Join-Path $FeatureDir "checklists"
if (-not (Test-Path $checklistsDir -PathType Container)) {
    if ($Json) {
        [PSCustomObject]@{
            checklists = @()
            overall_status = "NO_CHECKLISTS"
            total_incomplete = 0
        } | ConvertTo-Json -Compress
    } else {
        Write-Output "No checklists directory found at: $checklistsDir"
        Write-Output "Status: NO_CHECKLISTS"
    }
    exit 0
}

# Get all markdown files in checklists directory
$checklistFiles = Get-ChildItem -Path $checklistsDir -Filter "*.md" -File -ErrorAction SilentlyContinue

if ($checklistFiles.Count -eq 0) {
    if ($Json) {
        [PSCustomObject]@{
            checklists = @()
            overall_status = "NO_CHECKLISTS"
            total_incomplete = 0
        } | ConvertTo-Json -Compress
    } else {
        Write-Output "No checklist files found in: $checklistsDir"
        Write-Output "Status: NO_CHECKLISTS"
    }
    exit 0
}

# Process each checklist file
$results = @()
$totalIncomplete = 0

foreach ($file in $checklistFiles) {
    $content = Get-Content -Path $file.FullName -Raw -ErrorAction SilentlyContinue
    
    if (-not $content) {
        continue
    }
    
    # Count total items: lines matching "- [ ]" or "- [X]" or "- [x]" (with optional leading whitespace)
    $totalMatches = [regex]::Matches($content, '(?m)^\s*- \[([ Xx])\]')
    $totalCount = $totalMatches.Count
    
    # Count completed items: lines matching "- [X]" or "- [x]" (with optional leading whitespace)
    $completedMatches = [regex]::Matches($content, '(?m)^\s*- \[[Xx]\]')
    $completedCount = $completedMatches.Count
    
    # Calculate incomplete
    $incompleteCount = $totalCount - $completedCount
    
    # Determine status
    $status = if ($incompleteCount -eq 0) { "PASS" } else { "FAIL" }
    
    # Add to total incomplete count
    $totalIncomplete += $incompleteCount
    
    # Store result
    $results += [PSCustomObject]@{
        name = $file.Name
        total = $totalCount
        completed = $completedCount
        incomplete = $incompleteCount
        status = $status
    }
}

# Calculate overall status
$overallStatus = if ($totalIncomplete -eq 0) { "PASS" } else { "FAIL" }

# Output results
if ($Json) {
    # JSON output
    [PSCustomObject]@{
        checklists = $results
        overall_status = $overallStatus
        total_incomplete = $totalIncomplete
    } | ConvertTo-Json -Compress
} else {
    # Text output - table format
    Write-Output ""
    Write-Output "Checklist Status Summary:"
    Write-Output ""
    
    # Calculate column widths
    $maxNameWidth = ($results | ForEach-Object { $_.name.Length } | Measure-Object -Maximum).Maximum
    $nameWidth = [Math]::Max($maxNameWidth, 10) + 2
    
    # Header
    $header = "| {0,-$nameWidth} | {1,5} | {2,9} | {3,10} | {4,6} |" -f "Checklist", "Total", "Completed", "Incomplete", "Status"
    $separator = "|" + ("-" * ($nameWidth + 2)) + "|" + ("-" * 7) + "|" + ("-" * 11) + "|" + ("-" * 12) + "|" + ("-" * 8) + "|"
    
    Write-Output $separator
    Write-Output $header
    Write-Output $separator
    
    # Data rows
    foreach ($result in $results) {
        $statusIcon = if ($result.status -eq "PASS") { "✓" } else { "✗" }
        $row = "| {0,-$nameWidth} | {1,5} | {2,9} | {3,10} | {4} {5,-4} |" -f `
            $result.name, `
            $result.total, `
            $result.completed, `
            $result.incomplete, `
            $statusIcon, `
            $result.status
        Write-Output $row
    }
    
    Write-Output $separator
    Write-Output ""
    
    # Overall status
    if ($overallStatus -eq "PASS") {
        Write-Output "Overall Status: ✓ PASS - All checklists complete"
    } else {
        Write-Output "Overall Status: ✗ FAIL - $totalIncomplete incomplete item(s) found"
    }
    Write-Output ""
}

# Exit with appropriate code
if ($overallStatus -eq "PASS") {
    exit 0
} else {
    exit 1
}
