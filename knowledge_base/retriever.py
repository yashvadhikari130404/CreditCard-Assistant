# knowledge_base/retriever.py
import yaml
import numpy as np
from typing import List, Dict, Tuple, Optional

from huggingface_hub import InferenceClient
from config import settings

# Single global client for HF Inference (serverless)
hf_client = InferenceClient(
    provider="hf-inference",
    api_key=settings.HF_TOKEN,
)

class FAQRetriever:
    def __init__(self, path: str):
        # Load FAQs
        with open(path, "r", encoding="utf-8") as f:
            self.faqs: List[Dict] = yaml.safe_load(f)

        # Precompute embeddings for all FAQ entries at startup
        texts = [
            faq["question"] + " " + faq["answer"]
            for faq in self.faqs
        ]
        self.embeddings = self._embed_corpus(texts)

    # ---- Embedding helpers ----

    def _embed_text(self, text: str) -> np.ndarray:
        """
        Embed a single string using HF Inference feature_extraction.
        HF returns token-level vectors; we average over tokens to get a single vector.
        """
        result = hf_client.feature_extraction(
            text,
            model=settings.HF_EMBEDDING_MODEL,
        )
        arr = np.array(result, dtype=np.float32)

        # Typical shapes:
        #  - (seq_len, hidden_size)
        #  - sometimes nested, but np.array handles it
        if arr.ndim == 1:
            # Already a 1D embedding
            return arr
        elif arr.ndim == 2:
            # Average over sequence length
            return arr.mean(axis=0)
        else:
            # Fallback: flatten everything
            return arr.reshape(-1)

    def _embed_corpus(self, texts: List[str]) -> np.ndarray:
        vectors = [self._embed_text(t) for t in texts]
        return np.stack(vectors, axis=0)

    def _embed_query(self, query: str) -> np.ndarray:
        return self._embed_text(query)

    # ---- Public retrieval API ----

    def retrieve(self, query: str, top_k: int = 1) -> Tuple[Optional[Dict], float]:
        """
        Return best matching FAQ and cosine similarity score.
        """
        query_emb = self._embed_query(query)

        # Cosine similarity with all FAQ embeddings
        norms = np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_emb)
        scores = (self.embeddings @ query_emb) / (norms + 1e-8)

        idx = int(np.argmax(scores))
        return self.faqs[idx], float(scores[idx])
