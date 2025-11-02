from django.urls import path
from .views import GenerateMockupView, TaskStatusView, MockupListView, mockup_form_view

urlpatterns = [
    path('form/', mockup_form_view, name='mockup_form'),
    path('generate/', GenerateMockupView.as_view(), name='generate-mockup'),
    path('status/<uuid:task_id>/', TaskStatusView.as_view(), name='task-status'),
    path('', MockupListView.as_view(), name='mockup-list'),
]

