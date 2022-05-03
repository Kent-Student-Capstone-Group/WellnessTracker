#from this import d
from django.db import models
from django.conf import settings
#from django.utils import timezone
import datetime

# Create your models here.
#from django.db import models
#from sqlalchemy import ForeignKey, true


class UserInfo(models.Model):
    #FirstName = models.CharField(max_length=100)
    #LastName = models.CharField(max_length=100)
    #Email = models.CharField(max_length=100)
    #Password = models.CharField(max_length=100)
    DateOfBirth = models.DateField(blank=True, null=True)
    HeightFeet = models.IntegerField(blank=1, null=True)
    HeightInches = models.IntegerField(blank=1, null=True)
    Weight = models.FloatField(blank=1, null=True)
    Gender = models.CharField(max_length=20, blank=1, null=True)
    #IsActive = models.BooleanField(default=True, blank=1)
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    UserSteps = models.IntegerField(blank=1, default=0, null=True)

    def __str__(self):
        return self.User.username

class Group(models.Model):
    Owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    GroupName = models.CharField(max_length=100)
    NumMembers = models.IntegerField(default=1)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return self.GroupName

class Chat(models.Model):
    Sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Sender', null=True)
    Recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Recipient', null=True)
    TimeSent = models.DateTimeField(auto_now=True)
    MessageTitle = models.CharField(max_length=100, null=True)
    MessageBody = models.TextField(max_length=5000, null=True)

    # def __str__(self):
    #     return self.Sender.username + ' to ' + self.Recipient.username + ': ' + self.MessageTitle

class DailyReport(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    DateAndTime = models.DateTimeField(null=True)
    RatingOfDay = models.IntegerField(blank=1, null=True)
    StepsTaken = models.IntegerField(blank=1, null=True)
    HoursSitting = models.FloatField(blank=1, null=True)
    HoursSlept = models.FloatField(blank=1, null=True)
    LengthOfWorkout = models.FloatField(blank=1, null=True)
    IntensityOfWorkout = models.IntegerField(blank=1, null=True)
    MealsEaten = models.IntegerField(blank=1, null=True)
    SnacksEaten = models.IntegerField(blank=1, null=True)
    FoodHealth = models.FloatField(blank=1, null=True)
    CigarettesSmoked = models.IntegerField(blank=1, null=True)
    AlcoholicDrinks = models.IntegerField(blank=1, null=True)

    def __str__(self):
        return self.User.username + ": " + self.DateAndTime.strftime("%m/%d/%Y, %H:%M:%S")

class UserGroupRequest(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Group = models.ForeignKey(Group, on_delete=models.CASCADE)
    TimeOfRequest = models.DateTimeField()
    STATUS_CHOICES = [('R', 'Request'), ('I', 'Invite')]
    Status = models.CharField(max_length=1, choices=STATUS_CHOICES, null=True)

    def __str__(self):
        return self.User.username + ":" + self.Group.GroupName

class UserGroupJoinTable(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Group = models.ForeignKey(Group, on_delete=models.CASCADE)
    DateJoined = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.User.username + ":" + self.Group.GroupName

class MetalsTable(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ReachedUserGoal = models.BooleanField(default=False)
    FirstSteps = models.BooleanField(default=False)
    StepsTaken = models.BooleanField(default=False)
    Over6Months = models.BooleanField(default=False)
    Powerhouse = models.BooleanField(default=False)
    TeamWork = models.BooleanField(default=False)
    Teamleader = models.BooleanField(default=False)
    ReachedTeamGoal = models.BooleanField(default=False)

    def __str__(self):
        return "Medals: " + self.User.username


class FitBitData(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    DateAndTime = models.DateTimeField(null=True)
    StepsTaken = models.IntegerField(blank=1, null=True)
    HeartRate = models.IntegerField(blank=1, null=True)
    HoursSlept = models.FloatField(blank=1, null=True)
    ActiveHours = models.FloatField(blank=1, null=True)
    #Activity types ??
    def __str__(self):
         return '%s %s' % (self.StepsTaken, self.HeartRate, self.HoursSlept)

class UserCustomField(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Title = models.CharField(max_length=100, blank=1, null=True)

    class Meta:
        unique_together = ['User', 'Title']

    def __str__(self):
        return '%s %s' % (self.User.username, self.Title)

class UserCustomData(models.Model):
    Field = models.ForeignKey(UserCustomField, on_delete=models.CASCADE, null=True)
    Value = models.IntegerField(blank=1, null=True)
    Date = models.DateField(blank=True, null=True)

    def __str__(self):
        return '%s %s %s' % (self.Field.User.username, self.Field.Title , self.Date)

class CustomGoal(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    Field = models.ForeignKey(UserCustomField, on_delete=models.CASCADE)
    Value = models.IntegerField(blank=1, null=True)
    EndDate = models.DateField(blank=True, null=True)
    StartDate = models.DateField(blank=True, null=True)

    def __str__(self):
        return '%s %s %s' % (self.Field.User.username, self.Field.Title , self.StartDate)

class FitBitToken(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    UserID = models.TextField()
    AccessToken = models.TextField()
    RefreshToken = models.TextField()
    Expiration = models.DateTimeField()
    Type = models.TextField()
    Scope = models.TextField()
