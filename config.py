# config.py
import os
from pydantic import BaseModel

class Settings(BaseModel):
    HF_TOKEN: str = os.getenv("HF_TOKEN", "")
    # LLM for planning + answers (works with Inference Providers)
    HF_LLM_MODEL: str = "openai/gpt-oss-20b"
    # Embeddings (already working)
    HF_EMBEDDING_MODEL: str = "intfloat/multilingual-e5-large"

settings = Settings()
