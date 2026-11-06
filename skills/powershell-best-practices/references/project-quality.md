# Project Quality

PowerShell code should be:

- Clear.
- Typed.
- Pipeline-aware when useful.
- Object-output focused.
- Safe by default.
- Well documented.
- Easy to test.
- Easy to review.
- PSScriptAnalyzer clean.

Avoid:

- Aliases in scripts and reusable functions.
- `Write-Host` used as logging instead of an explicit logger.
- Untyped parameters.
- Silent catches.
- Global mutable state.
- Array building with `+=` inside loops.
- Formatting objects inside reusable functions.
- `New-Object` for simple objects or .NET types that support `::new()`.
- Backtick line continuations for long commands.
- Overuse of classes.
- Overuse of dynamic parameters.
- Concurrency without a clear reason.
- Large functions that mix unrelated responsibilities.

## Dependencies

Avoid external modules unless explicitly allowed by the user or already established by the repository. Prefer built-in cmdlets and .NET APIs when they are clear and maintainable.

For installing PowerShell modules, prefer `Install-PSResource` over `Install-Module`.

```powershell
# Prefer:
Install-PSResource -Name Pester -TrustRepository

# Avoid for new code:
Install-Module -Name Pester
```

`Install-PSResource` is the modern PowerShellGet v3 command surface and is generally faster in practice than the older `Install-Module` command. Local reports have shown the `PSResource` cmdlets running about twice as fast as the older `*Module` counterparts on PowerShell 7.4.5 across Windows and LinuxMint, but still measure in your own environment when install performance matters.

Use `RequiredModules` in the module manifest for modules required at import time. Use README/setup scripts or CI bootstrap steps for development-only tools such as Pester, PSScriptAnalyzer, and PlatyPS.

## Aliases And Shorthand

Do not use aliases in scripts, modules, or reusable functions. Write the full command and parameter names so code is easier to read, search, review, and analyze.

```powershell
# Avoid:
gci -Path $Path | ? { $_.Length -gt 1MB } | % { $_.FullName }

# Prefer:
Get-ChildItem -Path $Path | Where-Object { $PSItem.Length -gt 1MB } | ForEach-Object { $PSItem.FullName }
```

Prefer `$PSItem` over `$_` in script blocks. `$PSItem` is more explicit and easier to scan in code reviews.

## Where-Object Filters

Filter as close to the data source as possible. Prefer native filter parameters over broad retrieval followed by `Where-Object`.

```powershell
# Prefer:
Get-ChildItem -Path $ProfilePath -File -Filter 'ntuser*'

# Avoid when the provider can filter for you:
Get-ChildItem -Path $ProfilePath |
    Where-Object {
        -not $PSItem.PSIsContainer -and
        $PSItem.Name -like 'ntuser*'
    }
```

Use inline `Where-Object` for one or two simple conditions.

```powershell
Get-Process |
    Where-Object { $PSItem.CPU -gt 10 }
```

Spread longer filters across multiple lines. Use parentheses when mixing `-and` and `-or` so operator precedence is obvious.

```powershell
Get-Something |
    Where-Object {
        (
            $PSItem.Property -like 'a*' -or
            $PSItem.Property -like 'b*'
        ) -and
        $PSItem.Property -notlike 'c*' -and
        $PSItem.Property -notlike 'd*'
    }
```

When a filter remains dense, extract repeated or distracting work before the pipeline.

```powershell
$nameExclusionPattern = $whereNameFilter -join '|'

Get-ChildItem -Path $ProfilePath -File -Filter 'ntuser*' |
    Where-Object {
        $PSItem.Name -notmatch $nameExclusionPattern
    }
```

For many similar string conditions, build a regex pattern instead of writing many `-like` checks. Escape values when they may contain regex characters.

```powershell
$includeWords = @(
    'sometext'
    'someothertext'
    'moretext'
)

$matchPattern = ($includeWords | ForEach-Object {
    [regex]::Escape($PSItem)
}) -join '|'

Get-Something |
    Where-Object -Property Property -Match $matchPattern
```

## Formatting Long Commands

Avoid backtick line continuations for long commands. Backticks are fragile because trailing spaces break continuation and the resulting command is harder to edit.

```powershell
# Avoid:
New-PSDrive `
    -Name HKCC `
    -Root 'registry::HKEY_CURRENT_CONFIG' `
    -PSProvider Registry
```

Use splatting for long command calls. The splat variable must be a hashtable (`@{}`), not a script block (`{}`).

```powershell
$driveSplat = @{
    Name       = 'HKCU'
    Root       = 'registry::HKEY_CURRENT_USER'
    PSProvider = 'Registry'
}

New-PSDrive @driveSplat
```

## Tests And Validation

Run targeted validation when possible:

- Existing project tests for changed behavior.
- PSScriptAnalyzer for scripts and modules.
- Targeted manual invocation for advanced functions, including pipeline input when supported.
- `-WhatIf` checks for commands that implement `SupportsShouldProcess`.

If validation cannot be run, state that clearly in the final response.
