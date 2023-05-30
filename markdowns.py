import html2text
import datetime
from langchaindb import process_documents
import tempfile

def convert_html_to_text(html_file_path):
    # Read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Convert HTML to Markdown
    markdown_content = html2text.html2text(html_content)

    # Create a temporary file with UTF-8 encoding
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as temp_file:
        temp_file.write(markdown_content)
        temp_file_path = temp_file.name

    # Return the path to the temporary file
    return temp_file_path
