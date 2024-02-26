from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain import OpenAI
from pinecone import Pinecone
import os

# Set up OpenAI and Pinecone
os.environ["OPENAI_API_KEY"] = "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"
os.environ["PINECONE_API_KEY"] = "db879104-835a-44c9-9499-fbe6611541b9"

# Load documents
directory = 'data'
def load_docs(directory):
    loader = DirectoryLoader(directory)
    documents = loader.load()
    return documents

documents = load_docs(directory)

# Split documents
def split_docs(documents, chunk_size=1000, chunk_overlap=20):
    text_spliter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_spliter.split_documents(documents)
    return docs

docs = split_docs(documents)

# Set up embeddings
embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])

# Set up Pinecone
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"], environment="gcp-starter")
index_name = "synexty"
from langchain.vectorstores import Pinecone
index = Pinecone.from_documents(docs, embeddings, index_name=index_name)

# Get similar documents
def get_similiar_docs(query, k=2, score=False):
    if score:
        similar_docs = index.similarity_search_with_score(query, k=k)
    else:
        similar_docs = index.similarity_search(query, k=k)
    return similar_docs

# Load question-answering model
llm = OpenAI(openai_api_key=os.environ["OPENAI_API_KEY"])
chain = load_qa_chain(llm, chain_type="stuff")

# Get answer
def get_answer(query):
    similar_docs = get_similiar_docs(query)
    answer = chain.run(input_documents=similar_docs, question=query)
    return answer

# llm_differentiation function
def llm_differentiation(text):
    query = f"Identify the category of this medical document. Provide the response in the format 'category: [CategoryName]'. Please avoid explanatory formats such as 'category: the category is CategoryName'. The document content is: {text}"
    answer = get_answer(query)
    return answer