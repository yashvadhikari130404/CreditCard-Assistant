import os
from huggingface_hub import InferenceClient
import pprint

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise SystemExit("HF_TOKEN env var is not set")

client = InferenceClient(
    provider="hf-inference",          # <— serverless HF Inference API
    api_key=HF_TOKEN,
)

result = client.feature_extraction(
    "hello world",
    model="intfloat/multilingual-e5-large",  # solid embedding model
)

print("Type:", type(result))
print("First 2 levels of structure:")
pprint.pp(result[:2] if isinstance(result, list) else result)
