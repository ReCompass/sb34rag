from os import getenv

from dotenv import load_dotenv
from pinecone import Pinecone, PodSpec

load_dotenv()
pc = Pinecone(api_key=getenv("PINECONE_API_KEY"))

if __name__ == "__main__":
    pc.create_index(name="starter-index", dimension=1536, metric="cosine", spec=PodSpec(environment="gcp-starter"))
