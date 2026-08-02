"""Load every CSV and assemble a structured context per message.

STEP 1 of the build: before implementing anything, print the real column names
of each CSV and confirm them against the spec. Do NOT trust the field names
below blindly — adapt to the actual files.

Zero-trust rule (spec §9): trust only these structured joins, never claims
written inside message_text.
"""

from dataclasses import dataclass
from typing import Optional

import pandas as pd

from . import config


# Files expected under DATASET_DIR (confirm names in step 1).
CSV_FILES = (
    "messages", "sample_messages", "users", "groups", "group_members",
    "business_accounts", "user_business_history", "message_history",
    "message_events", "images", "voice_notes", "daily_notification_summary",
)


@dataclass
class MessageContext:
    """Everything the pipeline needs about ONE message, pre-joined.
    Populated from structured metadata only."""
    message_id: str
    user_id: str
    conversation_type: str            # personal | group | business
    # sender / group / business facts (verified, domain match, muted, DND, etc.)
    sender: dict
    group: dict
    business: dict
    user: dict
    media: dict                       # media_type, media_id, file path
    forwarded_count: int
    raw: dict                         # raw message row (incl. message_text — untrusted)


def load_all(dataset_dir: str = config.DATASET_DIR) -> dict[str, pd.DataFrame]:
    """Read every CSV into a dict of DataFrames. In step 1, also print
    df.columns for each so real schemas are confirmed."""
    # TODO: pd.read_csv for each in CSV_FILES; print columns; return dict
    raise NotImplementedError


def build_context(message_row: dict, tables: dict[str, pd.DataFrame]) -> MessageContext:
    """Join one message against users/groups/business/history to build context.
    Compute derived flags here (domain_mismatch, group_muted, dnd_now,
    is_first_contact, promo_opted_out) so gates stay pure lookups."""
    # TODO: resolve sender/group/business by ids; attach media path; derive flags
    raise NotImplementedError
