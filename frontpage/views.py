from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
import datetime
from django.contrib.auth import get_user_model
from .models import DailyReport, UserInfo, UserGroupJoinTable, UserInfo, Group, Chat, UserGroupRequest, FitBitData, UserCustomData, UserCustomField, UserCustomData, CustomGoal, FitBitToken
from .forms import EditUserInfo, MakeGroup, DailyReportForm, SendChat, SendGroupJoinRequest
from django.contrib import messages
import time
#import fitapp
from django.conf import settings
#import requests
#import urllib2
import urllib
import base64
#from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp
import json

# Create your views here.


def welcome(request):
    if(request.user.is_authenticated):
        return redirect('frontpage:index')
        # try:
        #     info = UserInfo.objects.get(User=request.user)
        #     return render(request, 'frontpage/index.html', {'info':info})
        # except UserInfo.DoesNotExist:
        #     return render(request, 'frontpage/index.html')
    else:
        return redirect('/accounts/google/login')

def index(request):

    if(request.user.is_authenticated):
        customFields = UserCustomField.objects.filter(User=request.user) 
        goals = CustomGoal.objects.filter(User=request.user)
        
        goalStats = {}
        for goal in goals:
            goalData = UserCustomData.objects.filter(Field=goal.Field, Date__range=(goal.StartDate,goal.EndDate))
            goalSum = 0
            for data in goalData:
                goalSum += data.Value
            goalCompletion = (goalSum/goal.Value) * 100
            if goal.EndDate > datetime.date.today():
                dailyAvg = goalSum / int((goal.EndDate - datetime.date.today()).days)
            else:
                dailyAvg = goalSum/ int((goal.EndDate - goal.StartDate).days)
            requiredAvg = goal.Value / int((goal.EndDate - goal.StartDate).days)
            #goalDetails = {'goalSum':goalSum, 'goalCompletion':goalCompletion, 'dailyAvg':dailyAvg, 'requiredAvg':requiredAvg}#[goalSum, goalCompletion, dailyAvg, requiredAvg]
            goalStats[str(goal.id)+"goalSum"] = goalSum
            goalStats[str(goal.id)+"goalCompletion"] = round(goalCompletion,2)
            goalStats[str(goal.id)+"dailyAvg"] = round(dailyAvg, 2)
            goalStats[str(goal.id)+"requiredAvg"] = round(requiredAvg,2)
            


        
        if not request.GET.get('end_date'):
            end_date = datetime.datetime.now() + datetime.timedelta(days=1)
        else:
            end_date = datetime.datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d') + datetime.timedelta(hours=23, minutes=59, seconds=59)
        if not request.GET.get('start_date'):
            start_date = datetime.datetime.now() + datetime.timedelta(days=-31)
        else:
            start_date = datetime.datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d')
            
        chartData = DailyReport.objects.filter(User=request.user, DateAndTime__range=(start_date,end_date)).order_by('DateAndTime')
        customChartData = UserCustomData.objects.filter(Field__User=request.user, Date__range=(start_date.date(),end_date.date())).order_by('Date')

        if request.POST.get('form') == 'goalForm':
            newCustomGoal = CustomGoal()
            newCustomGoal.User=request.user
            newCustomGoal.StartDate = request.POST.get('start_date')
            newCustomGoal.EndDate = request.POST.get('end_date')
            if newCustomGoal.StartDate >= newCustomGoal.EndDate:
                messages.error(request, "Start date must be less than end date")
                return redirect('frontpage:index')
            newCustomGoal.Field = UserCustomField.objects.get(User=request.user, Title=request.POST.get('field'))
            newCustomGoal.Value = request.POST.get('value')
            try:
                newCustomGoal.save()
                messages.success(request, "Goal added!")
            except:
                messages.warning(request, "The form was incorrect.")
            return redirect('frontpage:index')

        #UserData = UserCustomData.objects.filter(User = request.user)
        #FitBitToday = FitBitData.object.filter(DateAndTime.date.today() == datetime.date.today())   # Will likely move to another view
        #context = {'chartData': chartData, 'customFields':customFields, 'goals':goals}
        context = {}
        context['chartData'] = chartData
        context['customFields'] = customFields
        context['goals'] = goals
        context['goalStats'] = goalStats
        context['customChartData'] = customChartData
        #context['string'] = string
        return render(request, 'frontpage/index.html', context)
    else:
        return redirect('frontpage:welcome')


def badges(request):
    if (request.user.is_authenticated):
        return render(request, 'frontpage/badges.html')
    
    else:
        return redirect('frontpage:welcome')

def createUserInfo(request):
    if (request.user.is_authenticated):
        try:
            info_sel = UserInfo.objects.get(User= request.user)
        except UserInfo.DoesNotExist:
            obj = UserInfo()
            obj.User = request.user
            obj.save()
            return redirect('frontpage:userInfo')
        form = EditUserInfo(request.POST or None, instance = info_sel)
        if form.is_valid():
            form.save()
            messages.success(request, "Info Submitted")
            return redirect('frontpage:index')
        else:
            messages.warning(request, "Invalid Form")
        return render(request, 'frontpage/userInfo_form.html', {'upload_form':form})
    else:
        return redirect('frontpage:welcome')

def chat(request):   
    if (request.user.is_authenticated):
        chats = Chat.objects.filter(Recipient=request.user)
        form = SendChat(request.POST or None)
        if form.is_valid():
            newChat = Chat(Sender = request.user, MessageTitle = request.POST.get("MessageTitle"), MessageBody = request.POST.get("MessageBody"))
            newChat.Recipient = get_user_model().objects.get(id=request.POST.get("Recipient"))
            try:
                newChat.save()
                messages.success(request, "Message Sent")
            except:
                messages.warning(request, "Could not Send Message")
            return render(request, 'frontpage/index.html')
        return render(request, 'frontpage/chat.html', {'chats': chats, 'form': form})
    
    else:
        return redirect('frontpage:welcome')

def contact(request):   
    return render(request, 'frontpage/contact.html')

def dailyReport(request):
    if (request.user.is_authenticated):

        if request.POST.get('form') == 'field-form':
            newUserCustomField = UserCustomField()
            newUserCustomField.User = request.user
            newUserCustomField.Title = request.POST.get('title')
            try:
                newUserCustomField.save()
            except:
                messages.error(request, "A field by that name already exists")
            return redirect('frontpage:dailyreport')

        customFields = UserCustomField.objects.filter(User=request.user)
        form = DailyReportForm(request.POST or None)
        TodayReports = DailyReport.objects.filter(DateAndTime=datetime.date.today())
        alreadySubmittedToday = len(TodayReports) > 0
        
        # form.User = request.user
        if form.is_valid():
            newDailyReport = DailyReport()
            newDailyReport.User = request.user
            newDailyReport.DateAndTime = datetime.datetime.now()
            newDailyReport.RatingOfDay = request.POST.get("RatingOfDay")
            newDailyReport.StepsTaken = request.POST.get("StepsTaken")
            newDailyReport.HoursSitting = request.POST.get("HoursSitting")
            newDailyReport.HoursSlept = request.POST.get("HoursSlept")
            newDailyReport.LengthOfWorkout = request.POST.get("LengthOfWorkout")
            newDailyReport.IntensityOfWorkout = request.POST.get("IntensityOfWorkout")
            newDailyReport.MealsEaten = request.POST.get("MealsEaten")
            newDailyReport.SnacksEaten = request.POST.get("SnacksEaten")
            newDailyReport.FoodHealth = request.POST.get("FoodHealth")
            newDailyReport.CigarettesSmoked = request.POST.get("CigarettesSmoked")
            newDailyReport.AlcoholicDrinks = request.POST.get("AlcoholicDrinks")
            try:
                newDailyReport.save()
            except:
                messages.warning(request, "All fields must be filled correctly.")
                return redirect('frontpage:dailyReport')

            for field in customFields:
                newUserCustomData = UserCustomData()
                newUserCustomData.Field = field
                nameStr = str(field.Title) + "-" + str(field.id)
                newUserCustomData.Value = request.POST.get(nameStr)
                newUserCustomData.Date = datetime.date.today()
                try:
                    newUserCustomData.save()
                except:
                    messages.warning(request, "All fields must be filled correctly.")


            messages.success(request, "Daily Report Submitted")
            try:
                userInfo = UserInfo.objects.get(User = request.user)
                userInfo.UserSteps = userInfo.UserSteps + int(newDailyReport.StepsTaken)
                userInfo.save()
            except:
                messages.warning(request,"No user info")
            
            return redirect('frontpage:index')
        return render(request, 'frontpage/dailyreport.html', {'form': form, 'alreadySubmittedToday': alreadySubmittedToday, 'customFields':customFields})
    else:
        return redirect('frontpage:welcome')
    

def group(request):  
    if request.user.is_authenticated:
        user = request.user
        context = {
            'userGroups': UserGroupJoinTable.objects.filter(User = user),
            'ownerGroups': Group.objects.filter(Owner = request.user),
            'invites': UserGroupRequest.objects.filter(User=request.user, Status='I'),
        }
        if request.method=="POST":
                NewUserGroupJoin = UserGroupJoinTable()
                NewUserGroupJoin.User = request.user
                NewUserGroupJoin.Group = Group.objects.get(id=request.POST.get("Group"))
                NewUserGroupJoin.DateJoined = datetime.datetime.now()
                try:
                    NewUserGroupJoin.save()
                    UserGroupRequest.objects.get(User=request.user, Group=Group.objects.get(id = request.POST.get("Group"))).delete()
                    messages.success(request, 'Group Succesfully Joined')
                    return redirect('frontpage:group')
                except:
                    messages.warning(request, "Could not join group.")
                    return redirect('frontpage:group')
                
        elif request.GET.get("groupSearch"):
            try:
                groupSearch = request.GET.get("groupSearch")
                matchGroups = Group.objects.filter(GroupName__icontains=groupSearch)
                return render(request, 'frontpage/searchGroups.html', {'groupSearch':groupSearch,'matchGroups':matchGroups})
            except Group.DoesNotExist:
                return render(request, 'frontpage/searchGroups.html', {'groupSearch':groupSearch})
        else:
            return render(request, 'frontpage/group.html', context)
    else:
        return redirect('frontpage:welcome')

def groupstat(request):   
    if request.user.is_authenticated:
        return render(request, 'frontpage/groupstat.html')
    else:
        return redirect('frontpage:welcome')

def info(request):   
    return render(request, 'frontpage/info.html')

def makeGroup(request):
    #info_sel = UserInfo.objects.get(User= request.user)

    if (request.user.is_authenticated):
        if request.method == 'POST':
            
            #Ensure that there is not already a group with the same owner and name
            try:
                userCurrentOwnedGroups = Group.objects.get(Owner = request.user, GroupName=request.POST.get("GroupName"))  
            except Group.DoesNotExist:
                form = MakeGroup(request.POST or None)
                if form.is_valid():
                    NewGroup = Group()
                    NewGroup.Owner = request.user
                    NewGroup.GroupName = request.POST.get("GroupName")

                    NewUserGroupJoin = UserGroupJoinTable()
                    NewUserGroupJoin.Group = NewGroup
                    NewUserGroupJoin.User = request.user
                    try:
                        NewGroup.save()
                        NewUserGroupJoin.save()
                        messages.success(request, 'Group Succesfully Created')
                    except:
                        messages.warning(request, 'Could not create group')
                    return redirect('frontpage:makegroup')
                    
                else:
                    #messages.warning(request, 'Group Already Exists')
                    return HttpResponse("Invalid Form")
            #return HttpResponse("Group Already Exists")
            messages.warning(request, 'Group Already Exists')
            return redirect('frontpage:makegroup')
        else:
            form = MakeGroup()
            return render(request, 'frontpage/makegroup.html', {'form':form})
        
    else:
        return redirect('frontpage:welcome')


def profile(request):   
    if request.user.is_authenticated:
        info_sel = 0
        try:
            info_sel = UserInfo.objects.get(User=request.user)
        except UserInfo.DoesNotExist:
            NewUserInfo = UserInfo()
            NewUserInfo.User = request.user
            NewUserInfo.save()
            return render(request, 'frontpage/profile.html')
        
        if request.method == 'POST':
            info_sel = UserInfo.objects.get(User=request.user)
            request.user.first_name = request.POST.get('firstname')
            request.user.last_name = request.POST.get('lastname')
            
            info_sel.DateOfBirth = request.POST.get('dob')
            info_sel.HeightFeet = request.POST.get('heightfeet')
            info_sel.HeightInches = request.POST.get('heightinches')
            info_sel.Weight = request.POST.get('weight')
            info_sel.Gender = request.POST.get('gender')
            try:
                request.user.save()
                info_sel.save()
                messages.success(request,"Info Submitted")
            except:
                messages.warning(request, "Please ensure the form is filled out correctly.")

        return render(request, 'frontpage/profile.html', {'info_sel':info_sel})
    else:
        return redirect('frontpage:welcome')

def ps(request):   
    if request.user.is_authenticated:
        return render(request, 'frontpage/ps.html')
    else:
        return redirect('frontpage:welcome')

def result(request):   
    if request.user.is_authenticated:
        return render(request, 'frontpage/result.html')
    else:
        return redirect('frontpage:welcome')

def settings(request):   
    return render(request, 'frontpage/settings.html')

# I don't believe we'er using this anymore -patrick
# def signup(request):   
#     return render(request, 'frontpage/signup.html')

def status(request):   
    if request.user.is_authenticated:
        return render(request, 'frontpage/status.html')
    else:
        return redirect('frontpage:welcome')

# I don't believe we're using this anymore -patrick
# def upload(request):   
#     return render(request, 'frontpage/upload.html')

def weekreport(request):   
    if request.user.is_authenticated:
        return render(request, 'frontpage/weekreport.html')
    else:
        return redirect('frontpage:welcome')

def searchGroups(request):
    if request.user.is_authenticated:
        try:
            sendRequest = SendGroupJoinRequest()
            groups = Group.objects.all()
            return render(request, 'frontpage/searchGroups.html', {'groups':groups, 'sendRequest':sendRequest})
        except Group.DoesNotExist:
            return render(request, 'frontpage/index.html')
    else:
        return redirect('frontpage:welcome')

def groupView(request, group_id):
    if request.user.is_authenticated:
        group_id = int(group_id)
        try:
            group_sel = Group.objects.get(id = group_id)
        except Group.DoesNotExist:
            return redirect("frontpage:index")

        groupMembers = UserGroupJoinTable.objects.filter(Group = group_sel)
        if group_sel.Owner == request.user:
            groupRequests = UserGroupRequest.objects.filter(Group = group_sel, Status='R')
            if(request.method == "POST"):
                if request.POST.get("User"):
                    djangoUser = get_user_model().objects.get(id=request.POST.get("User"))
                    NewUserGroupJoin = UserGroupJoinTable()
                    NewUserGroupJoin.User = djangoUser
                    NewUserGroupJoin.Group = Group.objects.get(id=group_id)
                    NewUserGroupJoin.DateJoined = datetime.datetime.now()
                    try:
                        NewUserGroupJoin.save()
                        UserGroupRequest.objects.get(User=djangoUser, Group=Group.objects.get(id = group_id)).delete()
                        messages.success(request, "User Added to Group")
                    except:
                        messages.warning(request, "Could not add user to Group")
                if request.POST.get("emails"):
                    emails = str(request.POST.get("emails"))
                    emails = emails.replace(' ', '')
                    emails = emails.split(',')
                    for email in emails:
                        try:
                            djangoUser = get_user_model().objects.get(email=email)
                            if djangoUser != request.user and not UserGroupRequest.objects.filter(Group=group_sel, User=djangoUser).exists():
                                newGroupRequest = UserGroupRequest()
                                newGroupRequest.Group = group_sel
                                newGroupRequest.User = djangoUser
                                newGroupRequest.TimeOfRequest = datetime.datetime.now()
                                newGroupRequest.Status = 'I'
                                newGroupRequest.save()
                        except:
                            pass
                    messages.success(request, "Invitations Sent")
                    return render(request, 'frontpage/groupView.html', {'group':group_sel, 'groupMembers':groupMembers, 'groupRequests':groupRequests, 'emails':emails})
            return render(request, 'frontpage/groupView.html', {'group':group_sel, 'groupMembers':groupMembers, 'groupRequests':groupRequests})
        try:
            groupUser = groupMembers.get(User=request.user)
            return render(request, 'frontpage/groupView.html', {'group':group_sel, 'groupMembers':groupMembers})
        except :
            if(request.method == "POST"):
                if not UserGroupRequest.objects.filter(User=request.user, Group=group_sel).exists():
                    newGroupRequest = UserGroupRequest()
                    newGroupRequest.Group = group_sel
                    newGroupRequest.User = request.user
                    newGroupRequest.TimeOfRequest = datetime.datetime.now()
                    newGroupRequest.Status = 'R'
                    newGroupRequest.save()
                    messages.success(request, "Request Sent")
                    return render(request, 'frontpage/groupView.html', {'group':group_sel})
                else:
                    messages.warning(request, "Request Pending")
            return render(request, 'frontpage/groupView.html', {'group':group_sel})
    else:
        return redirect('frontpage:welcome')


def addUsers(request, group_id):
    if request.user.is_authenticated:
        group_id = int(group_id)
        allUsers = get_user_model().objects.all()
        allUsers = allUsers.exclude(id=request.user.id)
        try:
            group_sel = Group.objects.get(Owner=request.user, id=group_id)
        except Group.DoesNotExist:
            return HttpResponse("OOPS!")
        if request.method == "POST":
            djangoUser = get_user_model().objects.get(id=request.POST.get("User"))
            newGroupRequest = UserGroupRequest()
            newGroupRequest.Group = group_sel
            newGroupRequest.User = djangoUser
            newGroupRequest.TimeOfRequest = datetime.datetime.now()
            newGroupRequest.Status = 'I'
            newGroupRequest.save()
            return HttpResponse("Invite Sent!")
        return render(request, 'frontpage/addUsers.html', {'allUsers':allUsers})
    else:
        return redirect('frontpage:welcome')

def notifications(request):
    if request.user.is_authenticated:
        return render(request, 'frontpage/notification.html')
    else:
        return redirect('frontpage:welcome')

def profileEdit(request):
    if request.user.is_authenticated:
        return render(request, 'frontpage/profileedit.html')
    else:
        return redirect('frontpage:welcome')

def fitbit(request):
    if request.user.is_authenticated:
        if fitapp.utils.is_integrated(request.user):
            FitBitData.StepsTaken = fitapp.views.get_data(request, 'activities', 'steps')
            FitBitData.HeartRate = fitapp.views.get_data(request, 'activities', 'heart')
        else:
            return redirect('frontpage:fitbitLogin')
    else:
        return redirect('frontpage:welcome')

def fitbitCustom(request):
    authURL = 'https://www.fitbit.com/oauth2/authorize?response_type=code&client_id='
    authURL += '238FG4'
    authURL += '&redirect_uri=https://healm-fqgvr.ondigitalocean.app/fitbitCallback&'
    authURL += 'scope=activity+heartrate+profile+sleep+social+weight'
    return redirect(authURL)

def fitbitCallback(request):
    ClientID = "238FG4"
    ClientSecret = "3cc4f6f0e58d4aa98995e3a63f4513c1"
    TokenURL = "https://api.fitbit.com/oauth2/token"
    code = request.GET['code']
    BodyText = {
        'code' : code,
        'redirect_uri' : 'https://healm-fqgvr.ondigitalocean.app/fitbitCallback',
        'client_id' : ClientID,
        'grant_type' : 'authorization_code'
    }
    BodyURLEncoded = urllib.parse.urlencode(BodyText).encode()
    encodedString = ClientID + ":" + ClientSecret
    encodedString = encodedString.encode()
    headers={'Authorization' : 'Basic '.encode() + base64.b64encode(encodedString), 'Content-Type' : 'application/x-www-form-urlencoded'}
    req = urllib.request.Request(TokenURL, BodyURLEncoded, headers )
    response = urllib.request.urlopen(req)
    # req.add_header('Authorization', 'Basic ' + base64.base64encode(ClientID + ":" + ClientSecret))
    # req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    #response = requests.post(TokenURL, data=BodyURLEncoded, headers={'Authorization' : 'Basic ' + base64.base64encode(ClientID + ":" + ClientSecret), 'Content-Type' : 'application/x-www-form-urlencoded'})
    #content = response.content
    test = response
    fullResponse = response.read()
    ResponseJSON = json.loads(fullResponse)
    newFitBitToken = FitBitToken()
    newFitBitToken.User = request.user
    newFitBitToken.AccessToken = str(ResponseJSON['access_token'])
    newFitBitToken.RefreshToken = str(ResponseJSON['refresh_token'])
    newFitBitToken.UserID = str(ResponseJSON['user_id'])
    newFitBitToken.Expiration = int(ResponseJSON['expires_in'])
    newFitBitToken.Scope = str(ResponseJSON['scope'])
    newFitBitToken.Type = str(ResponseJSON['token_type'])
    newFitBitToken.save()

    FitBitProfileURL = "https://api.fitbit.com/1/user/-/profile.json"
    headers={'Authorization' : 'Bearer '.encode() + newFitBitToken.AccessToken.encode()}
    req = urllib.request.Request(FitBitProfileURL, headers)
    response = urllib.request.urlopen(req)
    fullResponse = response.read()
    ResponseJSON = json.loads(fullResponse)
    userInfo_sel = UserInfo.objects.get(user=request.user)
    userInfo_sel.Gender = str(ResponseJSON['user']['displayName'])
    userInfo_sel.save()
    return render(request, 'frontpage/fitbit.html', {'code':code, 'test':test})


# These are custom error views -pat
def custom404(request, exception):
    return render(request, 'errorHandlers/404.html')

def custom500(request):
    return render(request, 'errorHandlers/500.html')

def custom403(request, exception):
    return render(request, 'errorHandlers/403.html')

def custom400(request, exception):
    return render(request, 'errorHandlers/400.html')