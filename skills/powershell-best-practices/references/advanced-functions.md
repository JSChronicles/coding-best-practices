# Advanced Functions

Use advanced functions by default for reusable code.

## Default Non-Mutating Function

```powershell
function Get-ExampleItem {
    <#
    .SYNOPSIS
        Gets example items.

    .DESCRIPTION
        Retrieves example items from the provided path.

    .PARAMETER Path
        The path to inspect.

    .INPUTS
        System.String

    .OUTPUTS
        System.IO.FileInfo

    .EXAMPLE
        Get-ExampleItem -Path ./logs -Verbose

        Gets files from the ./logs directory.

    .NOTES
        Requires PowerShell 7.6 or later.
    #>
    [CmdletBinding()]
    [OutputType([System.IO.FileInfo])]
    param (
        [Parameter(
            Mandatory,
            ValueFromPipeline,
            ValueFromPipelineByPropertyName
        )]
        [ValidateNotNullOrEmpty()]
        [string]$Path
    )

    begin {
        Write-Verbose "Starting item discovery."
    }

    process {
        try {
            Write-Debug "Processing path: $Path"
            Get-ChildItem -Path $Path -File -ErrorAction Stop
        }
        catch {
            $PSCmdlet.ThrowTerminatingError($PSItem)
        }
    }

    end {
        Write-Verbose "Finished item discovery."
    }
}
```

## Pipeline Input

Support pipeline input when it improves usability.

- Use `ValueFromPipeline` for direct values.
- Use `ValueFromPipelineByPropertyName` for object properties.
- Prefer streaming output one object at a time.
- Do not collect all pipeline input into an array unless the command truly requires batch-level behavior.

## `clean` Blocks

Use `clean` only when there is cleanup work:

- Removing temporary files.
- Closing streams.
- Disposing .NET objects.
- Stopping or removing jobs.
- Cleaning up runspaces.
- Releasing handles or sessions.

Do not add an empty `clean` block by default.
