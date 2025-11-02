from rest_framework import status, generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404, render

from .serializers import GenerationTaskSerializer, MockupSerializer
from .models import GenerationTask, Mockup
from .tasks import generate_mockups_task

import uuid


# VIEW GENERATE
class GenerateMockupView(APIView):
    def post(self, request):
        data = request.data

        text = str(data.get('text', '')).strip()
        font = str(data.get('font', '')).strip()
        text_color = int(data.get('text_color', 1))
        shirt_color_raw = data.get('shirt_color', [4])

        # CHECKING shirt_color TYPE
        if isinstance(shirt_color_raw, str):
            try:
                shirt_colors = json.loads(shirt_color_raw)
            except json.JSONDecodeError:
                shirt_colors = [int(shirt_color_raw)]
        else:
            shirt_colors = [int(c) for c in shirt_color_raw]

        print("🟢 Received:", data)

        # task_id MUST BE unique THATS WHY WE USE UUID FOR EACH TASK
        task_id = str(uuid.uuid4())
        gen_task = GenerationTask.objects.create(task_id=task_id, status='PENDING')

        # SENDING DATA TO CELERY TASK
        generate_mockups_task.delay(
            gen_task.id,
            text,
            font,
            text_color,
            shirt_colors
        )

        return Response({
            'task_id': task_id,
            'status': 'PENDING',
            'message': 'ساخت تصویر آغاز شد'
        }, status=status.HTTP_202_ACCEPTED)


# VIEW TASK STATUS
class TaskStatusView(APIView):
    def get(self, request, task_id):
        gen_task = get_object_or_404(GenerationTask, task_id=task_id)
        serializer = GenerationTaskSerializer(gen_task, context={'request': request})
        return Response(serializer.data)


# VIEW MOCKUP LIST
class MockupListView(generics.ListAPIView):
    serializer_class = MockupSerializer
    queryset = Mockup.objects.all().order_by('-created_at')
    filter_backends = [filters.SearchFilter]
    search_fields = ['text', 'shirt_color']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
