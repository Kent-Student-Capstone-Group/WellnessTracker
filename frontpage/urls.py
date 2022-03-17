from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views

app_name= 'frontpage'
urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view(), name="logout"),
    path('userInfo_form', views.createUserInfo, name='userInfo'),
    path('chat/', views.chat), #Latti
    path('contact/', views.contact), 
    path('group/', views.group), 
    path('groupstat/', views.groupstat), 
    path('info/', views.info), 
    path('profile/', views.profile), 
    path('ps/', views.ps), 
    path('result/', views.result), 
    path('settings/', views.settings), 
    path('signup/', views.signup), 
    path('status/', views.status), 
    path('upload/', views.upload), 
    path('weekreport/', views.weekreport), 
    path('welcome/', views.welcome), 
]