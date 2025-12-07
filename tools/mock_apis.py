# tools/mock_apis.py
from datetime import date
from typing import Dict, Any, List

USERS: Dict[str, Dict[str, Any]] = {
    "user_123": {
        "name": "Alex",
        "card_last4": "4321",
        "status": "active",
        "credit_limit": 100000,
        "available_limit": 65000,
        "current_outstanding": 35000,
        "due_date": str(date.today().replace(day=25)),
        "overdue": False,
        "transactions": [
            {"id": "txn_001", "amount": 1500, "merchant": "Amazon", "date": "2025-12-01"},
            {"id": "txn_002", "amount": 2000, "merchant": "Uber", "date": "2025-12-03"},
        ],
    }
}

def get_summary(user_id: str) -> Dict[str, Any]:
    user = USERS.get(user_id)
    if not user:
        return {"success": False, "message": "User not found"}
    return {"success": True, "data": user}

def block_card(user_id: str) -> Dict[str, Any]:
    user = USERS.get(user_id)
    if not user:
        return {"success": False, "message": "User not found"}
    user["status"] = "blocked"
    return {
        "success": True,
        "message": "Your card has been blocked.",
        "status": user["status"],
    }

def pay_bill(user_id: str, amount: float) -> Dict[str, Any]:
    user = USERS.get(user_id)
    if not user:
        return {"success": False, "message": "User not found"}
    user["current_outstanding"] = max(user["current_outstanding"] - amount, 0)
    user["available_limit"] += amount
    return {
        "success": True,
        "message": f"Payment of ₹{amount:.2f} received.",
        "current_outstanding": user["current_outstanding"],
        "available_limit": user["available_limit"],
    }

def list_recent_transactions(user_id: str, limit: int = 5) -> Dict[str, Any]:
    user = USERS.get(user_id)
    if not user:
        return {"success": False, "message": "User not found"}
    txns: List[Dict[str, Any]] = user["transactions"][:limit]
    return {"success": True, "transactions": txns}


def check_balance(user_id: str) -> Dict[str, Any]:
    """Return the available credit balance for the user."""
    user = USERS.get(user_id)
    if not user:
        return {"success": False, "message": "User not found"}
    return {
        "success": True,
        "available_limit": user["available_limit"],
        "current_outstanding": user["current_outstanding"],
    }

def increase_credit_limit(user_id: str, amount: float) -> Dict[str, Any]:
    """Increase the user's credit limit by a given amount."""
    user = USERS.get(user_id)
    if not user:
        return {"success": False, "message": "User not found"}
    user["credit_limit"] += amount
    user["available_limit"] += amount
    return {
        "success": True,
        "message": f"Credit limit increased by ₹{amount:.2f}.",
        "new_credit_limit": user["credit_limit"],
        "available_limit": user["available_limit"],
    }

def get_due_date(user_id: str) -> Dict[str, Any]:
    """Return the due date for the user's bill."""
    user = USERS.get(user_id)
    if not user:
        return {"success": False, "message": "User not found"}
    return {
        "success": True,
        "due_date": user["due_date"],
        "overdue": user["overdue"],
    }

def add_transaction(user_id: str, amount: float, merchant: str, txn_date: str) -> Dict[str, Any]:
    """Add a new transaction to the user's account."""
    user = USERS.get(user_id)
    if not user:
        return {"success": False, "message": "User not found"}
    txn_id = f"txn_{len(user['transactions'])+1:03d}"
    txn = {"id": txn_id, "amount": amount, "merchant": merchant, "date": txn_date}
    user["transactions"].insert(0, txn)  # add to the front
    user["current_outstanding"] += amount
    user["available_limit"] = max(user["available_limit"] - amount, 0)
    return {
        "success": True,
        "message": f"Transaction added: {merchant} ₹{amount:.2f}",
        "transaction": txn,
        "current_outstanding": user["current_outstanding"],
        "available_limit": user["available_limit"],
    }

def unblock_card(user_id: str) -> Dict[str, Any]:
    """Unblock the user's card if it was blocked."""
    user = USERS.get(user_id)
    if not user:
        return {"success": False, "message": "User not found"}
    if user["status"] != "blocked":
        return {"success": False, "message": "Card is not blocked."}
    user["status"] = "active"
    return {
        "success": True,
        "message": "Your card has been unblocked.",
        "status": user["status"],
    }
