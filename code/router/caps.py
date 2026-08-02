"""Guardrail Layer B — post-hoc caps (spec §3). Applied to the LLM's Decision.
Can only make the action MORE restrictive, never less.
"""

from .schema import Decision
from .data_loader import MessageContext
from .features import Features
from . import config

_RANK = {"mute": 0, "digest": 1, "notify": 2}


def apply_caps(d: Decision, ctx: MessageContext, feats: Features) -> Decision:
    """Run all caps; each may lower the action. Order among caps doesn't matter
    since they only ratchet downward."""
    d = _b7_new_sender_ceiling(d, ctx)
    d = _b8_forward_dampening(d, ctx)
    d = _b9_confidence_floor(d)
    # B10 (ignore in-message instructions) is enforced upstream by never trusting
    # message_text claims — nothing to apply post-hoc here.
    return d


def _cap_to(d: Decision, ceiling: str, why: str) -> Decision:
    """Lower d.action to `ceiling` if it currently outranks it."""
    # TODO: if _RANK[d.action] > _RANK[ceiling]: set action, append why to source
    raise NotImplementedError


def _b7_new_sender_ceiling(d: Decision, ctx: MessageContext) -> Decision:
    """New/unverified sender -> max digest, never notify (scoped to sender)."""
    raise NotImplementedError


def _b8_forward_dampening(d: Decision, ctx: MessageContext) -> Decision:
    """forwarded_count > threshold -> never notify (unless emergency already fired)."""
    raise NotImplementedError


def _b9_confidence_floor(d: Decision) -> Decision:
    """confidence < floor -> default digest, never mute."""
    raise NotImplementedError
