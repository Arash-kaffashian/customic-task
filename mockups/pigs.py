from PIL import Image
from django.conf import settings
import os

BASE_DIR = settings.BASE_DIR

COLOR_MAP = {
    1: ('white', '#FFFFFF'),
    2: ('yellow', '#FFFF00'),
    3: ('blue', '#0000FF'),
    4: ('black', '#000000'),
}

def create_mockup_image(text, shirt_color, text_color=1, font_name='default'):
    """
    فقط عکس پایه تی‌شرت رو بر اساس رنگ انتخاب می‌سازه و برمی‌گردونه.
    هیچ متنی روی عکس نوشته نمی‌شه.
    """

    # تعیین رنگ و مسیر عکس پایه
    shirt_name, _ = COLOR_MAP.get(shirt_color, ('white', '#FFFFFF'))
    base_path = os.path.join(BASE_DIR, 'static', 'mockup_bases', f'{shirt_name}.png')

    # اگه فایل وجود نداشت، از white.png استفاده کن
    if not os.path.exists(base_path):
        base_path = os.path.join(BASE_DIR, 'static', 'mockup_bases', 'white.png')

    # باز کردن تصویر و تبدیل به RGB
    base = Image.open(base_path).convert('RGB')

    # خروجی: فقط عکس پایه
    return base
