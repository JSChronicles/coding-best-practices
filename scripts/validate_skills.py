#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "PyYAML==6.0.3",
# ]
# ///
"""Validate skill packages and synchronized plugin metadata."""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml

ALLOWED_FRONTMATTER_KEYS = {
    "allowed-tools",
    "description",
    "license",
    "metadata",
    "name",
}
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_PATTERN = re.compile(
    r"^\d+\.\d+(?:\.\d+)?(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)
FRONTMATTER_PATTERN = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
MARKDOWN_LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)\n]+)\)")
URI_SCHEME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def _load_yaml_mapping(path: Path) -> dict[str, object]:
    """Load a YAML file and require a top-level mapping.

    Args:
        path: YAML file to load.

    Returns:
        Parsed YAML mapping.

    Raises:
        TypeError: If the parsed document is not a mapping.
        ValueError: If the file contains invalid YAML.
    """
    try:
        parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise ValueError(f"invalid YAML: {error}") from error

    if not isinstance(parsed, dict):
        raise TypeError("top-level YAML value must be a mapping")
    return parsed


def _parse_skill(path: Path) -> tuple[dict[str, object], str]:
    """Parse a SKILL.md frontmatter mapping and body.

    Args:
        path: SKILL.md file to parse.

    Returns:
        A tuple containing the frontmatter and Markdown body.

    Raises:
        TypeError: If parsed frontmatter is not a mapping.
        ValueError: If frontmatter is missing or contains invalid YAML.
    """
    content = path.read_text(encoding="utf-8")
    match = FRONTMATTER_PATTERN.match(content)
    if match is None:
        raise ValueError("missing or malformed YAML frontmatter")

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        raise ValueError(f"invalid frontmatter YAML: {error}") from error

    if not isinstance(frontmatter, dict):
        raise TypeError("frontmatter must be a mapping")
    return frontmatter, content[match.end() :]


def _without_fenced_code(content: str) -> str:
    """Return Markdown content with fenced code blocks removed.

    Args:
        content: Markdown content.

    Returns:
        Markdown outside fenced code blocks.
    """
    visible_lines: list[str] = []
    fence_character: str | None = None
    fence_length = 0

    for line in content.splitlines():
        match = re.match(r"^[ \t]*(?:[-+*]|\d+[.)])?[ \t]*(`{3,}|~{3,})(.*)$", line)
        if match is not None:
            marker = match.group(1)
            if fence_character is None:
                fence_character = marker[0]
                fence_length = len(marker)
            elif (
                marker[0] == fence_character
                and len(marker) >= fence_length
                and not match.group(2).strip()
            ):
                fence_character = None
                fence_length = 0
            continue

        if fence_character is None:
            visible_lines.append(line)

    return "\n".join(visible_lines)


def _display_path(path: Path, repository_root: Path) -> str:
    """Return a repository-relative path for diagnostics.

    Args:
        path: Path to display.
        repository_root: Repository root.

    Returns:
        Portable relative path text.
    """
    return path.relative_to(repository_root).as_posix()


def _validate_markdown(
    markdown_path: Path,
    repository_root: Path,
) -> list[str]:
    """Validate local links and unfinished placeholders in Markdown.

    Args:
        markdown_path: Markdown file to validate.
        repository_root: Repository root used for diagnostics.

    Returns:
        Validation issue messages.
    """
    issues: list[str] = []
    display_path = _display_path(markdown_path, repository_root)
    visible_content = _without_fenced_code(markdown_path.read_text(encoding="utf-8"))

    if re.search(r"(?m)^[ ]{0,3}\[TODO:[^\n]*\][ \t]*$", visible_content):
        issues.append(f"{display_path}: unfinished TODO placeholder")

    for raw_target in MARKDOWN_LINK_PATTERN.findall(visible_content):
        target = raw_target.strip()
        if target.startswith("<") and ">" in target:
            target = target[1 : target.index(">")]
        else:
            target = target.split(maxsplit=1)[0]

        if (
            not target
            or target.startswith(("#", "/"))
            or URI_SCHEME_PATTERN.match(target)
        ):
            continue

        local_target = unquote(target.split("#", 1)[0].split("?", 1)[0])
        if not local_target:
            continue

        resolved_target = (markdown_path.parent / local_target).resolve()
        try:
            resolved_target.relative_to(repository_root)
        except ValueError:
            issues.append(
                f"{display_path}: local link escapes the repository: {target}"
            )
            continue

        if not resolved_target.exists():
            issues.append(f"{display_path}: broken local link: {target}")

    return issues


def _validate_openai_yaml(
    skill_directory: Path,
    skill_name: str,
    repository_root: Path,
) -> list[str]:
    """Validate optional OpenAI-facing skill metadata.

    Args:
        skill_directory: Skill directory.
        skill_name: Validated skill name.
        repository_root: Repository root used for diagnostics.

    Returns:
        Validation issue messages.
    """
    path = skill_directory / "agents" / "openai.yaml"
    if not path.exists():
        return []

    display_path = _display_path(path, repository_root)
    try:
        document = _load_yaml_mapping(path)
    except (TypeError, ValueError) as error:
        return [f"{display_path}: {error}"]

    interface = document.get("interface")
    if not isinstance(interface, dict):
        return [f"{display_path}: interface must be a mapping"]

    issues: list[str] = []
    display_name = interface.get("display_name")
    if not isinstance(display_name, str) or not display_name.strip():
        issues.append(f"{display_path}: interface.display_name is required")

    short_description = interface.get("short_description")
    if not isinstance(short_description, str):
        issues.append(f"{display_path}: interface.short_description is required")
    elif not 25 <= len(short_description.strip()) <= 64:
        issues.append(
            f"{display_path}: interface.short_description must be 25-64 characters"
        )

    default_prompt = interface.get("default_prompt")
    required_invocation = f"${skill_name}"
    if not isinstance(default_prompt, str) or required_invocation not in default_prompt:
        issues.append(
            f"{display_path}: interface.default_prompt must mention "
            f"{required_invocation}"
        )

    return issues


def _validate_skill(
    skill_directory: Path,
    repository_root: Path,
) -> list[str]:
    """Validate one canonical skill directory.

    Args:
        skill_directory: Skill directory to validate.
        repository_root: Repository root used for diagnostics.

    Returns:
        Validation issue messages.
    """
    skill_path = skill_directory / "SKILL.md"
    display_path = _display_path(skill_path, repository_root)
    if not skill_path.exists():
        return [f"{display_path}: missing SKILL.md"]

    try:
        frontmatter, body = _parse_skill(skill_path)
    except (TypeError, ValueError) as error:
        return [f"{display_path}: {error}"]

    issues: list[str] = []
    unexpected_keys = set(frontmatter) - ALLOWED_FRONTMATTER_KEYS
    if unexpected_keys:
        keys = ", ".join(sorted(str(key) for key in unexpected_keys))
        issues.append(f"{display_path}: unexpected frontmatter keys: {keys}")

    name = frontmatter.get("name")
    if not isinstance(name, str) or not SKILL_NAME_PATTERN.fullmatch(name):
        issues.append(f"{display_path}: name must be lowercase hyphen-case")
        skill_name = skill_directory.name
    else:
        skill_name = name
        if len(name) > 64:
            issues.append(f"{display_path}: name exceeds 64 characters")
        if name != skill_directory.name:
            issues.append(
                f"{display_path}: name '{name}' does not match directory "
                f"'{skill_directory.name}'"
            )

    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        issues.append(f"{display_path}: description is required")
    elif len(description.strip()) > 1024:
        issues.append(f"{display_path}: description exceeds 1024 characters")
    elif "<" in description or ">" in description:
        issues.append(f"{display_path}: description cannot contain angle brackets")

    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        issues.append(f"{display_path}: metadata must be a mapping")
    else:
        author = metadata.get("author")
        if not isinstance(author, str) or not author.strip():
            issues.append(f"{display_path}: metadata.author is required")

        version = metadata.get("version")
        if not isinstance(version, str) or not VERSION_PATTERN.fullmatch(version):
            issues.append(
                f"{display_path}: metadata.version must be a quoted version "
                "such as 0.1 or 0.1.0"
            )

    if re.search(r"(?m)^[ ]{0,3}\[TODO:[^\n]*\][ \t]*$", _without_fenced_code(body)):
        issues.append(f"{display_path}: unfinished TODO placeholder")

    for markdown_path in sorted(skill_directory.rglob("*.md")):
        issues.extend(_validate_markdown(markdown_path, repository_root))

    issues.extend(_validate_openai_yaml(skill_directory, skill_name, repository_root))
    return issues


def _load_json_mapping(path: Path) -> dict[str, object]:
    """Load a JSON file and require a top-level object.

    Args:
        path: JSON file to load.

    Returns:
        Parsed JSON object.

    Raises:
        TypeError: If the parsed document is not an object.
        ValueError: If the document contains invalid JSON.
    """
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON: {error}") from error

    if not isinstance(parsed, dict):
        raise TypeError("top-level JSON value must be an object")
    return parsed


def _validate_plugin_manifests(repository_root: Path) -> list[str]:
    """Validate plugin manifests and synchronized package versions.

    Args:
        repository_root: Repository root containing plugin manifests.

    Returns:
        Validation issue messages.
    """
    manifest_paths = {
        "plugin": repository_root / "plugin.json",
        "claude": repository_root / ".claude-plugin" / "plugin.json",
        "claude_marketplace": (repository_root / ".claude-plugin" / "marketplace.json"),
        "agents_marketplace": (
            repository_root / ".agents" / "plugins" / "marketplace.json"
        ),
    }
    documents: dict[str, dict[str, object]] = {}
    issues: list[str] = []

    for key, path in manifest_paths.items():
        display_path = _display_path(path, repository_root)
        if not path.exists():
            issues.append(f"{display_path}: required manifest is missing")
            continue
        try:
            documents[key] = _load_json_mapping(path)
        except (TypeError, ValueError) as error:
            issues.append(f"{display_path}: {error}")

    required_documents = {
        "plugin",
        "claude",
        "claude_marketplace",
        "agents_marketplace",
    }
    if set(documents) != required_documents:
        return issues

    plugin_name = documents["plugin"].get("name")
    if not isinstance(plugin_name, str) or not plugin_name:
        issues.append("plugin.json: name is required")
        return issues

    for key in ("claude", "agents_marketplace"):
        if documents[key].get("name") != plugin_name:
            path = _display_path(manifest_paths[key], repository_root)
            issues.append(f"{path}: name must match plugin.json")

    agents_plugins = documents["agents_marketplace"].get("plugins")
    agents_entry = None
    if isinstance(agents_plugins, list):
        agents_entry = next(
            (
                entry
                for entry in agents_plugins
                if isinstance(entry, dict) and entry.get("name") == plugin_name
            ),
            None,
        )
    if agents_entry is None:
        issues.append(
            ".agents/plugins/marketplace.json: plugin entry does not match plugin.json"
        )

    marketplace_plugins = documents["claude_marketplace"].get("plugins")
    marketplace_entry: dict[str, object] | None = None
    if isinstance(marketplace_plugins, list):
        marketplace_entry = next(
            (
                entry
                for entry in marketplace_plugins
                if isinstance(entry, dict) and entry.get("name") == plugin_name
            ),
            None,
        )
    if marketplace_entry is None:
        issues.append(
            ".claude-plugin/marketplace.json: plugin entry does not match plugin.json"
        )
        return issues

    plugin_description = documents["plugin"].get("description")
    claude_description = documents["claude"].get("description")
    if (
        not isinstance(plugin_description, str)
        or not plugin_description.strip()
        or plugin_description != claude_description
    ):
        issues.append(
            "plugin.json and .claude-plugin/plugin.json descriptions must be "
            "nonempty and synchronized"
        )

    versions = {
        "plugin.json": documents["plugin"].get("version"),
        ".claude-plugin/plugin.json": documents["claude"].get("version"),
        ".claude-plugin/marketplace.json": marketplace_entry.get("version"),
    }
    if any(
        not isinstance(version, str) or not VERSION_PATTERN.fullmatch(version)
        for version in versions.values()
    ):
        issues.append("plugin manifests must use valid quoted versions")
    elif len(set(versions.values())) != 1:
        values = ", ".join(f"{path}={version}" for path, version in versions.items())
        issues.append(f"plugin manifest versions are not synchronized: {values}")

    return issues


def validate_repository(repository_root: Path) -> tuple[list[str], int]:
    """Validate every skill and plugin manifest in a repository.

    Args:
        repository_root: Repository root to validate.

    Returns:
        A tuple containing validation issues and the number of skills checked.
    """
    repository_root = repository_root.resolve()
    skills_directory = repository_root / "skills"
    if not skills_directory.is_dir():
        return (["skills/: canonical skill directory is missing"], 0)

    skill_directories = sorted(
        path for path in skills_directory.iterdir() if path.is_dir()
    )
    if not skill_directories:
        return (["skills/: no skill directories found"], 0)

    issues: list[str] = []
    for skill_directory in skill_directories:
        issues.extend(_validate_skill(skill_directory, repository_root))
    issues.extend(_validate_plugin_manifests(repository_root))
    return issues, len(skill_directories)


def _build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser.

    Returns:
        Configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Validate skill packages and plugin metadata."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root to validate (default: current directory).",
    )
    return parser


def main() -> int:
    """Run repository validation and return a process exit code.

    Returns:
        Zero when validation passes; otherwise one.
    """
    arguments = _build_parser().parse_args()
    issues, skill_count = validate_repository(arguments.root)

    if issues:
        print(f"Validation failed with {len(issues)} issue(s):", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    print(f"Validated {skill_count} skills and synchronized plugin metadata.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
