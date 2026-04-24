"""Preset prompt templates for the Preset Style mode.

Each template is a format string with `{title}` as the required placeholder
and `{extra_instructions}` as an optional placeholder appended at the end.

All presets target 1280x720 YouTube thumbnails with the provided face image.
"""

STYLE_PRESETS: dict[str, str] = {
    "hormozi_bold": (
        "Create a 1280x720 YouTube thumbnail in the Alex Hormozi style. "
        "Large, bold, centered sans-serif text reading exactly: \"{title}\". "
        "High contrast. The person from the provided face image is prominently "
        "positioned on one side (not centered). Saturated solid background. "
        "No gradients, no busy patterns. {extra_instructions}"
    ),
    "mrbeast_reaction": (
        "Create a 1280x720 YouTube thumbnail in the MrBeast style. "
        "The person from the provided face image has a shocked, wide-eyed expression. "
        "Bright, saturated background. Large bold title text: \"{title}\". "
        "Include a red circle or arrow annotation drawing attention to an element. "
        "{extra_instructions}"
    ),
    "podcast_split": (
        "Create a 1280x720 YouTube thumbnail in podcast-style split layout. "
        "Left half: the person from the provided face image, well-lit, looking serious. "
        "Right half: large bold title text on a solid dark background reading: \"{title}\". "
        "Minimal other elements. {extra_instructions}"
    ),
    "minimal_text": (
        "Create a 1280x720 YouTube thumbnail with a clean, minimal aesthetic. "
        "The person from the provided face image is prominent and well-lit. "
        "Small, understated title text at the bottom: \"{title}\". "
        "Plain neutral background. No annotations, no clutter. {extra_instructions}"
    ),
    "alex_hormozi_black": (
        "Create a 1280x720 YouTube thumbnail with an all-black background. "
        "Large white bold sans-serif text reading exactly: \"{title}\". "
        "A cutout of the person from the provided face image is placed to one side, "
        "with sharp edges and no background halo. Extremely high contrast. "
        "{extra_instructions}"
    ),
}

PRESET_LABELS: dict[str, str] = {
    "hormozi_bold": "Hormozi Bold",
    "mrbeast_reaction": "MrBeast Reaction",
    "podcast_split": "Podcast Split",
    "minimal_text": "Minimal Text",
    "alex_hormozi_black": "Alex Hormozi Black",
}


def render_preset(preset_key: str, title: str, extra_instructions: str = "") -> str:
    """Return the rendered preset prompt for a given key.

    Raises KeyError if preset_key is not defined.
    """
    template = STYLE_PRESETS[preset_key]
    return template.format(title=title, extra_instructions=extra_instructions).strip()
