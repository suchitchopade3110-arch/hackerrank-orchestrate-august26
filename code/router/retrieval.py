"""Evidence retrieval (spec §8 retrieval). Two-tier, in-memory.

Tier 1: same-sender history (last few messages + how the user reacted).
Tier 2: if sparse, TF-IDF / small-embedding cosine over this user's history.

The LLM may ONLY cite IDs that this module returned — enforced later in
schema.finalize via the retrieved-id set.
"""

import pandas as pd

from .data_loader import MessageContext
from . import config


class EvidenceRetriever:
    def __init__(self, message_history: pd.DataFrame, message_events: pd.DataFrame):
        # TODO: keep handles; optionally pre-fit a TF-IDF matrix over message_text
        self._history = message_history
        self._events = message_events

    def retrieve(self, ctx: MessageContext) -> list[dict]:
        """Return candidate evidence rows (id, text, reactions), recency-sorted.
        Tier 1 first; fall back to Tier 2 if fewer than config.SPARSE_HISTORY."""
        raise NotImplementedError

    @staticmethod
    def ids(candidates: list[dict]) -> set[str]:
        """The retrieved-id set used to validate the LLM's evidence claims."""
        # TODO: {c["message_id"] for c in candidates}
        raise NotImplementedError
