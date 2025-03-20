import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import re
import lxml
import requests
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


location = 'Indore'
experience = 0
query = 'Data+Scientist'
url = f'https://www.foundit.in/srp/results?query={query}&locations={location}&experienceRanges={experience}%7E0&experience={experience}'

def get_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/122.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(f'Link Successfully fetched')
        return response.text
    except Exception as e:
        print(f'Failed to fetch the data from the link due to error {e}')
        return None

def get_selenium_source(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)  # Ensures JavaScript content loads fully
    page_source = driver.page_source
    driver.quit()
    return page_source

def html_code(response):
    try:
        soup = BeautifulSoup(response, 'html.parser')
        if soup:
            print(f'Successfully fetched the website html data')
            return soup
        else:
            print(f'Some error in parameters passed')
            return None
    except Exception as e:
        print(f'Failed to fetch the response due to error {e}')

def scrape_job_data(soup):
    try:
        data = soup.find_all('div', class_='srpResultCardContainer')
        job_list = {}
        
        title = [ item.find('div', attrs={'id': "jobCardTitle"}).text.strip() if item.find('div', attrs={'id': "jobCardTitle"}) else 'N/A' for item in data] 
        company_name=[name.find('div',attrs={'class':'companyName'}).get_text().strip() if name.find('div',attrs={'class':'companyName'}) else 'N/A'  for name in data] 
        job_type=[job.find('div',attrs={'class':'details location'}).get_text().strip() if job.find('div',attrs={'class':'details location'}) else 'N/A' for job in data] 
        exp=[exper.find('span',attrs={'class':'details'}).get_text().strip() if exper.find('span', attrs={'class': 'details'}) else 'N/A' for exper in data] 
        # amount=[]
        # for li in data :
        #     spns=li.find_all('span',attrs={'class':'details'})
        #     if spns :
        #      amount.append(spns[1].get_text().strip())
        #     else :
        #      amount.append('N/A')
        # lim=[spn.find_all('span',attrs={'class':'details'}) for spn in data]
        # amount=[amt[1].get_text().strip() if amt[1].get_text().strip() else 'N/A' for amt in lim ]

        # for item in data :
        #     ActionChains(response).move_to_element(item).click().perform()
        #     time.sleep(2)
        #     info=soup.find('div',attrs={'id':'jdSection'})
        #     package = info.find('div', attrs={'class': 'jobDescriptionNew'})
        #     if package:
        #        description = [p.get_text().strip() for p in package.find_all('p')] or ['N/A']
             

        # # company_name=[item.find('div',attrs={'class':'companyName'})[0].text.strip() for item in data] or 'N\\A'
        # job_type=[item.find('span',attrs={'class':'details'}).text.strip() for item in data] or 'N\\A'
        job_list={
            'Title':title,
            # 'Description':description
            'Company Name':company_name,
            'Job Type':job_type,
            'Experience':exp,
            # 'Package Offered':amount,
        }


       
        return job_list
    except Exception as e:
        print(f'Soup failed to find the HTML source code for extraction due to error {e}')

# Use Selenium for dynamic content
response = get_selenium_source(url)
soup = html_code(response)
info = scrape_job_data(soup)
# print(info)
data=soup.find_all('div',attrs={'id':'jdSection'})
print(len(data))
inn=soup.find('div',attrs={'id':'jdSection'})
package = inn.find('div', attrs={'class': 'jobDescriptionNew'})
if package:
        description = [p.get_text().strip() for p in package.find_all('p')] or ['N/A']
df=pd.DataFrame(info)
df.to_csv('Job_Details.csv')
print(df.head(2))
