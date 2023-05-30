import openai
import os
from dotenv import load_dotenv
load_dotenv()

# this will remove the front and back the url to get the domain name.
def remove_www_and_tld(url):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    print(url)
    prompt = f"URL: {url}\nRemove the Hypertext Transfer Protocol and 'www.'if there, and remove the top-level domain (TLD)."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.1,
        messages=[
            {"role": "system", "content": "/start"},
            {"role": "user", "content": prompt}
        ]
    )

    generated_text = response.choices[0].message.content.strip()

    return generated_text


