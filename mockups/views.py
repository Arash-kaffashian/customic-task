from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.core.cache import cache

from .serializers import MockupSerializer
from .models import Mockup
from .tasks import generate_mockups_task

import uuid
import json


# green code : why apiview (what is the different between apiview and generic view)
# VIEW GENERATE
class GenerateMockupView(APIView):
    def post(self, request):
        data = request.data

        text = str(data.get('text', '')).strip()
        font = str(data.get('font', '')).strip()
        text_color = int(data.get('text_color', 1))
        shirt_colors = data.get('shirt_color', [4])
        if isinstance(shirt_colors, str):
            shirt_colors = json.loads(shirt_colors)

        task_id = uuid.uuid4().hex

        cache.set(f"task:{task_id}", json.dumps({
            "status": "PENDING"
        }), timeout=86400)

        generate_mockups_task.delay(task_id, text, font, text_color, shirt_colors)

        return Response({
            "task_id": task_id,
            "status": "PENDING"
        })


# VIEW TASK STATUS
class TaskStatusView(APIView):
    def get(self, request, task_id):

        # 1) وضعیت را از Redis بخوان
        redis_key = f"task:{task_id}"
        cached = cache.get(redis_key)

        if not cached:
            return Response({
                "error": "Task not found or expired"
            }, status=status.HTTP_404_NOT_FOUND)

        task_data = json.loads(cached)

        # 2) تمام mockup های این task_id را از دیتابیس بگیر
        mockups = Mockup.objects.filter(task_id=task_id).order_by('-created_at')

        results = []
        for m in mockups:
            results.append({
                "image_url": request.build_absolute_uri(m.image.url),
                "created_at": m.created_at.isoformat()
            })

        # 3) خروجی نهایی را دستی بساز و برگردان
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
        # همه Mockupها بر اساس task_id مرتب شده بر اساس تاریخ
        mockups = Mockup.objects.all().order_by('-created_at')

        # Serialize با MockupSerializer
        serializer = MockupSerializer(mockups, many=True, context={"request": request})
        return Response(serializer.data)
