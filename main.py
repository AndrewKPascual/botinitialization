from seleniumscrape import scrape_website
from webmapscrapper import remove_www_and_tld

# Prompt the user to enter the URL
url = input("Enter the URL: ")

# Scrape the website using the entered URL
scrape_website(url)

# Print the modified URL after removing www and top-level domain
print(remove_www_and_tld(url))
