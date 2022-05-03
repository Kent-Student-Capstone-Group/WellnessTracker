import datetime
import json
import urllib
import base64
from .models import FitBitToken

def createToken(user, code):
    expTime = datetime.datetime.now()
    ClientID = "238FG4"
    ClientSecret = "3cc4f6f0e58d4aa98995e3a63f4513c1"
    TokenURL = "https://api.fitbit.com/oauth2/token"
    code = code
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
    fullResponse = response.read()
    ResponseJSON = json.loads(fullResponse)

    
    try:
        newFitBitToken = FitBitToken.objects.get(User=request.user)
    except FitBitToken.DoesNotExist:
        newFitBitToken = FitBitToken()

    newFitBitToken.User = user
    newFitBitToken.AccessToken = str(ResponseJSON['access_token'])
    newFitBitToken.RefreshToken = str(ResponseJSON['refresh_token'])
    newFitBitToken.UserID = str(ResponseJSON['user_id'])
    expTime = expTime + datetime.timedelta(seconds=int(ResponseJSON['expires_in']))
    newFitBitToken.Expiration = expTime
    newFitBitToken.Scope = str(ResponseJSON['scope'])
    newFitBitToken.Type = str(ResponseJSON['token_type'])
    newFitBitToken.save()



def refreshToken(user):
    userToken = FitBitToken.objects.get(User=user)
    expTime = datetime.datetime.now()
    ClientID = "238FG4"
    ClientSecret = "3cc4f6f0e58d4aa98995e3a63f4513c1"
    TokenURL = "https://api.fitbit.com/oauth2/token"

    BodyText = {
        'grant_type' : 'refresh_token',
        'refresh_token' : userToken.RefreshToken
    }

    BodyURLEncoded = urllib.parse.urlencode(BodyText).encode()
    encodedString = ClientID + ":" + ClientSecret
    encodedString = encodedString.encode()
    headers={'Authorization' : 'Basic '.encode() + base64.b64encode(encodedString), 'Content-Type' : 'application/x-www-form-urlencoded'}
    req = urllib.request.Request(TokenURL, BodyURLEncoded, headers)
    response = urllib.request.urlopen(req)
    fullResponse = response.read()
    ResponseJSON = json.loads(fullResponse)
    
    userToken.AccessToken = str(ResponseJSON['access_token'])
    userToken.RefreshToken = str(ResponseJSON['refresh_token'])
    expTime = expTime + datetime.timedelta(seconds=int(ResponseJSON['expires_in']))
    userToken.Expiration = expTime
    userToken.Scope = str(ResponseJSON['scope'])
    userToken.Type = str(ResponseJSON['token_type'])
    userToken.save()



def fitbitRequest(user, url):

    userToken = FitBitToken.objects.get(User=user)
    if datetime.datetime.now() > userToken.Expiration:
        refreshToken(user)

    url = "https://api.fitbit.com" + url
    
    headers={'Authorization'.encode() : 'Bearer '.encode() + userToken.AccessToken.encode()}
    req = urllib.request.Request(url=url, data=None, headers=headers)
    response = urllib.request.urlopen(req)
    fullResponse = response.read()
    ResponseJSON = json.loads(fullResponse)

    return ResponseJSON