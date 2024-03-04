import click
from dotenv import load_dotenv
from pinecone import Pinecone, PodSpec

from constants import PinceconeIndex

load_dotenv()
pc = Pinecone()


@click.command
@click.option("-D", "--delete-all", is_flag=True)
def main(delete_all: bool) -> None:
    if delete_all:
        idx = pc.Index(PinceconeIndex.STARTER)
        if click.confirm(f"Remove all records from {PinceconeIndex.STARTER}?\n\n{idx.describe_index_stats()}\n\n"):
            idx.delete(delete_all=True)
    else:  # Was only used the once, maybe we take in an Index option later?
        pc.create_index(
            name=PinceconeIndex.STARTER,
            dimension=1536,
            metric="cosine",
            spec=PodSpec(environment="gcp-starter"),
        )


if __name__ == "__main__":
    main()
