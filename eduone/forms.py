from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Options


class createuserform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password']

class OptionsForm(form.ModelForm):
    class Meta:
        model = Option
        fields=['text']