"""Regression tests for skill frontmatter validation."""

import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import ModuleType


def _load_validator() -> ModuleType:
    """Load the repository validator without making scripts a package."""
    validator_path = Path(__file__).parents[1] / "scripts" / "validate_skills.py"
    spec = importlib.util.spec_from_file_location("validate_skills", validator_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load validator from {validator_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = _load_validator()


class SkillValidationTests(unittest.TestCase):
    """Verify Agent Skills specification and repository policy checks."""

    def _validate(self, frontmatter: str, body: str = "# Test skill\n") -> list[str]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository_root = Path(temporary_directory)
            skill_directory = repository_root / "skills" / "test-skill"
            skill_directory.mkdir(parents=True)
            (skill_directory / "SKILL.md").write_text(
                f"---\n{frontmatter.strip()}\n---\n\n{body}",
                encoding="utf-8",
            )
            return VALIDATOR._validate_skill(skill_directory, repository_root)

    def test_accepts_all_supported_frontmatter_fields(self) -> None:
        issues = self._validate(
            """
name: test-skill
description: Validates a test skill when exercising the validator.
license: MIT
compatibility: Requires Python 3.14 or newer.
allowed-tools: Read Bash(git:*)
metadata:
  author: JSChronicles
  version: "1.0.0"
"""
        )

        self.assertEqual([], issues)

    def test_rejects_invalid_compatibility_values(self) -> None:
        base = """
name: test-skill
description: Validates a test skill when exercising the validator.
metadata:
  author: JSChronicles
  version: "1.0.0"
"""
        oversized = "x" * 501
        non_string_issues = self._validate(f"{base}\ncompatibility: 3.14")
        oversized_issues = self._validate(
            f'{base}\ncompatibility: "{oversized}"'
        )

        self.assertTrue(
            any(
                "compatibility must be a non-empty string" in issue
                for issue in non_string_issues
            )
        )
        self.assertTrue(
            any(
                "compatibility exceeds 500 characters" in issue
                for issue in oversized_issues
            )
        )

    def test_rejects_non_string_metadata_values(self) -> None:
        issues = self._validate(
            """
name: test-skill
description: Validates a test skill when exercising the validator.
metadata:
  author: JSChronicles
  version: 1.0
"""
        )

        self.assertTrue(
            any("metadata values must be strings" in issue for issue in issues)
        )
        self.assertTrue(
            any(
                "metadata.version must be a quoted version" in issue
                for issue in issues
            )
        )

    def test_rejects_empty_optional_strings_and_body(self) -> None:
        issues = self._validate(
            """
name: test-skill
description: Validates a test skill when exercising the validator.
license: ""
allowed-tools: ""
metadata:
  author: JSChronicles
  version: "1.0.0"
""",
            body="\n",
        )

        self.assertTrue(
            any("license must be a non-empty string" in issue for issue in issues)
        )
        self.assertTrue(
            any(
                "allowed-tools must be a non-empty string" in issue
                for issue in issues
            )
        )
        self.assertTrue(
            any("Markdown instructions are required" in issue for issue in issues)
        )


if __name__ == "__main__":
    unittest.main()
