from bs4 import BeautifulSoup
import requests
import pandas as pd

URL = 'https://en.wikipedia.org/wiki/Main_Page'

try:
    response = requests.get(URL)
    response.raise_for_status()  # Better error handling
    soup = BeautifulSoup(response.content, 'html.parser')
except requests.exceptions.RequestException as e:
    print(f'Error occurred: {e}')
    exit()

# Extracting data
on_17_march = soup.find(id='mp-otd')
if not on_17_march:
    print("Couldn't find the 'On this day' section.")
    exit()

events = [li.text for li in on_17_march.find_all('li')]

# Writing data to CSV
try:
    df = pd.DataFrame({'On 17 March following Incidents took Place': events})
    df.to_csv('ON_17_MARCH.csv', index=False)
    print('Data successfully written to CSV.')
except Exception as e:
    print(f'Failed to write CSV file because {e}')
