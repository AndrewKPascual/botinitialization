import html2text

def convert_html_to_text(html_content, file_path):
    # Convert HTML to Markdown
    markdown_content = html2text.html2text(html_content)

    # Save the Markdown content to the specified file path
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(markdown_content)

    # Return the Markdown content as a value
    return markdown_content
