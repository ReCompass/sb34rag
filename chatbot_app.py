from os import getenv

from dotenv import load_dotenv
from langchain import OpenAI
# from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from pinecone import Pinecone, PodSpec

load_dotenv()

# load the documents and split them.
# This can be substituted with any data type loader according to your requirement.
loader = TextLoader('./savings-accounts.txt')
documents = loader.load()

# We proceed by segmenting the documents and generating their embeddings.
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder("gpt2", chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
print(len(docs))
embeddings = OpenAIEmbeddings().embed_documents(docs)

# initialize pinecone
# get the api key and environment from the .env file
pc = Pinecone(api_key=getenv("PINECONE_API_KEY"))
pc_index = pc.Index(name="starter-index")
# pc_index.upsert(items=[{"id": doc, "vector": embed} for doc, embed in zip(docs, embeddings)])

if __name__ == "__main__":
    print(embeddings)
