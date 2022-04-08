from django.forms import ClearableFileInput
import fitbit
import pandas as pd
import datetime

import gather_keys_oauth2 as Oauth2

CLIENT_ID = "238FG4"
CLIENT_SECRET = "c7a44bea786fec9db0cf0b2cd2e0956d"
#ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhGRzQiLCJzdWIiOiI5WEs0U0YiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNjQ5NDU4NzI0LCJpYXQiOjE2NDk0Mjk5MjR9.lbLoV3yppHXwaUfcGTZLcO8D5zWrmpgNQhPnWn_Zny4"
#REFRESH_TOKEN = "9fc6465f6273b1c2d06ffbb05d9fca0dfd01becc9269ccc0a803227fb594c739"

#http://127.0.0.1:8080/?code=da92ee1fa84656caca6a8c1c366935d7621c0b1d&state=N7gIuIZk3LQNtAcvX0oLzT1kKRhs7N#_=_

#client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, REFRESH_TOKEN)

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN=str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN,refresh_token=REFRESH_TOKEN)