# Module Design And Naming

Use this reference when creating, refactoring, or reviewing PowerShell modules, module folders, public/private functions, command names, and exports.

## Module Setup

Use a module when code is reusable, exposes public commands, or needs a clean import boundary. Use a script when the code is a one-off entry point or task runner.

Mandated installed/published module shape:

```text
MyModule/
`-- 0.1.0/
    |-- MyModule.psd1
    |-- MyModule.psm1
    |-- Public/
    |   `-- Get-ExampleItem.ps1
    |-- Private/
    |   `-- Resolve-ExamplePath.ps1
    |-- Classes/
    |   `-- ExampleItem.ps1
    `-- en-US/
        |-- about_MyModule.help.txt
        `-- MyModule-help.xml
```

Rules:

- Use the versioned module layout for module scaffolding, packaging, examples, and installable output.
- Name the parent module folder after the module, such as `MyModule`.
- Place each module version in a semantic-version child folder, such as `0.1.0`.
- Name the module manifest after the parent module folder, not the version folder: `MyModule/0.1.0/MyModule.psd1`.
- Set manifest `ModuleVersion` to exactly match the version folder name.
- Set manifest `RootModule` to the script module file name, such as `MyModule.psm1`.
- Name the `.psm1` after the manifest by convention. This is not required by PowerShell when a manifest exists, but use the convention unless there is a strong repo-specific reason not to.
- When a module has no manifest, the `.psm1` file must have the same name as the module directory.
- Put public commands in `Public/`.
- Put internal helper functions in `Private/`.
- Put class definitions in `Classes/` only when classes are justified.
- Put about-help files in a locale folder such as `en-US/`.
- Keep each public function in its own file named after the function.
- Keep module import side effects minimal. Dot-source functions and define types; do not perform network calls, broad filesystem changes, or expensive discovery during import.
- Use a module manifest (`.psd1`) for published or reusable modules.
- Export only public commands. Prefer manifest `FunctionsToExport` for stable modules, or `Export-ModuleMember` when the module loader pattern requires it.

Allowed source repository shape for active development:

```text
RepositoryRoot/
|-- MyModule/
|   `-- 0.1.0/
|       |-- MyModule.psd1
|       |-- MyModule.psm1
|       |-- Public/
|       |-- Private/
|       |-- Classes/
|       `-- en-US/
|-- tests/
|   |-- Public/
|   |   `-- Get-ExampleItem.Tests.ps1
|   `-- MyModule.Tests.ps1
|-- docs/
|-- README.md
`-- .github/
    `-- workflows/
```

Use this root layout for template repositories so source, tests, docs, and CI files have clear ownership. If an existing repository intentionally keeps unversioned source under `src/MyModule/`, preserve that local pattern only when the build/package step emits the mandated versioned layout.

## Module Manifest

Use a `.psd1` manifest for modules that are intended to be imported by other scripts, published, versioned, or tested in CI.

Recommended manifest fields:

- `RootModule`: the `.psm1` file.
- `ModuleVersion`: semantic module version.
- `GUID`: stable module GUID.
- `Author`, `CompanyName`, `Copyright`.
- `Description`: short module purpose.
- `PowerShellVersion`: minimum supported PowerShell version.
- `FunctionsToExport`: explicit list of public functions.
- `CmdletsToExport`, `VariablesToExport`, `AliasesToExport`: use empty arrays unless intentionally exporting them.
- `RequiredModules`: modules required at import time.
- `PrivateData.PSData`: tags, license URL, project URL, release notes, and prerelease metadata when publishing.

Create a starter manifest with splatting:

```powershell
$manifestSplat = @{
    Path              = './MyModule/0.1.0/MyModule.psd1'
    RootModule        = 'MyModule.psm1'
    ModuleVersion     = '0.1.0'
    PowerShellVersion = '7.6'
}

New-ModuleManifest @manifestSplat
```

Avoid wildcard exports in stable modules:

```powershell
# Avoid for stable modules:
FunctionsToExport = '*'

# Prefer:
FunctionsToExport = @(
    'Get-ExampleItem'
    'Test-ExampleItem'
)
```

Wildcard exports can be acceptable while prototyping, but pin exports before release so private helpers do not leak into the public contract.

`New-ModuleManifest` can generate files as UTF-16 LE depending on the host/version. If an editor displays replacement characters before the opening `#`, convert the file to UTF-8.

```powershell
$manifestPath = './MyModule/0.1.0/MyModule.psd1'
$manifestContent = Get-Content -Path $manifestPath -Raw -Encoding Unicode
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)

[System.IO.File]::WriteAllText(
    (Resolve-Path -Path $manifestPath),
    $manifestContent,
    $utf8NoBom
)
```

After generating a manifest, review and replace wildcard exports before release:

```powershell
FunctionsToExport = @(
    'Get-ExampleItem'
)
CmdletsToExport = @()
VariablesToExport = @()
AliasesToExport = @()
```

## Module Names And Command Nouns

Module names should describe the domain, product, resource family, or automation area the module owns. Public command nouns should usually align with that domain so commands feel like a coherent command set.

Examples:

| Module | Good command nouns | Avoid |
| --- | --- | --- |
| `UserManagement` | `Get-User`, `Set-UserRole`, `Remove-UserSession` | `Get-Thing`, `Run-UserStuff` |
| `ReportTools` | `New-Report`, `Export-Report`, `Test-ReportDefinition` | `Do-Report`, `Process-Data` |
| `FoundryProject` | `Get-FoundryProject`, `Test-FoundryConfig`, `New-FoundryTemplate` | `Get-ProjectThing`, `Handle-Template` |

Rules:

- Choose a module name that is specific enough to make command ownership clear.
- Keep nouns consistent across related commands.
- Prefix command nouns with the product or domain name when the noun would otherwise be too generic, such as `Project`, `Config`, or `Template`.
- Avoid repeating the full module name in every command noun when the noun is already clear and unlikely to collide.
- Avoid broad module names such as `Utilities`, `Helpers`, or `Common` unless the repository already uses that convention intentionally.

## Public And Private Function Files

Public functions are the user-facing contract of the module. Private functions are implementation details used by public commands.

Rules:

- Public function names should use approved `Verb-Noun` naming and be exported.
- Public function files should match the function name, such as `Get-UserData.ps1`.
- Private helper files should also have descriptive names, but they do not need to be exported.
- Prefer `Verb-Noun` for private helpers when it remains clear, such as `Resolve-ProjectPath` or `ConvertTo-ReportRecord`.
- Do not expose private helpers just because tests need them. Test public behavior when possible.
- Keep private helpers in `Private/` and public commands in `Public/` so exports are easy to reason about.

Example module loader:

```powershell
$moduleFolders = @(
    'Classes'
    'Public'
    'Private'
)

foreach ($moduleFolder in $moduleFolders) {
    $moduleFolderPath = Join-Path -Path $PSScriptRoot -ChildPath $moduleFolder

    if (-not (Test-Path -LiteralPath $moduleFolderPath -PathType Container)) {
        continue
    }

    $moduleFiles = Get-ChildItem -LiteralPath $moduleFolderPath -Filter '*.ps1' -File |
        Sort-Object -Property Name

    foreach ($moduleFile in $moduleFiles) {
        . $moduleFile.FullName
    }
}
```

Prefer non-recursive loading unless the module intentionally supports nested source folders. Keep the order deterministic so classes and dependencies load predictably. For large stable modules where import speed matters, generate a built `.psm1` during packaging instead of discovering source files at import time.

## Approved Verbs

Public commands should use approved PowerShell verbs.

Find approved verbs with:

```powershell
Get-Verb | Sort-Object Verb
```

Rules:

- Use `Verb-Noun` for public functions and scripts intended to behave like commands.
- Choose the approved verb that best describes the action.
- Keep nouns singular unless the domain term is naturally plural.
- Prefer specific nouns that describe the resource, not implementation details.
- Avoid inventing verbs such as `Process`, `Handle`, `Run`, or `Do` for public commands when an approved verb fits.
- Keep private helper names descriptive; they may still use `Verb-Noun`, but they do not need to be exported.

Examples:

```powershell
Get-UserData
Set-UserPreference
New-ReportFile
Remove-ExpiredSession
Test-Configuration
Resolve-ProjectPath
```

## Naming Conventions

| Type | Naming Convention | Example |
| --- | --- | --- |
| Script | `Pascal-Case.ps1` | `Get-UserData.ps1` |
| Function/Cmdlet | `Pascal-Case` | `Test-Connection` |
| Module | `PascalCase` | `UserManagement` |
| Class/Enum | `PascalCase` | `UserRole` |
| Parameter | `PascalCase` | `UserName` |
| Public Field/Property | `PascalCase` | `MaxRetries` |
| Global Variables | `PascalCase` | `$GlobalVariable` |
| Constants | `PascalCase` | `MaxRetries` |
| Logs | `snake_case` | `error_log.txt` |
| Language Keywords | Lowercase | `foreach`, `dynamicparam` |
| Help Keywords | UPPERCASE | `.SYNOPSIS`, `.PARAMETER` |

Terminology:

- `lowercase`: all lowercase with no word separation.
- `UPPERCASE`: all capitals with no word separation.
- `PascalCase`: capitalize the first letter of each word.
- `camelCase`: capitalize the first letter of each word except the first.

## Module Use

Import local modules explicitly during development:

```powershell
Import-Module ./MyModule/MyModule.psm1 -Force
```

Inspect exported commands:

```powershell
Get-Command -Module MyModule
```

Remove and reload during local testing when needed:

```powershell
Remove-Module MyModule -ErrorAction SilentlyContinue
Import-Module ./MyModule/MyModule.psm1 -Force
```
