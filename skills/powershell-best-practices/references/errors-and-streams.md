# Errors And Streams

## Error Handling

Use explicit `try`/`catch` blocks around operations that can fail when handling adds context, cleanup, controlled recovery, or clearer termination.

Every `try`/`catch` chain must end with a generic catch:

```powershell
catch {
    $PSCmdlet.ThrowTerminatingError($PSItem)
}
```

Use `-ErrorAction Stop` when calling cmdlets inside a `try` block if the error must be caught.

```powershell
try {
    $content = Get-Content -Path $Path -ErrorAction Stop
}
catch [System.UnauthorizedAccessException] {
    Write-Error "Access denied for path '$Path'."
}
catch [System.IO.FileNotFoundException] {
    Write-Error "File not found: '$Path'."
}
catch {
    $PSCmdlet.ThrowTerminatingError($PSItem)
}
```

Do not silently swallow errors.

```powershell
# Avoid:
try {
    Remove-Item -Path $Path
}
catch {
}

# Prefer:
try {
    Remove-Item -Path $Path -Force -ErrorAction Stop
}
catch {
    $PSCmdlet.ThrowTerminatingError($PSItem)
}
```

## Streams

Use the appropriate PowerShell stream.

| Stream | Use for |
| --- | --- |
| `Write-Verbose` | User-requested operational details, not persistent logs. |
| `Write-Debug` | Deeper troubleshooting details for developers, not persistent logs. |
| `Write-Warning` | Recoverable problems or risky conditions. |
| `Write-Error` | Non-terminating errors. |
| `$PSCmdlet.ThrowTerminatingError()` | Terminating errors from advanced functions. |
| Output stream | Actual command output objects. |

## Verbose Output

Use `Write-Verbose` for optional operational detail that helps a caller understand what the command is doing when they pass `-Verbose`.

Good verbose messages describe meaningful work or decisions:

```powershell
Write-Verbose "Resolving path '$Path'."
Write-Verbose "Found $($items.Count) items to process."
Write-Verbose "Skipping disabled item '$Name'."
```

Rules:

- Use `[CmdletBinding()]` so `-Verbose` is available automatically.
- Do not use `Write-Verbose` for normal output. Output objects to the pipeline instead.
- Do not use `Write-Verbose` as persistent logging. Use a file logger when logs must be retained.
- Avoid noisy verbose messages inside very large loops unless they are gated, summarized, or genuinely useful for troubleshooting.
- Include useful context, but do not leak secrets, tokens, credentials, or sensitive payloads.

Do not use output text or `Write-Host` as logging. Output text pollutes the pipeline, and `Write-Host` is host display, not a durable logging mechanism.

```powershell
Write-Verbose "Checking path '$Path'."
Write-Debug "Resolved provider path: $resolvedPath"

[pscustomobject]@{
    Path   = $Path
    Exists = Test-Path -Path $Path
}
```

When durable logs are required, use a dedicated file logger or project logging helper. See [logging.md](logging.md).
