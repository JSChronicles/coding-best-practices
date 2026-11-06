# Performance

Use the simplest clear implementation first, but avoid PowerShell patterns that scale poorly with normal data sizes.

## Contents

- [Avoid Array Plus-Equals In Loops](#avoid-array-plus-equals-in-loops)
- [Collection Type Guidance](#collection-type-guidance)
- [Filter As Far Left As Possible](#filter-as-far-left-as-possible)
- [Use `.Where()` And `.ForEach()` Intentionally](#use-where-and-foreach-intentionally)
- [Use StringBuilder For Repeated String Construction](#use-stringbuilder-for-repeated-string-construction)
- [Measuring](#measuring)

## Avoid Array Plus-Equals In Loops

Do not build arrays with `+=` inside loops. Each `+=` creates a new copy of the current array and appends one item. As the array grows, every iteration copies more data, so performance degrades quickly.

Avoid growing an array with `+=`:

```powershell
$collection = @()

foreach ($item in 0..50000) {
    $collection += $item
}
```

Prefer assigning loop output directly to a variable:

```powershell
$collection = foreach ($item in 0..50000) {
    $item
}
```

Do not preinitialize the variable as an empty array when assigning loop output. The loop assignment replaces the variable, so the empty array is wasted work and makes the code look like it was meant to append.

```powershell
# Avoid the extra empty array assignment:
$collection = @()
$collection = foreach ($item in 0..50000) {
    $item
}

# Prefer direct assignment:
$collection = foreach ($item in 0..50000) {
    $item
}
```

Use a generic list when you need explicit collection mutation:

```powershell
$collection = [System.Collections.Generic.List[int]]::new()

foreach ($item in 0..50000) {
    $collection.Add($item)
}
```

Rules:

- Use loop output assignment when the loop naturally emits the values you want.
- Do not initialize `$collection = @()` before loop output assignment.
- Use `[System.Collections.Generic.List[T]]` when you need to pass a mutable collection around, add conditionally from multiple branches, or call collection methods.
- Do not use `+=` to grow arrays in loops.
- Treat `+=` array growth in loops as a review finding every time.

## Collection Type Guidance

Choose the collection type based on whether the size is fixed, whether element types are known, whether order matters, and whether lookup speed matters.

| Type | Use when | Example |
| --- | --- | --- |
| Array | Element type and size are fixed or known up front. | `[string[]]@('one', 'two')` |
| `List[T]` | Element type is known but collection size grows or is unknown. | `[System.Collections.Generic.List[int]]::new()` |
| `List[object]` | Values are mixed type and collection size grows or is unknown. | `[System.Collections.Generic.List[object]]::new()` |
| Hashtable | Key-based lookups are needed and values are mixed or untyped. | `@{ Key = 'Value' }` |
| `Dictionary[TKey, TValue]` | Key and value types are known and key-based lookup matters. | `[System.Collections.Generic.Dictionary[string, string]]::new()` |
| `HashSet[T]` | Unique typed values and fast membership checks are needed. | `[System.Collections.Generic.HashSet[string]]::new()` |
| `LinkedList[T]` | Very high-volume insertions/removals from known nodes in an ordered list justify the added complexity. | `[System.Collections.Generic.LinkedList[string]]::new()` |
| `Queue[T]` | Items are processed first-in, first-out. | `[System.Collections.Generic.Queue[string]]::new()` |
| `Stack[T]` | Items are processed last-in, first-out. | `[System.Collections.Generic.Stack[string]]::new()` |
| `SortedSet[T]` | Unique typed values must stay sorted. | `[System.Collections.Generic.SortedSet[string]]::new()` |
| `SortedList[TKey, TValue]` | Sorted keys are needed and collection changes are relatively infrequent. | `[System.Collections.Generic.SortedList[string, string]]::new()` |
| `SortedDictionary[TKey, TValue]` | Sorted keys are needed and collection changes often. | `[System.Collections.Generic.SortedDictionary[string, string]]::new()` |

Rules:

- Avoid explicitly using `Object[]` as a design choice. Prefer typed arrays, loop output assignment, or a collection type that matches the behavior.
- Do not use `+=` on arrays when a collection will grow or shrink.
- Use typed `List[T]` for known element types, including value types such as `int`, `long`, `char`, and `bool`.
- Do not introduce `ArrayList` in new code. Use `List[T]` or `List[object]` instead.
- Avoid arrays and lists for repeated lookup/search operations. Use dictionaries for key lookups and sets for membership checks.
- Use linked lists only when the insertion/removal pattern genuinely benefits from linked-list behavior; most PowerShell code is clearer with arrays, lists, queues, stacks, dictionaries, or sets.
- Use sorted collection types only when sorted order must be maintained during collection operations. If sorting is only needed once for output or reconstruction, sorting keys or values at the edge is often simpler.

Examples:

```powershell
$stringArray = [string[]]@('string1', 'string2')
$intArray = [int[]]@(1, 2, 3, 4, 5)

$list = [System.Collections.Generic.List[string]]::new()
$list.Add('String1')
$list.Add('String2')

$mixed = [System.Collections.Generic.List[object]]::new()
$mixed.Add(1)
$mixed.Add('String1')

$hashTable = @{
    Key1 = 'Value1'
    Key2 = 'Value2'
}

$dictionary = [System.Collections.Generic.Dictionary[string, string]]::new()
$dictionary['key1'] = 'Value1'
$dictionary['key2'] = 'Value2'

$comparer = [System.StringComparer]::InvariantCultureIgnoreCase
$caseInsensitiveDictionary = [System.Collections.Generic.Dictionary[string, string]]::new($comparer)
$caseInsensitiveDictionary['key1'] = 'Value1'
$caseInsensitiveDictionary['Key1'] = 'Value2'

$processesById = [System.Collections.Generic.Dictionary[int, System.Diagnostics.Process]]::new()
Get-Process | ForEach-Object {
    $processesById[$PSItem.Id] = $PSItem
}
```

## Filter As Far Left As Possible

When gathering data, filter as close to the source as possible. Provider, API, service, database, and cmdlet-native filters usually reduce the amount of data PowerShell has to materialize, pass through the pipeline, and filter later.

Prefer cmdlet parameters over right-side pipeline filtering when the cmdlet can do the filtering itself.

```powershell
# Avoid:
Get-ChildItem -Path $Path | Where-Object { $PSItem.Extension -eq '.log' }

# Prefer:
Get-ChildItem -Path $Path -Filter '*.log'
```

Use provider or service-side filters when available.

```powershell
# Avoid:
Get-Process | Where-Object { $PSItem.Name -eq 'pwsh' }

# Prefer:
Get-Process -Name pwsh
```

Rules:

- Prefer native parameters such as `-Filter`, `-Include`, `-Exclude`, `-Name`, `-Id`, `-Path`, date ranges, status parameters, or API query parameters when available.
- Use `Where-Object` when the source cannot express the predicate or the filter depends on calculated PowerShell-only logic.
- Put the highest-selectivity filter earliest in the pipeline.
- Avoid gathering broad datasets and filtering on the right unless the dataset is small or no source-side filter exists.
- For remote APIs, databases, Graph, cloud services, directory services, and file providers, check whether the backend supports server-side filtering before filtering locally.

## Use `.Where()` And `.ForEach()` Intentionally

PowerShell arrays and many collections have intrinsic `.Where()` and `.ForEach()` methods. They can be faster and more expressive than pipeline `Where-Object` and `ForEach-Object` for in-memory collections.

Prefer `.Where()` for filtering an existing in-memory collection:

```powershell
$largeFiles = $files.Where({ $PSItem.Length -gt 10MB })
```

Prefer `.ForEach()` for simple projections over an existing in-memory collection:

```powershell
$names = $files.ForEach({ $PSItem.Name })
```

Use regular `foreach` when the logic is multi-step, needs `break` or `continue`, mutates state, or is easier to read as a statement block:

```powershell
foreach ($file in $files) {
    if ($file.Length -le 10MB) {
        continue
    }

    [pscustomobject]@{
        Name   = $file.Name
        Length = $file.Length
    }
}
```

Rules:

- Use `.Where()` and `.ForEach()` only after data is already in memory.
- Do not replace streaming pipeline code with `.Where()` or `.ForEach()` when streaming behavior matters.
- Prefer `Where-Object` and `ForEach-Object` in command pipelines where readability and streaming are more important than in-memory collection speed.
- Prefer plain `foreach` for complex logic.

## Use StringBuilder For Repeated String Construction

Avoid repeated string concatenation in large loops. Strings are immutable, so repeated concatenation can create many intermediate strings.

`StringBuilder` is a .NET object designed for building strings efficiently. It keeps an internal mutable buffer so repeated appends do not repeatedly recreate the full string.

Basic usage:

```powershell
$builder = [System.Text.StringBuilder]::new()

[void]$builder.Append('Was it a car ')
[void]$builder.AppendLine('or a cat I saw?')

$content = $builder.ToString()
```

Use `[void]` to suppress the object returned by `Append()` and `AppendLine()`. Call `.ToString()` when the final string is needed.

Avoid:

```powershell
$content = ''

foreach ($line in $lines) {
    $content += "$line`n"
}
```

Use `[System.Text.StringBuilder]` when building large strings incrementally:

```powershell
$builder = [System.Text.StringBuilder]::new()

foreach ($line in $lines) {
    [void]$builder.AppendLine($line)
}

$content = $builder.ToString()
```

Illustrative comparison:

```powershell
$content = ''

Measure-Command {
    foreach ($item in 1..10000) {
        $content += 'Was it a car or a cat I saw? '
    }

    $content
}

$builder = [System.Text.StringBuilder]::new()

Measure-Command {
    foreach ($item in 1..10000) {
        [void]$builder.Append('Was it a car or a cat I saw? ')
    }

    $builder.ToString()
}
```

The exact timings depend on the machine and PowerShell session, but repeated concatenation commonly becomes much slower as the number of appends grows.

Do not assume `StringBuilder` is always fastest for every string-heavy loop. If the task is producing many separate strings, loop output assignment or pipeline output can be competitive or faster because PowerShell is already optimized for emitting objects.

```powershell
$builder = [System.Text.StringBuilder]::new()

Measure-Command {
    foreach ($item in 1..1000000) {
        [void]$builder.AppendLine('Was it a car or a cat I saw?')
    }

    $builder.ToString()
}

Measure-Command {
    $strings = foreach ($item in 1..1000000) {
        'Was it a car or a cat I saw?'
    }

    $strings
}

function PipelineTest {
    process {
        'Was it a car or a cat I saw?'
    }
}

Measure-Command {
    $strings = 1..1000000 | PipelineTest
    $strings
}
```

Use the shape that matches the output contract: `StringBuilder` for one final string, loop output or pipeline output for many string objects.

Rules:

- Use `StringBuilder` for large or unknown numbers of string appends when the result should be one final string.
- Use loop output assignment when the result should be a collection of strings.
- Use `-join` when the complete set of strings already exists.
- Keep normal string interpolation for simple one-off strings.
- Cast append calls to `[void]` or assign to `$null` so `StringBuilder` does not write intermediate objects to the pipeline.

## Measuring

Use `Measure-Command` for quick local comparisons, but do not hard-code benchmark numbers into code comments. Hardware, PowerShell version, profile state, and current system load affect the results.

```powershell
Measure-Command {
    $items = foreach ($item in 0..50000) {
        $item
    }
}
```
