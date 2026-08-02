"""CLI entry point. Loads the dataset, routes every message, writes output.csv.

Usage:
    GEMINI_API_KEY=... DATASET_DIR=dataset python code/main.py
"""

import csv

from router import config
from router.data_loader import load_all, build_context
from router.retrieval import EvidenceRetriever
from router.pipeline import route_message

OUTPUT_COLUMNS = [
    "message_id", "action", "message_type", "reason", "confidence", "evidence_message_ids",
]


def load_few_shot(tables) -> list[dict]:
    """A few sample_messages.csv rows for tone/format only — NEVER a lookup table."""
    # TODO: take 2-3 diverse rows (one notify/digest/mute) as style examples
    raise NotImplementedError


def main() -> None:
    tables = load_all(config.DATASET_DIR)
    retriever = EvidenceRetriever(tables["message_history"], tables["message_events"])
    few_shot = load_few_shot(tables)

    rows = []
    for msg in tables["messages"].to_dict("records"):
        ctx = build_context(msg, tables)
        out = route_message(ctx, retriever, few_shot)
        rows.append(out.model_dump())

    # One row per input message — no drops, no dupes (spec §1).
    assert len(rows) == len(tables["messages"]), "row count must match messages.csv"

    with open(config.OUTPUT_PATH, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows -> {config.OUTPUT_PATH}")


if __name__ == "__main__":
    main()
