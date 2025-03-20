import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

url=' https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/netflix_data_webpage.html'


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/122.0.0.0 Safari/537.36'
}

try :
 response=requests.get(url,headers=headers)
 response.raise_for_status()
 soup=BeautifulSoup(response.text,'html.parser')
 print('Link Fetched Successfully')
except Exception as e :
 print(f'Failed to fetch the data from link due to {e}')

netflix_data=pd.DataFrame(columns=['Date','Open','High','Low','Close','Adj Close'])

data=soup.find('tbody')
list=[]
for row in data.find_all('tr') :
   info=row.find_all('td')
   date=info[0].get_text().strip()
   open=info[1].get_text().strip()
   high=info[2].get_text().strip()
   low=info[3].get_text().strip()
   close=info[4].get_text().strip()
   adj_close=info[5].get_text().strip()
   list.append(
     {
       'Date':date,
       'Open':open,
       'High':high,
       'Low':low,
       'Close':close,
       'Adj Close':adj_close
     }
   )

netflix_data=pd.concat([netflix_data,pd.DataFrame(list)])
print(netflix_data.head(2))
print(netflix_data.dtypes)
netflix_data[['Open','Close','High','Low','Adj Close']]=netflix_data[['Open','Close','High','Low','Adj Close']].fillna(0).astype(float)
netflix_data['Date']=netflix_data['Date'].astype(str)
print(netflix_data.dtypes)
netflix_data.to_csv('Netflix_Stock.csv')

