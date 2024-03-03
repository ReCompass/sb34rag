from os import getenv

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from pinecone import Pinecone

load_dotenv()

# load the documents and split them.
# This can be substituted with any data type loader according to your requirement.
loader = TextLoader('./savings-accounts.txt')
documents = loader.load()

# We proceed by segmenting the documents and generating their embeddings.
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings().embed_documents(docs)

# initialize pinecone
# get the api key and environment from the .env file
# pc = Pinecone(api_key=getenv("PINECONE_API_KEY"))
# pc_index = pc.Index(name="starter-index")
# pc_index.upsert(items=[{"id": doc, "vector": embed} for doc, embed in zip(docs, embeddings)])

if __name__ == "__main__":
    print(embeddings)