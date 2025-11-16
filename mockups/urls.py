from django.urls import path
from .views import GenerateMockupView, TaskStatusView, MockupListView

# 3 ENDPOINTS
# futures : authentication for endpoint login
# futures : what is swagger ?
urlpatterns = [
    path('mockups/generate', GenerateMockupView.as_view(), name='generate-mockup'),
    path('tasks/<str:task_id>/', TaskStatusView.as_view(), name='task-status'),
    path('mockups/', MockupListView.as_view(), name='active-mockup-list'),
]
