from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserInfo
from .forms import EditUserInfo

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

def chat(request):  # Latti 
    return render(request, 'chat.html')

def contact(request):   
    return render(request, 'contact.html')

def group(request):  
    return render(request, 'group.html')

def groupstat(request):   
    return render(request, 'groupstat.html')

def info(request):   
    return render(request, 'info.html')

def notification(request):   
    return render(request, 'notification.html')

def profile(request):   
    return render(request, 'profile.html')

def ps(request):   
    return render(request, 'ps.html')

def result(request):   
    return render(request, 'result.html')

def settings(request):   
    return render(request, 'settings.html')

def signup(request):   
    return render(request, 'signup.html')

def status(request):   
    return render(request, 'status.html')

def upload(request):   
    return render(request, 'upload.html')

def weekreport(request):   
    return render(request, 'weekreport.html')

def welcome(request):   
    return render(request, 'welcome.html')

