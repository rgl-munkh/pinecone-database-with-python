# Pinecone Database Learning Project

A Python project for learning and experimenting with Pinecone vector database. This project demonstrates basic operations including index creation, data upsertion, and semantic search using integrated embeddings.

## Overview

This project demonstrates how to:
- Create a Pinecone index with integrated embeddings
- Upsert text records into a Pinecone index
- Perform semantic search with metadata filtering
- Use namespaces for data organization

## Prerequisites

- Python 3.8 or higher
- A Pinecone account and API key ([Sign up here](https://www.pinecone.io/))
- pip (Python package manager)

## Setup

### 1. Clone or download this repository

```bash
cd vector-python
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```bash
PINECONE_API_KEY=your-pinecone-api-key-here
```

**Important:** Never commit your `.env` file to version control. It's already included in `.gitignore`.

### 5. Get your Pinecone API key

1. Sign up at [pinecone.io](https://www.pinecone.io/)
2. Navigate to your API keys section
3. Copy your API key
4. Add it to your `.env` file

## Usage

### Run the main script

```bash
python main.py
```

### What the script does

1. **Connects to Pinecone** - Initializes the Pinecone client using your API key
2. **Creates an index** (if it doesn't exist) - Creates `quickstart-py` index with:
   - Integrated embedding model: `llama-text-embed-v2`
   - Cloud: AWS
   - Region: us-east-1
   - Field mapping: `text` → `chunk_text`
3. **Upserts sample records** - Adds 4 movie-related text records with metadata (genre, year) to the `example-namespace` namespace
4. **Performs semantic search** - Searches for "funny" with a filter for "comedy" genre

## Project Structure

```
vector-python/
├── main.py              # Main script demonstrating Pinecone operations
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in git)
├── .gitignore          # Git ignore file
├── AGENTS.md           # Detailed Pinecone best practices reference
└── README.md           # This file
```

## Key Concepts Demonstrated

### 1. Integrated Embeddings
The index uses Pinecone's integrated embedding model (`llama-text-embed-v2`), which automatically generates embeddings from text. You don't need to create vectors manually.

### 2. Namespaces
Namespaces provide data isolation. Records are stored in the `example-namespace` namespace, allowing you to organize data by tenant, project, or use case.

### 3. Semantic Search
The search operation finds records semantically similar to the query text "funny", not just exact keyword matches.

### 4. Metadata Filtering
Filters allow you to narrow search results by metadata fields (e.g., `genre: "comedy"`).

## Code Examples

### Creating an Index

```python
pc.create_index_for_model(
    name="quickstart-py",
    cloud="aws",
    region="us-east-1",
    embed={
        "model": "llama-text-embed-v2",
        "field_map": {"text": "chunk_text"}
    }
)
```

### Upserting Records

```python
records = [
    {
        "_id": "A",
        "chunk_text": "A hilarious comedy movie released in 2020",
        "genre": "comedy",
        "year": 2020
    }
]
index.upsert_records("example-namespace", records)
```

### Searching with Filters

```python
results = index.search(
    namespace="example-namespace",
    query={
        "inputs": {"text": "funny"},
        "top_k": 3,
        "filter": {"genre": "comedy"}
    },
    fields=["chunk_text"]
)
```

## Best Practices

For detailed best practices and advanced patterns, see `AGENTS.md`. Key highlights:

- ✅ Always use namespaces for data isolation
- ✅ Use `upsert_records()` for indexes with integrated embeddings
- ✅ Use `search()` method (not `query()`) for semantic search
- ✅ Store API keys in environment variables, never hardcode them
- ✅ Use the Pinecone CLI for index management (create, delete, configure)

## Learning Resources

- [Pinecone Documentation](https://docs.pinecone.io/)
- [Pinecone Python SDK](https://sdk.pinecone.io/python/index.html)
- [Pinecone Quickstart Guide](https://docs.pinecone.io/guides/get-started/quickstart)

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your `.env` file contains `PINECONE_API_KEY=your-key`
2. **Index Not Found**: The script will create the index automatically if it doesn't exist
3. **Import Errors**: Make sure you've installed dependencies with `pip install -r requirements.txt`

### Getting Help

- Check `AGENTS.md` for detailed troubleshooting
- Visit [Pinecone Documentation](https://docs.pinecone.io/)
- Join the [Pinecone Community](https://www.pinecone.io/community/)

## Next Steps

1. Experiment with different search queries
2. Add more records with different metadata
3. Try creating multiple namespaces
4. Explore reranking for better search results (see `AGENTS.md`)
5. Build a RAG (Retrieval-Augmented Generation) system

## License

This is a learning project. Feel free to use and modify as needed.

## Contributing

This is a personal learning project, but suggestions and improvements are welcome!

