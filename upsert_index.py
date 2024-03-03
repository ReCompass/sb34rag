from os import getenv
import argparse


from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from pinecone import Pinecone

def main(fname, separator):
    load_dotenv()

    loader = TextLoader('./data/SB34.txt')
    documents = loader.load()

    # TODO adopt a better chunking strategy
    text_splitter = CharacterTextSplitter(separator="\n\n", chunk_size=100, chunk_overlap=10)
    docs = text_splitter.split_documents(documents)

    strings = [doc.dict()['page_content'] for doc in docs]
    embeddings = OpenAIEmbeddings().embed_documents(strings)

    vectors = [
        {"id": str(idx), "values": embeddings[idx]}
        for idx in range(len(embeddings))
    ]

    pc = Pinecone(api_key=getenv("PINECONE_API_KEY"))
    pc_index = pc.Index(name="starter-index")
    pc_index.upsert(vectors=vectors)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str)
    parser.add_argument('--separator', type=str)
    args = parser.parse_args()

    separator = args.separator if args.separator is not None else '\n\n'
    fname = args.filename
    main(fname, separator)
