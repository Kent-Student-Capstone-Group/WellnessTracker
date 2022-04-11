from django import forms
from zmq import Message
from .models import DailyReport, UserInfo, Group
from django.contrib.auth import get_user_model

User = get_user_model()

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
            'User',
            'DateAndTime',
            'RatingOfDay',
            'StepsTaken',
            'HoursSitting',
            'HoursSlept',
            'WorkedOut',
            'LengthOfWorkout',
            'IntensityOfWorkout',
            'MealsEaten',
            'SnacksEaten',
            'FoodHealth',
            'CigarettesSmoked',
            'AlcoholicDrinks'
        ]

class SendMessage(forms.ModelForm):
    class Meta:
        model = Message
        fields=[
            'Recipient',
            'MessageTitle',
            'MessageBody'
        ]