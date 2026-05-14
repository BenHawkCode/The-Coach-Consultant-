"""Shared constants + utilities for the YouTube competitor analysis skill."""
import os
import sys
import json
import pathlib
from datetime import datetime, timezone

# Resolve paths from this file (scripts/_shared.py) up to the skill root
SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DATA_DIR = SKILL_DIR / "data"
OUTPUTS_DIR = SKILL_DIR / "outputs"
PROJECT_ROOT = SKILL_DIR.parent.parent  # The Coach Consultant/
ENV_PATH = PROJECT_ROOT / ".env"

# Make sure data + outputs dirs exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def load_env():
    """Load key/value pairs from the project root .env."""
    env = {}
    if not ENV_PATH.exists():
        return env
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


ENV = load_env()


# The 10 selected channels, mirroring competitor-list.md.
# All 10 also appear in 2-instagram/ig-competitor-analysis/competitor-list.md
# so the same competitor universe is tracked across IG and YouTube.
CHANNELS = [
    {"handle": "@AlexHormozi", "name": "Alex Hormozi", "tier": 1},
    {"handle": "@DanMartell", "name": "Dan Martell", "tier": 1},
    {"handle": "@ImanGadzhi", "name": "Iman Gadzhi", "tier": 1},
    {"handle": "@RussellBrunson", "name": "Russell Brunson", "tier": 1},
    {"handle": "@LeilaHormozi", "name": "Leila Hormozi", "tier": 1},
    {"handle": "@myrongolden", "name": "Myron Golden", "tier": 1},
    {"handle": "@BrendonBurchard", "name": "Brendon Burchard", "tier": 1},
    {"handle": "@aliabdaal", "name": "Ali Abdaal", "tier": 2},
    {"handle": "@garyvee", "name": "Gary Vaynerchuk", "tier": 2},
    {"handle": "@JamesSinclairEntrepreneur", "name": "James Sinclair", "tier": 5},
]


# The six new IP pain layers (from docs/new-ip/06-pain-isolation.md)
PAIN_LAYERS = [
    "guesswork_tax",
    "bottleneck_identity",
    "ai_era_anxiety",
    "trust_trauma",
    "plate_anxiety",
    "partner_pressure",
    "no_anchor",
]

# Channels used for the Ben Video Idea Bank brief (subset of CHANNELS).
# All 5 are in the main CHANNELS list. Picked for ICP fit + Ben's preferred competitors.
IDEA_BANK_HANDLES = [
    "@AlexHormozi",
    "@DanMartell",
    "@ImanGadzhi",
    "@aliabdaal",
    "@JamesSinclairEntrepreneur",
]


def today_str():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_json(path: pathlib.Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))


def read_json(path: pathlib.Path, default=None):
    if not path.exists():
        return default if default is not None else None
    return json.loads(path.read_text())
