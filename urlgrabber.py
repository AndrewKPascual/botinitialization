import os
import re
from dotenv import load_dotenv
load_dotenv()

# Set up your target string
target_string = 'stack-ai'

def check_url_content(url, target_string):
    return target_string.lower() in url.lower()

def extract_urls(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Using regular expression to find URLs in the content
    url_pattern = re.compile(r'http[s]?://[^)\s]+')
    urls = url_pattern.findall(content)

    # Removing duplicate URLs
    unique_urls = list(set(urls))
    return unique_urls

def save_unique_urls(unique_urls, target_string, file_path):
    with open(file_path, 'w') as file:
        for url in unique_urls:
            if check_url_content(url, target_string):
                file.write(url + '\n')

# Main program
input_file = 'output.txt'
output_file = 'unique_urls.txt'

# Extracting unique URLs
unique_urls = extract_urls(input_file)

# Saving unique URLs to file, filtering by target string
save_unique_urls(unique_urls, target_string, output_file)
