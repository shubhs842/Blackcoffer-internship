import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Read the input file
input_file = 'Input.xlsx'
df = pd.read_excel(input_file)

# Function to extract article text
def extract_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract title
    title = soup.find('title').text

    # Extract article text
    paragraphs = soup.find_all('p')
    article_text = ' '.join([p.get_text() for p in paragraphs])

    return title, article_text

# Create a directory to save articles
if not os.path.exists('articles'):
    os.makedirs('articles')

# Extract and save articles
for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    try:
        title, article_text = extract_article(url)
        with open(f'articles/{url_id}.txt', 'w', encoding='utf-8') as file:
            file.write(title + '\n' + article_text)
    except Exception as e:
        print(f"Failed to extract article {url_id}: {e}")
