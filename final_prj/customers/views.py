from django.shortcuts import render

# Create your views here.
from .models import CustomUserModel
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomUserView(LoginRequiredMixin):
    model = CustomUserModel
