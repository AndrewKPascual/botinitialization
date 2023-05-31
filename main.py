from flask import Flask, request
from seleniumscrape import scrape_website
from webmapscrapper import remove_www_and_tld
from markdowns import convert_html_to_text
from summarizer import summarize_text
from langchaindb import process_documents
import os
import shutil

app = Flask(__name__)

@app.route('/', methods=['POST'])
def process_url():
    # Get the URL from the POST request
    url = request.form['url']

    # This will name the chroma database
    db_name = remove_www_and_tld(url)

    # Scrape the website using the entered URL
    temp_file1 = scrape_website(url)

    # This will convert the HTML scraped into a markdown written in a txt file and return the file path.
    temp_file2 = convert_html_to_text(temp_file1)

    # This creates a summary of the markdown text that will create a summary from OpenAI
    # NEED to add a section to create a new summary based on the user input I.E. is this summary long enough, good enough or has all the details.
    temp_file3 = summarize_text(temp_file2)

    # This will add the document to the Database in Chroma
    process_documents(temp_file3, db_name)

    # Move the newly created folder to "Campaign_start"
    new_folder_path = db_name
    destination_path = os.path.join("Campaign_start", db_name)

    # Check if the folder exists before moving it
    if os.path.exists(new_folder_path):
        shutil.move(new_folder_path, destination_path)

    return "URL processed successfully!"

if __name__ == '__main__':
    app.run()
