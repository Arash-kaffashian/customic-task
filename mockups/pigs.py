from PIL import Image, ImageDraw, ImageFont

from django.conf import settings

import os
import logging


logger = logging.getLogger(__name__)
BASE_DIR = settings.BASE_DIR

# FONT PATHS
FONTS_MAP = {
    'arial': os.path.join(BASE_DIR, 'static', 'fonts', 'arial.ttf'),
    'times': os.path.join(BASE_DIR, 'static', 'fonts', 'times.ttf'),
    'default': os.path.join(BASE_DIR, 'static', 'fonts', 'DejaVuSans.ttf'),
}

# green code : it can be a color.model
# COLORS
COLOR_MAP = {
    1: ('white', '#FFFFFF'),
    2: ('yellow', '#FFFF00'),
    3: ('blue', '#0000FF'),
    4: ('black', '#000000'),
}


# IMAGE BUILDER DEF
def create_mockup_image(text, shirt_color, text_color, font_name):

    # COLORS
    shirt_name, _ = COLOR_MAP.get(shirt_color, ('white', '#FFFFFF'))
    _, text_hex = COLOR_MAP.get(text_color, ('black', '#000000'))

    # orange code : must be change if the shirts path changed
    # BASE IMAGE PATH
    base_path = os.path.join(BASE_DIR, 'static', 'mockup_bases', f'{shirt_name}.png')
    if not os.path.exists(base_path):
        logger.warning(f"⚠️ تصویر پایه {base_path} پیدا نشد، white.png جایگزین می‌شود.")
        base_path = os.path.join(BASE_DIR, 'static', 'mockup_bases', 'white.png')

    # OPENING BASE IMAGE
    base = Image.open(base_path).convert('RGBA')
    width, height = base.size

    # TEXT LAYER
    txt_layer = Image.new('RGBA', base.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    # FONT
    font_path = FONTS_MAP.get(font_name, FONTS_MAP['default'])
    try:
        font = ImageFont.truetype(font_path, size=int(height * 0.08))
    except Exception as e:
        logger.warning(f"⚠️ فونت {font_name} پیدا نشد ({e})، فونت پیش‌فرض استفاده می‌شود.")
        fallback_font = FONTS_MAP['default']
        font = ImageFont.truetype(fallback_font, size=int(height * 0.08))

    # TEXT SIZE AND CENTRALIZATION
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (width - text_w) / 2
    y = (height - text_h) / 2

    # TEXT DRAWING
    draw.text((x, y), text, fill=text_hex, font=font)

    # LAYERS BINDING AND CONVERTING
    result = Image.alpha_composite(base, txt_layer).convert('RGB')

    return result
