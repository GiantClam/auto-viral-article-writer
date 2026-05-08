#!/usr/bin/env python3

import re
import sys
from pathlib import Path


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _skill_names(skills_dir: Path) -> list[str]:
    names = []
    for skill_md in skills_dir.glob("*/SKILL.md"):
        names.append(skill_md.parent.name)
    return sorted(names)


def _readme_skill_count(readme: Path) -> int | None:
    text = _read(readme)
    match = re.search(r"Skills-(\d+)-", text)
    if not match:
        return None
    return int(match.group(1))


def check_repo(root: Path) -> list[str]:
    errors: list[str] = []

    skills_dir = root / "skills"
    manifest = root / "MANIFEST.txt"
    readme = root / "README.md"
    readme_en = root / "README.en.md"
    showcase_index = root / "docs" / "skills" / "README.md"
    overview_dir = root / "docs" / "overview"

    skill_names = _skill_names(skills_dir)

    if readme.exists():
        expected_count = _readme_skill_count(readme)
        if expected_count is not None and expected_count != len(skill_names):
            errors.append(
                f"README.md badge says {expected_count} skills but found {len(skill_names)} directory-style skills"
            )

    if readme_en.exists():
        expected_count = _readme_skill_count(readme_en)
        if expected_count is not None and expected_count != len(skill_names):
            errors.append(
                f"README.en.md badge says {expected_count} skills but found {len(skill_names)} directory-style skills"
            )

    manifest_text = _read(manifest) if manifest.exists() else ""
    showcase_text = _read(showcase_index) if showcase_index.exists() else ""

    for path in [
        overview_dir / "article-artifact-family.md",
        overview_dir / "slug-rules.md",
        overview_dir / "skill-package-overview.md",
    ]:
        if not path.exists():
            errors.append(f"Missing core overview doc: {path.relative_to(root).as_posix()}")

    for name in skill_names:
        showcase_path = f"docs/skills/{name}.md"
        manifest_skill_path = f"skills/{name}/SKILL.md"

        if showcase_path not in manifest_text:
            errors.append(f"Missing manifest entry: {showcase_path}")
        if manifest_skill_path not in manifest_text:
            errors.append(f"Missing manifest entry: {manifest_skill_path}")
        if f"`{name}.md`" not in showcase_text:
            errors.append(f"Missing showcase index entry: {showcase_path}")
        if not (root / "docs" / "skills" / f"{name}.md").exists():
            errors.append(f"Missing showcase doc: {showcase_path}")

    return errors


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    errors = check_repo(root)

    if errors:
        for error in errors:
            print(error)
        return 1

    print("Repository consistency OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
