import os
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader

load_dotenv()

persist_directory = 'dbs'
embedding = OpenAIEmbeddings()
# Now we can load the persisted database from disk, and use it as normal. 
vectordb = Chroma(persist_directory=persist_directory, 
                  embedding_function=embedding)

retriever = vectordb.as_retriever()

docs = retriever.get_relevant_documents("output.txtoutput_2023-05-28_14-31-41.txt")
len(docs)
retriever = vectordb.as_retriever(search_kwargs={"k": 2})
retriever.search_type
retriever.search_kwargs
# create the chain to answer questions 
qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(), 
                                  chain_type="stuff", 
                                  retriever=retriever, 
                                  return_source_documents=True)
## Cite sources
def process_llm_response(llm_response):
    print(llm_response['result'])


# Rest of your code...

        # full example
query = "What is tryhungry?"
llm_response = qa_chain(query)
process_llm_response(llm_response)