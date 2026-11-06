# Pester Testing

Use this reference when creating, editing, or reviewing PowerShell tests with Pester.

## Test Layout

Place tests under `tests/` and name files after the behavior or public command they cover.

```text
tests/
|-- Public/
|   `-- Get-ExampleItem.Tests.ps1
|-- Private/
|   `-- Resolve-ExamplePath.Tests.ps1
`-- MyModule.Tests.ps1
```

Prefer testing public behavior. Test private helpers only when they contain meaningful isolated logic that is hard to cover through public commands.

## Module Import Pattern

Import the module in `BeforeAll` so tests run against the module boundary.

```powershell
BeforeAll {
    $modulePath = Join-Path -Path $PSScriptRoot -ChildPath '../MyModule/MyModule.psd1'
    Import-Module -Name $modulePath -Force
}

AfterAll {
    Remove-Module -Name MyModule -ErrorAction SilentlyContinue
}
```

Use the `.psd1` manifest when available. Import the `.psm1` directly only when testing an unpublished module that does not have a manifest yet.

## Test Shape

Use `Describe`, `Context`, and `It` blocks to describe behavior.

```powershell
Describe 'Get-ExampleItem' {
    Context 'when the path exists' {
        It 'returns one object per file' {
            $result = Get-ExampleItem -Path $TestDrive

            $result | Should -Not -BeNullOrEmpty
            $result[0].PSObject.Properties.Name | Should -Contain 'Name'
        }
    }
}
```

Rules:

- Use `BeforeAll` for expensive setup shared by the file.
- Use `BeforeEach` for state that must be reset per test.
- Use `$TestDrive` for filesystem tests instead of writing into the repository or user profile.
- Keep assertions specific to behavior and output contracts.
- Test objects and properties, not formatted display text.
- Include tests for pipeline input when functions support `ValueFromPipeline`.
- Include `-WhatIf` or `ShouldProcess` behavior tests for mutating commands when practical.
- Avoid tests that depend on machine-specific paths, installed software, current time, network access, or user profile state unless explicitly isolated.

## Assertions

Prefer clear assertions:

```powershell
$result | Should -HaveCount 2
$result.Name | Should -Contain 'example.txt'
$result.Enabled | Should -BeTrue
{ Get-ExampleItem -Path './missing' -ErrorAction Stop } | Should -Throw
```

Avoid assertions that only prove a command ran:

```powershell
# Weak:
$result | Should -Not -BeNullOrEmpty
```

Use weak assertions only as supporting checks, not as the main behavior contract.

## Mocking

Use `Mock` for external boundaries such as network calls, service calls, destructive commands, slow commands, or non-deterministic dependencies.

```powershell
Describe 'Remove-ExampleItem' {
    BeforeAll {
        Mock Remove-Item {}
    }

    It 'calls Remove-Item when ShouldProcess allows the change' {
        Remove-ExampleItem -Path 'TestDrive:/old.log' -Confirm:$false

        Should -Invoke -CommandName Remove-Item -Times 1 -Exactly
    }
}
```

Do not over-mock internal implementation details. If a refactor breaks the test without changing behavior, the test is probably too tightly coupled.

## Running Tests

Run all tests:

```powershell
Invoke-Pester -Path ./tests
```

Run with detailed output:

```powershell
Invoke-Pester -Path ./tests -Output Detailed
```

CI can install Pester and run:

```powershell
Install-PSResource -Name Pester -TrustRepository
Import-Module -Name Pester
Invoke-Pester -Path './tests/*' -Passthru
```

## Review Checklist

- Tests import the module in a way that matches real usage.
- Public commands have behavior tests.
- Pipeline input, object output, errors, and `ShouldProcess` behavior are tested when applicable.
- Tests use `$TestDrive` or controlled fixtures for filesystem work.
- External systems are mocked or isolated.
- Tests avoid aliases and use `$PSItem` over `$_`.
- Test names describe behavior, not implementation.
