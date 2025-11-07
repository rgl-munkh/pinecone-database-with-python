import os
import time
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("PINECONE_API_KEY")


pc = Pinecone(api_key=api_key)

index_name = "quickstart-py"

if not pc.has_index(index_name):
    print(f"Index '{index_name}' does not exist. Creating it...")
    pc.create_index_for_model(
        name=index_name,
        cloud="aws",
        region="us-east-1",
        embed={
            "model": "llama-text-embed-v2",
            "field_map": {"text": "chunk_text"}
        }
    )
    print("Index created. Waiting for it to be ready...")
    time.sleep(5)

index = pc.Index(index_name)

# upsert records
records = [
    {
        "_id": "A",
        "chunk_text": "A hilarious comedy movie released in 2020",
        "genre": "comedy",
        "year": 2020
    },
    {
        "_id": "B",
        "chunk_text": "An informative documentary from 2019",
        "genre": "documentary",
        "year": 2019
    },
    {
        "_id": "C",
        "chunk_text": "A funny comedy film from 2019",
        "genre": "comedy",
        "year": 2019
    },
    {
        "_id": "D",
        "chunk_text": "A dramatic and emotional story",
        "genre": "drama"
    }
]

index.upsert_records("example-namespace", records)

print("Successfully upserted records to namespace 'example-namespace'")

# query by keyword

index = pc.Index(index_name)

filtered_results = index.search(
    namespace="example-namespace",
    query={
        "inputs": {"text": "funny"},
        "top_k": 3,
        "filter": {"genre": "comedy"}
    },
    fields=["chunk_text"]
)

print("Filtered results:", filtered_results)