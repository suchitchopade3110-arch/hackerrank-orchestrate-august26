"""Signal scoring (spec §5). These are INPUTS the LLM reasons over, not answers,
and none are output columns. Keep the math rough — don't over-tune weights.
"""

from dataclasses import dataclass

from .data_loader import MessageContext


@dataclass
class Features:
    relationship_strength: float   # 0..1
    interruption_cost: float       # 0..1
    priority_score: int            # 0..100 (internal tiebreaker + digest ranking)


def compute_features(ctx: MessageContext, evidence: list[dict]) -> Features:
    rs = _relationship_strength(ctx, evidence)
    ic = _interruption_cost(ctx)
    ps = _priority_score(ctx, rs)
    return Features(rs, ic, ps)


def _relationship_strength(ctx: MessageContext, evidence: list[dict]) -> float:
    """Reply frequency + speed to this sender, shared groups/role, open history."""
    raise NotImplementedError


def _interruption_cost(ctx: MessageContext) -> float:
    """DND position + today's notification load (daily_notification_summary)."""
    raise NotImplementedError


def _priority_score(ctx: MessageContext, relationship_strength: float) -> int:
    """Rough 0..100 blend of relationship, sender-relevance, historical engagement
    with this message_type, and urgency/deadline keywords. Tiebreaker only."""
    raise NotImplementedError
