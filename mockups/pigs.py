from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)
BASE_DIR = settings.BASE_DIR


def create_mockup_image(text, shirt_obj, color_obj, font_obj):

    # ------------------------------
    # 1) Fetching Shirt.image.url from model
    # ------------------------------
    if not shirt_obj or not shirt_obj.image:
        raise ValueError("❌ shirt_obj معتبر نیست یا تصویر ندارد.")

    shirt_path = shirt_obj.image.path
    if not os.path.exists(shirt_path):
        raise FileNotFoundError(f"❌ تصویر تیشرت {shirt_path} پیدا نشد!")

    # ------------------------------
    # 2) Fetching Color from model
    # ------------------------------
    if not color_obj or not color_obj.color:
        text_hex = "#000000"  # رنگ پیشفرض سیاه
    else:
        text_hex = color_obj.color.strip()

    # ------------------------------
    # 3) Fetching Font from model
    # ------------------------------
    if font_obj and font_obj.font:
        font_path = font_obj.font.path
    else:
        # fallback default font
        font_path = os.path.join(BASE_DIR, 'static', 'fonts', 'DejaVuSans.ttf')

    if not os.path.exists(font_path):
        logger.warning(f"⚠️ فونت {font_path} پیدا نشد! از فونت پیش‌فرض استفاده می‌شود.")
        font_path = os.path.join(BASE_DIR, 'static', 'fonts', 'DejaVuSans.ttf')

    # ------------------------------
    # 4) Opening Shirt image
    # ------------------------------
    base = Image.open(shirt_path).convert('RGBA')
    width, height = base.size

    # ------------------------------
    # 5) text layer
    # ------------------------------
    txt_layer = Image.new('RGBA', base.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    # Font size
    font_size = int(height * 0.08)
    font = ImageFont.truetype(font_path, size=font_size)

    # calculating text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = (width - text_w) / 2
    y = (height - text_h) / 2

    # Drawing text on Transparent layer
    draw.text((x, y), text, fill=text_hex, font=font)

    # ------------------------------
    # 6) merging layers
    # ------------------------------
    result = Image.alpha_composite(base, txt_layer).convert('RGB')

    return result
