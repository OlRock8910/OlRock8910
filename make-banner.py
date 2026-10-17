"""Draws banner.png for the GitHub profile README (1280x360)."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1280, 360
BLACK = '/usr/share/fonts/opentype/inter/Inter-Black.otf'
SEMI = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
EMOJI = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'


def emoji(ch, size):
    # Noto Color Emoji only renders at 109px; draw there and scale.
    f = ImageFont.truetype(EMOJI, 109)
    tile = Image.new('RGBA', (136, 128), (0, 0, 0, 0))
    ImageDraw.Draw(tile).text((0, 0), ch, font=f, embedded_color=True)
    tile = tile.crop(tile.getbbox())
    return tile.resize((size, int(size * tile.height / tile.width)), Image.LANCZOS)


img = Image.new('RGBA', (W, H), (11, 11, 30, 255))
glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
g = ImageDraw.Draw(glow)
g.ellipse((-260, -320, 560, 380), fill=(124, 58, 237, 160))
g.ellipse((820, 40, 1560, 700), fill=(219, 39, 119, 120))
g.ellipse((520, 220, 900, 520), fill=(14, 165, 233, 70))
img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(110)))
d = ImageDraw.Draw(img)

d.text((72, 70), 'OlRock8910', font=ImageFont.truetype(BLACK, 92), fill=(255, 255, 255))
d.text((76, 182), 'I build free Android apps and games.', font=ImageFont.truetype(SEMI, 36), fill=(221, 214, 254))

# Glass chips: shapes go on an overlay so their transparency blends in.
chips = Image.new('RGBA', (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(chips)
f = ImageFont.truetype(SEMI, 24)
x, spots = 76, []
for label in ['No ads', 'No accounts', 'Nothing uploaded']:
    w = d.textlength(label, font=f) + 34
    cd.rounded_rectangle((x, 250, x + w, 292), 21, fill=(255, 255, 255, 30), outline=(255, 255, 255, 80), width=2)
    spots.append((x + 17, 257, label))
    x += w + 12
img = Image.alpha_composite(img, chips)
d = ImageDraw.Draw(img)
for tx, ty, label in spots:
    d.text((tx, ty), label, font=f, fill=(255, 255, 255))

# One glass tile per project, staggered.
for i, ch in enumerate(['🎬', '🇪🇸', '🏋️']):
    cx = 800 + i * 150
    cy = 70 + (i % 2) * 90
    tile = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(tile).rounded_rectangle((cx, cy, cx + 136, cy + 128), 30, fill=(255, 255, 255, 34), outline=(255, 255, 255, 70), width=2)
    img = Image.alpha_composite(img, tile)
    e = emoji(ch, 72)
    img.alpha_composite(e, (cx + (136 - e.width) // 2, cy + (128 - e.height) // 2))

img.convert('RGB').save(HERE / 'banner.png', optimize=True)
print('banner.png written')
