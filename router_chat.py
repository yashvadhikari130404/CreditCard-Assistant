# router_chat.py
from typing import Optional, List
from fastapi import APIRouter
from models.schemas import ChatRequest, ChatResponse, ToolCallResult, Message
from knowledge_base.retriever import FAQRetriever
from tools.dispatcher import execute_tool
from llm_client import ask_llm_for_plan, generate_final_answer

router = APIRouter()

# Load FAQ retriever once at startup
retriever = FAQRetriever("knowledge_base/faqs.yaml")

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(body: ChatRequest) -> ChatResponse:
    user_question = body.messages[-1].content

    # 1. Retrieve from KB (information retrieval)
    faq, score = retriever.retrieve(user_question)
    kb_snippet: Optional[str] = None
    if score > 0.7:  # threshold, adjust as needed
        kb_snippet = faq["answer"]

    # 2. Ask LLM: info-only or needs tool?
    history_messages: List[Message] = [Message(**m.model_dump()) for m in body.messages]
    plan = ask_llm_for_plan(history_messages, kb_snippet)

    tool_calls_details: List[ToolCallResult] = []
    tool_result: Optional[dict] = None
    source: Optional[str] = None

    if plan.get("type") == "action":
        action = plan.get("action")
        params = plan.get("parameters", {}) or {}
        # Always include user_id for tools
        params["user_id"] = body.user_id

        tool_result = execute_tool(action, params)
        tool_calls_details.append(
            ToolCallResult(
                tool_name=action,
                success=tool_result.get("success", True),
                result=tool_result,
            )
        )
        source = "tool"
    else:
        # Informational answer
        source = "knowledge_base" if kb_snippet else "llm"

    # 3. Generate final answer text
    reply_text = generate_final_answer(history_messages, tool_result, kb_snippet)

    return ChatResponse(
        reply=reply_text,
        tool_calls=tool_calls_details or None,
        source=source,
    )
