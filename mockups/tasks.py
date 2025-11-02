from django.core.files.base import ContentFile
from .models import GenerationTask, Mockup
from .pigs import create_mockup_image
from celery import shared_task
from django.conf import settings
import uuid
import io

@shared_task(bind=True)
def generate_mockups_task(self, task_db_id, text, font, text_color, shirt_colors):
    try:
        gen_task = GenerationTask.objects.get(id=task_db_id)
        gen_task.status = 'IN_PROGRESS'
        gen_task.save()
    except GenerationTask.DoesNotExist:
        return {'error': 'GenerationTask not found'}

    # اطمینان از اینکه مقادیر عددی‌اند
    shirt_colors = [int(c) for c in shirt_colors]
    text_color = int(text_color)

    results = []
    for color in shirt_colors:
        try:
            # ساخت تصویر ماکاپ
            img = create_mockup_image(
                text=text or '',
                shirt_color=color,
                text_color=text_color,
                font_name=font or 'default'
            )

            # ذخیره در حافظه موقت
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)

            filename = f'mockup_{gen_task.task_id}_{color}_{uuid.uuid4().hex[:8]}.png'

            # مسیر نهایی فایل رو چک کنیم
            print("🖼 در حال ذخیره تصویر:", filename)
            print("📁 MEDIA_ROOT:", settings.MEDIA_ROOT)

            # ساخت رکورد مدل Mockup
            mockup = Mockup.objects.create(
                gen_task=gen_task,  # ✅ فیلد درست
                text=text,
                font=font,
                text_color=text_color,
                shirt_color=color,
            )

            # ذخیره تصویر فیزیکی
            mockup.image.save(filename, ContentFile(buffer.read()), save=True)

            results.append({
                'image_url': mockup.image.url,
                'created_at': mockup.created_at.isoformat()
            })

        except Exception as e:
            print(f"❌ Error generating mockup for color {color}: {e}")

    gen_task.status = 'SUCCESS'
    gen_task.save()
    return {'task_id': gen_task.task_id, 'status': 'SUCCESS', 'results': results}
