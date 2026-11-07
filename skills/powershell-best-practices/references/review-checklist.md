# PowerShell Review Checklist

When reviewing PowerShell, lead with concrete risks and specific fixes. Use exact file and line references when possible.

Prioritize:

- Missing `SupportsShouldProcess` on modifying commands.
- Unsafe deletes, writes, updates, sends, service changes, or broad state changes.
- Missing `-ErrorAction Stop` inside `try` blocks when cmdlet errors must be caught.
- Missing generic catch blocks.
- Generic catch blocks that do not use `$PSCmdlet.ThrowTerminatingError($PSItem)`.
- Untyped parameters.
- Missing validation for important inputs.
- Credential handling that uses plaintext secrets, untyped credential parameters, or passes empty credentials instead of conditional splatting.
- Legacy WMI cmdlets used where CIM cmdlets and `CimSession` should be used.
- Poor pipeline behavior.
- Aliases or `$_` used in scripts or reusable functions instead of full command names and `$PSItem`.
- `New-Object` used where `[pscustomobject]@{}` or `[Type]::new()` is clearer.
- Outputting formatted strings instead of objects.
- A script or function that builds a well-formed result (its own or a helper's return value) but only logs/prints it and declares `.OUTPUTS None` instead of returning it. See [objects-and-modeling.md](objects-and-modeling.md#scripts-and-automation-entry-points).
- Native-command or cmdlet calls left uncaptured (not assigned, piped, or sent to `Out-Null`/`$null =`) in a script that also has real pipeline output, risking accidental objects mixed into that output.
- Any array building with `+=` inside loops.
- Backtick line continuation where splatting would be clearer and safer.
- Right-side filtering after broad data gathering when source-side filtering is available.
- Collection choices that do not match behavior, such as list scans for repeated key lookups or sorted types when sorting only at output would work.
- Use of `Write-Host` as logging, or console output that is not explicitly optional.
- `Install-Module` used in new setup or CI code instead of `Install-PSResource`.
- Missing comment-based help.
- Module structure that mixes public/private functions, lacks an explicit manifest for reusable modules, or exports private helpers.
- Pester tests that do not import the module like real users, miss public behavior, or depend on machine-specific state.
- Overly complex abstractions.
- Uncontrolled concurrency.
- Remote sessions or jobs created by the function without cleanup.
- `Start-Job` used where `Start-ThreadJob`, `ForEach-Object -Parallel`, or a normal loop would fit the PowerShell 7.6 baseline better.
- Code likely to fail PSScriptAnalyzer.
- Missing tests for changed behavior.
- PowerShell GitHub Actions do not check formatting, PSScriptAnalyzer, Pester,
  and generated documentation as required by the repository, or do not follow
  `github-actions-best-practices` for workflow security and dependencies.

If no issues are found, say so directly and mention any validation that was not run.

## Review Response Shape

1. Findings first, ordered by severity.
2. Open questions or assumptions.
3. Brief change summary only when useful.
4. Validation or test gaps.
