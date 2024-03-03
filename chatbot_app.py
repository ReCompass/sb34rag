from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain_pinecone import PineconeVectorStore

load_dotenv()
vector_store = PineconeVectorStore(index_name="starter-index", embedding=OpenAIEmbeddings())
llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0)
