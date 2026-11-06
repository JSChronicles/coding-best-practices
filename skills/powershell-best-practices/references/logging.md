# Logging

Use dedicated logging when the command needs durable operational records. Streams are for PowerShell interaction; logs are for persisted diagnostic or operational history.

## Contents

- [Rules](#rules)
- [Simple Log Writer](#simple-log-writer)
- [Log Parser](#log-parser)
- [Custom PsLogger Reference Implementation](#custom-pslogger-reference-implementation)

## Rules

- Do not use `Write-Host` as logging.
- Keep file or structured logging as the source of truth.
- Make console mirroring explicit and optional, such as a `-Write` switch or class constructor switch.
- Use stable severity names consistently: `Emergency`, `Alert`, `Critical`, `Error`, `Warning`, `Notice`, `Informational`, and `Debug`.
- Prefer UTC timestamps for log lines.
- Use simple file logging for low-volume scripts.
- Use a queued logger such as the custom `PsLogger` reference implementation for chatty or long-running scripts where frequent disk writes would add friction.
- Flush and dispose background logging resources before the script exits.

## Simple Log Writer

For straightforward scripts, use a small advanced function that accepts pipeline input and writes one log line per message.

```powershell
function Write-SimpleLog {
    <#
    .SYNOPSIS
        Writes messages to a log file.

    .PARAMETER Path
        The .log file path.

    .PARAMETER Message
        The message to write.

    .PARAMETER Severity
        The severity for the message.

    .INPUTS
        System.String

    .OUTPUTS
        None.
    #>
    [CmdletBinding()]
    param (
        [Parameter(Mandatory, Position = 0)]
        [ValidateNotNullOrEmpty()]
        [ValidatePattern('\.log$')]
        [string]$Path,

        [Parameter(Mandatory, Position = 1, ValueFromPipeline)]
        [ValidateNotNullOrEmpty()]
        [string]$Message,

        [Parameter(Position = 2)]
        [ValidateSet('Emergency', 'Alert', 'Critical', 'Error', 'Warning', 'Notice', 'Informational', 'Debug')]
        [string]$Severity = 'Informational'
    )

    process {
        try {
            $entry = '<{0}> [{1}] - {2}' -f [DateTime]::UtcNow.ToString('yyyy-MM-dd HH:mm:ssK'), $Severity, $Message
            Add-Content -Path $Path -Value $entry -ErrorAction Stop
        }
        catch {
            $PSCmdlet.ThrowTerminatingError($PSItem)
        }
    }
}
```

## Log Parser

For project logs using the `<timestamp> [Severity] - message` shape, expose filtering and counting as object or match output. Keep parsing separate from writing.

```powershell
function Get-LogInformation {
    <#
    .SYNOPSIS
        Parses a supported log file.

    .PARAMETER Path
        The .log file to parse.

    .PARAMETER Filter
        Text to filter on.

    .PARAMETER Severity
        Severity values to filter on.

    .PARAMETER Count
        Returns counts by severity.
    #>
    [CmdletBinding(DefaultParameterSetName = 'Filter')]
    param (
        [Parameter(Mandatory, ValueFromPipeline, ValueFromPipelineByPropertyName, Position = 0)]
        [ValidateScript({
            if (-not (Test-Path -Path $PSItem -PathType Leaf)) {
                throw 'The path argument must be an existing file.'
            }
            if ($PSItem -notmatch '\.log$') {
                throw 'The file specified in the path argument must be .log.'
            }
            return $true
        })]
        [string]$Path,

        [Parameter(ValueFromPipelineByPropertyName, ParameterSetName = 'Filter')]
        [ValidateNotNullOrEmpty()]
        [string]$Filter,

        [Parameter(ValueFromPipelineByPropertyName, ParameterSetName = 'Severity')]
        [ValidateSet('Emergency', 'Alert', 'Critical', 'Error', 'Warning', 'Notice', 'Informational', 'Debug')]
        [string[]]$Severity,

        [Parameter(ValueFromPipelineByPropertyName)]
        [switch]$Count
    )

    begin {
        $levels = 'Emergency', 'Alert', 'Critical', 'Error', 'Warning', 'Notice', 'Informational', 'Debug'
    }

    process {
        try {
            $log = Get-Content -Path $Path -ErrorAction Stop
            $matchesByLevel = @{}

            foreach ($level in $levels) {
                $matchesByLevel[$level] = $log | Select-String -SimpleMatch "[$level]"
            }

            if ($PSBoundParameters.ContainsKey('Filter')) {
                $log | Select-String -SimpleMatch $Filter
            }
            elseif ($PSBoundParameters.ContainsKey('Severity')) {
                foreach ($level in $Severity) {
                    $matchesByLevel[$level]
                }
            }
            elseif (-not $Count) {
                $log
            }

            if ($Count) {
                [pscustomobject]@{
                    Emergency     = $matchesByLevel['Emergency'].Count
                    Alert         = $matchesByLevel['Alert'].Count
                    Critical      = $matchesByLevel['Critical'].Count
                    Error         = $matchesByLevel['Error'].Count
                    Warning       = $matchesByLevel['Warning'].Count
                    Notice        = $matchesByLevel['Notice'].Count
                    Informational = $matchesByLevel['Informational'].Count
                    Debug         = $matchesByLevel['Debug'].Count
                }
            }
        }
        catch {
            $PSCmdlet.ThrowTerminatingError($PSItem)
        }
    }
}
```

## Custom PsLogger Reference Implementation

`PsLogger` is not built into PowerShell. It is a custom user-provided class pattern for lean call-site logging with a concurrent queue and background runspace.

Use this pattern when logging should be buffered and lightweight for callers. Console mirroring may use `Write-Host` only when explicitly enabled by the caller; it must not be the logging mechanism.

```powershell
Class PsLogger {
    <#
    .SYNOPSIS
        Creates a runspace to run your event driven logger.
    .DESCRIPTION
        Creates a runspace to run your event driven logger.
    .PARAMETER Path
        Path of the logfile you want it to log to.
    .PARAMETER Write
        Writes to the console as well as the log file.
    .PARAMETER Severity
        "Emergency","Alert","Critical","Error","Warning","Notice","Informational","Debug"
    .PARAMETER CleanLogs
        Remove Logs older than $X days from Path.
    .PARAMETER IsEmpty
        IsEmpty method to see if anything is still processing
    .PARAMETER Remove
        Remove method to close and dispose of the logging thread
    .PARAMETER GetStatus
        Get Status Method Tells you the runspace information and its state and availability.
    .INPUTS
        Description of objects that can be piped to the script.
    .OUTPUTS
        Description of objects that are output by the script.
    .EXAMPLE
        # Create a new log with the name Test
        $logger = [PSLogger]::new("C:\Temp","Test")
    .EXAMPLE
        # Create a new log with the name Test1 and write to the console
        $logger = [PSLogger]::new("C:\Temp","Test1",$True)
    .EXAMPLE
        # write to the log with a informational severity
        $logger.Informational("info goes here")
    .EXAMPLE
        # Clean logs older than "-1"
        $logger.CleanLogs("C:\Temp",-1)
    .EXAMPLE
        # Checks if the queue is empty
        $logger.IsEmpty()
        True
    .EXAMPLE
        # Waits one second for the queue to empty and then closes the thread
        $logger.Remove()
    .EXAMPLE
        $logger.GetStatus()
        Id Name            ComputerName    Type          State         Availability
        -- ----            ------------    ----          -----         ------------
        2 PSLogger        localhost       Local         Opened        Available
    .EXAMPLE
        $logPath = "C:\temp"
        if (!("PSLogger" -as [type])) {
            $callingScript = ($MyInvocation.MyCommand.Name) -split('.ps1')
            ."\\server\path\here\Logging.ps1"
            $logger = [PSLogger]::new($logPath,$callingScript)
        }
    .LINK
        Links to further documentation.
    .NOTES
        Detail on what the script does, if this is needed.
    #>
    hidden $loggingScript = {

        function Start-Logging {
            $loggingTimer = New-Object Timers.Timer
            $action = { logging }
            $loggingTimer.Interval = 1000
            $null = Register-ObjectEvent -InputObject $loggingTimer -EventName elapsed -Sourceidentifier loggingTimer -Action $action
            $loggingTimer.start()
        }

        function logging {
            $sw = $logFile.AppendText()
            while (-not $logEntries.IsEmpty) {
                $entry = ''
                $null = $logEntries.TryDequeue([ref]$entry)
                $sw.WriteLine($entry)
            }
            $sw.Flush()
            $sw.Close()
        }
        $logFile = New-Item -ItemType File -Name "$ExecutingScript`_$([DateTime]::UtcNow.ToString(`"yyyyMMddTHHmmssZ`")).log" -Path $logLocation

        Start-Logging
    }

    hidden $loggingRunspace = [runspacefactory]::CreateRunspace()
    hidden $logEntries = [System.Collections.Concurrent.ConcurrentQueue[string]]::new()
    hidden $logLocation = "C:\Temp"
    hidden $ExecutingScript = "Default"
    hidden $Write = $False

    PsLogger() {
        $this.logLocation = "C:\Temp"
        $this.ExecutingScript = "Default"
        $this.Write = $False

        if (!(Test-Path -Path $this.logLocation)) {
            [void](New-Item -path $this.logLocation -ItemType directory -force)
        }

        $this.StartLogging()
    }

    PsLogger([string]$logLocation, [string]$ExecutingScript) {
        $this.logLocation = $logLocation
        $this.ExecutingScript = $ExecutingScript
        $this.Write = $False

        if (!(Test-Path -Path $this.logLocation)) {
            [void](New-Item -path $this.logLocation -ItemType directory -force)
        }

        $this.StartLogging()
    }

    PsLogger([string]$logLocation, [string]$ExecutingScript, [switch]$Write) {
        $this.logLocation = $logLocation
        $this.ExecutingScript = $ExecutingScript
        $this.Write = $Write

        if (!(Test-Path -Path $this.logLocation)) {
            [void](New-Item -path $this.logLocation -ItemType directory -force)
        }

        $this.StartLogging()
    }

    Emergency([string]$message) {
        $this.LogMessage($message, "Emergency")
    }

    Alert([string]$message) {
        $this.LogMessage($message, "Alert")
    }

    Critical([string]$message) {
        $this.LogMessage($message, "Critical")
    }

    Error([string]$message) {
        $this.LogMessage($message, "Error")
    }

    Warning([string]$message) {
        $this.LogMessage($message, "Warning")
    }

    Notice([string]$message) {
        $this.LogMessage($message, "Notice")
    }

    Informational([string]$message) {
        $this.LogMessage($message, "Informational")
    }

    Debug([string]$message) {
        $this.LogMessage($message, "Debug")
    }

    hidden LogMessage([string]$message, [string]$severity) {
        $addResult = $false

        $funcName = (Get-PSCallStack).FunctionName[2]

        if ($funcName -eq "<ScriptBlock>") {
            $funcName = ""
        }

        $msg = $null

        while ($addResult -eq $false) {
            $msg = '<{0}> [{1}] {2} - {3}' -f [DateTime]::UtcNow.tostring('yyyy-MM-dd HH:mm:ssK'), $severity, $funcName, $message
            $addResult = $this.logEntries.TryAdd($msg)
        }

        if ($this.Write) {
            write-host "$msg"
        }
    }

    hidden StartLogging() {
        $this.LoggingRunspace.ThreadOptions = "ReuseThread"
        $this.loggingRunspace.name = 'PSLogger'
        $this.LoggingRunspace.Open()
        $this.LoggingRunspace.SessionStateProxy.SetVariable("logEntries", $this.logEntries)
        $this.LoggingRunspace.SessionStateProxy.SetVariable("logLocation", $this.logLocation)
        $this.LoggingRunspace.SessionStateProxy.SetVariable("ExecutingScript", $this.ExecutingScript)
        $this.LoggingRunspace.SessionStateProxy.SetVariable("Write", $this.Write)
        $cmd = [PowerShell]::Create().AddScript($this.loggingScript)

        $cmd.Runspace = $this.LoggingRunspace
        $null = $cmd.BeginInvoke()
    }

    CleanLogs([string]$logLocation, [int]$Days) {
        $Logs = (Get-ChildItem $logLocation -Filter "*.log").Where( { $PSItem.LastWriteTime -LT (Get-Date).AddDays($Days) })
        foreach ($Log in $Logs) {
            Try {
                $Log | Remove-Item -Force
                $this.Logger.Informational("Cleaned $($log.Name)")
            }
            Catch {
                $PSitem
            }
        }
    }

    [bool]IsEmpty() {
        if ($this.logEntries.IsEmpty) {
            return $true
        } else {
            return $false
        }
    }

    Remove() {
        Start-Sleep -Seconds 1
        $This.LoggingRunspace.close()
        $This.LoggingRunspace.Dispose()
        If ($This.LoggingRunspace) {
            $This.LoggingRunspace.close()
            $This.LoggingRunspace.Dispose()
        }
    }

    [object]GetStatus() {
        return $This.LoggingRunspace
    }
}
```
