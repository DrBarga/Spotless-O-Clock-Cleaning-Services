from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image
from pathlib import Path
import textwrap

ROOT = Path(r"C:\Users\bogda\OneDrive\Desktop\Spotless O’Clock Cleaning Services")
OUT = ROOT / "Spotless-OClock-Website-Concept.pdf"
HERO = ROOT / "assets" / "spotless-hero.png"

W, H = A4
GREEN = HexColor("#173F35")
GREEN2 = HexColor("#215347")
INK = HexColor("#15362F")
MUTED = HexColor("#61716B")
CREAM = HexColor("#F7F3EB")
PAPER = HexColor("#FFFDF8")
GOLD = HexColor("#D5A85B")
SAGE = HexColor("#91A99A")
PALE = HexColor("#EDF1EB")
LINE = HexColor("#D8E0DC")

pdfmetrics.registerFont(TTFont("UI", r"C:\Windows\Fonts\segoeui.ttf"))
pdfmetrics.registerFont(TTFont("UI-B", r"C:\Windows\Fonts\segoeuib.ttf"))
pdfmetrics.registerFont(TTFont("SERIF", r"C:\Windows\Fonts\georgia.ttf"))
pdfmetrics.registerFont(TTFont("SERIF-B", r"C:\Windows\Fonts\georgiab.ttf"))


def rounded_rect(c, x, y, w, h, r, fill, stroke=None, sw=1):
    c.setLineWidth(sw)
    if fill:
        c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
    c.roundRect(x, y, w, h, r, fill=1 if fill else 0, stroke=1 if stroke else 0)


def line(c, x1, y1, x2, y2, color=LINE, width=1):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)


def text(c, value, x, y, font="UI", size=10, color=INK):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x, y, value)


def text_right(c, value, x, y, font="UI", size=10, color=INK):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawRightString(x, y, value)


def paragraph(c, value, x, y, width, font="UI", size=10.5, leading=15, color=MUTED, max_lines=None):
    approx = max(12, int(width / (size * 0.52)))
    lines = []
    for block in value.split("\n"):
        lines.extend(textwrap.wrap(block, approx, break_long_words=False) or [""])
    if max_lines:
        lines = lines[:max_lines]
    c.setFillColor(color)
    c.setFont(font, size)
    for i, item in enumerate(lines):
        c.drawString(x, y - i * leading, item)
    return y - len(lines) * leading


def title(c, value, x, y, width=470, size=31, color=INK):
    words = value.split()
    lines, current = [], ""
    for word in words:
        test = f"{current} {word}".strip()
        if pdfmetrics.stringWidth(test, "SERIF", size) <= width:
            current = test
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    c.setFillColor(color)
    c.setFont("SERIF", size)
    for i, item in enumerate(lines):
        c.drawString(x, y - i * size * 1.08, item)
    return y - len(lines) * size * 1.08


def label(c, value, x, y, light=False):
    c.setFillColor(GOLD if light else GREEN)
    c.setFont("UI-B", 7.5)
    c.drawString(x, y, value.upper())


def logo(c, x, y, scale=1, light=False):
    col = white if light else GREEN
    c.setStrokeColor(col)
    c.setLineWidth(1.8 * scale)
    c.circle(x + 15 * scale, y + 15 * scale, 12 * scale, stroke=1, fill=0)
    c.line(x + 15 * scale, y + 15 * scale, x + 15 * scale, y + 23 * scale)
    c.line(x + 15 * scale, y + 15 * scale, x + 22 * scale, y + 11 * scale)
    c.setFillColor(GOLD)
    c.circle(x + 30 * scale, y + 29 * scale, 2.4 * scale, stroke=0, fill=1)
    text(c, "Spotless", x + 36 * scale, y + 17 * scale, "UI-B", 12 * scale, col)
    text(c, "O'CLOCK", x + 36 * scale, y + 8 * scale, "UI-B", 5.8 * scale, GOLD if light else MUTED)


def page_no(c, n, title_text=None, dark=False):
    col = Color(1, 1, 1, .62) if dark else MUTED
    if title_text:
        text(c, title_text, 42, 27, "UI", 7.5, col)
    text_right(c, f"0{n}", W - 42, 27, "UI-B", 7.5, col)


def draw_cover(c):
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    img = Image.open(HERO)
    iw, ih = img.size
    frame_h = 425
    crop_ratio = W / frame_h
    src_ratio = iw / ih
    if src_ratio > crop_ratio:
        crop_w = int(ih * crop_ratio)
        left = int(iw * .28)
        left = min(left, iw - crop_w)
        img = img.crop((left, 0, left + crop_w, ih))
    img_reader = ImageReader(img)
    c.drawImage(img_reader, 0, H - frame_h, W, frame_h, preserveAspectRatio=False, mask='auto')
    c.setFillColor(Color(1, 1, 1, .15))
    c.rect(0, H - frame_h, W, frame_h, fill=1, stroke=0)
    rounded_rect(c, 36, H - 72, 188, 38, 19, Color(1, 1, 1, .92))
    logo(c, 47, H - 68, .72)

    c.setFillColor(GREEN)
    c.rect(0, 0, W, H - frame_h + 12, fill=1, stroke=0)
    label(c, "Website concept proposal", 46, 354, light=True)
    text(c, "A digital home for", 46, 312, "SERIF", 26, white)
    text(c, "a beautifully clean brand.", 46, 273, "SERIF", 34, white)
    paragraph(c, "A calm, modern and conversion-focused website concept for Spotless O'Clock Cleaning Services in Birmingham.", 47, 226, 470, "UI", 12, 18, Color(1,1,1,.72))
    line(c, 46, 154, W - 46, 154, Color(1,1,1,.18))
    text(c, "Prepared for", 46, 128, "UI-B", 7.5, Color(1,1,1,.5))
    text(c, "Spotless O'Clock", 46, 108, "UI-B", 11, white)
    text_right(c, "Concept 01 / 2026", W - 46, 108, "UI-B", 8, Color(1,1,1,.64))
    page_no(c, 1, "SPOTLESS O'CLOCK WEBSITE CONCEPT", dark=True)


def draw_strategy(c):
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    logo(c, 42, H - 61, .66)
    label(c, "01 / Strategic direction", 42, H - 112)
    y = title(c, "Turn a local service into a trusted digital brand.", 42, H - 148, 500, 30)
    paragraph(c, "Spotless O'Clock is a young, personal cleaning business with a broad service range. The website gives that offer one clear, professional home - making it easier for local customers and Airbnb hosts to understand the value and ask for a quote.", 42, y - 10, 505, "UI", 11, 16, MUTED)

    cards_y = 405
    cards = [
        ("The opportunity", "No standalone website means a chance to define the brand correctly from day one."),
        ("The audience", "Busy households, Airbnb hosts, tenants and small Birmingham workplaces."),
        ("The objective", "Build confidence quickly and turn interest into a simple WhatsApp conversation."),
    ]
    for i, (heading, body) in enumerate(cards):
        x = 42 + i * 173
        rounded_rect(c, x, cards_y, 157, 144, 15, white, LINE)
        text(c, f"0{i+1}", x + 16, cards_y + 115, "SERIF", 11, GOLD)
        text(c, heading, x + 16, cards_y + 84, "UI-B", 11, INK)
        paragraph(c, body, x + 16, cards_y + 61, 124, "UI", 8.6, 12.5, MUTED)

    rounded_rect(c, 42, 150, W - 84, 215, 18, GREEN)
    label(c, "Core positioning", 64, 330, light=True)
    text(c, "Reliable. Personal. On time.", 64, 283, "SERIF", 26, white)
    paragraph(c, "The concept avoids corporate language and discount-led selling. It positions Spotless O'Clock as a dependable local service that cares about the finish, communicates directly and works around the customer's routine.", 64, 248, 450, "UI", 10.5, 16, Color(1,1,1,.72))
    text(c, "Brand promise", 64, 182, "UI-B", 7.5, Color(1,1,1,.48))
    text(c, "Your space, spotless on time.", 64, 163, "UI-B", 11, HexColor("#F0D29C"))
    page_no(c, 2, "STRATEGY")


def draw_design(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    logo(c, 42, H - 61, .66)
    label(c, "02 / Design language", 42, H - 112)
    y = title(c, "Premium enough to inspire trust. Warm enough to feel personal.", 42, H - 148, 500, 29)
    paragraph(c, "The visual system is intentionally quiet. Generous space, soft natural imagery and a small palette create a sense of calm - the same feeling customers want after a professional clean.", 42, y - 10, 500, "UI", 11, 16, MUTED)

    # Palette
    text(c, "COLOUR SYSTEM", 42, 497, "UI-B", 7.5, MUTED)
    palette = [(GREEN, "Deep green", "Trust"), (SAGE, "Soft sage", "Freshness"), (GOLD, "Warm gold", "Care"), (PAPER, "Warm ivory", "Calm")]
    for i, (col, name, role) in enumerate(palette):
        x = 42 + i * 128
        rounded_rect(c, x, 405, 112, 73, 12, col, LINE if col == PAPER else None)
        text(c, name, x, 390, "UI-B", 8.5, INK)
        text(c, role, x, 377, "UI", 7.5, MUTED)

    # Typography
    rounded_rect(c, 42, 204, 240, 140, 16, white)
    text(c, "TYPOGRAPHY", 60, 318, "UI-B", 7.5, MUTED)
    text(c, "A calm, editorial", 60, 280, "SERIF", 22, INK)
    text(c, "sense of quality.", 60, 251, "SERIF", 22, INK)
    text(c, "Clear modern text keeps every action effortless.", 60, 222, "UI", 8.2, MUTED)

    # Visual tone
    rounded_rect(c, 302, 204, 251, 140, 16, PALE)
    text(c, "VISUAL TONE", 320, 318, "UI-B", 7.5, MUTED)
    tags = ["Natural", "Local", "Uncluttered", "Confident", "Human", "Fresh"]
    positions = [(320,278),(407,278),(320,240),(425,240),(320,202),(398,202)]
    for (tag, (x, yy)) in zip(tags, positions):
        w = pdfmetrics.stringWidth(tag, "UI-B", 8) + 22
        rounded_rect(c, x, yy, w, 24, 12, white)
        text(c, tag, x + 11, yy + 8, "UI-B", 8, GREEN)

    paragraph(c, "The original hero photograph was created specifically for this concept. It uses a real-home atmosphere, Birmingham context and generous text space instead of generic cleaning-product imagery.", 42, 167, 510, "UI", 9.4, 14, MUTED)
    page_no(c, 3, "DESIGN LANGUAGE")


def draw_ux(c):
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    logo(c, 42, H - 61, .66)
    label(c, "03 / User experience", 42, H - 112)
    y = title(c, "A short path from first impression to real enquiry.", 42, H - 148, 500, 30)
    paragraph(c, "Visitors should never have to search for the next step. The page answers the main questions in sequence and keeps a clear quote action within easy reach.", 42, y - 10, 495, "UI", 11, 16, MUTED)

    flow_y = 434
    steps = [
        ("01", "Understand", "What the business does and where it works."),
        ("02", "Explore", "Services, benefits and flexible visit plans."),
        ("03", "Trust", "Simple process and clear, honest expectations."),
        ("04", "Enquire", "A pre-filled WhatsApp quote message."),
    ]
    for i, (num, head, body) in enumerate(steps):
        x = 42 + i * 129
        rounded_rect(c, x, flow_y, 113, 145, 14, PALE if i != 3 else GREEN)
        text(c, num, x + 14, flow_y + 114, "SERIF", 11, GOLD)
        text(c, head, x + 14, flow_y + 80, "UI-B", 11, white if i == 3 else INK)
        paragraph(c, body, x + 14, flow_y + 56, 87, "UI", 8, 11.5, Color(1,1,1,.7) if i == 3 else MUTED)
        if i < 3:
            text(c, ">", x + 117, flow_y + 66, "UI-B", 10, GOLD)

    text(c, "WHY THE WHATSAPP-FIRST FORM WORKS", 42, 397, "UI-B", 7.5, MUTED)
    bullets = [
        ("Less friction", "Customers stay in a familiar channel instead of sending a cold web form."),
        ("Better information", "The message already includes name, postcode, service and key details."),
        ("More control", "Customers review the message before sending; the business receives a usable enquiry."),
    ]
    for i, (head, body) in enumerate(bullets):
        yy = 340 - i * 72
        c.setFillColor(GOLD)
        c.circle(54, yy + 8, 5, fill=1, stroke=0)
        text(c, head, 72, yy + 13, "UI-B", 10.5, INK)
        paragraph(c, body, 72, yy - 5, 440, "UI", 9.4, 14, MUTED)

    rounded_rect(c, 42, 92, W - 84, 67, 14, CREAM)
    text(c, "Responsive by design", 60, 131, "UI-B", 9.5, GREEN)
    paragraph(c, "Navigation, content hierarchy, touch targets and imagery are adapted for mobile - not simply shrunk from desktop.", 60, 112, 450, "UI", 8.6, 12, MUTED)
    page_no(c, 4, "USER EXPERIENCE")


def draw_value(c):
    c.setFillColor(GREEN)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    logo(c, 42, H - 61, .66, light=True)
    label(c, "04 / Business value", 42, H - 112, light=True)
    y = title(c, "More than a good-looking page.", 42, H - 148, 500, 31, white)
    paragraph(c, "The concept gives Spotless O'Clock a credible destination for every social post, referral and future campaign.", 42, y - 10, 490, "UI", 11, 16, Color(1,1,1,.7))

    value_cards = [
        ("Sharper first impression", "A coherent visual identity makes a new business feel established and considered."),
        ("Clearer service offer", "Customers can understand the range without reading a long social profile."),
        ("Higher-quality enquiries", "The quote flow collects useful context before the first conversation."),
        ("Ready to grow", "The structure can later support pricing, reviews, booking tools and local SEO pages."),
    ]
    for i, (head, body) in enumerate(value_cards):
        col = i % 2
        row = i // 2
        x = 42 + col * 258
        yy = 421 - row * 154
        rounded_rect(c, x, yy, 242, 135, 16, Color(1,1,1,.07), Color(1,1,1,.13))
        text(c, f"0{i+1}", x + 18, yy + 101, "SERIF", 11, GOLD)
        text(c, head, x + 18, yy + 73, "UI-B", 10.5, white)
        paragraph(c, body, x + 18, yy + 50, 202, "UI", 8.7, 12.5, Color(1,1,1,.64))

    line(c, 42, 229, W - 42, 229, Color(1,1,1,.16))
    text(c, "WHAT IS INCLUDED", 42, 205, "UI-B", 7.5, Color(1,1,1,.5))
    included = ["Responsive landing page", "Custom visual direction", "Original hero image", "Interactive service selection", "WhatsApp quote flow", "Accessible, lightweight code"]
    for i, item in enumerate(included):
        x = 42 + (i % 3) * 173
        yy = 171 - (i // 3) * 34
        text(c, "+", x, yy, "UI-B", 10, GOLD)
        text(c, item, x + 14, yy, "UI", 8.4, white)
    page_no(c, 5, "BUSINESS VALUE", dark=True)


def draw_next(c):
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    logo(c, 42, H - 61, .66)
    label(c, "05 / Recommended next step", 42, H - 112)
    y = title(c, "Review the direction. Then make it fully yours.", 42, H - 148, 500, 31)
    paragraph(c, "This concept is ready for review. The final version should be completed with the business owner's preferred service area wording, policies, verified trust signals and any real work photography or testimonials available.", 42, y - 10, 500, "UI", 11, 16, MUTED)

    rounded_rect(c, 42, 398, W - 84, 166, 18, CREAM)
    text(c, "Three quick decisions", 64, 529, "SERIF", 20, INK)
    decisions = [
        "Confirm the service areas and opening hours.",
        "Confirm which trust details can be published (insurance, checks, guarantees).",
        "Choose the launch domain and preferred enquiry process.",
    ]
    for i, item in enumerate(decisions):
        yy = 488 - i * 35
        rounded_rect(c, 64, yy - 5, 24, 24, 12, GREEN)
        text(c, str(i + 1), 73, yy + 2, "UI-B", 8, white)
        text(c, item, 102, yy + 1, "UI", 9.5, INK)

    rounded_rect(c, 42, 181, W - 84, 176, 18, GREEN)
    label(c, "Concept summary", 64, 320, light=True)
    text(c, "Calm. Clear. Credible.", 64, 279, "SERIF", 26, white)
    paragraph(c, "A website that feels like the service should feel: organised, reassuring and finished with care.", 64, 243, 445, "UI", 11, 16, Color(1,1,1,.7))
    text(c, "spotlessoclock@gmail.com", 64, 204, "UI-B", 8.5, HexColor("#F0D29C"))
    text_right(c, "07915 847472", W - 64, 204, "UI-B", 8.5, white)
    page_no(c, 6, "NEXT STEP")


def build():
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle("Spotless O'Clock - Website Concept Proposal")
    c.setAuthor("Website concept prepared for Spotless O'Clock Cleaning Services")
    for fn in [draw_cover, draw_strategy, draw_design, draw_ux, draw_value, draw_next]:
        fn(c)
        c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    build()
