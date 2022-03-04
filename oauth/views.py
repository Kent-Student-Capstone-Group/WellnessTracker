from django.shortcuts import render

# Create your views here.

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView

# Custom adapter is created because obsolete URLs are used inside django-allauth library
class GoogleLogin(SocialLoginView):

    class GoogleAdapter(GoogleOAuth2Adapter):
        access_token_url = "https://oauth2.googleapis.com/token"
        authorize_url = "https://accounts.google.com/o/oauth2/v2/auth"
        profile_url = "https://www.googleapis.com/oauth2/v2/userinfo"   

    adapter_class = GoogleAdapter
    callback_url = "https://healm-e5z3j.ondigitalocean.app/oauth/"
    client_class = OAuth2Client