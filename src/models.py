from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class Record(BaseModel):
    id: str = Field(..., alias="_id")
    chunk_text: str
    genre: Optional[str] = None
    year: Optional[int] = None

class UpsertRequest(BaseModel):
    namespace:str = 'example-namespace'
    records: List[Record]

class SearchRequest(BaseModel):
    namespace:str = 'example-namespace'
    query_text: str
    top_k: int = 3
    filter: Optional[Dict[str, Any]] = None

class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    count: int
    
