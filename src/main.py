from fastapi import FastAPI
from .routes import router

app = FastAPI(
    title="Pinecone Learning API",
    description="API for learning Pinecone vector database operations",
    version="0.0.1",
)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Pinecone Quickstart API!",
        "docs": "/docs",
        "endpoints": {
            "upsert": "/records/upsert",
            "search": "/records/search",
            "get_record": "/records/{record_id}",
            "stats": "/stats",
        },
    }


app.include_router(router, prefix="/api", tags=["pinecone"])
