from pinecone import Pinecone
from .configs import settings
import time

class PineconeClient:
    def __init__(self):
        if not settings.PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY is not set")
        
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index_name = settings.INDEX_NAME
        self._ensure_index_exists()
        self.index = self.pc.Index(self.index_name)

    def _ensure_index_exists(self):
        """Create index if it doesn't exist"""
        if not self.pc.has_index(self.index_name):
            print(f"Index '{self.index_name}' does not exist. Creating it...")
            self.pc.create_index_for_model(
                name=self.index_name,
                cloud=settings.pinecone_config["cloud"],
                region=settings.pinecone_config["region"],
                embed=settings.pinecone_config["embed"]
            )
            print("Index created. Waiting for it to be ready...")
            time.sleep(5)

pinecone_client = PineconeClient()
