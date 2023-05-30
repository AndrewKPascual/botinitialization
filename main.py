from seleniumscrape import scrape_website
from webmapscrapper import remove_www_and_tld
from markdowns import convert_html_to_text
from summarizer import summarize_text
from langchaindb import process_documents
# Prompt the user to enter the URL
url = 'https://www.stack-ai.com/'

# Scrape the website using the entered URL
temp_file1=scrape_website(url)

#this will convert the html scraped into a markdown written in a txt file and return the file path.
temp_file2 = convert_html_to_text(temp_file1)

#This creates a summary of the markdown text that will create a summary from openai
temp_file3 = summarize_text(temp_file2)

#This will add the document to the Database in chroma
process_documents(temp_file3)

# Print the modified URL after removing www and top-level domain
# un-used due to the level of scraping required and errors that occured. Will come back to this later
#print(remove_www_and_tld(url)) 

