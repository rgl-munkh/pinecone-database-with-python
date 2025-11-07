# Pinecone Database Learning Project

A FastAPI-based REST API for learning and experimenting with Pinecone vector database. This project demonstrates basic operations including index creation, data upsertion, and semantic search using integrated embeddings through a web API.

## Overview

This project demonstrates how to:
- Create a Pinecone index with integrated embeddings
- Build a REST API with FastAPI for Pinecone operations
- Upsert text records into a Pinecone index via API endpoints
- Perform semantic search with metadata filtering
- Use namespaces for data organization
- Structure a Python project with service layers and dependency injection

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

**Note:** The project also requires `fastapi`, `uvicorn`, and `pydantic` which should be installed separately if not already present:

```bash
pip install fastapi uvicorn pydantic
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

### Run the FastAPI server

Start the development server:

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, you can access:
- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc
- **Root endpoint**: http://localhost:8000/

### What the application does

1. **Connects to Pinecone** - Initializes the Pinecone client using your API key on startup
2. **Creates an index** (if it doesn't exist) - Automatically creates `quickstart-py` index with:
   - Integrated embedding model: `llama-text-embed-v2`
   - Cloud: AWS
   - Region: us-east-1
   - Field mapping: `text` → `chunk_text`
3. **Provides REST API endpoints** - Exposes endpoints for upserting records, searching, fetching records, and getting index statistics

## Project Structure

```
vector-python/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application entry point
│   ├── configs.py           # Configuration settings (API keys, index settings)
│   ├── models.py            # Pydantic models for request/response validation
│   ├── pinecone_client.py   # Pinecone client wrapper and initialization
│   ├── routes.py            # FastAPI route handlers
│   └── services/
│       └── index.py         # Service layer for Pinecone operations
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in git)
├── .gitignore              # Git ignore file
├── AGENTS.md               # Detailed Pinecone best practices reference
└── README.md               # This file
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

## API Endpoints

### POST `/api/records/upsert`

Upsert records into the Pinecone index.

**Request Body:**
```json
{
  "namespace": "example-namespace",
  "records": [
    {
      "_id": "A",
      "chunk_text": "A hilarious comedy movie released in 2020",
      "genre": "comedy",
      "year": 2020
    }
  ]
}
```

**Response:**
```json
{
  "message": "Successfully upserted 1 records",
  "count": 1
}
```

### GET `/api/records/search`

Search for records using semantic search.

**Query Parameters:**
- `namespace` (string, default: "example-namespace")
- `query_text` (string, required) - The search query
- `top_k` (integer, default: 3) - Number of results to return
- `filter` (JSON string, optional) - Metadata filter criteria as a JSON-encoded string

**Example Request:**
```bash
GET /api/records/search?namespace=example-namespace&query_text=funny&top_k=3&filter=%7B%22genre%22%3A%22comedy%22%7D
```

**Note:** The `filter` parameter should be URL-encoded JSON. For example, `{"genre":"comedy"}` becomes `%7B%22genre%22%3A%22comedy%22%7D`.

**Response:**
```json
{
  "results": [
    {
      "id": "A",
      "score": 0.85,
      "text": "A hilarious comedy movie released in 2020"
    }
  ],
  "count": 1
}
```

### GET `/api/records/{record_id}`

Fetch a single record by ID.

**Path Parameters:**
- `record_id` (string, required) - The record ID to fetch

**Query Parameters:**
- `namespace` (string, default: "example-namespace")

**Example Request:**
```bash
GET /api/records/A?namespace=example-namespace
```

### GET `/api/stats`

Get index statistics including total vector count and namespaces.

**Response:**
```json
{
  "total_vector_count": 10,
  "namespaces": ["example-namespace"]
}
```

## Code Examples

### Application Structure

The application follows a layered architecture:

- **Routes** (`src/routes.py`): Handle HTTP requests and responses
- **Services** (`src/services/index.py`): Business logic for Pinecone operations
- **Client** (`src/pinecone_client.py`): Pinecone client initialization and index management
- **Models** (`src/models.py`): Pydantic models for data validation
- **Config** (`src/configs.py`): Configuration management

### Creating an Index (Automatic)

The index is automatically created on application startup if it doesn't exist:

```python
# src/pinecone_client.py
def _ensure_index_exists(self):
    if not self.pc.has_index(self.index_name):
        self.pc.create_index_for_model(
            name=self.index_name,
            cloud=settings.pinecone_config["cloud"],
            region=settings.pinecone_config["region"],
            embed=settings.pinecone_config["embed"]
        )
```

### Upserting Records via API

```python
# Using curl
curl -X POST "http://localhost:8000/api/records/upsert" \
  -H "Content-Type: application/json" \
  -d '{
    "namespace": "example-namespace",
    "records": [
      {
        "_id": "A",
        "chunk_text": "A hilarious comedy movie released in 2020",
        "genre": "comedy",
        "year": 2020
      }
    ]
  }'
```

### Searching with Filters via API

```python
# Using curl
curl "http://localhost:8000/api/records/search?namespace=example-namespace&query_text=funny&top_k=3&filter=%7B%22genre%22%3A%22comedy%22%7D"
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
2. **Index Not Found**: The application will create the index automatically if it doesn't exist on startup
3. **Import Errors**: Make sure you've installed dependencies with `pip install -r requirements.txt` and `pip install fastapi uvicorn pydantic`
4. **ModuleNotFoundError**: Make sure you're running uvicorn from the project root directory, not from within the `src` folder
5. **Port Already in Use**: If port 8000 is in use, specify a different port: `uvicorn src.main:app --reload --port 8001`

### Getting Help

- Check `AGENTS.md` for detailed troubleshooting
- Visit [Pinecone Documentation](https://docs.pinecone.io/)
- Join the [Pinecone Community](https://www.pinecone.io/community/)

## Next Steps

1. Experiment with different search queries using the API endpoints
2. Add more records with different metadata via the upsert endpoint
3. Try creating multiple namespaces and querying them separately
4. Explore reranking for better search results (see `AGENTS.md`)
5. Build a RAG (Retrieval-Augmented Generation) system by integrating with LLM APIs
6. Add authentication and authorization to secure the API
7. Implement request validation and error handling improvements
8. Add logging and monitoring capabilities

## License

This is a learning project. Feel free to use and modify as needed.

## Contributing

This is a personal learning project, but suggestions and improvements are welcome!

