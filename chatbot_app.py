from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.llms import OpenAI
from langchain_pinecone import PineconeVectorStore


load_dotenv()
vector_store = PineconeVectorStore(index_name="starter-index", embedding=OpenAIEmbeddings())
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
