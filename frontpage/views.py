from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
import datetime
from django.contrib.auth import get_user_model
from .models import DailyReport, UserInfo, UserGroupJoinTable, UserInfo, Group, Chat, UserGroupRequest
from .forms import EditUserInfo, MakeGroup, DailyReportForm, SendChat, SendGroupJoinRequest
from django.contrib import messages
import time

# Create your views here.


def welcome(request):
    if(request.user.is_authenticated):
        return render(request, 'frontpage/index.html')
        # try:
        #     info = UserInfo.objects.get(User=request.user)
        #     return render(request, 'frontpage/index.html', {'info':info})
        # except UserInfo.DoesNotExist:
        #     return render(request, 'frontpage/index.html')
    else:
        return redirect('/accounts/google/login')

def index(request):
    if(request.user.is_authenticated):
        return render(request, 'frontpage/index.html')
    else:
        return redirect('/accounts/google/login')

def badges(request):
    if (request.user.is_authenticated):
        return render(request, 'frontpage/badges.html')
    
    else:
        return HttpResponse("Not Authenticated")

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
            return redirect('frontpage:index')
        return render(request, 'frontpage/userInfo_form.html', {'upload_form':form})
    else:
        return HttpResponse("Not Authenticated")

def chat(request):   
    if (request.user.is_authenticated):
        chats = Chat.objects.filter(Recipient=request.user)
        form = SendChat(request.POST or None)
        if form.is_valid():
            newChat = Chat(Sender = request.user, MessageTitle = request.POST.get("MessageTitle"), MessageBody = request.POST.get("MessageBody"))
            newChat.Recipient = get_user_model().objects.get(id=request.POST.get("Recipient"))
            newChat.save()
            return render(request, 'frontpage/index.html')
        return render(request, 'frontpage/chat.html', {'chats': chats, 'form': form})
    
    else:
        return HttpResponse("Not Authenticated")

def contact(request):   
    return render(request, 'frontpage/contact.html')

def dailyReport(request):
    if (request.user.is_authenticated):
        form = DailyReportForm(request.POST or None)
        TodayReports = DailyReport.objects.filter(DateAndTime=datetime.date.today())
        alreadySubmittedToday = len(TodayReports) > 0
        
        # form.User = request.user
        if form.is_valid():
            newDailyReport = DailyReport()
            newDailyReport.User = request.user
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
            newDailyReport.save()
            try:
                userInfo = UserInfo.objects.get(User = request.user)
                userInfo.UserSteps = userInfo.UserSteps + int(newDailyReport.StepsTaken)
                userInfo.save()
            except:
                print("No user info")
            
            return redirect('frontpage:index')
        return render(request, 'frontpage/dailyreport.html', {'form': form, 'alreadySubmittedToday': alreadySubmittedToday})
    else:
        return HttpResponse("Not Authenticated")
    

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
                NewUserGroupJoin.save()
                UserGroupRequest.objects.get(User=request.user, Group=Group.objects.get(id = request.POST.get("Group"))).delete()
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
        return redirect('/accounts/google/login')

def groupstat(request):   
    return render(request, 'frontpage/groupstat.html')

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
                    NewGroup.save()
                    NewUserGroupJoin = UserGroupJoinTable()
                    NewUserGroupJoin.Group = NewGroup
                    NewUserGroupJoin.User = request.user
                    NewUserGroupJoin.save()
                    messages.success(request, 'Group Succesfully Created')
                    return redirect('frontpage:makegroup')
                    
                else:
                    #messages.warning(request, 'Group Already Exists')
                    return HttpResponse("Invalid Form")
            #return HttpResponse("Group Already Exists")
            messages.warning(request, 'Group Already Exists')
            return redirect('frontpage:makegroup')
            # groupAlreadyExists = False
            # for e in userCurrentOwnedGroups:
            #     if e.GroupName == form.GroupName:
            #         groupAlreadyExists = True

            # if groupAlreadyExists:
            #     if form.is_valid():
            #         form.save()
            #         return redirect('frontpage:index')
            #     context = {
            #         'form': form
            #     }
            #     return render(request, 'frontpage/makegroup.html', context)
        else:
            form = MakeGroup()
            return render(request, 'frontpage/makegroup.html', {'form':form})
        
    else:
        return HttpResponse("Not Authenticated")

def notification(request):   
    return render(request, 'frontpage/notification.html')

def profile(request):   
    return render(request, 'frontpage/profile.html')

def ps(request):   
    return render(request, 'frontpage/ps.html')

def result(request):   
    return render(request, 'frontpage/result.html')

def settings(request):   
    return render(request, 'frontpage/settings.html')

def signup(request):   
    return render(request, 'frontpage/signup.html')

def status(request):   
    return render(request, 'frontpage/status.html')

def upload(request):   
    return render(request, 'frontpage/upload.html')

def weekreport(request):   
    return render(request, 'frontpage/weekreport.html')

def searchGroups(request):
        try:
            sendRequest = SendGroupJoinRequest()
            groups = Group.objects.all()
            return render(request, 'frontpage/searchGroups.html', {'groups':groups, 'sendRequest':sendRequest})
        except Group.DoesNotExist:
            return render(request, 'frontpage/index.html')

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
                    NewUserGroupJoin.save()
                    UserGroupRequest.objects.get(User=djangoUser, Group=Group.objects.get(id = group_id)).delete()
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

                    return render(request, 'frontpage/groupView.html', {'group':group_sel, 'groupMembers':groupMembers, 'groupRequests':groupRequests, 'emails':emails})
            return render(request, 'frontpage/groupView.html', {'group':group_sel, 'groupMembers':groupMembers, 'groupRequests':groupRequests})
        try:
            groupUser = groupMembers.get(User=request.user)
            return render(request, 'frontpage/groupView.html', {'group':group_sel, 'groupMembers':groupMembers})
        except :
            if(request.method == "POST"):
                newGroupRequest = UserGroupRequest()
                newGroupRequest.Group = group_sel
                newGroupRequest.User = request.user
                newGroupRequest.TimeOfRequest = datetime.datetime.now()
                newGroupRequest.Status = 'R'
                newGroupRequest.save()
                return HttpResponse("Request Sent!")
            return render(request, 'frontpage/groupView.html', {'group':group_sel})
    else:
        return redirect('frontpage:index')


def addUsers(request, group_id):
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

def notifications(request):
    return render(request, 'frontpage/notification.html')

def profileEdit(request):
    return render(request, 'frontpage/profileedit.html')

def custom404(request, exception):
    return render(request, 'errorHandlers/404.html')

def custom500(request):
    return render(request, 'errorHandlers/500.html')

def custom403(request, exception):
    return render(request, 'errorHandlers/403.html')

def custom400(request, exception):
    return render(request, 'errorHandlers/400.html')