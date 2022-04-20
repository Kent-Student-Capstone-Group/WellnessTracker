from email.mime import base
from django.forms import ClearableFileInput
import fitbit
import pandas as pd
import datetime
import gather_keys_oauth2 as Oauth2

CLIENT_ID = "238FG4"
CLIENT_SECRET = "c7a44bea786fec9db0cf0b2cd2e0956d"

### AUTHORIZATION FOR FITBIT
server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()

### RETRIEVES ACCESS TOKEN AND REFRESH TOKEN FOR AUTHORIZATION
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

## AUTHORIZATION CODE USED FROM https://towardsdatascience.com/using-the-fitbit-web-api-with-python-f29f119621ea

### Get today's data
currentDate = datetime.date.today()

### This function gets the total number of steps for a certain date
## That date is currently set to today
currentDayData = auth2_client.time_series(resource='activities/steps', user_id= None, base_date= 'today', period= '1d')
print(currentDayData)

## Pandas dataframe creation

# stepdf = pd.DataFrame(currentDayData['activities-steps'])
# filename = str(datetime.date.today()) + '_steps'
# stepdf.to_csv(filename + '.csv', index = False)

### Get alltime data

#alltimeData = auth2_client.time_series(resource='activities/steps', base_date=)