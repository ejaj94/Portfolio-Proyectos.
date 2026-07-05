"""
config.py — Application Configuration (SRP)
============================================
Centralises all runtime paths and environment variables.
No hard-coded user paths. Everything resolves dynamically
or from a .env file sitting next to this package.
"""
import os


def _load_env(env_path: str) -> None:
    """Parse a .env file and inject variables into os.environ."""
    if not os.path.exists(env_path):
        return
    with open(env_path, "r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


# ── Locate project root (two levels up from this file) ──────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(_HERE)

# Load .env if present
_load_env(os.path.join(ROOT_DIR, ".env"))

# ── Resolved paths ───────────────────────────────────────────────────────────
ASSETS_DIR: str = os.path.join(ROOT_DIR, "assets")
OUTPUT_DIR: str = os.environ.get(
    "OUTPUT_DIR",
    os.path.join(os.path.expanduser("~"), "Desktop"),
)
DEFAULT_PHOTO_PATH: str = os.path.join(ASSETS_DIR, "profile.jpg")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
