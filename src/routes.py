from fastapi import APIRouter, HTTPException
from .models import UpsertRequest, SearchRequest, SearchResponse
from .services.index import pinecone_service

router = APIRouter()


@router.post("/records/upsert", response_model=dict)
async def upsert_records(request: UpsertRequest):
    """Upsert records into index"""

    try:
        result = pinecone_service.upsert_records(request.namespace, request.records)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/records/search", response_model=SearchResponse)
async def saerch_records(request: SearchRequest):
    """Search records in index"""

    try:
        result = pinecone_service.search(
            namespace=request.namespace,
            query_text=request.query_text,
            top_k=request.top_k,
            filter=request.filter,
        )

        return SearchResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/records/{record_id}")
async def get_record(record_id: str, namespace: str = "example-namespace"):
    """Fetch a single record by id"""

    try:
        result = pinecone_service.fetch_record(namespace=namespace, ids=[record_id])

        fetched = getattr(result, "records", None) or getattr(result, "vectors", None)

        if fetched and record_id in fetched:
            return {"record": fetched[record_id]}
        raise HTTPException(status_code=404, detail="Record not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_stats():
    """Get index stats"""

    try:
        stats = pinecone_service.index.describe_index_stats()
        print(stats)
        return {
            "total_vector_count": stats.total_vector_count,
            "namespaces": list(stats.namespaces.keys())
            if hasattr(stats, "namespaces")
            else [],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
