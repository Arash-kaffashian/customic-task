from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)
BASE_DIR = settings.BASE_DIR


def create_mockup_image(text, shirt_obj, color_obj, font_obj):

    # ------------------------------
    # 1) گرفتن مسیر تصویر تیشرت از مدل Shirt
    # ------------------------------
    if not shirt_obj or not shirt_obj.image:
        raise ValueError("❌ shirt_obj معتبر نیست یا تصویر ندارد.")

    shirt_path = shirt_obj.image.path
    if not os.path.exists(shirt_path):
        raise FileNotFoundError(f"❌ تصویر تیشرت {shirt_path} پیدا نشد!")

    # ------------------------------
    # 2) گرفتن رنگ متن از مدل Color
    # ------------------------------
    if not color_obj or not color_obj.color:
        text_hex = "#000000"  # رنگ پیشفرض سیاه
    else:
        text_hex = color_obj.color.strip()

    # ------------------------------
    # 3) گرفتن فونت از مدل Font
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
    # 4) باز کردن تصویر تیشرت
    # ------------------------------
    base = Image.open(shirt_path).convert('RGBA')
    width, height = base.size

    # ------------------------------
    # 5) لایه متن
    # ------------------------------
    txt_layer = Image.new('RGBA', base.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    # اندازه فونت
    font_size = int(height * 0.08)
    font = ImageFont.truetype(font_path, size=font_size)

    # محاسبه اندازه متن
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = (width - text_w) / 2
    y = (height - text_h) / 2

    # رسم متن روی لایه شفاف
    draw.text((x, y), text, fill=text_hex, font=font)

    # ------------------------------
    # 6) چسباندن لایه‌ها
    # ------------------------------
    result = Image.alpha_composite(base, txt_layer).convert('RGB')

    return result
