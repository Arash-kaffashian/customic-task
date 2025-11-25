from django.core.files.base import ContentFile
from django.conf import settings
from django.core.cache import cache

from .models import Mockup, Shirt, Font, Color
from .pigs import create_mockup_image
from celery import shared_task

import uuid
import json
import io


@shared_task(bind=True)
def generate_mockups_task(self, task_id, text, font_id, text_color_id, shirt_color_ids):

    redis_key = f"task:{task_id}"

    cache.set(redis_key, json.dumps({
        "status": "IN_PROGRESS"
    }), timeout=86400)

    results = []

    # --------------------------
    # گرفتن اشیاء واقعی از DB
    # --------------------------
    font_obj = Font.objects.filter(id=font_id).first()
    color_obj = Color.objects.filter(id=text_color_id).first()

    for shirt_id in shirt_color_ids:

        try:
            shirt_obj = Shirt.objects.filter(id=shirt_id).first()
            if not shirt_obj:
                continue

            # ساخت تصویر
            img = create_mockup_image(
                text=text,
                shirt_obj=shirt_obj,
                color_obj=color_obj,
                font_obj=font_obj,
            )

            filename = f"mockup_{task_id}_{shirt_id}_{uuid.uuid4().hex[:6]}.png"
            image_bytes = io.BytesIO()
            img.save(image_bytes, format='PNG')

            # ساخت رکورد Mockup
            mockup = Mockup.objects.create(
                task_id=task_id,
                text=text,
                font=font_obj,
                text_color=color_obj,
                shirt_color=shirt_obj
            )

            # ذخیره عکس
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
