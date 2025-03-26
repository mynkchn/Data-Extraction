import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import requests

def scrape_details(url):
    try :
     driver=webdriver.Chrome()
     driver.get(url)
     time.sleep(5)
     if driver :
       page_source=driver.page_source
       print('Successfully Fetched the Data')
     else :
        print('No data Found')
     driver.quit()

     return page_source
    except Exception as e :
       print(f'Failed to fetch the url due to following issue {e}')

def scrape_bs4(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/121.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}
    try :
       response=requests.get(url)
       response.raise_for_status()
       if response :
          print('Successfully fetched the data')
          return response.text
       else :
          print('No data found')
    except Exception as e :
       print(f'Failed to fetch the url due to folowing issue {e}')

def parse_html(source):
   if source :
      soup=BeautifulSoup(source,'html.parser')
      if soup :
         print('Successfully Stored the html content')
         return soup
      else :
         print('Failed to store html content')
   else :
      print('No source to fetch html found')

# Fetching Data From url
url='https://leetcode.com/problems/two-sum/description/'
source=scrape_details(url)
soup=parse_html(source)


title=soup.find('div',attrs={'class':'text-title-large font-semibold text-text-primary dark:text-text-primary'}).get_text().strip()
diff=soup.find('div',attrs={'class':'flex gap-1'})
difficulty=diff.find('div').text.strip()
data=soup.find('div',attrs={'class':'elfjS'}).get_text().strip()


dict={
   'Title':title[2:].strip(),
   'Difficulty':difficulty,
   'Information':re.sub(r'[^\x00-\x7F]+','',data),

}

with open('Leetcode_Problem', 'a+') as writefiles:
      writefiles.write(f'Title - {dict['Title']}'+'\n')
      writefiles.write(f'Difficulty - {dict['Difficulty']}'+'\n')
      writefiles.write(f'{dict['Information']}')


