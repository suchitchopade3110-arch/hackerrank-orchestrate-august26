"""Guardrail Layer A — deterministic gates (spec §2). No LLM.

Checked IN ORDER. First match short-circuits and returns a Decision; the rest
are skipped. If nothing fires, returns None and the message goes to the LLM path.

Order is load-bearing — do not reorder.
"""

from typing import Optional

from .schema import Decision
from .data_loader import MessageContext
from . import config


def run_gates(ctx: MessageContext) -> Optional[Decision]:
    """Run A1..A7 in order; return first Decision or None."""
    for gate in (_a1_scam_hardmute, _a2_first_contact_sensitive, _a4_group_muted,
                 _a5_promo_opted_out, _a6_dnd_window):
        d = gate(ctx)
        if d is not None:
            # A3 emergency override may lift A4/A6 (not A1/A2). Apply here.
            return _a3_emergency_override(ctx, d)
    return None


def _a1_scam_hardmute(ctx: MessageContext) -> Optional[Decision]:
    """Unverified sender + domain mismatch -> mute/scam. Hard, not scored."""
    # TODO: if not verified and domain_mismatch: Decision(mute, scam, flags=["scam"])
    raise NotImplementedError


def _a2_first_contact_sensitive(ctx: MessageContext) -> Optional[Decision]:
    """First contact + money/OTP/credential ask -> mute + visible alert."""
    # TODO: if is_first_contact and sensitive_action_detected(ctx):
    #       Decision(mute, scam, flags=["scam", "alert"])
    raise NotImplementedError


def _a3_emergency_override(ctx: MessageContext, base: Decision) -> Decision:
    """May force notify through DND/muted-group ONLY if base isn't scam-flagged
    and there's no money/OTP/credential ask. Weakest rule (keyword-based)."""
    # TODO: guard on "scam" not in base.flags and not sensitive_action_detected(ctx)
    raise NotImplementedError


def _a4_group_muted(ctx: MessageContext) -> Optional[Decision]:
    """group_muted_by_user -> mute (unless A3 lifts it)."""
    raise NotImplementedError


def _a5_promo_opted_out(ctx: MessageContext) -> Optional[Decision]:
    """Promotions opted out for this business -> mute. No override, ever."""
    raise NotImplementedError


def _a6_dnd_window(ctx: MessageContext) -> Optional[Decision]:
    """created_at within DND window -> suppress notify, route to digest."""
    raise NotImplementedError


def sensitive_action_detected(ctx: MessageContext) -> bool:
    """Keyword scan for payment/OTP/credential asks (config.SENSITIVE_ACTION_HINTS).
    Reads message_text for DETECTION only — never for trusting its claims."""
    raise NotImplementedError
