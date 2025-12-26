# Scripts

This directory contains utility scripts for Spec Kit workflows.

## Directory Structure

- `bash/` - Bash scripts for Unix-like systems
- `powershell/` - PowerShell scripts for cross-platform use

## Checklist Counting Scripts

The checklist counting scripts provide a durable solution for counting completed and incomplete checklist items across multiple checklist files.

### Purpose

When implementing features using the `/speckit.implement` command, agents need to check the status of all checklists before proceeding. These scripts eliminate PowerShell quoting/escaping issues that occur with complex inline commands.

### Available Scripts

#### Bash Version

**Location:** `scripts/bash/count-checklists.sh`

**Usage:**
```bash
# Count checklists in current feature (auto-detect)
./scripts/bash/count-checklists.sh

# Count checklists with JSON output
./scripts/bash/count-checklists.sh --json

# Count checklists in specific feature directory
./scripts/bash/count-checklists.sh --feature-dir "/path/to/specs/001-feature-name"
```

#### PowerShell Version

**Location:** `scripts/powershell/count-checklists.ps1`

**Usage:**
```powershell
# Count checklists in current feature (auto-detect)
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/powershell/count-checklists.ps1

# Count checklists with JSON output
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/powershell/count-checklists.ps1 -Json

# Count checklists in specific feature directory
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/powershell/count-checklists.ps1 -FeatureDir "C:\repo\specs\001-feature-name"
```

### Output Formats

#### Text Output (Default)

```text
Checklist Status Summary:

|---------------|-------|-----------|------------|--------|
| Checklist     | Total | Completed | Incomplete | Status |
|---------------|-------|-----------|------------|--------|
| security.md   |     4 |         4 |          0 | ✓ PASS |
| ux.md         |     8 |         6 |          2 | ✗ FAIL |
|---------------|-------|-----------|------------|--------|

Overall Status: ✗ FAIL - 2 incomplete item(s) found
```

#### JSON Output

```json
{
  "checklists": [
    {"name": "security.md", "total": 4, "completed": 4, "incomplete": 0, "status": "PASS"},
    {"name": "ux.md", "total": 8, "completed": 6, "incomplete": 2, "status": "FAIL"}
  ],
  "overall_status": "FAIL",
  "total_incomplete": 2
}
```

### Exit Codes

- `0` - All checklists passed OR no checklists found
- `1` - One or more checklists have incomplete items

### Technical Details

#### Why Use `-File` Instead of Inline Commands?

The previous approach used inline PowerShell commands with complex `foreach` loops. These suffered from:

1. **Quoting Issues**: Shell/JSON/host-layer quoting loss when commands pass through multiple wrappers
2. **Variable Interpolation**: `$` characters being interpolated by the host shell before PowerShell sees them
3. **Parse Errors**: "Missing variable name after foreach" and similar errors due to escaping problems

The `-File` approach solves these issues by:

- Avoiding all intermediate escaping/quoting layers
- Making the code auditable and maintainable
- Providing consistent behavior across different shells and environments
- Offering proper error handling and help documentation

#### Alternative Approaches Considered

1. **-EncodedCommand**: Base64-encode the script to bypass escaping
   - ✅ Robust against quoting issues
   - ❌ Not auditable or readable
   - ❌ More complex to maintain

2. **Simplified inline pipeline**: Use simpler PowerShell pipelines without `foreach`
   - ✅ Quick fix
   - ❌ Still susceptible to some quoting issues
   - ❌ Less maintainable

3. **-File with dedicated script** (CHOSEN):
   - ✅ Safe and auditable
   - ✅ Easy to maintain and test
   - ✅ Proper error handling
   - ✅ Built-in help documentation

## Other Scripts

### Prerequisite Checking

- `bash/check-prerequisites.sh` - Check if feature directory and required files exist
- `powershell/check-prerequisites.ps1` - PowerShell version of prerequisite checking

### Feature Management

- `bash/create-new-feature.sh` - Create a new feature directory structure
- `powershell/create-new-feature.ps1` - PowerShell version of feature creation

### Context Management

- `bash/update-agent-context.sh` - Update agent context files
- `powershell/update-agent-context.ps1` - PowerShell version of context updates

For detailed usage of each script, run the script with `--help` (bash) or `-Help` (PowerShell).
