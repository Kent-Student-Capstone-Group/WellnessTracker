from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
#from django.db import models
#from sqlalchemy import ForeignKey, true


class UserInfo(models.Model):
    #FirstName = models.CharField(max_length=100)
    #LastName = models.CharField(max_length=100)
    #Email = models.CharField(max_length=100)
    #Password = models.CharField(max_length=100)
    DateOfBirth = models.DateTimeField(blank=True, null=True)
    HeightFeet = models.IntegerField(blank=1, null=True)
    HeightInches = models.IntegerField(blank=1, null=True)
    Weight = models.FloatField(blank=1, null=True)
    Gender = models.CharField(max_length=20, blank=1, null=True)
    #IsActive = models.BooleanField(default=True, blank=1)
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.FirstName + ' ' + self.LastName

class Group(models.Model):
    Owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    GroupName = models.CharField(max_length=100)
    NumMembers = models.IntegerField(default=1)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return self.GroupName

class Message(models.Model):
    Sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Sender')
    Recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Recipient')
    TimeSent = models.DateTimeField()
    MessageTitle = models.CharField(max_length=100)
    MessageBody = models.CharField(max_length=5000)

    # def __str__(self):
    #     return self.Sender + ': ' + self.MessageTitle

class DailyReport(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    DateAndTime = models.DateTimeField(default=timezone.now())
    RatingOfDay = models.IntegerField(blank=1)
    StepsTaken = models.IntegerField(blank=1)
    HoursSitting = models.FloatField(blank=1)
    HoursSlept = models.FloatField(blank=1)
    WorkedOut = models.BooleanField(blank=1)
    LengthOfWorkout = models.FloatField(blank=1)
    IntensityOfWorkout = models.IntegerField(blank=1)
    MealsEaten = models.IntegerField(blank=1)
    SnacksEaten = models.IntegerField(blank=1)
    FoodHealth = models.FloatField(blank=1)
    CigarettesSmoked = models.IntegerField(blank=1)
    AlcoholicDrinks = models.IntegerField(blank=1)

    # def __str__(self):
    #     return self.User.FirstName + self.User.LastName + ":" + self.DateAndTime

class UserGroupRequest(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Group = models.ForeignKey(Group, on_delete=models.CASCADE)
    TimeOfRequest = models.DateTimeField()

    # def __str__(self):
    #     return self.User.FirstName + self.User.LastName + ":" + self.Group.GroupName

class UserGroupJoinTable(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Group = models.ForeignKey(Group, on_delete=models.CASCADE)
    DateJoined = models.DateTimeField(default=timezone.now())

    # def __str__(self):
    #     return self.User.FirstName + self.User.LastName + ":" + self.Group.GroupName