from django.core.files.base import ContentFile
from django.conf import settings

from .models import GenerationTask, Mockup
from .pigs import create_mockup_image
from celery import shared_task

import uuid
import io


# CELERY TASK GENERATOR
@shared_task(bind=True)
def generate_mockups_task(self, task_db_id, text, font, text_color, shirt_colors):
    try:
        gen_task = GenerationTask.objects.get(id=task_db_id)
        gen_task.status = 'IN_PROGRESS'
        # red code : save() = hard code ? is it not scalable ?
        gen_task.save()
    except GenerationTask.DoesNotExist:
        return {'error': 'GenerationTask not found'}

    # green code : need to change ?
    shirt_colors = [int(c) for c in shirt_colors]
    text_color = int(text_color)
    results = []
    for color in shirt_colors:
        try:
            img = create_mockup_image(
                text=text,
                shirt_color=color,
                text_color=text_color,
                font_name=font
            )

            # need to change if we change taskid generation method
            filename = f'mockup_{gen_task.task_id}_{color}_{uuid.uuid4().hex[:8]}.png'
            image_bytes = io.BytesIO()
            img.save(image_bytes, format='PNG')

            mockup = Mockup.objects.create(
                gen_task=gen_task,
                text=text,
                font=font,
                text_color=text_color,
                shirt_color=color,
            )

            mockup.image.save(filename, ContentFile(image_bytes.getvalue()), save=True)
            mockup.refresh_from_db()

            print("✅ Saved mockup to:", mockup.image.path)

            # orange code : created at or updated at
            results.append({
                'image_url': mockup.image.url,
                'created_at': mockup.created_at.isoformat()
            })

        except Exception as e:
            print(f"❌ Error generating mockup for color {color}: {e}")

    gen_task.status = 'SUCCESS'
    # red code : save() = hard code ?
    gen_task.save()
    return {'task_id': gen_task.task_id, 'status': 'SUCCESS', 'results': results}
