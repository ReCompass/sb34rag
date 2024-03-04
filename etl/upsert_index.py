from enum import StrEnum

import click
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import CSVLoader, PyPDFLoader
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone  # type: ignore[import-untyped]

from constants import PinceconeIndex

load_dotenv()


class SupportedDocType(StrEnum):
    CSV = ".csv"
    PDF = ".pdf"


def leafly_data_loader(filename: str) -> list[Document]:
    """
    Upsert Cannabis data from Leafly.com to our Pinecone starter index. Data is made on Kaggle under a CC0: Public
    Domain license in CSV and JSON formats. We appreciate the labor that Gustavo Rosa put into collecting this data and
    open sourcing the scrape at https://github.com/gugarosa/leaflyer.

    Kaggle: https://www.kaggle.com/datasets/gthrosa/leafly-cannabis-strains-metadata/data

    TODO: Pre-processing, Transforming, & Splitting
    Right now, we're loading the entire row of data as a doc, this is ripe for improvement! The rows all fit into 2000
    char chunks, so we do not split. I was thinking we could use another chat model to write some comments using the
    effects data, maybe split descriptions and all other data into two resultant docs, maybe even more. There are many
    transforms and metadata opportunity to explore more.
    """
    loader = CSVLoader(filename, source_column="name")  # Making source the strain name rather than doc path.
    documents: list[Document] = loader.load()
    print(f"Loaded {len(documents)} documents from {filename!r}.")
    return documents


def pdf_data_loader(filename: str) -> list[Document]:
    """
    TODO adopt a better chunking strategy
    https://python.langchain.com/docs/modules/data_connection/document_transformers/#evaluate-text-splitters
    ☝️ Elliot, this will be a good jumping off point! Switching to Recursive based on this info from the same doc. 👇
    > Recursively splits text. Splitting text recursively serves the purpose of trying to keep related pieces of text
    > next to each other. This is the recommended way to start splitting text.
    """
    loader = PyPDFLoader(filename)
    documents: list[Document] = loader.load()
    print(f"Loaded {len(documents)} documents from {filename!r}.")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    split_docs = text_splitter.split_documents(documents)
    print(f"Split documents into {len(split_docs)} chunks.")
    return split_docs


@click.command
@click.option("-f", "--filename", type=click.Path(path_type=str, exists=True))
def main(filename: str) -> None:
    if filename.endswith(SupportedDocType.CSV):
        if "leafly_strain_data" not in filename:  # TODO: CSVs will probably all be custom?
            raise ValueError("We only support the Leafly CSV so far. Would love to see a PR to support more CSVs!")

        documents = leafly_data_loader(filename)

    elif filename.endswith(SupportedDocType.PDF):
        documents = pdf_data_loader(filename)

    else:
        raise ValueError(f"{filename!r} is in an unsupported file type.")

    pc_index = Pinecone().Index(name=PinceconeIndex.STARTER)

    vector_store = PineconeVectorStore(index_name=PinceconeIndex.STARTER, embedding=OpenAIEmbeddings())
    print(f"Index before Upsert:\n{pc_index.describe_index_stats()}")

    vector_store.add_texts(str(d) for d in documents)
    print(f"Index after Upsert:\n{pc_index.describe_index_stats()}")


if __name__ == "__main__":
    main()
