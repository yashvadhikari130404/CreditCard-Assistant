# tools/dispatcher.py
from typing import Dict, Any
from . import mock_apis

def execute_tool(action: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map high-level action names to specific mock functions.
    """
    user_id = params.get("user_id")
    if action == "get_summary":
        return mock_apis.get_summary(user_id)
    if action == "block_card":
        return mock_apis.block_card(user_id)
    if action == "pay_bill":
        amount = float(params.get("amount", 0))
        return mock_apis.pay_bill(user_id, amount)
    if action == "list_recent_transactions":
        limit = int(params.get("limit", 5))
        return mock_apis.list_recent_transactions(user_id, limit)
    if action == "check_balance":
        return mock_apis.check_balance(user_id)
    if action == "increase_credit_limit":
        amount = float(params.get("amount", 0))
        return mock_apis.increase_credit_limit(user_id, amount)
    if action == "get_due_date":
        return mock_apis.get_due_date(user_id)
    if action == "add_transaction":
        amount = float(params.get("amount", 0))
        merchant = params.get("merchant", "Unknown")
        txn_date = params.get("date", "2025-12-07")
        return mock_apis.add_transaction(user_id, amount, merchant, txn_date)
    if action == "unblock_card":
        return mock_apis.unblock_card(user_id)


    return {"success": False, "message": f"Unknown action: {action}"}
