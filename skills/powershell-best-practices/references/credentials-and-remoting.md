# Credentials And Remoting

Use this reference when a function needs optional credentials for remote systems, CIM sessions, PowerShell remoting, APIs, or service connections.

## Credential Parameters

Use the PowerShell credential type and credential transformation attribute.

```powershell
param (
    [Parameter(
        Position = 1,
        ValueFromPipelineByPropertyName
    )]
    [ValidateNotNull()]
    [System.Management.Automation.PSCredential]
    [System.Management.Automation.Credential()]
    $Credential = [System.Management.Automation.PSCredential]::Empty
)
```

Rules:

- Type credential parameters as `[System.Management.Automation.PSCredential]`.
- Add `[System.Management.Automation.Credential()]` so callers can pass a username and be prompted securely.
- Default to `[System.Management.Automation.PSCredential]::Empty` for optional credentials.
- Do not store plaintext passwords.
- Do not log credentials, secure strings, tokens, or authorization headers.
- Do not make credentials mandatory unless the command cannot support current-user/default authentication.

## Conditional Splatting

Build the command splat once, then add credentials only when the caller supplied them.

```powershell
$sessionSplat = @{
    ErrorAction = 'Stop'
}

if ($PSBoundParameters.ContainsKey('Credential')) {
    $sessionSplat.Credential = $Credential
}
```

This avoids passing an empty credential object to commands that should use the current user or default authentication when no credential is provided.

Use the same pattern for command families such as `Connect-VIServer`, `Invoke-Command`, `New-CimSession`, API clients, or service SDKs.

```powershell
$connectSplat = @{
    Server      = $Server
    ErrorAction = 'Stop'
}

if ($PSBoundParameters.ContainsKey('Credential')) {
    $connectSplat.Credential = $Credential
}

Connect-VIServer @connectSplat
```

For `Invoke-Command`, build the splat once and add `Credential` only when supplied.

```powershell
$invokeSplat = @{
    ComputerName = $ComputerName
    ErrorAction  = 'Stop'
}

if ($PSBoundParameters.ContainsKey('Credential')) {
    $invokeSplat.Credential = $Credential
}
```

## Invoke-Command Preferences

When invoking remote script blocks from a command that supports `ShouldProcess` or verbose output, pass useful caller preferences into the remote runspace with `$using:`.

```powershell
$invokeSplat.ScriptBlock = {
    try {
        $WhatIfPreference = $using:WhatIfPreference
        $ConfirmPreference = $using:ConfirmPreference
        $VerbosePreference = $using:VerbosePreference

        if ($WhatIfPreference) {
            Write-Verbose "WhatIf preference was forwarded to $env:COMPUTERNAME."
        }
    }
    catch {
        $PSCmdlet.ThrowTerminatingError($PSItem)
    }
}

Invoke-Command @invokeSplat
```

Rules:

- Forward `$WhatIfPreference` when remote code performs changes and the calling function supports `ShouldProcess`.
- Forward `$ConfirmPreference` when remote code may prompt or suppress confirmation.
- Forward `$VerbosePreference` when remote code writes useful `Write-Verbose` messages.
- Keep preference forwarding at the top of the script block so the rest of the remote logic behaves consistently.
- Still use `ShouldProcess` in the caller around high-level changes; forwarding preferences does not replace good command design.

## CIM Session Pattern

Use a session splat for remote CIM work and clean up sessions that the function creates.

Prefer CIM cmdlets and CIM sessions over WMI cmdlets. WMI is Microsoft's legacy implementation of the CIM standard. Use `Get-CimInstance`, `New-CimSession`, and `Remove-CimSession` instead of `Get-WmiObject` or other legacy WMI cmdlets in new code.

```powershell
function Get-MachineInformation {
    [CmdletBinding()]
    param (
        [Parameter(
            Position = 0,
            ValueFromPipeline,
            ValueFromPipelineByPropertyName
        )]
        [ValidateNotNullOrEmpty()]
        [string[]]$ComputerName = $env:COMPUTERNAME,

        [Parameter(
            Position = 1,
            ValueFromPipelineByPropertyName
        )]
        [ValidateNotNull()]
        [System.Management.Automation.PSCredential]
        [System.Management.Automation.Credential()]
        $Credential = [System.Management.Automation.PSCredential]::Empty
    )

    begin {
        $sessionSplat = @{
            ErrorAction = 'Stop'
        }

        if ($PSBoundParameters.ContainsKey('Credential')) {
            $sessionSplat.Credential = $Credential
        }
    }

    process {
        foreach ($computer in $ComputerName) {
            $session = $null

            try {
                $sessionSplat.ComputerName = $computer
                $session = New-CimSession @sessionSplat

                $computerSystem = Get-CimInstance -ClassName 'Win32_ComputerSystem' -CimSession $session -ErrorAction Stop

                [pscustomobject]@{
                    ComputerName = $computerSystem.Name
                    Manufacturer = $computerSystem.Manufacturer
                    Model        = $computerSystem.Model
                    CurrentUser  = $computerSystem.UserName
                }
            }
            catch {
                $PSCmdlet.ThrowTerminatingError($PSItem)
            }
            finally {
                if ($null -ne $session) {
                    Remove-CimSession -CimSession $session -ErrorAction SilentlyContinue
                }
            }
        }
    }
}
```

Rules:

- Use CIM instead of legacy WMI cmdlets for new code.
- Prefer source-side filters and selected properties when querying remote systems.
- Use `-ErrorAction Stop` for session creation and remote calls that must be caught.
- Clean up only sessions created by the function.
- Prefer `finally` for per-item session cleanup.
- Avoid `Get-CimSession | Remove-CimSession` because it can remove sessions the function did not create.
- Output structured objects.

## Review Checklist

- Credential parameters are typed as `[System.Management.Automation.PSCredential]`.
- `[System.Management.Automation.Credential()]` is present when username-to-credential prompting is useful.
- Credentials are only splatted when supplied by the caller.
- `Invoke-Command` forwards `WhatIf`, `Confirm`, and `Verbose` preferences when remote code performs changes or emits verbose details.
- Secrets are not logged or written to verbose/debug output.
- Remote sessions created by the function are cleaned up.
- The function does not remove unrelated global sessions.
