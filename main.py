from flask import Flask, request, jsonify
from seleniumscrape import scrape_website
from webmapscrapper import remove_www_and_tld
from markdowns import convert_html_to_text
from summarizer import summarize_text
from langchaindb import process_documents
import os
import shutil

app = Flask(__name__)

# Declare temp_file2 and summary as global variables
temp_file2 = None
summary = None

@app.route('/', methods=['POST'])
def process_url():
    global temp_file2, summary  # declare that we're using the global temp_file2 and summary variables

    # Get the URL from the POST request
    url = request.form['url']

    # This will name the chroma database
    db_name = remove_www_and_tld(url)

    # Scrape the website using the entered URL
    temp_file1 = scrape_website(url)

    # This will convert the HTML scraped into a markdown written in a txt file and return the file path.
    temp_file2 = convert_html_to_text(temp_file1)

    # This creates a summary of the markdown text that will create a summary from OpenAI
    temp_file3 = summarize_text(temp_file2)

    # Return the summary and path
    with open(temp_file3, 'r') as f:
        summary = f.read()

    # Change this into a webhook post once we get it
    return jsonify({"message": "URL processed and summary generated successfully!", "summary": summary})

@app.route('/change_summary', methods=['POST'])
def change_summary():
    global temp_file2, summary  # declare that we're using the global temp_file2 and summary variables

    # Get the feedback from the POST request
    feedback = request.form['feedback']

    # Use the feedback to generate a new summary
    temp_file3 = summarize_text(temp_file2, user_feedback=feedback)

    # Return the new summary
    with open(temp_file3, 'r') as f:
        summary = f.read()

    # Change this into a webhook post once we get it
    return jsonify({"message": "Summary changed successfully!", "summary": summary})

@app.route('/campaign_start', methods=['POST'])
def move_to_campaign_start():
    # Get the database name from the POST request
    db_name = request.form['db_name']

    # Move the newly created folder to "Campaign_start"
    new_folder_path = db_name
    destination_path = os.path.join("Campaign_start", db_name)

    # Check if the folder exists before moving it
    if os.path.exists(new_folder_path):
        shutil.move(new_folder_path, destination_path)
        return "Folder moved successfully!"
    else:
        return "Folder does not exist!", 400

if __name__ == '__main__':
    app.run()
