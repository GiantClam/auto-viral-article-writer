import subprocess
import sys
from pathlib import Path


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _build_sample_repo(root: Path) -> None:
    _write(
        root / "README.md",
        "\n".join(
            [
                "![Skills](https://img.shields.io/badge/Skills-2-10B981?style=for-the-badge)",
                "![Skills](https://img.shields.io/badge/Skills-2-10B981?style=for-the-badge)",
                "- 技能展示页：`docs/skills/README.md`",
                "- Changelog: `CHANGELOG.md`",
            ]
        ),
    )
    _write(
        root / "README.en.md",
        "\n".join(
            [
                "![Skills](https://img.shields.io/badge/Skills-2-10B981?style=for-the-badge)",
                "- Skill showcase pages: `docs/skills/README.md`",
                "- Changelog: `CHANGELOG.md`",
            ]
        ),
    )
    _write(root / "MANIFEST.txt", "\n".join(["skills/foo/SKILL.md", "skills/bar/SKILL.md", "docs/skills/README.md", "docs/skills/foo.md", "docs/skills/bar.md"]))
    _write(root / "skills/foo/SKILL.md", "---\nname: foo\n---\n")
    _write(root / "skills/bar/SKILL.md", "---\nname: bar\n---\n")
    _write(root / "docs/skills/README.md", "- `foo.md`\n- `bar.md`\n")
    _write(root / "docs/skills/foo.md", "# foo\n")
    _write(root / "docs/skills/bar.md", "# bar\n")
    _write(root / "docs/overview/article-artifact-family.md", "# family\n")
    _write(root / "docs/overview/slug-rules.md", "# slug\n")
    _write(root / "docs/overview/skill-package-overview.md", "# overview\n")
    _write(root / "CHANGELOG.md", "# changelog\n")


def test_repo_consistency_checker_passes_for_consistent_repo(tmp_path: Path):
    repo = tmp_path / "repo"
    _build_sample_repo(repo)

    result = subprocess.run(
        [sys.executable, "tools/repo_consistency.py", str(repo)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_repo_consistency_checker_reports_missing_showcase_doc(tmp_path: Path):
    repo = tmp_path / "repo"
    _build_sample_repo(repo)
    (repo / "docs/skills/bar.md").unlink()

    result = subprocess.run(
        [sys.executable, "tools/repo_consistency.py", str(repo)],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "docs/skills/bar.md" in (result.stdout + result.stderr)


def test_repo_consistency_checker_reports_readme_en_badge_mismatch(tmp_path: Path):
    repo = tmp_path / "repo"
    _build_sample_repo(repo)
    (repo / "README.en.md").write_text(
        "\n".join(
            [
                "![Skills](https://img.shields.io/badge/Skills-5-10B981?style=for-the-badge)",
                "- Skill showcase pages: `docs/skills/README.md`",
            ]
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, "tools/repo_consistency.py", str(repo)],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "README.en.md badge says 5 skills" in (result.stdout + result.stderr)


def test_repo_consistency_checker_reports_missing_core_overview_doc(tmp_path: Path):
    repo = tmp_path / "repo"
    _build_sample_repo(repo)
    (repo / "docs/overview/slug-rules.md").unlink()

    result = subprocess.run(
        [sys.executable, "tools/repo_consistency.py", str(repo)],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "docs/overview/slug-rules.md" in (result.stdout + result.stderr)
