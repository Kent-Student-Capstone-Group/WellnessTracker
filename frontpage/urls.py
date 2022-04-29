from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views

import fitapp.views as fitapp
#from fitapp import path, include

app_name= 'frontpage'
urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('index/', views.index, name='index'),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view(), name="logout"),
    path('userInfo_form', views.createUserInfo, name='userInfo'),
    path('badges/', views.badges, name='badges'),
    path('chat/', views.chat, name='chat'), 
    path('contact/', views.contact, name='contact'), 
    path('dailyreport/', views.dailyReport, name='dailyreport'),
    path('group/', views.group, name='group'), 
    path('groupstat/', views.groupstat, name='groupstat'), 
    path('info/', views.info, name='info'), 
    path('makegroup/', views.makeGroup, name='makegroup'),
    path('profile/', views.profile, name='profile'), 
    path('ps/', views.ps, name='ps'), 
    path('result/', views.result, name='result'), 
    path('settings/', views.settings, name='settings'), 
    #path('signup/', views.signup, name='signup'), #don't think we'er using this anymore -pat
    path('status/', views.status, name='status'), 
    #path('upload/', views.upload, name='upload'), #don't think we'er using this anymore -pat
    path('weekreport/', views.weekreport, name='weekreport'), 
    path('welcome/', views.welcome, name='welcome'), 
    path('searchGroups/', views.searchGroups, name='searchGroups'),
    path('groupView/<int:group_id>', views.groupView, name='groupView'),
    path('addUsers/<int:group_id>', views.addUsers, name='addUsers'),
    path('profileEdit/', views.profileEdit, name='profileEdit'),
    path('notifications', views.notifications, name='notifications'),
    path('fitbitConnect', views.fitbit, name='fitbitConnect'),
    path('fitbitlogin', fitapp.login, name='fitbitLogin'),
    path('fitbitComplete', fitapp.complete, name='fitbitComplete'),
]