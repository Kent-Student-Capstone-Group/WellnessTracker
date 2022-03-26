from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserInfo, Group
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
        return render(request, 'frontpage/chat.html')
    
    else:
        return HttpResponse("Not Authenticated")

def contact(request):   
    return render(request, 'frontpage/contact.html')

def group(request):  
    return render(request, 'frontpage/group.html')

def groupstat(request):   
    return render(request, 'frontpage/groupstat.html')

def info(request):   
    return render(request, 'frontpage/info.html')

def makeGroup(request):
    #info_sel = UserInfo.objects.get(User= request.user)
    if (request.user.is_authenticated):
        form = MakeGroup(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('frontpage:index')
        context = {
            'form': form
        }
        return render(request, 'frontpage/makegroup.html', context)
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

