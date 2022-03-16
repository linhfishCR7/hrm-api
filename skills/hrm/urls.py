from django.urls import path
from .views import (
    ListCreateSkillsAPIView,
    RetrieveUpdateDestroySkillsAPIView
)


urlpatterns = [
    path('', ListCreateSkillsAPIView.as_view(), name='list-create-skill'),
    path('<uuid:id>/', RetrieveUpdateDestroySkillsAPIView.as_view(), name='retrieve-update-destroy-skill'),
]
