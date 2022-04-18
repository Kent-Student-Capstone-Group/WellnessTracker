from django.forms import ClearableFileInput
import fitbit
import pandas as pd
import datetime

import gather_keys_oauth2 as Oauth2

CLIENT_ID = "238FG4"
CLIENT_SECRET = "c7a44bea786fec9db0cf0b2cd2e0956d"

#AUTHORIZATION FOR FITBIT
server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()

#RETRIEVES ACCESS TOKEN AND REFRESH TOKEN FOR AUTHORIZATION
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN=str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)
#auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN, expires_at=604800)


#AUTHORIZATION CODE USED FROM https://towardsdatascience.com/using-the-fitbit-web-api-with-python-f29f119621ea

### Help commands

# help(auth2_client.intraday_time_series)
## Intraday time series is what we use to get the data 


### Get today's data
currentDate = datetime.date.today()
currentDayData = auth2_client.intraday_time_series('activities/steps', currentDate, detail_level='1min')

time_list = []
val_list = []

for i in currentDayData["activities-steps-intraday"]["dataset"]:
    val_list.append(i['value'])
    time_list.append(i['time'])

stepdf = pd.DataFrame({'Steps':val_list, 'Time':time_list})


#filename = currentDayData['activities-steps-intraday'][0]['dateTime'] +'_intraday'

#stepdf.to_csv(filename + '.csv', index = False)

### Get alltime data

