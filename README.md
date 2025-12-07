# GenAI Credit Card Assistant

A conversational AI assistant for credit card customers, built with **FastAPI**, **Hugging Face Inference API**, and mock APIs to simulate real banking operations.  
The assistant can answer FAQs, retrieve account information, and perform actions like blocking a card, paying bills, or checking balances.

---

## Features
- **Chatbot interface** (web frontend + FastAPI backend).
- **Knowledge Base Retrieval**: Answers common FAQs using embeddings.
- **Tool Execution**: Performs actions via mock APIs:
  - Get account summary
  - Block / Unblock card
  - Pay bill
  - List recent transactions
  - Check balance
  - Increase credit limit
  - Get due date
  - Add new transactions
- **LLM Integration**: Uses Hugging Face models for embeddings and chat completions.
- **Multi‑channel ready**: Designed to work across web, app, WhatsApp, and IVR.

---

## Tech Stack
- **Backend**: FastAPI + Uvicorn
- **LLM**: Hugging Face Inference API
- **Data**: YAML‑based FAQ knowledge base
- **Mock APIs**: Simulated credit card operations
- **Frontend**: Simple web UI (HTML/JS)

---

## Project Structure
CreditCard-Assistant/
│
├── app.py                  # FastAPI entrypoint
├── config.py               # Configuration (HF token, model settings)
├── index.html              # Frontend UI
├── llm_client.py           # Hugging Face LLM client
├── router_chat.py          # FastAPI routes for chat
├── requirements.txt        # Python dependencies
├── test.py                 # Basic tests
├── README.md               # Project documentation
│
├── knowledge_base/         # FAQ knowledge base
│   ├── faqs.yaml           # FAQ data
│   └── retriever.py        # Retriever logic with embeddings
│
├── models/                 # Data schemas
│   └── schemas.py          # Pydantic models for requests/responses
│
└── tools/                  # Mock APIs and dispatcher
    ├── mock_apis.py        # Simulated credit card operations
    └── dispatcher.py       # Maps actions to mock APIs


---
## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/credit-chatbot.git
cd credit-chatbot

```
### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate # On Mac/Linux
```

### 3.Install Dependencies
```bash
pip install -r requirements.txt
```

### 4.Set Hugging Face API token
```bash
export HF_TOKEN="your_hf_token_here"
```
### 5.Run Backend
```bash
uvicorn app:app --reload
```
### 6. Test
```bash
# Get account summary
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
        "user_id": "user_123",
        "channel": "web",
        "messages": [{"role":"user","content":"Show me my account summary"}]
      }'
```
---


