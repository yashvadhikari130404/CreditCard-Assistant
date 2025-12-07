# # app.py
# from fastapi import FastAPI
# from router_chat import router as chat_router

# app = FastAPI(
#     title="GenAI Credit Card Assistant (Hugging Face)",
#     version="0.1.0",
# )

# app.include_router(chat_router, prefix="/api")

# @app.get("/")
# async def root():
#     return {"message": "GenAI Credit Card Assistant API is running (HF version)"}


# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router_chat import router as chat_router

app = FastAPI(
    title="GenAI Credit Card Assistant (HF)",
    version="0.1.0",
)

# Allow local frontend (file://, localhost) to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # for demo; in prod, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "GenAI Credit Card Assistant API is running"}
