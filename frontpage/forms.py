from django import forms
from .models import UserInfo
from django.contrib.auth import get_user_model

User = get_user_model()

class EditUserInfo(forms.ModelForm):#forms.Form
    class Meta:
        model=UserInfo
        fields=['DateOfBirth','HeightFeet','HeightInches','Weight','Gender']