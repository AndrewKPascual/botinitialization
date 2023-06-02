import requests
from bs4 import BeautifulSoup

def scrape_website(url, file_path):
    # Make a request to the website
    r = requests.get(url)

    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(r.content, 'html.parser')

    # Get the page source (HTML code)
    page_source = str(soup.prettify())

    # Save the page source to the specified file path
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(page_source)

    return page_source
