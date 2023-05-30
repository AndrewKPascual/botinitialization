from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import chromedriver_autoinstaller
import tempfile

chromedriver_autoinstaller.install()

def scrape_website(url):
    # Set up the Selenium Chrome driver
     
    options = Options()
    options.add_argument('--headless')  # Run Chrome in headless mode, no GUI
    driver = webdriver.Chrome(options=options)

    # Load the website
    driver.get(url)  # Replace with the URL of the website you want to scrape

    # Wait for the dynamic content to load (you may need to adjust the wait time)
    time.sleep(10)  # Adjust the delay as needed (in seconds)

    # Get the page source (HTML code) after the dynamic content has loaded
    page_source = driver.page_source

    # Create a temporary file with UTF-8 encoding
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(page_source)
        temp_file_path = temp_file.name
    
    # Close the driver
    driver.quit()
    return temp_file_path
