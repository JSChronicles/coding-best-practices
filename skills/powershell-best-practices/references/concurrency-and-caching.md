# Concurrency And Caching

## Concurrency

Use concurrency only when it clearly helps.

Good candidates:

- Independent network calls.
- Independent API calls.
- Independent file processing.
- Independent long-running checks.
- Large batches of unrelated work.

Avoid concurrency when:

- The work is already fast.
- Ordering is critical and hard to preserve.
- Shared state would make the code fragile.
- The bottleneck is not parallelizable.
- The added complexity is not justified.

## Preferred Parallel Options

This template targets PowerShell 7.6. Use modern runspace-based parallelism when concurrency is justified.

Preferred choices:

- Use `ForEach-Object -Parallel` for simple pipeline-oriented parallel work.
- Use `Start-ThreadJob` when job lifecycle commands such as `Receive-Job`, `Wait-Job`, and `Remove-Job` make the flow clearer.
- Use custom runspaces only when a module needs specialized pooling, lifecycle control, shared session state, or advanced coordination that the built-in options cannot provide.
- Use a normal `foreach` loop when parallel overhead would dominate the work.

Avoid:

- Do not use workflows. Workflows are a Windows PowerShell 5.1 feature and are not available in PowerShell 7+.
- Do not use `Start-Job` for normal PowerShell 7.6 module code. Use `Start-Job` only when process isolation is explicitly required or when writing for older PowerShell compatibility.

For simple parallel work, prefer `ForEach-Object -Parallel` with a throttle limit.

```powershell
$paths | ForEach-Object -Parallel {
    [pscustomobject]@{
        Path   = $PSItem
        Exists = Test-Path -Path $PSItem
    }
} -ThrottleLimit 5
```

Use `Start-ThreadJob` when job lifecycle commands make the flow clearer. It is lighter than `Start-Job` because it uses runspaces instead of separate PowerShell processes, and it avoids cross-process serialization loss.

```powershell
$jobs = foreach ($path in $paths) {
    Start-ThreadJob -ScriptBlock {
        param ($Path)

        [pscustomobject]@{
            Path   = $Path
            Exists = Test-Path -Path $Path
        }
    } -ArgumentList $path
}

$results = $jobs | Receive-Job -Wait -AutoRemoveJob
```

Prefer a normal loop when parallel overhead would dominate the work.

```powershell
$results = foreach ($path in $paths) {
    [pscustomobject]@{
        Path   = $path
        Exists = Test-Path -Path $path
    }
}
```

## Limit Execution Concurrency

Running scripts in parallel does not guarantee better performance. Parallel execution adds overhead for scheduling, runspace or process creation, data transfer, and result collection.

Good candidates:

- CPU-bound work on multi-core processors.
- Independent network or API calls that spend time waiting.
- Independent file operations that do not block each other.
- Long-running checks where each item is independent.

Always control concurrency with a throttle limit. Start conservatively and measure.

```powershell
$items | ForEach-Object -Parallel {
    Invoke-SlowIndependentWork -InputObject $PSItem
} -ThrottleLimit 5
```

For batch-style code, process a fixed number of jobs at a time instead of starting everything at once.

Overhead guidance:

- `ForEach-Object -Parallel` usually has less overhead than job-based approaches for pipeline work.
- `Start-ThreadJob` is the preferred job-style option for this PowerShell 7.6 template.
- `Start-Job` has significant overhead and can lose type fidelity because results cross a process boundary.

Use thread jobs, custom runspaces, or custom concurrency only when the scenario justifies the complexity.

## Caching

Use caching when it prevents repeated expensive work and remains easy to understand.

Good candidates:

- Repeated API lookups.
- Repeated file reads.
- Repeated metadata discovery.
- Repeated expensive calculations.
- Repeated configuration resolution.

```powershell
$cache = @{}

function Get-CachedValue {
    <#
    .SYNOPSIS
        Gets a cached value.

    .PARAMETER Key
        The cache key.

    .OUTPUTS
        System.String
    #>
    [CmdletBinding()]
    [OutputType([string])]
    param (
        [Parameter(Mandatory)]
        [ValidateNotNullOrEmpty()]
        [string]$Key
    )

    process {
        try {
            if ($cache.ContainsKey($Key)) {
                Write-Debug "Cache hit for key '$Key'."
                return $cache[$Key]
            }

            Write-Debug "Cache miss for key '$Key'."

            $value = "Computed value for $Key"
            $cache[$Key] = $value

            return $value
        }
        catch {
            $PSCmdlet.ThrowTerminatingError($PSItem)
        }
    }
}
```

Avoid caching when it creates stale data risks, hidden behavior, or unnecessary complexity.
