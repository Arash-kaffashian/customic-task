from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters

from django.shortcuts import get_object_or_404, render

from .models import GenerationTask, Mockup
from .serializers import GenerationTaskSerializer, MockupSerializer
from .tasks import generate_mockups_task

import uuid


def mockup_form_view(request):
    return render(request, 'generate-page.html')


class GenerateMockupView(APIView):
    def post(self, request):
        data = request.data
        text = data.get('text', '')
        font = data.get('font')
        text_color = int(data.get('text_color', 1))  # تبدیل به عدد چون مدل عدد می‌خواد
        shirt_color_raw = data.get('shirt_color', 4)

        # اگه کاربر چند رنگ داده باشه (لیست)
        if isinstance(shirt_color_raw, list):
            shirt_colors = [int(c) for c in shirt_color_raw]
        else:
            # اگه فقط یه رنگ داده باشه
            shirt_colors = [int(shirt_color_raw)]

        text_color = int(data.get('text_color', 1))

        task_id = str(uuid.uuid4())
        gen_task = GenerationTask.objects.create(task_id=task_id, status='PENDING')

        shirt_colors = [1, 2, 3, 4]

        generate_mockups_task.delay(gen_task.id, text, font, text_color, shirt_colors)

        return Response({'task_id': task_id, 'status': 'PENDING', 'message': 'ساخت تصویر آغاز شد'},status=status.HTTP_202_ACCEPTED)


class TaskStatusView(APIView):
    def get(self, request, task_id):
        gen_task = get_object_or_404(GenerationTask, task_id=task_id)
        serializer = GenerationTaskSerializer(gen_task, context={'request': request})
        return Response(serializer.data)


class MockupListView(generics.ListAPIView):
    serializer_class = MockupSerializer
    queryset = Mockup.objects.all().order_by('-created_at')
    filter_backends = [filters.SearchFilter]
    search_fields = ['text', 'shirt_color']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
