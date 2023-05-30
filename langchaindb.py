import os
import unicodedata
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

def process_documents(filepath):
    load_dotenv()

    # Embed and store the texts
    # Supplying a persist_directory will store the embeddings on disk
    persist_directory = 'db'

    ## here we are using OpenAI embeddings but in the future, we will swap out to local embeddings
    embedding = OpenAIEmbeddings()

    # Define a custom Document class
    class MyDocument:
        def __init__(self, page_content, metadata):
            self.page_content = page_content
            self.metadata = metadata

    # Load the text files
    with open(filepath, 'r', encoding='utf-8') as file:
        file_contents1 = file.read()
        file_contents1 = ''.join(c for c in file_contents1 if unicodedata.category(c)[0] != 'C')  # Remove non-UTF-8 characters


    # Create document objects
    document1 = MyDocument(page_content=file_contents1, metadata={'id': 1})

    # Create the Chroma vector store from the document objects
    vectordb = Chroma.from_documents(documents=[document1],
                                     embedding=embedding,
                                     persist_directory=persist_directory)

    # Persist the db to disk
    vectordb.persist()

    # Clear the reference to the vector store
    vectordb = None

    # Load the persisted database from disk
    vectordb = Chroma(persist_directory=persist_directory,
                      embedding_function=embedding)
