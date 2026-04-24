"""Streamlit UI for the Thumbnail Generator."""
from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from PIL import Image

from thumbnail_engine import load_recent_generations

ROOT_DIR = Path(__file__).parent
FACE_LIBRARY_DIR = ROOT_DIR / "assets" / "ben-faces"

load_dotenv(ROOT_DIR / ".env")

st.set_page_config(
    page_title="TCC Thumbnail Generator",
    page_icon="🎬",
    layout="wide",
)


def _api_key_present() -> bool:
    return bool(os.environ.get("GEMINI_API_KEY"))


def _load_face_library() -> list[Path]:
    if not FACE_LIBRARY_DIR.exists():
        return []
    return sorted(
        p for p in FACE_LIBRARY_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    )


def _save_uploaded_face(uploaded_file) -> Path:
    FACE_LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
    target = FACE_LIBRARY_DIR / uploaded_file.name
    target.write_bytes(uploaded_file.getbuffer())
    return target


def render_sidebar() -> Path | None:
    st.sidebar.header("Face Library")

    faces = _load_face_library()
    if not faces:
        st.sidebar.warning("No faces in library. Upload one below.")

    selected_name = st.sidebar.radio(
        "Select a face",
        options=[p.name for p in faces],
        index=0 if faces else None,
        key="selected_face",
    ) if faces else None

    for face in faces:
        st.sidebar.image(str(face), caption=face.name, width=120)

    uploaded = st.sidebar.file_uploader(
        "Upload new face",
        type=["jpg", "jpeg", "png", "webp"],
        key="face_uploader",
    )
    if uploaded is not None:
        saved = _save_uploaded_face(uploaded)
        st.sidebar.success(f"Saved {saved.name}")
        st.rerun()

    st.sidebar.divider()
    render_history_sidebar()

    if selected_name is None:
        return None
    return FACE_LIBRARY_DIR / selected_name


def render_history_sidebar() -> None:
    st.sidebar.header("Recent generations")
    entries = load_recent_generations(limit=10)
    if not entries:
        st.sidebar.caption("No generations yet.")
        return
    for entry in entries:
        with st.sidebar.expander(f"{entry['timestamp'][:19]} — {entry['title'][:40]}"):
            st.caption(f"Mode: {entry['mode']}")
            for out_path in entry["output_paths"]:
                if out_path.exists():
                    st.image(str(out_path), width=200)


def main() -> None:
    st.title("YouTube Thumbnail Generator")
    st.caption("Gemini 3.1 Flash Image Preview — for Ben Hawksworth")

    if not _api_key_present():
        st.error(
            "`GEMINI_API_KEY` is not set. Copy `.env.example` to `.env` and "
            "add your key, then restart the app."
        )
        st.stop()

    selected_face = render_sidebar()

    if selected_face is None:
        st.info("Add a face to the library (sidebar) to get started.")
        return

    st.write(f"**Selected face:** `{selected_face.name}`")
    st.image(str(selected_face), width=200)
    st.caption("Tabs and generation are wired up in the next task.")


if __name__ == "__main__":
    main()
