import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY")
    INDEX_NAME: str = "quickstart-py"
    DEFAULT_NAMESPACE: str = "example-namespace"

    @property
    def pinecone_config(self):
        return {
            "cloud": "aws",
            "region": "us-east-1",
            "embed": {
                "model": "llama-text-embed-v2",
                "field_map": {"text": "chunk_text"},
            },
        }


settings = Settings()
