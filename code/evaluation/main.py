"""Evaluation (spec §9). Runs the SAME pipeline against the 30 labeled rows in
sample_messages.csv and prints one report. Re-run on every rule/prompt change.

Usage:
    python code/evaluation/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # make `router` importable

from router import config
from router.data_loader import load_all, build_context
from router.retrieval import EvidenceRetriever
from router.pipeline import route_message


def evaluate() -> None:
    tables = load_all(config.DATASET_DIR)
    labeled = tables["sample_messages"]        # held-out set (also used for few-shot)
    retriever = EvidenceRetriever(tables["message_history"], tables["message_events"])

    preds, golds = [], []
    for row in labeled.to_dict("records"):
        ctx = build_context(row, tables)
        # NOTE: exclude this row from its own few-shot set to avoid leakage.
        preds.append(route_message(ctx, retriever, few_shot=[]).model_dump())
        golds.append(row)

    # TODO: report all five criteria:
    _action_accuracy_and_confusion(preds, golds)   # 1: exact match + confusion matrix
    _message_type_accuracy(preds, golds)           # 2: exact match, per-type
    _reason_sanity(preds)                          # 3: non-empty, concrete, consistent
    _evidence_validity(preds, tables)              # 4: exists + retrieved; overlap w/ labels
    _confidence_calibration(preds, golds)          # 5: confidence vs correctness
    _print_disagreements(preds, golds)             # list the rows that differ


def _action_accuracy_and_confusion(preds, golds): raise NotImplementedError
def _message_type_accuracy(preds, golds): raise NotImplementedError
def _reason_sanity(preds): raise NotImplementedError
def _evidence_validity(preds, tables): raise NotImplementedError
def _confidence_calibration(preds, golds): raise NotImplementedError
def _print_disagreements(preds, golds): raise NotImplementedError


if __name__ == "__main__":
    evaluate()
