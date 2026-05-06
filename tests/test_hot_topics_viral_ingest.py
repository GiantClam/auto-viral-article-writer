import json
from pathlib import Path

from tools.hot_topics_viral_ingest import ingest_hot_topics


def test_ingests_high_signal_items_only(tmp_path):
    source = tmp_path / "hot.json"
    source.write_text(
        json.dumps(
            [
                {"title": "AI Agent can deploy websites", "score": 120, "url": "https://example.com/a", "source": "HN"},
                {"title": "Small update", "score": 3, "url": "https://example.com/b", "source": "HN"},
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    kb_dir = tmp_path / "kb"
    result = ingest_hot_topics([str(source)], str(kb_dir), min_score=50)

    assert result["ingested"] == 1
    records = [json.loads(line) for line in (kb_dir / "patterns.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(records) == 1
    assert records[0]["title"] == "AI Agent can deploy websites"
    assert records[0]["viral_elements"]["title_formula"]


def test_skips_duplicate_urls(tmp_path):
    source = tmp_path / "hot.json"
    source.write_text(
        json.dumps(
            [
                {"title": "AI Agent story", "score": 100, "url": "https://example.com/a", "source": "HN"},
                {"title": "AI Agent story again", "score": 99, "url": "https://example.com/a", "source": "HN"},
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    kb_dir = tmp_path / "kb"
    result = ingest_hot_topics([str(source)], str(kb_dir), min_score=50)

    assert result["ingested"] == 1
    assert result["skipped_duplicates"] == 1
