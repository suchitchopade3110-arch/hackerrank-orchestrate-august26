"""Per-message orchestration. This is the spine — the fixed order the whole
design depends on. Read top-to-bottom, it IS the pipeline:

    gates (Layer A) --short-circuit--> done
        else: retrieve -> features -> Gemini -> caps (Layer B) -> validate -> row
"""

from .schema import Decision, OutputRow, finalize
from .data_loader import MessageContext
from .retrieval import EvidenceRetriever
from .features import compute_features
from .gates import run_gates
from .caps import apply_caps
from . import gemini_call


def route_message(ctx: MessageContext, retriever: EvidenceRetriever,
                  few_shot: list[dict]) -> OutputRow:
    # --- Layer A: deterministic, may short-circuit ---
    decision = run_gates(ctx)
    if decision is not None:
        return finalize(ctx.message_id, decision, retrieved_ids=set())

    # --- Undecided middle: retrieve -> score -> one Gemini call ---
    evidence = retriever.retrieve(ctx)
    feats = compute_features(ctx, evidence)
    media_bytes = None  # TODO: load image/voice bytes when ctx.media present
    decision = gemini_call.decide(ctx, feats, evidence, few_shot, media_bytes)

    # --- Layer B: post-hoc caps (ratchet down only) ---
    decision = apply_caps(decision, ctx, feats)

    return finalize(ctx.message_id, decision, retrieved_ids=EvidenceRetriever.ids(evidence))
