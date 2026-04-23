from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

W, H = 1280, 640
out = Path('assets/figureflow_banner.png')
out.parent.mkdir(parents=True, exist_ok=True)

BG1 = (9, 18, 40)
BG2 = (20, 54, 110)
ACCENT = (83, 175, 255)
ACCENT2 = (129, 106, 255)
WHITE = (247, 250, 255)
MUTED = (200, 213, 235)
PILL_FILL = (255, 255, 255, 240)
PILL_TEXT = (24, 38, 74)
CARD_STROKE = (255, 255, 255, 76)

img = Image.new('RGBA', (W, H), BG1)
pix = img.load()
for y in range(H):
    t = y / (H - 1)
    r = int(BG1[0] * (1 - t) + BG2[0] * t)
    g = int(BG1[1] * (1 - t) + BG2[1] * t)
    b = int(BG1[2] * (1 - t) + BG2[2] * t)
    for x in range(W):
        pix[x, y] = (r, g, b, 255)

# glow
for cx, cy, radius, color in [
    (1040, 100, 230, (71, 154, 255, 110)),
    (1110, 520, 200, (126, 102, 255, 100)),
]:
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=color)
    layer = layer.filter(ImageFilter.GaussianBlur(56))
    img = Image.alpha_composite(img, layer)

draw = ImageDraw.Draw(img)
font_kr = '/System/Library/Fonts/AppleSDGothicNeo.ttc'
font_en = '/System/Library/Fonts/SFNS.ttf'

title_font = ImageFont.truetype(font_en, 76)
sub_font = ImageFont.truetype(font_kr, 32)
body_font = ImageFont.truetype(font_kr, 23)
pill_font = ImageFont.truetype(font_en, 20)
card_title_font = ImageFont.truetype(font_en, 22)
card_label_font = ImageFont.truetype(font_kr, 18)
card_small_font = ImageFont.truetype(font_en, 16)

left = 84
draw.text((left, 94), 'FigureFlow AI', font=title_font, fill=WHITE)
draw.text((left, 188), '논문을 발표 가능한 도식으로 바꾸는 멀티에이전트 시각화 워크플로우', font=sub_font, fill=MUTED)
draw.text((left, 244), 'OpenAI GPT Image · Korean README · Streamlit Refine', font=body_font, fill=(230, 238, 250))

# accent line
ax1, ay = left, 298
ax2 = left + 430
for i in range(6):
    draw.rounded_rectangle((ax1 + i*74, ay, ax1 + i*74 + 48, ay + 6), radius=3, fill=(110 + i*15, 175, 255))

# pills
pills = ['OPENAI GPT IMAGE', 'KOREAN README', 'REFINE READY']
x = left
y = 340
for pill in pills:
    bbox = draw.textbbox((0, 0), pill, font=pill_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    box = (x, y, x + tw + 34, y + th + 22)
    draw.rounded_rectangle(box, radius=18, fill=PILL_FILL)
    draw.text((x + 17, y + 11), pill, font=pill_font, fill=PILL_TEXT)
    x = box[2] + 14

# small footer
footer = 'Academic visualization fork of PaperVizAgent'
draw.text((left, 560), footer, font=card_small_font, fill=(185, 198, 225))

# right feature card
card = (730, 82, 1188, 560)
draw.rounded_rectangle(card, radius=34, fill=(255, 255, 255, 20), outline=CARD_STROKE, width=2)
inner = (766, 122, 1150, 520)
draw.rounded_rectangle(inner, radius=28, fill=(255, 255, 255, 245), outline=(226, 232, 243), width=2)
draw.text((794, 150), 'Paper-to-Diagram Workflow', font=card_title_font, fill=(22, 35, 64))

# workflow nodes
nodes = [
    ('논문 PDF', 804),
    ('구조 설계', 930),
    ('최종 도해', 1056),
]
ny = 220
for idx, (label, nx) in enumerate(nodes):
    fill = (247, 250, 255) if idx < 2 else (234, 245, 255)
    outline = (174, 192, 221) if idx < 2 else (87, 156, 238)
    draw.rounded_rectangle((nx, ny, nx+84, ny+84), radius=20, fill=fill, outline=outline, width=3)
    if idx < 2:
        draw.line((nx+84, ny+42, nx+114, ny+42), fill=(88, 118, 170), width=4)
        draw.polygon([(nx+114, ny+42), (nx+100, ny+34), (nx+100, ny+50)], fill=(88, 118, 170))
    tb = draw.textbbox((0, 0), label, font=card_label_font)
    tw = tb[2] - tb[0]
    draw.text((nx + (84 - tw)/2, ny + 100), label, font=card_label_font, fill=(35, 51, 89))

# icons inside nodes
# pdf
nx = nodes[0][1]
draw.rounded_rectangle((nx+24, ny+16, nx+60, ny+60), radius=8, fill=(255,255,255), outline=(150,165,195), width=2)
draw.text((nx+29, ny+29), 'PDF', font=card_small_font, fill=(195, 66, 66))
# planner icon
nx = nodes[1][1]
draw.line((nx+20, ny+58, nx+42, ny+30, nx+62, ny+50), fill=ACCENT2, width=4)
for px, py in [(nx+20, ny+58), (nx+42, ny+30), (nx+62, ny+50)]:
    draw.ellipse((px-4, py-4, px+4, py+4), fill=ACCENT2)
# final icon
nx = nodes[2][1]
# mini bars and lines
for i, h in enumerate([20, 32, 42]):
    x0 = nx + 18 + i*16
    draw.rounded_rectangle((x0, ny+56-h, x0+10, ny+56), radius=3, fill=ACCENT)
draw.line((nx+50, ny+52, nx+64, ny+42, nx+74, ny+48), fill=ACCENT2, width=3)

# lower description panel
panel = (804, 382, 1114, 470)
draw.rounded_rectangle(panel, radius=18, fill=(245, 248, 253), outline=(213, 223, 238), width=2)
draw.text((828, 404), 'OpenAI GPT Image + Streamlit Demo + Korean Docs', font=card_small_font, fill=(52, 74, 120))
for yy, ww in [(430, 220), (448, 180)]:
    draw.rounded_rectangle((828, yy, 828+ww, yy+8), radius=4, fill=(157, 170, 198))

img.convert('RGB').save(out, quality=95)
print(out)
