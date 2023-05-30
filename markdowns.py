import html2text
import datetime
from langchaindb import process_documents
from summarizer import summarize_text
def convert_html_to_text(html_file_path, output_file_path):
    # Read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Convert HTML to Markdown
    markdown_content = html2text.html2text(html_content)

    # Generate the output file name with current date and time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file_name = f"output_{current_time}.txt"
    output_file_path_with_time = output_file_path + output_file_name

    # Save the Markdown content to the file with time
    with open(output_file_path_with_time, 'w', encoding='utf-8') as file:
        file.write(markdown_content)
    summarize_text(output_file_path_with_time)
    