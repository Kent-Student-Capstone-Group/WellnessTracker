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

