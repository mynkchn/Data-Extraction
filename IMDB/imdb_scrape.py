import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml

# URL of IMDb Top 250 Movies
url = "https://m.imdb.com/chart/top/"
base_url = "https://m.imdb.com/"

# Headers to mimic a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/122.0.0.0 Safari/537.36'
}

# Send a GET request with headers
response = requests.get(url, headers=headers)
response.raise_for_status()

# Parse the content
soup = BeautifulSoup(response.text, 'html.parser')
movies = soup.select('li.ipc-metadata-list-summary-item')

# Extracting movie details
list = []
for movie in movies:
    name = movie.find(class_='ipc-title__text').get_text().strip()
    details = movie.find_all(class_='sc-f30335b4-7 jhjEEd cli-title-metadata-item')
    year = details[0].text
    time = details[1].text
    a_tags = movie.find_all('a')
    link = a_tags[0]['href']
    ratings = movie.find(class_='ipc-rating-star--rating').get_text()
    list.append(
        {'Movie': name[2:],
         'Year': year,
         'Duration': time,
         'Ratings': ratings,
         'link': link}
    )

# Saving initial data to CSV
df = pd.DataFrame(list)
print(df.head(2))
df.to_csv('Top_Movies.csv')

# Extracting more details (Creators)
more_details = []
for link in list:
    try:
        responses = requests.get(f'{base_url}{link["link"]}', headers=headers)
        responses.raise_for_status()
        soups = BeautifulSoup(responses.text, 'html.parser')
    except Exception as e:
        print(f'Unable to fetch link due to the given error {e}')
        continue

    # Extract movie type (genre)
    movie_type = soups.find(class_='ipc-chip-list--baseAlt')
    types = [typ.text.strip() for typ in movie_type.find_all('span')] if movie_type else 'N/A'

    # Extract creators (Director, Writer, etc.)
    creators_section = soups.find_all('li', class_='ipc-metadata-list__item')
    directors, writers, stars = 'N/A', 'N/A', 'N/A'

   
   
   
    for item in creators_section:
        heading_tag = item.find('span', class_='ipc-metadata-list-item__label')
        if not heading_tag:
            continue  # Skip entries where the heading tag is missing

        heading = heading_tag.get_text().strip()

        if 'Director' in heading:
            directors = ', '.join([a.text.strip() for a in item.find_all('a')]) or 'N/A'
        elif 'Writer' in heading:
            writers = ', '.join([a.text.strip() for a in item.find_all('a')]) or 'N/A'
        elif 'Stars' in heading:
            stars = ', '.join([a.text.strip() for a in item.find_all('a')]) or 'N/A'
    # Append details
    more_details.append(
        {
            'Type': types,
            'Director': directors,
            'Writer': writers,
            'Stars': stars
        }
    )

# Saving detailed data to CSV
dff = pd.DataFrame(more_details)
print(dff.head(2))
dff.to_csv('Top_Movies_Details.csv')
