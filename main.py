from flask import Flask, request, jsonify
from seleniumscrape import scrape_website
from webmapscrapper import remove_www_and_tld
from markdowns import convert_html_to_text
from summarizer import summarize_text
from langchaindb import process_documents
from pyngrok import ngrok

app = Flask(__name__)

@app.route('/', methods=['POST'])
def process_url():
    # Get the URL from the POST request
    url = request.args.get('url')
    summary = request.args.get('summary', '')  # Get the summary if provided, otherwise use an empty string
    # This will name the chroma database
    db_name = remove_www_and_tld(url)

    # Scrape the website using the entered URL
    file1 = scrape_website(url,db_name)

    # This will convert the HTML scraped into a markdown written in a txt file and return the file path.
    file2 = convert_html_to_text(file1,db_name)

    # This creates a summary of the markdown text that will create a summary from OpenAI
    file3 = summarize_text(file2)

    # Return the summary and path
    with open(file3, 'r') as f:
        summary = f.read()

    # Change this into a webhook post once we get it
    return jsonify({"message": "URL processed and summary generated successfully!", "summary": summary})


@app.route('/change_summary', methods=['POST'])
def change_summary():
    # Get the URL from the POST request they gotta resend this data so I don't have to add global variables
    url = request.form['url']

    # Get the feedback from the POST request
    feedback = request.form['feedback']

    # This will name summary
    db_name = remove_www_and_tld(url)

    # Use the feedback to generate a new summary
    file_path = db_name + '.txt'
    summarize_text(user_feedback=feedback, file_path=file_path)

    # Return the new summary
    with open(file_path, 'r') as file:
        summary = file.read()

    # Change this into a webhook post once we get it
    return jsonify({"message": "Summary changed successfully!", "summary": summary})

@app.route('/campaign_start', methods=['POST'])
def move_to_campaign_start():
    # Get the database name from the POST request
    db_name = request.form['db_name']

    # Move the newly created folder to "Campaign_start"
    new_folder_path = db_name
    process_documents("Campaign_start", db_name)

if __name__ == '__main__':
    # Start ngrok tunnel
    ngrok_url = ngrok.connect(5000).public_url
    print('Ngrok URL:', ngrok_url)
    app.run()
