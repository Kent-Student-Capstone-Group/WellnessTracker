from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserGroupJoinTable, UserInfo, Group, Message
from .forms import EditUserInfo, MakeGroup

# Create your views here.


def index(request):
    if(request.user.is_authenticated):
        try:
            info = UserInfo.objects.get(User=request.user)
            return render(request, 'frontpage/index.html', {'info':info})
        except UserInfo.DoesNotExist:
            return render(request, 'frontpage/index.html')
    else:
        return render(request, 'frontpage/index.html')

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
        userMessages = Message.objects.all()
        return render(request, 'frontpage/chat.html', {'Messages': userMessages})
    
    else:
        return HttpResponse("Not Authenticated")

def contact(request):   
    return render(request, 'frontpage/contact.html')

def dailyReport(request):
    return render(request, 'frontpage/dailyreport.html')

def group(request):  
    user = request.user
    context = {
        'userGroups': UserGroupJoinTable.objects.filter(User = user),
        'ownerGroups': Group.objects.filter(Owner = request.user),
    }
    return render(request, 'frontpage/group.html', context)

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
                form.Owner = request.user
                if form.is_valid():
                    form.save()
                    return redirect('frontpage:index')
                else:
                    return HttpResponse("Invalid Form")
            return HttpResponse("Group Already Exists")
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

def welcome(request):   
    return render(request, 'frontpage/welcome.html')

