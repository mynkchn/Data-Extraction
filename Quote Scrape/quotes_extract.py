import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice

url = 'http://quotes.toscrape.com'
link = '/page/1'

allquotes = []

while link:
    try:
        response = requests.get(f'{url}{link}')
        response.raise_for_status()  # Raises an exception for 4xx or 5xx errors
        soup = BeautifulSoup(response.text, 'html.parser')

    except requests.RequestException as e:
        print(f'Error {e} occurred while fetching quotes.')
        break

    quotes = soup.find_all(class_='quote')
    for quote in quotes:
        try:
            allquotes.append(
                {
                    'text': quote.find(class_='text').get_text(),
                    'author': quote.find(class_='author').get_text(),
                    'bio-link': quote.find('a')['href']
                }
            )
        except AttributeError:
            print("Error parsing a quote — skipping it.")
            continue

    next_btn = soup.find(class_='next')
    link = next_btn.find('a')['href'] if next_btn else None
    sleep(2)

# Write to file
try:
    with open('quotes.txt', 'a+') as writefile:
        writefile.write(' Quote | Author | Link ' + '\n')
        for quote in allquotes:
            writefile.write(f"{quote['text']} | {quote['author']} | {quote['bio-link']}\n")
except Exception as e:
    print(f'Failed to save quotes to file due to {e}')

# Quote guessing game logic
quote = choice(allquotes)
remaining_choices = 4
print("Here's a quote:")
print(quote['text'])

guess = ''

while guess.lower() != quote['author'].lower() and remaining_choices > 0:
    guess = input(f'Who said this quote? Guesses remaining {remaining_choices}: ')
    if guess.strip().lower() == quote['author'].strip().lower():
        print('🎯 Congratulations! You got it right.')
        break

    remaining_choices -= 1
    if remaining_choices == 1:
        try:
            res = requests.get(f"{url}{quote['bio-link']}")
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            birth_date = soup.find(class_='author-born-date').get_text()
            birth_place = soup.find(class_='author-born-location').get_text()
            print(f'Hint: The author was born on {birth_date} {birth_place}.')
        except Exception:
            print("Could not fetch author details.")
    elif remaining_choices == 2:
        print(f"Hint: The author's first name starts with {quote['author'][0]}")
    elif remaining_choices == 3:
        author_parts = quote['author'].split()
        if len(author_parts) > 1:
            last_initial = author_parts[1][0]
            print(f"Hint: The author's last name starts with {last_initial}")
        else:
            print("Hint: The author has only one name.")
    else:
        print(f'Sorry, you ran out of guesses. The correct answer is {quote["author"]}.')
