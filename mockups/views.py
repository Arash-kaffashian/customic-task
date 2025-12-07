from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.core.cache import cache

from .serializers import MockupSerializer
from .models import Mockup, Color, Font, Shirt
from .tasks import generate_mockups_task

import uuid
import json


class FontListView(APIView):
    def get(self, request):
        key = "fonts:list"
        data = cache.get(key)

        if not data:
            data = list(Font.objects.all().values("id", "name"))
            cache.set(key, data, 86400)

        return Response(data)


class ColorListView(APIView):
    def get(self, request):
        key = "colors:list"
        data = cache.get(key)
        print("رنگ‌ها کش شده‌اند")

        if not data:
            data = list(Color.objects.all().values("id", "color", "hex"))
            cache.set(key, data, 86400)
            print("رنگ‌ها هنوز کش نشده‌اند")

        return Response(data)


class ShirtColorListView(APIView):
    def get(self, request):
        key = "shirts:list"
        data = cache.get(key)

        if not data:
            data = list(Shirt.objects.filter(existence=True).values("id", "color", "image"))
            cache.set(key, data, 86400)

        return Response(data)


# VIEW GENERATE
class GenerateMockupView(APIView):
    def post(self, request):

        data = request.data

        # ---------------------------
        # TEXT VALIDATION
        # ---------------------------
        text = str(data.get('text', '')).strip()
        if not text:
            return Response({"error": "text field is required"}, status=400)

        # ---------------------------
        # FONT VALIDATION (optional)
        # ---------------------------
        font_val = data.get('font')
        font_obj = None
        if font_val:
            font_obj = Font.objects.filter(name=font_val).first()
            if not font_obj:
                return Response({"error": "font not found"}, status=404)

        # ---------------------------
        # TEXT COLOR VALIDATION (optional)
        # ---------------------------
        text_color_val = data.get('text_color')
        text_color_obj = None
        if text_color_val:
            text_color_obj = Color.objects.filter(color=text_color_val).first()
            if not text_color_obj:
                return Response({"error": "text color not found"}, status=404)

        # ---------------------------
        # SHIRT COLORS (required)
        # ---------------------------
        shirt_colors = data.get("shirt_color", [])

        # اگر رشته بود (مثلاً JSON string از فرانت)
        if isinstance(shirt_colors, str):
            try:
                shirt_colors = json.loads(shirt_colors)
            except:
                return Response({"error": "shirt_color must be a list"}, status=400)

        if not isinstance(shirt_colors, list):
            return Response({"error": "shirt_color must be a list"}, status=400)

        if len(shirt_colors) == 0:
            return Response({"error": "at least one shirt_color is required"}, status=400)

        shirt_objs = []
        for sc in shirt_colors:
            shirt_obj = Shirt.objects.filter(color=sc).first()
            if not shirt_obj:
                return Response({"error": f"shirt color '{sc}' not found"}, status=404)

            if not shirt_obj.existence:
                return Response({"error": f"shirt color '{sc}' is not available"}, status=400)

            shirt_objs.append(shirt_obj.id)

        # ---------------------------------------
        # CREATE TASK
        # ---------------------------------------
        task_id = uuid.uuid4().hex

        cache.set(
            f"task:{task_id}",
            json.dumps({"status": "PENDING"}),
            timeout=86400
        )

        generate_mockups_task.delay(
            task_id=task_id,
            text=text,
            font_id=font_obj.id if font_obj else None,
            text_color_id=text_color_obj.id if text_color_obj else None,
            shirt_color_ids=shirt_objs,
        )

        return Response({
            "task_id": task_id,
            "status": "PENDING"
        })


# VIEW TASK STATUS
class TaskStatusView(APIView):
    def get(self, request, task_id):

        # 1) reading status from redis
        redis_key = f"task:{task_id}"
        cached = cache.get(redis_key)

        if not cached:
            return Response({
                "error": "Task not found or expired"
            }, status=status.HTTP_404_NOT_FOUND)

        task_data = json.loads(cached)

        # 2) Fetching all mockups from DB with this task_id
        mockups = Mockup.objects.filter(task_id=task_id).order_by('-created_at')

        results = []
        for m in mockups:
            results.append({
                "image_url": request.build_absolute_uri(m.image.url),
                "created_at": m.created_at.isoformat()
            })

        # 3) generate final response and return
        return Response({
            "task_id": task_id,
            "status": task_data.get("status", "UNKNOWN"),
            "results": results
        })


# VIEW MOCKUP LIST
class MockupListView(APIView):
    """
    List all Mockups stored in the DB
    """
    def get(self, request):
        # all mockups by task_id ordered by created_at
        mockups = Mockup.objects.all().order_by('-created_at')

        # Serialize with MockupSerializer
        serializer = MockupSerializer(mockups, many=True, context={"request": request})
        return Response(serializer.data)
