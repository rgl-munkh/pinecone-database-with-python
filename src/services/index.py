from ..pinecone_client import pinecone_client
from ..models import Record
from typing import List, Dict, Any, Optional


class PineconeService:
    def __init__(self):
        self.index = pinecone_client.index

    def upsert_records(self, namespace: str, records: List[Record]) -> Dict[str, Any]:
        """Upsert records into the index"""

        records_dict = [record.dict(by_alias=True) for record in records]
        self.index.upsert_records(namespace, records_dict)

        return {
            "message": f"Successfully upserted {len(records)} records",
            "count": len(records),
        }

    def search(
        self,
        namespace: str,
        query_text: str,
        top_k: int = 3,
        filter: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Search records in index"""

        query_dict = {
            "inputs": {"text": query_text},
            "top_k": top_k,
        }

        if filter:
            query_dict["filter"] = filter

        results = self.index.search(namespace, query=query_dict, fields=["chunk_text"])

        hits = []

        if hasattr(results, "result") and hasattr(results.result, "hits"):
            for hit in results.result.hits:
                hits.append(
                    {
                        "id": hit.get("-Id", ""),
                        "score": hit.get("_score", 0),
                        "text": hit.fields.get("chunk_text", "")
                        if hasattr(hit, "fields")
                        else "",
                    }
                )

        return {
            "results": hits,
            "count": len(hits),
        }

pinecone_service = PineconeService()