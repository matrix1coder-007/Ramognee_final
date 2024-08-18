from django.urls import path

app_label = 'incidents'

from .views import IncidentView

urlpatterns = [
    path('close_incident/', IncidentView.as_view()),
]
