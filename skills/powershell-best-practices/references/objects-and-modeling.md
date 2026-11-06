# Objects And Modeling

## Output Behavior

Reusable functions should output objects.

```powershell
[pscustomobject]@{
    Name = $Name
    Path = $Path
}
```

Avoid formatted strings as primary output.

```powershell
# Avoid:
"Name: $Name Path: $Path"
```

Formatting should happen at the edge, not inside the core function. Use `[OutputType()]` for public functions when the output type is known.

## Scripts And Automation Entry Points

The "output objects" rule is not limited to reusable functions. A top-level script that performs
a real action (create, install, deploy, back up, restore, or similar) and has a nameable result should
return that result as an object, in addition to whatever exit code or log entry it already
produces. Do not settle for `.OUTPUTS None` just because the script's purpose is "do a thing" and
not "compute a value" - most scripts that do something worth logging also produce something worth
returning.

Watch specifically for this anti-pattern: a script calls a helper (a module function, a local
function, a native command) and captures a well-formed result into a variable, then only uses
that variable to build a log line or a console message, and never returns it.

```powershell
# Avoid: the object already exists, but only its text representation survives.
$result = New-Resource -Name $Name
Write-Log -Message "Resource $($result.Status): $($result.Name)" -Level Success
# ...script ends here, $result is discarded.
```

```powershell
# Prefer: log for humans, return the object for callers/automation.
$result = New-Resource -Name $Name
Write-Log -Message "Resource $($result.Status): $($result.Name)" -Level Success
[pscustomobject]@{
    Name   = $result.Name
    Status = $result.Status
}
```

When a script is genuinely fire-and-forget (for example, launching an interactive GUI with no
verifiable outcome to report), it is fine to keep `.OUTPUTS None` - but that should be a deliberate
conclusion reached by checking what the script already knows at its success point, not the
default.

Rules for adding result output to an existing script:

- Emit the object only on the real success path. Respect existing `ShouldProcess`/`-WhatIf`
  gating: a declined confirmation or a `-WhatIf` run should not emit a result object claiming
  something happened.
- If a script is invoked by unattended automation (a scheduled task, a CI job, a monitoring agent)
  that relies on its exit code, add the object output alongside the exit code, not instead of it. Do
  not change the exit-code contract to add object output.
- If a mutable collection (a `List[T]`) is part of the result, convert it to an array (`.ToArray()`)
  before putting it on an output object so callers get a snapshot instead of a live reference to
  the script's internal state.
- Before adding the first real object output to a script, audit the rest of the script for
  uncaptured native-command or cmdlet output (any external executable, database client, or cmdlet
  call whose return value is not assigned, piped, or redirected to `Out-Null`/`$null =`). Once a script
  has a real object flowing through its output stream, any of these accidental leftovers will mix
  into it. This is a good time to fix them, not just avoid new ones.
- A script that runs a series of independent checks (a test/validation script) should prefer
  emitting one result object per check over a single pass/fail summary, mirroring how Pester
  reports results - this is more useful to a caller than a single boolean or count.

## Select-Object Projections

Inline a single calculated property when it remains readable.

```powershell
Get-Process |
    Select-Object -Property Name, @{
        Name       = 'MemoryMB'
        Expression = { [math]::Round($PSItem.WorkingSet64 / 1MB, 2) }
    }
```

When using multiple calculated properties, define them as a named array before the pipeline so the command stays readable.

```powershell
$properties = @(
    @{
        Name       = 'User'
        Expression = { $PSItem.Properties[0].Value }
    }
    @{
        Name       = 'LockedBy'
        Expression = { $PSItem.Properties[1].Value }
    }
    @{
        Name       = 'TimeStamp'
        Expression = { $PSItem.TimeCreated }
    }
    @{
        Name       = 'DCName'
        Expression = { $PSItem.Properties[4].Value }
    }
)

Get-WinEvent -FilterHashtable @{
    LogName = 'Security'
    ID      = 4740
} | Select-Object -Property $properties
```

Use `Name` consistently for calculated properties. Prefer property names without spaces when output may be exported, filtered, grouped, or consumed by later commands.

## Objects

Prefer `[pscustomobject]` for simple structured output.

```powershell
[pscustomobject]@{
    Name      = $Name
    Path      = $Path
    Exists    = Test-Path -Path $Path
    CheckedAt = Get-Date
}
```

Avoid `New-Object PSObject -Property` for simple objects. It is slower, noisier, and less idiomatic in modern PowerShell.

```powershell
# Avoid:
New-Object PSObject -Property @{
    Name   = $Name
    Path   = $Path
    Exists = Test-Path -Path $Path
}

# Prefer:
[pscustomobject]@{
    Name   = $Name
    Path   = $Path
    Exists = Test-Path -Path $Path
}
```

For .NET objects, prefer static `::new()` constructors when available.

```powershell
# Avoid:
$timer = New-Object Timers.Timer

# Prefer:
$timer = [System.Timers.Timer]::new()
```

Use classes only when they provide clear value:

- Shared behavior through methods.
- Stronger modeling across a larger module.
- Repeated construction of the same structured object.
- Validation or encapsulation that would otherwise be scattered.
- Clear domain modeling.

Avoid classes when a `[pscustomobject]` is enough.

```powershell
class InventoryItem {
    [string]$Name
    [string]$Path
    [bool]$Exists

    InventoryItem([string]$name, [string]$path, [bool]$exists) {
        $this.Name = $name
        $this.Path = $path
        $this.Exists = $exists
    }
}
```

## Naming

Use approved PowerShell verbs for public commands. Run `Get-Verb | Sort-Object Verb` to list approved verbs. Keep parameter and variable names descriptive. Avoid single-character names except in narrow mathematical expressions or conventional script blocks where the meaning is immediate. See [module-design.md](module-design.md) for module and command naming conventions.
