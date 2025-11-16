from django.core.files.base import ContentFile
from django.conf import settings
from django.core.cache import cache

from .models import Mockup
from .pigs import create_mockup_image
from celery import shared_task

import uuid
import json
import io


# CELERY TASK GENERATOR
@shared_task(bind=True)
def generate_mockups_task(self, task_id, text, font, text_color, shirt_colors):

    redis_key = f"task:{task_id}"

    cache.set(redis_key, json.dumps({
        "status": "IN_PROGRESS"
    }), timeout=86400)

    results = []

    for color in shirt_colors:
        try:
            img = create_mockup_image(
                text=text,
                shirt_color=int(color),
                text_color=int(text_color),
                font_name=font
            )

            filename = f"mockup_{task_id}_{color}_{uuid.uuid4().hex[:6]}.png"
            image_bytes = io.BytesIO()
            img.save(image_bytes, format='PNG')

            mockup = Mockup.objects.create(
                task_id=task_id,
                text=text,
                font=font,
                text_color=text_color,
                shirt_color=color
            )

            mockup.image.save(filename, ContentFile(image_bytes.getvalue()))
            mockup.save()

            results.append({
                "image_url": mockup.image.url,
                "id": mockup.id
            })

        except Exception as e:
            print("Mockup error:", e)

    cache.set(redis_key, json.dumps({
        "status": "SUCCESS",
        "results": results
    }), timeout=86400)

    return {"task_id": task_id, "status": "SUCCESS", "results": results}