from django.urls import path
from .views import GenerateMockupView, TaskStatusView, MockupListView

# 3 ENDPOINTS
urlpatterns = [
    path('mockups/generate', GenerateMockupView.as_view(), name='generate-mockup'),
    path('tasks/<uuid:task_id>/', TaskStatusView.as_view(), name='task-status'),
    path('mockups', MockupListView.as_view(), name='mockup-list'),
]

