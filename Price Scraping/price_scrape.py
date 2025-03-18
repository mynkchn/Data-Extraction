import re
import pandas as pd
from bs4 import BeautifulSoup
import lxml
import requests
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/122.0.0.0 Safari/537.36'
}

with open('D:\\Data Extraction\\urls.csv', 'r+') as readfile:
    urls = readfile.readlines()

def scrape_details(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f'Failed to connect to the link due to given error: {e}')
        return None

    title = soup.find('span', attrs={'id': 'productTitle'})
    product_title = title.text.strip() if title else 'N\\A'

    price = soup.find('span', attrs={'class': 'a-price-whole'})
    product_price = price.text.strip().replace('.', ' ') if price else 'N\\A'

    ratings = soup.find('span', attrs={'id': "acrCustomerReviewText"})
    product_ratings = ratings.text.strip() if ratings else 'N\\A'

    star_rates = soup.find('span', attrs={'class': 'a-icon-alt'})
    overall_ratings = star_rates.text.strip() if star_rates else 'N\\A'

    availability = soup.find('span', class_='a-size-medium a-color-success')
    product_availability = availability.text.strip() if availability else 'N\\A'

    product_details = {
        'Product Title': product_title,
        'Product Price': product_price,
        'Overall Rating': overall_ratings,
        'Total Reviews': product_ratings,
        'Availibilty': product_availability,
    }
    return product_details

# Column headers
columns = ['Product Title', 'Product Price', 'Overall Rating', 'Total Reviews', 'Availibilty']

with open('products.csv', 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    file.seek(0)  # Move pointer to the start
    writer.writerow(columns)  # Write headers only once

    for url in urls:
        details = scrape_details(url.strip(), headers)
        if details:
            product_details = [
                details['Product Title'],
                details['Product Price'],
                details['Overall Rating'],
                details['Total Reviews'],
                details['Availibilty']
            ]
            writer.writerow(product_details)  # Append data
        else:
            print(f'Failed to write details for URL: {url.strip()}')
