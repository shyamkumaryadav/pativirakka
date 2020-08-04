from django import forms
from django.contrib.auth.forms import UserCreationForm as UCF
from .models import User


class UserCreationForm(UCF):
    class Meta(UCF.Meta):
        model = User
