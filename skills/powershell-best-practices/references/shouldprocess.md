# ShouldProcess And WhatIf

Any function or script that creates, updates, deletes, modifies, sends, starts, stops, restarts, enables, disables, or changes state must implement `SupportsShouldProcess`.

Use `ShouldProcess()` around the operation that changes state. For read-only functions, do not add `SupportsShouldProcess`.

```powershell
function Remove-ExampleItem {
    <#
    .SYNOPSIS
        Removes an example item.

    .DESCRIPTION
        Removes an example item using ShouldProcess so -WhatIf and -Confirm are supported.

    .PARAMETER Path
        The path to remove.

    .INPUTS
        System.String

    .OUTPUTS
        None.

    .EXAMPLE
        Remove-ExampleItem -Path ./old.log -WhatIf

        Shows what would happen without removing the file.
    #>
    [CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'High')]
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
        Write-Verbose "Starting remove operation."
    }

    process {
        try {
            if ($PSCmdlet.ShouldProcess($Path, 'Remove item')) {
                Remove-Item -Path $Path -Force -ErrorAction Stop
            }
        }
        catch {
            $PSCmdlet.ThrowTerminatingError($PSItem)
        }
    }

    end {
        Write-Verbose "Finished remove operation."
    }
}
```

Use a specific target and action in `ShouldProcess($target, $action)`. Choose `ConfirmImpact = 'High'` for destructive operations such as deletes, irreversible updates, or broad state changes.
