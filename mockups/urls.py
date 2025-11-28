from django.urls import path
from .views import GenerateMockupView, TaskStatusView, MockupListView, ShirtColorListView, FontListView, ColorListView

# 3 ENDPOINTS
# futures : authentication for endpoint login
# futures : what is swagger ?
urlpatterns = [
    path('mockups/generate', GenerateMockupView.as_view(), name='generate-mockup'),
    path('tasks/<str:task_id>/', TaskStatusView.as_view(), name='task-status'),
    path('mockups/', MockupListView.as_view(), name='active-mockup-list'),

    # cached lists
    path('colors/', ColorListView.as_view()),
    path('fonts/', FontListView.as_view()),
    path('shirts/', ShirtColorListView.as_view()),
]
