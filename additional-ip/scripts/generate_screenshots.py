"""
Generate pixel-accurate mockup screenshots matching Claude's actual interface.
Based on real screenshots of the Claude app provided by user.
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "screenshots")
FONTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "fonts")

os.makedirs(ASSETS_DIR, exist_ok=True)

def get_font(size, bold=False):
    fname = "Poppins-Bold.ttf" if bold else "Poppins-Regular.ttf"
    return ImageFont.truetype(os.path.join(FONTS_DIR, fname), size)

def get_font_medium(size):
    return ImageFont.truetype(os.path.join(FONTS_DIR, "Poppins-Medium.ttf"), size)

def get_font_semibold(size):
    return ImageFont.truetype(os.path.join(FONTS_DIR, "Poppins-SemiBold.ttf"), size)

# ─── Claude's ACTUAL UI colors (from real screenshots) ───
BG = "#F5F4EF"              # Warm cream background
SIDEBAR_BG = "#F5F4EF"      # Sidebar is same cream, not dark
WHITE = "#FFFFFF"
BLACK = "#1A1A1A"
TEXT_PRIMARY = "#1A1A1A"
TEXT_SECONDARY = "#6B6963"
TEXT_MUTED = "#9B9890"
BORDER = "#E5E3DE"
BORDER_LIGHT = "#EDEBE6"
INPUT_BG = "#FFFFFF"
CARD_BG = "#FFFFFF"
TAB_BAR_BG = "#ECEAE4"
TAB_ACTIVE_BG = "#FFFFFF"
BUTTON_BLACK = "#1A1A1A"
BLUE_LINK = "#4A6FA5"
BLUE_BAR = "#3B82F6"
CALLOUT_RED = "#DC4A3C"
CALLOUT_BG = "#FEF0EE"
STEP_BADGE = "#1A1A1A"
SIDEBAR_DIVIDER = "#E5E3DE"
ICON_COLOR = "#6B6963"
SEARCH_BG = "#FFFFFF"
SEARCH_BORDER = "#4A6FA5"


def rounded_rect(draw, xy, radius, fill):
    x0, y0, x1, y1 = xy
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.pieslice([x0, y0, x0 + 2*radius, y0 + 2*radius], 180, 270, fill=fill)
    draw.pieslice([x1 - 2*radius, y0, x1, y0 + 2*radius], 270, 360, fill=fill)
    draw.pieslice([x0, y1 - 2*radius, x0 + 2*radius, y1], 90, 180, fill=fill)
    draw.pieslice([x1 - 2*radius, y1 - 2*radius, x1, y1], 0, 90, fill=fill)


def rounded_rect_outline(draw, xy, radius, outline, width=1):
    x0, y0, x1, y1 = xy
    # Top and bottom edges
    draw.rectangle([x0 + radius, y0, x1 - radius, y0 + width], fill=outline)
    draw.rectangle([x0 + radius, y1 - width, x1 - radius, y1], fill=outline)
    # Left and right edges
    draw.rectangle([x0, y0 + radius, x0 + width, y1 - radius], fill=outline)
    draw.rectangle([x1 - width, y0 + radius, x1, y1 - radius], fill=outline)
    # Corners
    draw.arc([x0, y0, x0 + 2*radius, y0 + 2*radius], 180, 270, fill=outline, width=width)
    draw.arc([x1 - 2*radius, y0, x1, y0 + 2*radius], 270, 360, fill=outline, width=width)
    draw.arc([x0, y1 - 2*radius, x0 + 2*radius, y1], 90, 180, fill=outline, width=width)
    draw.arc([x1 - 2*radius, y1 - 2*radius, x1, y1], 0, 90, fill=outline, width=width)


def draw_arrow(draw, start, end, color=CALLOUT_RED, width=3):
    draw.line([start, end], fill=color, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    al = 14
    aa = math.pi / 6
    x1 = end[0] - al * math.cos(angle - aa)
    y1 = end[1] - al * math.sin(angle - aa)
    x2 = end[0] - al * math.cos(angle + aa)
    y2 = end[1] - al * math.sin(angle + aa)
    draw.polygon([end, (x1, y1), (x2, y2)], fill=color)


def draw_callout_number(draw, pos, number, font):
    x, y = pos
    size = 26
    draw.ellipse([x, y, x + size, y + size], fill=CALLOUT_RED)
    bbox = font.getbbox(str(number))
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x + (size - tw) // 2, y + (size - th) // 2 - 2), str(number), fill=WHITE, font=font)


def draw_callout_label(draw, pos, text, font):
    x, y = pos
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad = 8
    rounded_rect(draw, (x, y, x + tw + pad * 2, y + th + pad * 2), 6, CALLOUT_BG)
    draw.text((x + pad, y + pad - 1), text, fill=CALLOUT_RED, font=font)


def draw_traffic_lights(draw, x, y):
    """macOS traffic light buttons."""
    colors = ["#FF5F57", "#FFBD2E", "#27C93F"]
    for i, c in enumerate(colors):
        draw.ellipse([x + i * 22, y, x + i * 22 + 14, y + 14], fill=c)


def draw_top_bar(draw, w):
    """Top bar with Chat | Cowork | Code tabs."""
    # Background
    draw.rectangle([0, 0, w, 44], fill=BG)
    # Divider
    draw.rectangle([0, 44, w, 45], fill=BORDER)

    # Traffic lights
    draw_traffic_lights(draw, 16, 15)

    # Navigation arrows
    draw.text((80, 11), "\u2190", fill=TEXT_MUTED, font=get_font(16))
    draw.text((108, 11), "\u2192", fill=TEXT_MUTED, font=get_font(16))

    # Center tabs: Chat | Cowork | Code
    tab_font = get_font_medium(13)
    tabs = ["Chat", "Cowork", "Code"]
    center_x = w // 2
    total_w = 220
    tx = center_x - total_w // 2

    # Tab container
    rounded_rect(draw, (tx - 4, 8, tx + total_w + 4, 38), 8, TAB_BAR_BG)

    tab_w = total_w // 3
    for i, tab in enumerate(tabs):
        tab_x = tx + i * tab_w
        bbox = tab_font.getbbox(tab)
        tw = bbox[2] - bbox[0]

        if i == 0:  # Chat is active
            rounded_rect(draw, (tab_x + 2, 10, tab_x + tab_w - 2, 36), 6, TAB_ACTIVE_BG)
            draw.text((tab_x + (tab_w - tw) // 2, 13), tab, fill=TEXT_PRIMARY, font=tab_font)
        else:
            draw.text((tab_x + (tab_w - tw) // 2, 13), tab, fill=TEXT_MUTED, font=tab_font)


def draw_sidebar(draw, w, h):
    """Claude's actual sidebar - light cream background."""
    sidebar_w = 265

    draw.rectangle([0, 45, sidebar_w, h], fill=SIDEBAR_BG)
    # Right border
    draw.rectangle([sidebar_w - 1, 45, sidebar_w, h], fill=BORDER)

    font_item = get_font(13)
    font_item_med = get_font_medium(13)

    # + New chat
    y = 58
    draw.text((32, y), "+", fill=TEXT_PRIMARY, font=get_font(14))
    draw.text((50, y + 1), "New chat", fill=TEXT_PRIMARY, font=font_item)

    # Search
    y += 34
    draw.text((32, y + 2), "\u26B2", fill=ICON_COLOR, font=get_font(12))  # magnifying glass approx
    draw.text((50, y), "Search", fill=TEXT_SECONDARY, font=font_item)

    # Customize
    y += 34
    draw.text((50, y), "Customize", fill=TEXT_SECONDARY, font=font_item)

    # Divider
    y += 38
    draw.rectangle([16, y, sidebar_w - 16, y + 1], fill=SIDEBAR_DIVIDER)

    # Chats
    y += 14
    draw.text((50, y), "Chats", fill=TEXT_SECONDARY, font=font_item)

    # Projects (highlighted)
    y += 34
    draw.text((50, y), "Projects", fill=TEXT_PRIMARY, font=font_item_med)

    # Artifacts
    y += 34
    draw.text((50, y), "Artifacts", fill=TEXT_SECONDARY, font=font_item)

    # Recents divider
    y += 42
    draw.text((16, y), "Recents", fill=TEXT_MUTED, font=get_font(11))

    # Recent chats list
    y += 26
    font_recent = get_font(12)
    recents = [
        "Getting started with Clau...",
        "Content strategy for Inst...",
        "Email sequence for laun...",
        "Client onboarding auto...",
        "YouTube script for coac...",
        "Sales page copy review...",
        "Weekly content calendar...",
        "Lead magnet ideas for...",
    ]
    for r in recents:
        draw.text((16, y), r, fill=TEXT_SECONDARY, font=font_recent)
        y += 28

    # User avatar at bottom
    avatar_y = h - 45
    # BH circle
    draw.ellipse([16, avatar_y, 42, avatar_y + 26], fill="#E8E6E0")
    draw.text((22, avatar_y + 4), "BH", fill=TEXT_SECONDARY, font=get_font(8, bold=True))
    draw.text((50, avatar_y - 2), "Your Name", fill=TEXT_PRIMARY, font=get_font(12))
    draw.text((50, avatar_y + 14), "Pro plan", fill=TEXT_MUTED, font=get_font(10))

    return sidebar_w


# ─── Screenshot 1: Projects page ───

def create_screenshot_1():
    w, h = 1100, 680
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)

    draw_top_bar(draw, w)
    sidebar_w = draw_sidebar(draw, w, h)

    content_x = sidebar_w + 40
    content_w = w - sidebar_w

    # "Projects" heading
    draw.text((content_x + 40, 70), "Projects", fill=TEXT_PRIMARY, font=get_font_semibold(24))

    # "+ New project" button (top right)
    btn_x = w - 190
    btn_y = 72
    rounded_rect(draw, (btn_x, btn_y, btn_x + 150, btn_y + 40), 8, BUTTON_BLACK)
    draw.text((btn_x + 14, btn_y + 10), "+ New project", fill=WHITE, font=get_font_medium(13))

    # Search bar
    search_y = 126
    rounded_rect(draw, (content_x + 40, search_y, w - 60, search_y + 44), 10, SEARCH_BG)
    rounded_rect_outline(draw, (content_x + 40, search_y, w - 60, search_y + 44), 10, SEARCH_BORDER, 2)
    draw.text((content_x + 72, search_y + 12), "Search projects...", fill=TEXT_MUTED, font=get_font(13))

    # Tabs: Your projects | Archived
    tab_y = search_y + 60
    draw.text((content_x + 40, tab_y), "Your projects", fill=TEXT_PRIMARY, font=get_font_medium(13))
    draw.rectangle([content_x + 40, tab_y + 22, content_x + 140, tab_y + 24], fill=TEXT_PRIMARY)
    draw.text((content_x + 160, tab_y), "Archived", fill=TEXT_MUTED, font=get_font(13))

    # Sort by
    draw.text((w - 200, tab_y), "Sort by", fill=TEXT_MUTED, font=get_font(12))
    draw.text((w - 148, tab_y), "Activity", fill=TEXT_PRIMARY, font=get_font_medium(12))
    draw.text((w - 85, tab_y + 2), "\u2304", fill=TEXT_PRIMARY, font=get_font(12))

    # Project cards - 2 column grid
    card_y = tab_y + 40
    card_gap = 16
    card_w = (content_w - 120 - card_gap) // 2
    card_h = 90

    projects = [
        ("Content Strategy", "Updated 2 days ago"),
        ("Email Marketing", "Updated 5 days ago"),
        ("Instagram Creator", "Updated 1 week ago"),
        ("YouTube Scripts", "Updated 1 week ago"),
        ("Sales Page Copy", "Updated 2 weeks ago"),
        ("Client Onboarding", "Updated 2 weeks ago"),
    ]

    for i, (name, updated) in enumerate(projects):
        col = i % 2
        row = i // 2
        cx = content_x + 40 + col * (card_w + card_gap)
        cy = card_y + row * (card_h + card_gap)

        rounded_rect(draw, (cx, cy, cx + card_w, cy + card_h), 10, CARD_BG)
        rounded_rect_outline(draw, (cx, cy, cx + card_w, cy + card_h), 10, BORDER, 1)

        draw.text((cx + 20, cy + 20), name, fill=TEXT_PRIMARY, font=get_font_medium(14))
        draw.text((cx + 20, cy + 50), updated, fill=TEXT_MUTED, font=get_font(11))

    # ─── Annotations ───
    font_num = get_font_semibold(13)
    font_lbl = get_font_semibold(11)

    # Callout 1: Projects in sidebar
    projects_y = 232  # approximate y of "Projects" in sidebar
    draw_callout_number(draw, (sidebar_w - 30, projects_y - 4), 1, font_num)
    draw_callout_label(draw, (16, h - 60), "Click 'Projects' in the sidebar", font_lbl)
    draw_arrow(draw, (120, h - 62), (sidebar_w - 34, projects_y + 18))

    # Callout 2: New project button
    draw_callout_number(draw, (btn_x - 30, btn_y + 7), 2, font_num)
    draw_callout_label(draw, (btn_x - 260, btn_y + 50), "Click '+ New project' to create one", font_lbl)
    draw_arrow(draw, (btn_x - 30, btn_y + 38), (btn_x - 30, btn_y + 20))

    # Step badge
    rounded_rect(draw, (w - 130, 52, w - 12, 80), 6, STEP_BADGE)
    draw.text((w - 120, 58), "Step 1 of 5", fill=WHITE, font=get_font_semibold(11))

    img.save(os.path.join(ASSETS_DIR, "step1-find-projects.png"), quality=95)
    print("  Created: step1-find-projects.png")


# ─── Screenshot 2: Create project dialog ───

def create_screenshot_2():
    w, h = 1100, 580
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)

    draw_top_bar(draw, w)
    sidebar_w = draw_sidebar(draw, w, h)

    content_x = sidebar_w + 40

    # "Projects" heading with back arrow
    draw.text((content_x + 40, 70), "\u2190  All projects", fill=TEXT_SECONDARY, font=get_font(13))

    # Project name area - as if creating/editing
    draw.text((content_x + 40, 110), "Create a new project", fill=TEXT_PRIMARY, font=get_font_semibold(22))

    # Name field
    draw.text((content_x + 40, 165), "Project name", fill=TEXT_PRIMARY, font=get_font_semibold(12))
    field_y = 190
    rounded_rect(draw, (content_x + 40, field_y, w - 80, field_y + 44), 8, INPUT_BG)
    rounded_rect_outline(draw, (content_x + 40, field_y, w - 80, field_y + 44), 8, BORDER, 1)
    draw.text((content_x + 56, field_y + 12), "Instagram Content Creator", fill=TEXT_PRIMARY, font=get_font(13))

    # Description field
    draw.text((content_x + 40, 255), "Description", fill=TEXT_PRIMARY, font=get_font_semibold(12))
    draw.text((content_x + 130, 257), "(optional)", fill=TEXT_MUTED, font=get_font(11))
    desc_y = 280
    rounded_rect(draw, (content_x + 40, desc_y, w - 80, desc_y + 80), 8, INPUT_BG)
    rounded_rect_outline(draw, (content_x + 40, desc_y, w - 80, desc_y + 80), 8, BORDER, 1)
    draw.text((content_x + 56, desc_y + 14), "Creates all my Instagram content including captions,", fill=TEXT_SECONDARY, font=get_font(12))
    draw.text((content_x + 56, desc_y + 36), "carousels, reels, and story sequences", fill=TEXT_SECONDARY, font=get_font(12))

    # Buttons
    btn_row_y = 390
    # Cancel
    rounded_rect(draw, (w - 260, btn_row_y, w - 170, btn_row_y + 40), 8, INPUT_BG)
    rounded_rect_outline(draw, (w - 260, btn_row_y, w - 170, btn_row_y + 40), 8, BORDER, 1)
    draw.text((w - 240, btn_row_y + 10), "Cancel", fill=TEXT_PRIMARY, font=get_font_medium(13))
    # Create
    rounded_rect(draw, (w - 155, btn_row_y, w - 80, btn_row_y + 40), 8, BUTTON_BLACK)
    draw.text((w - 140, btn_row_y + 10), "Create", fill=WHITE, font=get_font_semibold(13))

    # ─── Annotations ───
    font_num = get_font_semibold(13)
    font_lbl = get_font_semibold(11)

    draw_callout_number(draw, (w - 76, field_y + 8), 1, font_num)
    draw_callout_label(draw, (w - 76, field_y + 40), "Give it a clear name", font_lbl)

    draw_callout_number(draw, (w - 76, desc_y + 24), 2, font_num)
    draw_callout_label(draw, (w - 76, desc_y + 64), "Add a short description", font_lbl)

    draw_callout_number(draw, (w - 76, btn_row_y + 7), 3, font_num)
    draw_callout_label(draw, (content_x + 40, btn_row_y + 55), "Click 'Create' to set up your project", font_lbl)
    draw_arrow(draw, (content_x + 200, btn_row_y + 53), (w - 120, btn_row_y + 42))

    # Step badge
    rounded_rect(draw, (w - 130, 52, w - 12, 80), 6, STEP_BADGE)
    draw.text((w - 120, 58), "Step 2 of 5", fill=WHITE, font=get_font_semibold(11))

    img.save(os.path.join(ASSETS_DIR, "step2-create-project.png"), quality=95)
    print("  Created: step2-create-project.png")


# ─── Screenshot 3: Inside project - Instructions panel ───

def create_screenshot_3():
    w, h = 1100, 700
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)

    draw_top_bar(draw, w)
    sidebar_w = draw_sidebar(draw, w, h)

    content_x = sidebar_w + 20
    right_panel_x = w - 340

    # Back link
    draw.text((content_x + 20, 60), "\u2190  All projects", fill=TEXT_SECONDARY, font=get_font(12))

    # Project name
    draw.text((content_x + 20, 85), "Instagram Content Creator", fill=TEXT_PRIMARY, font=get_font_semibold(20))

    # Share button and icons (top right of content)
    draw.text((right_panel_x - 100, 88), "\u2606", fill=TEXT_MUTED, font=get_font(16))  # star
    rounded_rect(draw, (right_panel_x - 60, 83, right_panel_x - 2, 108), 6, INPUT_BG)
    rounded_rect_outline(draw, (right_panel_x - 60, 83, right_panel_x - 2, 108), 6, BORDER, 1)
    draw.text((right_panel_x - 48, 88), "Share", fill=TEXT_PRIMARY, font=get_font(12))

    # Chat input area (center)
    input_y = 135
    rounded_rect(draw, (content_x + 20, input_y, right_panel_x - 30, input_y + 80), 12, INPUT_BG)
    rounded_rect_outline(draw, (content_x + 20, input_y, right_panel_x - 30, input_y + 80), 12, BORDER, 1)
    draw.text((content_x + 44, input_y + 16), "Type / for skills", fill=TEXT_MUTED, font=get_font(13))
    # Model selector
    draw.text((content_x + 44, input_y + 48), "+", fill=TEXT_MUTED, font=get_font(14))
    draw.text((right_panel_x - 230, input_y + 50), "Sonnet 4.6", fill=TEXT_SECONDARY, font=get_font(11))
    draw.text((right_panel_x - 150, input_y + 50), "Extended", fill=TEXT_MUTED, font=get_font(11))

    # Chat history
    chats = [
        ("Getting started with content creation", "Last message 1 day ago"),
        ("Carousel ideas for coaching tips", "Last message 3 days ago"),
        ("Reel scripts for client testimonials", "Last message 5 days ago"),
        ("Caption writing for launch week", "Last message 1 week ago"),
    ]
    chat_y = input_y + 110
    for title, time_str in chats:
        draw.rectangle([content_x + 20, chat_y, right_panel_x - 30, chat_y + 1], fill=BORDER_LIGHT)
        draw.text((content_x + 20, chat_y + 10), title, fill=TEXT_PRIMARY, font=get_font_medium(13))
        draw.text((content_x + 20, chat_y + 32), time_str, fill=TEXT_MUTED, font=get_font(11))
        chat_y += 58

    # ─── RIGHT PANEL ───
    # Instructions card
    inst_y = 60
    rounded_rect(draw, (right_panel_x, inst_y, w - 16, inst_y + 80), 10, CARD_BG)
    rounded_rect_outline(draw, (right_panel_x, inst_y, w - 16, inst_y + 80), 10, BORDER_LIGHT, 1)
    draw.text((right_panel_x + 16, inst_y + 10), "Instructions", fill=TEXT_PRIMARY, font=get_font_semibold(14))
    # Edit icon
    draw.text((w - 40, inst_y + 10), "\u270E", fill=TEXT_MUTED, font=get_font(14))
    # Preview text
    draw.text((right_panel_x + 16, inst_y + 36), "You are my Instagram Content", fill=TEXT_MUTED, font=get_font(10))
    draw.text((right_panel_x + 16, inst_y + 52), "Creator for [YOUR BRAND NAME]...", fill=TEXT_MUTED, font=get_font(10))

    # Files card
    files_y = inst_y + 95
    rounded_rect(draw, (right_panel_x, files_y, w - 16, files_y + 250), 10, CARD_BG)
    rounded_rect_outline(draw, (right_panel_x, files_y, w - 16, files_y + 250), 10, BORDER_LIGHT, 1)

    draw.text((right_panel_x + 16, files_y + 10), "Files", fill=TEXT_PRIMARY, font=get_font_semibold(14))
    draw.text((w - 40, files_y + 12), "+", fill=TEXT_MUTED, font=get_font(16))

    # Capacity bar
    bar_y = files_y + 38
    bar_w = w - 16 - right_panel_x - 32
    rounded_rect(draw, (right_panel_x + 16, bar_y, right_panel_x + 16 + bar_w, bar_y + 6), 3, BORDER)
    rounded_rect(draw, (right_panel_x + 16, bar_y, right_panel_x + 16 + int(bar_w * 0.35), bar_y + 6), 3, BLUE_BAR)
    draw.text((right_panel_x + 16, bar_y + 12), "35% of project capacity used", fill=TEXT_MUTED, font=get_font(9))

    # File cards in grid
    file_cards = [
        ("Brand Voice Guide", "2,400 lines", "PDF"),
        ("Top Captions", "850 lines", "TEXT"),
        ("Hashtag Research", "320 lines", "CSV"),
    ]
    fy = bar_y + 35
    fc_w = (bar_w - 8) // 2
    fc_h = 75
    for i, (fname, lines, ftype) in enumerate(file_cards):
        col = i % 2
        row = i // 2
        fx = right_panel_x + 16 + col * (fc_w + 8)
        fcy = fy + row * (fc_h + 8)

        rounded_rect(draw, (fx, fcy, fx + fc_w, fcy + fc_h), 8, CARD_BG)
        rounded_rect_outline(draw, (fx, fcy, fx + fc_w, fcy + fc_h), 8, BORDER_LIGHT, 1)
        draw.text((fx + 10, fcy + 10), fname, fill=TEXT_PRIMARY, font=get_font_medium(9))
        draw.text((fx + 10, fcy + 28), lines, fill=TEXT_MUTED, font=get_font(8))
        rounded_rect(draw, (fx + 10, fcy + 50, fx + 46, fcy + 66), 4, "#F5F4EF")
        draw.text((fx + 15, fcy + 52), ftype, fill=TEXT_SECONDARY, font=get_font(8, bold=True))

    # ─── Annotations ───
    font_num = get_font_semibold(13)
    font_lbl = get_font_semibold(11)

    # Arrow to Instructions card
    draw_callout_number(draw, (w - 14, inst_y + 25), 1, font_num)
    draw_callout_label(draw, (right_panel_x + 10, inst_y + 85), "Click the edit icon to paste your instructions", font_lbl)

    # Arrow to Files
    draw_callout_number(draw, (w - 14, files_y + 8), 2, font_num)
    draw_callout_label(draw, (right_panel_x + 10, files_y + 255), "Click '+' to upload your knowledge files", font_lbl)

    # Step badge
    rounded_rect(draw, (w - 130, 52, w - 12, 80), 6, STEP_BADGE)
    draw.text((w - 120, 58), "Step 3 of 5", fill=WHITE, font=get_font_semibold(11))

    img.save(os.path.join(ASSETS_DIR, "step3-add-instructions.png"), quality=95)
    print("  Created: step3-add-instructions.png")


# ─── Screenshot 4: Files panel close-up ───

def create_screenshot_4():
    w, h = 700, 580
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)

    # This is a close-up of the right panel Files section
    # Like the user's 4th screenshot

    panel_x = 40
    panel_w = w - 80

    # Files heading
    draw.text((panel_x, 30), "Files", fill=TEXT_PRIMARY, font=get_font_semibold(22))
    draw.text((panel_x + panel_w - 20, 34), "+", fill=TEXT_MUTED, font=get_font(20))

    # Capacity bar
    bar_y = 72
    rounded_rect(draw, (panel_x, bar_y, panel_x + panel_w, bar_y + 10), 5, BORDER)
    rounded_rect(draw, (panel_x, bar_y, panel_x + int(panel_w * 0.35), bar_y + 10), 5, BLUE_BAR)
    # Small blue dot at start
    draw.ellipse([panel_x - 2, bar_y - 2, panel_x + 12, bar_y + 12], fill=BLUE_BAR)

    draw.text((panel_x, bar_y + 18), "35% of project capacity used", fill=TEXT_MUTED, font=get_font(12))
    draw.text((panel_x + panel_w - 90, bar_y + 18), "\u25CF  Indexing", fill=TEXT_MUTED, font=get_font(12))

    # File cards - matching Claude's actual card style
    files = [
        ("Brand Voice Guide", "2,400 lines", "PDF"),
        ("Top Performing Captions", "850 lines", "TEXT"),
        ("Hashtag Research", "320 lines", "CSV"),
        ("Content Pillars", "180 lines", "TEXT"),
    ]

    card_gap = 16
    card_w = (panel_w - card_gap) // 2
    card_h = 140
    card_start_y = bar_y + 50

    for i, (fname, lines, ftype) in enumerate(files):
        col = i % 2
        row = i // 2
        cx = panel_x + col * (card_w + card_gap)
        cy = card_start_y + row * (card_h + card_gap)

        rounded_rect(draw, (cx, cy, cx + card_w, cy + card_h), 12, CARD_BG)
        rounded_rect_outline(draw, (cx, cy, cx + card_w, cy + card_h), 12, BORDER, 1)

        draw.text((cx + 18, cy + 18), fname, fill=TEXT_PRIMARY, font=get_font_medium(14))
        draw.text((cx + 18, cy + 44), lines, fill=TEXT_MUTED, font=get_font(12))

        # File type badge at bottom
        rounded_rect(draw, (cx + 18, cy + card_h - 38, cx + 70, cy + card_h - 16), 4, "#F0EDE6")
        draw.text((cx + 24, cy + card_h - 36), ftype, fill=TEXT_SECONDARY, font=get_font(10, bold=True))

    # ─── Annotations ───
    font_lbl = get_font_semibold(11)

    callout_y = card_start_y + 2 * (card_h + card_gap) + 10
    draw_callout_label(draw, (panel_x, callout_y), "Click '+' to upload each file from your checklist", font_lbl)
    draw_arrow(draw, (panel_x + 200, callout_y - 2), (panel_x + panel_w - 22, 38))

    # Step badge
    rounded_rect(draw, (w - 130, 10, w - 12, 38), 6, STEP_BADGE)
    draw.text((w - 120, 16), "Step 4 of 5", fill=WHITE, font=get_font_semibold(11))

    img.save(os.path.join(ASSETS_DIR, "step4-upload-knowledge.png"), quality=95)
    print("  Created: step4-upload-knowledge.png")


# ─── Screenshot 5: Welcome / new chat screen ───

def create_screenshot_5():
    w, h = 1100, 680
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)

    draw_top_bar(draw, w)
    sidebar_w = draw_sidebar(draw, w, h)

    content_x = sidebar_w
    content_w = w - sidebar_w
    center_x = content_x + content_w // 2

    # Claude sunburst icon (simple representation)
    icon_y = 200
    # Draw a small starburst/asterisk shape
    for angle_deg in range(0, 360, 30):
        angle = math.radians(angle_deg)
        x1 = center_x + 8 * math.cos(angle)
        y1 = icon_y + 8 * math.sin(angle)
        x2 = center_x + 20 * math.cos(angle)
        y2 = icon_y + 20 * math.sin(angle)
        draw.line([(x1, y1), (x2, y2)], fill="#C4956A", width=2)

    # "Welcome, [Name]"
    welcome_font = get_font(28)
    welcome_text = "Welcome, Your Name"
    bbox = welcome_font.getbbox(welcome_text)
    tw = bbox[2] - bbox[0]
    draw.text((center_x - tw // 2, icon_y + 40), welcome_text, fill=TEXT_PRIMARY, font=welcome_font)

    # Chat input
    input_y = icon_y + 110
    input_x = center_x - 280
    input_w = 560
    rounded_rect(draw, (input_x, input_y, input_x + input_w, input_y + 80), 14, INPUT_BG)
    rounded_rect_outline(draw, (input_x, input_y, input_x + input_w, input_y + 80), 14, BORDER, 1)
    draw.text((input_x + 24, input_y + 16), "How can I help you today?", fill=TEXT_MUTED, font=get_font(14))
    # + button and model selector
    draw.text((input_x + 24, input_y + 50), "+", fill=TEXT_MUTED, font=get_font(14))
    draw.text((input_x + input_w - 180, input_y + 52), "Sonnet 4.6", fill=TEXT_SECONDARY, font=get_font(11))
    draw.text((input_x + input_w - 98, input_y + 52), "Extended", fill=TEXT_MUTED, font=get_font(11))

    # Action buttons below: Write, Learn, From Drive, etc.
    btn_y = input_y + 100
    buttons = ["Write", "Learn", "From Drive", "From Calendar", "From Gmail"]
    btn_x = center_x - 280
    for btn_text in buttons:
        bbox = get_font(12).getbbox(btn_text)
        bw = bbox[2] - bbox[0] + 36
        rounded_rect(draw, (btn_x, btn_y, btn_x + bw, btn_y + 34), 8, INPUT_BG)
        rounded_rect_outline(draw, (btn_x, btn_y, btn_x + bw, btn_y + 34), 8, BORDER, 1)
        draw.text((btn_x + 18, btn_y + 8), btn_text, fill=TEXT_SECONDARY, font=get_font(12))
        btn_x += bw + 10

    # ─── Annotations ───
    font_lbl = get_font_semibold(11)

    # Callout for chat input
    draw_callout_label(draw, (input_x, input_y + 88), "Type your first message here and start creating content", font_lbl)
    draw_arrow(draw, (input_x + 200, input_y + 86), (input_x + 200, input_y + 82))

    # Note about project context
    draw_callout_label(draw, (input_x, input_y - 30), "When chatting inside a project, Claude automatically uses your instructions and files", font_lbl)

    # Step badge
    rounded_rect(draw, (w - 130, 52, w - 12, 80), 6, STEP_BADGE)
    draw.text((w - 120, 58), "Step 5 of 5", fill=WHITE, font=get_font_semibold(11))

    img.save(os.path.join(ASSETS_DIR, "step5-start-chatting.png"), quality=95)
    print("  Created: step5-start-chatting.png")


def main():
    print("Generating Claude interface screenshots...\n")
    create_screenshot_1()
    create_screenshot_2()
    create_screenshot_3()
    create_screenshot_4()
    create_screenshot_5()
    print(f"\nDone! 5 screenshots created in: {ASSETS_DIR}")


if __name__ == "__main__":
    main()
