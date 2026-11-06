# Parameters And Help

## Parameters

Use a small default parameter pattern unless the command needs more.

```powershell
param (
    [Parameter(
        Mandatory,
        ValueFromPipeline,
        ValueFromPipelineByPropertyName
    )]
    [ValidateNotNullOrEmpty()]
    [string]$Uri
)
```

Do not use every possible parameter option by default.

Add parameter attributes only when they improve correctness or ergonomics:

| Attribute | Use when | Avoid when |
| --- | --- | --- |
| `ValidateSet` | The parameter has a fixed, known list of valid values. | Values change often or should be discovered dynamically. |
| `ValidateRange` | The parameter accepts numbers within a clear range. | The range is unclear or enforced elsewhere. |
| `ValidatePattern` | The value must match a specific string format. | The pattern would be fragile or hard to read. |
| `ValidateScript` | Built-in validation attributes cannot express the rule. | A simpler validation attribute works. |
| `Alias` | There is a common, useful alternate name. | It only saves a few characters. |
| `Position` | Positional usage improves common command-line ergonomics. | It makes calls ambiguous or harder to read. |
| `ParameterSetName` | The function has distinct calling patterns. | A single simple parameter set is enough. |
| `ValueFromPipeline` | Direct pipeline input makes sense. | Pipeline input would be surprising. |
| `ValueFromPipelineByPropertyName` | Binding matching object properties is useful and safe. | Property-name binding would be surprising or unsafe. |
| `ValueFromRemainingArguments` | The command intentionally collects trailing arguments. | Normal parameters are clearer. |

Prefer clear parameter names over aliases. Prefer named arguments in examples unless positional usage is deliberately part of the design.

## Comment-Based Help

Every public function and script should include comment-based help.

```powershell
<#
.SYNOPSIS
    Short summary.

.DESCRIPTION
    Detailed explanation.

.PARAMETER Name
    Description of the parameter.

.INPUTS
    Input object types accepted from the pipeline.

.OUTPUTS
    Output object types produced by the command.

.EXAMPLE
    Example-Command -Name Example

    Explanation of what the example does.

.NOTES
    Additional implementation or version notes.

.LINK
    Related documentation.
#>
```

Examples should show realistic usage. Include pipeline examples when the function supports pipeline input.

Parameter documentation can live in the help block or directly above the parameter. Prefer the style that is easiest to keep accurate.
