# llm_client.py
import json
from typing import List, Dict, Any, Optional

from huggingface_hub import InferenceClient
from config import settings
from models.schemas import Message

# Chat-based HF client (Inference Providers / router)
# We do NOT bind a model here; we pass it per call.
hf_llm_client = InferenceClient(api_key=settings.HF_TOKEN)

SYSTEM_PROMPT = """
You are a helpful credit-card assistant for a fintech company.

You can:
1. Answer questions from a knowledge base (FAQ text may be provided to you).
2. Decide when to call tools to perform actions on behalf of the user.

If an ACTION is required (like blocking a card, paying a bill, fetching account summary),
respond ONLY in this JSON format (no extra text):

{
  "type": "action",
  "action": "<one of: get_summary, block_card, pay_bill, list_recent_transactions, check_balance, increase_credit_limit, get_due_date, add_transaction, unblock_card>"
  "parameters": { ... }
}

If it's an informational question that can be answered from the KB snippet or your knowledge,
respond ONLY in this JSON format:

{
  "type": "answer",
  "answer": "<natural language response>"
}

Be strict about using these JSON shapes.
""".strip()


def _hf_chat(
    messages: List[Dict[str, str]],
    max_tokens: int = 256,
    temperature: float = 0.2,
) -> str:
    """
    Call Hugging Face Inference Providers chat-completions API.

    This uses the OpenAI-compatible chat API:
      POST https://router.huggingface.co/v1/chat/completions
    """
    completion = hf_llm_client.chat.completions.create(
        model=settings.HF_LLM_MODEL,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    # OpenAI-style response
    return completion.choices[0].message.content


def ask_llm_for_plan(
    chat_history: List[Message],
    kb_snippet: Optional[str] = None
) -> Dict[str, Any]:
    """
    Decide whether:
      - to answer directly (type='answer'), OR
      - to call a tool (type='action').

    Returns a dict shaped like one of:
      { "type": "answer", "answer": "<text>" }
      { "type": "action", "action": "<tool_name>", "parameters": {...} }
    """

    # Build a condensed conversation text (for context only)
    conversation = ""
    for m in chat_history[:-1]:
        conversation += f"{m.role.upper()}: {m.content}\n"

    last_user = chat_history[-1].content

    user_prompt_parts = []
    if conversation:
        user_prompt_parts.append("Conversation so far:\n" + conversation)
    user_prompt_parts.append(f"User question: {last_user}")
    if kb_snippet:
        user_prompt_parts.append(f"\nRelevant KB info:\n{kb_snippet}")

    user_prompt_parts.append(
        "\n\nNow decide whether to answer directly or call a tool, "
        "and respond ONLY in one of the JSON formats described in the system prompt."
    )

    user_prompt = "\n".join(user_prompt_parts)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    raw = _hf_chat(messages, max_tokens=256, temperature=0.1)

    # 1) Try parse raw as JSON
    try:
        return json.loads(raw)
    except Exception:
        pass

    # 2) Try extract JSON substring
    try:
        start = raw.index("{")
        end = raw.rindex("}") + 1
        json_str = raw[start:end]
        return json.loads(json_str)
    except Exception:
        # 3) Fallback: treat everything as an answer
        return {"type": "answer", "answer": raw}


def generate_final_answer(
    chat_history: List[Message],
    tool_result: Optional[Dict[str, Any]],
    kb_snippet: Optional[str],
) -> str:
    """
    Given:
      - the user's last question,
      - optional knowledge base snippet,
      - optional tool result (mock API data),

    ask the LLM to produce a nice, user-facing reply.
    """

    last_user = chat_history[-1].content

    context_parts = [f"User question: {last_user}"]

    if kb_snippet:
        context_parts.append(f"\nKnowledge base info:\n{kb_snippet}")
    if tool_result:
        context_parts.append(f"\nTool result (internal data):\n{tool_result}")

    context_parts.append(
        "\n\nUsing this context, write a clear, concise, friendly answer for the customer."
    )

    user_prompt = "\n".join(context_parts)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a concise, friendly credit-card assistant. "
                "Explain things in simple language."
            ),
        },
        {"role": "user", "content": user_prompt},
    ]

    return _hf_chat(messages, max_tokens=256, temperature=0.4)
