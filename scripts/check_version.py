#!/usr/bin/env python3
"""Check that version numbers are consistent across the project."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def get_changelog_version() -> str | None:
    """Extract the latest non-Unreleased version from CHANGELOG.md."""
    changelog = Path("CHANGELOG.md").read_text()
    match = re.search(r"## \[(\d+\.\d+\.\d+)\]", changelog)
    return match.group(1) if match else None


def get_pyproject_version() -> str | None:
    """Extract version from pyproject.toml."""
    pyproject = Path("pyproject.toml").read_text()
    match = re.search(r'^version = "(\d+\.\d+\.\d+)"', pyproject, re.MULTILINE)
    return match.group(1) if match else None


def get_docs_version() -> str | None:
    """Extract release version from docs/conf.py."""
    conf = Path("docs/conf.py").read_text()
    match = re.search(r'^release = "(\d+\.\d+\.\d+)"', conf, re.MULTILINE)
    return match.group(1) if match else None


def main() -> int:
    """Check version consistency across project files."""
    changelog_version = get_changelog_version()
    pyproject_version = get_pyproject_version()
    docs_version = get_docs_version()

    if not changelog_version:
        print("❌ Could not find version in CHANGELOG.md")
        return 1

    errors = []

    if pyproject_version != changelog_version:
        errors.append(
            f"  pyproject.toml: {pyproject_version} (expected {changelog_version})"
        )

    if docs_version != changelog_version:
        errors.append(
            f"  docs/conf.py:   {docs_version} (expected {changelog_version})"
        )

    if errors:
        print(f"❌ Version mismatch! CHANGELOG.md has version {changelog_version}")
        print("\nMismatched files:")
        for error in errors:
            print(error)
        print("\nPlease update all version numbers to match.")
        return 1

    print(f"✅ All versions match: {changelog_version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
