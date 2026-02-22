from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from ai_engine import ask_ai

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to static folder (same directory as main.py)
STATIC_DIR = Path(__file__).resolve().parent / "static"

# ---------------------------------------------------------------------------
# Multi-user credentials (username -> password). Demo only; use hashed in prod.
# ---------------------------------------------------------------------------
USERS: dict[str, str] = {
    "alice": "alice123",
    "bob": "bob456",
    "priya": "priya789",
    "admin": "admin@2026",
}

# Per-user account ID counter (so each user has their own 1, 2, 3...)
_user_account_counters: dict[str, int] = {}


def _default_account_data():
    return {
        "balance": 75000,
        "transactions": [
            {"amount": 5000, "type": "credit", "date": "2026-02-20"},
            {"amount": 2000, "type": "debit", "date": "2026-02-19"},
            {"amount": 10000, "type": "credit", "date": "2026-02-18"},
        ],
    }


# users_accounts[username][account_id] -> { name, balance, transactions }
def _ensure_user_accounts(username: str) -> dict:
    if not hasattr(app.state, "users_accounts"):
        app.state.users_accounts = {}
    if username not in app.state.users_accounts:
        app.state.users_accounts[username] = {
            "1": {"name": "Primary", **_default_account_data()},
        }
        _user_account_counters[username] = 2  # next new account will be "2"
    return app.state.users_accounts[username]


def _next_account_id(username: str) -> str:
    _ensure_user_accounts(username)
    n = _user_account_counters.get(username, 1)
    _user_account_counters[username] = n + 1
    return str(n)


def _get_account(username: str, account_id: str | None, accounts: dict):
    if account_id and account_id in accounts:
        return accounts[account_id]
    return next(iter(accounts.values()), None) if accounts else None


@app.get("/")
def root():
    """Serve the frontend app."""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Backend Running"}


class LoginRequest(BaseModel):
    username: str = ""
    password: str = ""


@app.post("/login")
def login(credentials: LoginRequest):
    """Validate username/password. Returns username on success so frontend can send it in X-Username header."""
    username = (credentials.username or "").strip().lower()
    password = credentials.password or ""
    if not username:
        return {"success": False}
    if username in USERS and USERS[username] == password:
        _ensure_user_accounts(username)
        return {"success": True, "username": username}
    return {"success": False}


def _require_username(x_username: str | None = Header(None, alias="X-Username")) -> str:
    if not x_username or not x_username.strip():
        raise HTTPException(status_code=401, detail="Missing X-Username header. Please log in again.")
    uname = x_username.strip().lower()
    if uname not in USERS:
        raise HTTPException(status_code=401, detail="Unknown user. Please log in again.")
    return uname


@app.get("/accounts")
def list_accounts(username: str = Depends(_require_username)):
    accounts = _ensure_user_accounts(username)
    return [
        {"id": aid, "name": acc.get("name", "Account"), "balance": acc.get("balance", 0)}
        for aid, acc in accounts.items()
    ]


class CreateAccountRequest(BaseModel):
    name: str = "New Account"


@app.post("/accounts")
def create_account(req: CreateAccountRequest, username: str = Depends(_require_username)):
    accounts = _ensure_user_accounts(username)
    aid = _next_account_id(username)
    accounts[aid] = {
        "name": (req.name or "New Account").strip() or "New Account",
        "balance": 0,
        "transactions": [],
    }
    return {"id": aid, "name": accounts[aid]["name"], "balance": 0}


@app.get("/balance")
def get_balance(account_id: str | None = None, username: str = Depends(_require_username)):
    accounts = _ensure_user_accounts(username)
    acc = _get_account(username, account_id, accounts)
    if not acc:
        return {"balance": 0}
    return {"balance": acc["balance"]}


class UpdateBalanceRequest(BaseModel):
    balance: float = 0
    account_id: str | None = None


@app.put("/balance")
def update_balance(req: UpdateBalanceRequest, username: str = Depends(_require_username)):
    accounts = _ensure_user_accounts(username)
    acc = _get_account(username, req.account_id, accounts)
    if not acc:
        return {"balance": 0}
    acc["balance"] = max(0, req.balance)
    return {"balance": acc["balance"]}


@app.get("/transactions")
def get_transactions(account_id: str | None = None, username: str = Depends(_require_username)):
    accounts = _ensure_user_accounts(username)
    acc = _get_account(username, account_id, accounts)
    if not acc:
        return []
    return acc["transactions"]


class AddTransactionRequest(BaseModel):
    amount: float = 0
    type: str = "credit"
    date: str = ""
    account_id: str | None = None


@app.post("/transactions")
def add_transaction(req: AddTransactionRequest, username: str = Depends(_require_username)):
    accounts = _ensure_user_accounts(username)
    acc = _get_account(username, req.account_id, accounts)
    if not acc:
        return {"balance": 0, "transactions": []}
    from datetime import date as dt_date
    amount = max(0, req.amount)
    tx_type = (req.type or "credit").lower()
    if tx_type not in ("credit", "debit"):
        tx_type = "credit"
    if tx_type == "debit" and amount > acc["balance"]:
        raise HTTPException(
            status_code=400,
            detail={"success": False, "error": "Not Sufficient Balance", "balance": acc["balance"]},
        )
    tx_date = (req.date or "").strip() or dt_date.today().isoformat()
    acc["transactions"].insert(0, {"amount": amount, "type": tx_type, "date": tx_date})
    if tx_type == "credit":
        acc["balance"] += amount
    else:
        acc["balance"] = max(0, acc["balance"] - amount)
    return {"balance": acc["balance"], "transactions": acc["transactions"]}


def _monthly_for_account(acc: dict) -> dict:
    monthly = {}
    for tx in acc.get("transactions", []):
        if tx.get("type") == "debit":
            parts = (tx.get("date") or "").split("-")
            if len(parts) >= 2:
                year, month = parts[0], parts[1]
                months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                key = f"{months[int(month) - 1]} {year}"
                monthly[key] = monthly.get(key, 0) + tx.get("amount", 0)
    if not monthly:
        monthly = {"Feb 2026": 2000}
    return monthly


class ChatRequest(BaseModel):
    message: str = ""
    account_id: str | None = None


@app.post("/chat")
def chat(request: ChatRequest, username: str = Depends(_require_username)):
    message = (request.message or "").strip()
    if not message:
        return {"response": "Please type a message so I can help you."}
    accounts = _ensure_user_accounts(username)
    acc = _get_account(username, request.account_id, accounts)
    if not acc:
        return {"response": "No account selected. Please switch to an account."}
    context = {
        "balance": acc["balance"],
        "transactions": acc["transactions"],
        "monthly_spending": _monthly_for_account(acc),
    }
    try:
        reply = ask_ai(message, context)
    except Exception as e:
        reply = f"I'm temporarily unable to answer. Please try again. ({str(e)[:80]})"
    return {"response": reply}