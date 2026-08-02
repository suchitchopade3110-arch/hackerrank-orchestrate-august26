"""The single Gemini call (spec §6).

Exactly ONE call per undecided message: temperature=0, JSON-schema-constrained.
Image/voice bytes go NATIVELY into the same call — no separate OCR/ASR stage.
Features + evidence are passed as inputs to reason over, not as answers.

If GEMINI_API_KEY is unset, `decide` uses `_offline_stub` so the whole pipeline
still runs end-to-end (useful for testing the non-LLM parts).
"""

import json
from typing import Optional

from .schema import Decision
from .data_loader import MessageContext
from .features import Features
from . import config


# JSON schema the model must fill (mirrors the output contract).
RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "action": {"type": "string", "enum": list(config.ACTIONS)},
        "message_type": {"type": "string", "enum": list(config.MESSAGE_TYPES)},
        "reason": {"type": "string"},
        "confidence": {"type": "number"},
        "evidence_message_ids": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["action", "message_type", "reason", "confidence", "evidence_message_ids"],
}


def build_prompt(ctx: MessageContext, feats: Features, evidence: list[dict],
                 few_shot: list[dict]) -> str:
    """Assemble the prompt: user/sender context, features, evidence, few-shot
    style examples (tone/format only — never a lookup table). message_text is
    included but explicitly marked untrusted."""
    raise NotImplementedError


def decide(ctx: MessageContext, feats: Features, evidence: list[dict],
           few_shot: list[dict], media_bytes: Optional[bytes] = None) -> Decision:
    """One schema-constrained Gemini call -> Decision. Falls back to stub if no key."""
    if not config.GEMINI_API_KEY:
        return _offline_stub(ctx, feats, evidence)
    # TODO: build client; send text + media in ONE call with response_schema;
    #       temperature=0; parse JSON; return Decision(..., source="llm")
    raise NotImplementedError


def _offline_stub(ctx: MessageContext, feats: Features, evidence: list[dict]) -> Decision:
    """Deterministic placeholder so the pipeline runs with no API key.
    Never used when GEMINI_API_KEY is set."""
    # TODO: cheap heuristic (e.g. priority_score threshold) -> Decision(source="stub")
    raise NotImplementedError
