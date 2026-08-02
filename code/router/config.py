"""Central config: enums, thresholds, paths, env. Nothing decides here; this is
the single source of truth every other module imports from."""

import os

# --- Closed enums (spec §1). Validated once, centrally, in schema.py. ---
ACTIONS = ("notify", "digest", "mute")
MESSAGE_TYPES = (
    "personal", "urgent", "event", "payment", "business_update",
    "promotion", "greeting", "forward", "spam", "scam", "unknown",
)

# --- Thresholds (tune during calibration; keep rough). ---
CONFIDENCE_FLOOR = 0.75      # below this -> default digest (cap B: floor)
FORWARD_DAMPEN_COUNT = 5     # forwarded_count above this -> never notify (cap B)
SPARSE_HISTORY = 3           # fewer same-sender msgs than this -> similarity fallback

# --- Provider ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")  # never hardcode
GEMINI_MODEL = "gemini-2.0-flash"                  # confirm exact model at build
GEMINI_TEMPERATURE = 0

# --- Paths (confirm against the real dataset/ folder before relying on these). ---
DATASET_DIR = os.environ.get("DATASET_DIR", "dataset")
OUTPUT_PATH = os.path.join(DATASET_DIR, "output.csv")

# Sensitive-action keywords for the first-contact gate (gate A1).
# NOTE: keep this list under review; it's the weakest, keyword-based part.
SENSITIVE_ACTION_HINTS = ("otp", "password", "login code", "verify", "pay", "upi", "qr")
