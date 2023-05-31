import requests
from bs4 import BeautifulSoup
import tempfile

def scrape_website(url):
    # Make a request to the website
    r = requests.get(url)

    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(r.content, 'html.parser')

    # Get the page source (HTML code)
    page_source = str(soup.prettify())

    # Create a temporary file with UTF-8 encoding
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(page_source)
        temp_file_path = temp_file.name

    return temp_file_path
