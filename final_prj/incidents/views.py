from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import IncidentSerializer

class IncidentView(APIView):

    ser_class = IncidentSerializer

    def post(self, request):

        print('data', request.data)

        return Response(status=status.HTTP_200_OK)