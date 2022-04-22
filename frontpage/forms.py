from django import forms
from .models import DailyReport, UserInfo, Group, Chat, UserGroupJoinTable, UserGroupRequest
from django.contrib.auth import get_user_model

User = get_user_model()

class SendGroupJoinRequest(forms.ModelForm):
    class Meta:
        model=UserGroupRequest
        fields=[
            'Group'
        ]

class EditUserInfo(forms.ModelForm):#forms.Form
    class Meta:
        model=UserInfo
        fields=['DateOfBirth','HeightFeet','HeightInches','Weight','Gender']

class MakeGroup(forms.ModelForm):
    class Meta:
        model=Group
        fields=[
            'GroupName'
        ]

class DailyReportForm(forms.ModelForm):
    class Meta:
        model = DailyReport
        fields=[
            'RatingOfDay',
            'StepsTaken',
            'HoursSitting',
            'HoursSlept',
            'LengthOfWorkout',
            'IntensityOfWorkout',
            'MealsEaten',
            'SnacksEaten',
            'FoodHealth',
            'CigarettesSmoked',
            'AlcoholicDrinks'
        ]

class SendChat(forms.ModelForm):
    class Meta:
        model = Chat
        fields=[
            'Recipient',
            'MessageTitle',
            'MessageBody'
        ]