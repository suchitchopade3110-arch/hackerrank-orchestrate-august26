"""Types and the one central validation point (spec §1 enforcement).

`Decision` is the internal representation passed between stages.
`OutputRow` is the validated, on-disk shape. Enum + evidence checks live ONLY
here — no other stage re-implements them.
"""

from dataclasses import dataclass, field
from typing import Optional

from pydantic import BaseModel, field_validator

from . import config


@dataclass
class Decision:
    """Internal, pre-validation. Carries provenance so every row is auditable."""
    action: str
    message_type: str
    reason: str
    confidence: float
    evidence_message_ids: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)   # e.g. "scam", "alert"
    source: str = ""                                  # e.g. "gate:A1", "llm", "cap:B7"


class OutputRow(BaseModel):
    """Validated output. Bad enum/evidence -> raise, caller falls back."""
    message_id: str
    action: str
    message_type: str
    reason: str
    confidence: float
    evidence_message_ids: str   # "none" or "id;id;id"

    @field_validator("action")
    @classmethod
    def _action_enum(cls, v: str) -> str:
        # TODO: assert v in config.ACTIONS
        raise NotImplementedError

    @field_validator("message_type")
    @classmethod
    def _type_enum(cls, v: str) -> str:
        # TODO: assert v in config.MESSAGE_TYPES
        raise NotImplementedError

    @field_validator("reason")
    @classmethod
    def _reason_nonempty(cls, v: str) -> str:
        # TODO: assert non-empty, references a concrete signal (spec §1)
        raise NotImplementedError


def finalize(message_id: str, decision: Decision, retrieved_ids: set[str]) -> OutputRow:
    """Turn a Decision into a validated OutputRow.

    - Drops any evidence ID not in `retrieved_ids` (hallucination guard, spec §1).
    - Enforces the scam invariant one last time (spec §2 rule 3).
    - On validation failure, fall back to unknown/digest rather than crashing.
    """
    # TODO: filter evidence against retrieved_ids; join with ';' or 'none'
    # TODO: if "scam" in decision.flags and decision.action == "notify": force mute
    # TODO: build OutputRow(...); on ValidationError return safe fallback row
    raise NotImplementedError
