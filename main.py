from seleniumscrape import scrape_website
from webmapscrapper import remove_www_and_tld
#
#this is just a program that runs through the process as needed
url = 'https://tryhungry.com/mission/catering-company-washington-dc'
scrape_website(url)
print(remove_www_and_tld(url))
#langchaindb