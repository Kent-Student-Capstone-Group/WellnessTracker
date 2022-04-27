"""healm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path 

#from fitapp import include, path

#from frontpage import fitbit, views
from frontpage import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', include('frontpage.urls')),
    path('accounts/', include('allauth.urls')),
    #path('fitbit/', include('fitapp.urls')),
]

handler404 = 'frontpage.views.custom404'
handler500 = 'frontpage.views.custom500'
handler403 = 'frontpage.views.custom403'
handler400 = 'frontpage.views.custom400'