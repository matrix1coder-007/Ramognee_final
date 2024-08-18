from rest_framework import serializers
from .models import IncidentModel


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentModel
        fields = ('__all__')