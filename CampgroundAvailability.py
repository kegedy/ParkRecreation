import json
import requests
import pandas as pd
from tabulate import tabulate

campgoundID = 232490
api_key = 'Qpecy5FD5ZDNL7oYns0jH4DvPM5b0K53zSY6e8nR'
headers = {
	#'Host': 'www.recreation.gov',
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate, br',
	'Connection': 'keep-alive',
	'TE': 'Trailers',
	'api_key': api_key
}

# FIND AVAILABLE 
url = f'https://www.recreation.gov/api/camps/availability/campground/{campgoundID}/month?start_date=2020-11-01T00%3A00%3A00.000Z'
#FIND CAMPGROUNDS
#url = f'https://developer.nps.gov/api/v1/campgrounds?api_key={api_key}'
r = requests.get(url=url,headers=headers)
print(url)
print(r.status_code)

# FORMAT RESPONSE
dct = r.json()
df = pd.read_json(json.dumps(dct['campsites'])).T
a = df.iloc[0].availabilities
num = len(a.keys())
dates = pd.DataFrame(a.keys())
dates.columns = ['dates']
df = pd.concat([df]*num,ignore_index=True)
df = df.sort_values('campsite_id')
df = df.reset_index(drop=True)
df = df.reset_index()
df['index'] = df['index'].apply(lambda x: int(x)%num )
df = df.join(dates,on='index')
df['dates'] = None
df['avails'] = None
for name,group in df.groupby('campsite_id'):
	a = group.iloc[0].availabilities
	df.loc[group.index,'dates'] = list(a.keys())
	df.loc[group.index,'avails'] = list(a.values())
df = df.sort_values(['campsite_id','dates'])
df = df.drop('availabilities',axis=1)

# OUTPUT
with open('test.csv', 'w+') as f0:
	f0.write(df.to_csv(index=False))
print(df.head(n=50))
