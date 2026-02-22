from datetime import datetime
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def _build_system_prompt(context: dict) -> str:
    """Build a system prompt that gives the AI current account context."""
    now = datetime.now()
    current_date = now.strftime("%A, %d %B %Y")   # e.g. Sunday, 22 February 2026
    current_time = now.strftime("%I:%M %p")       # e.g. 02:30 PM

    balance = context.get("balance", 0)
    transactions = context.get("transactions", [])
    monthly = context.get("monthly_spending", {})

    lines = [
        "You are MoneyCortex's friendly AI banking assistant. Be warm, clear, and creative.",
        "",
        "STRUCTURED RESPONSE RULES (follow every time):",
        "1. Structure your reply with clear sections. Use **bold** for key numbers and labels (e.g. **Balance: ₹75,000**).",
        "2. Use bullet points (start lines with • or -) for lists (transactions, tips, options).",
        "3. Add a short, friendly opening line, then the structured data, then an optional one-line tip or sign-off.",
        "4. When showing numbers (balance, amounts), use Indian format with commas (e.g. ₹75,000).",
        "5. Keep sections scannable: use line breaks between sections and short paragraphs.",
        "6. Be creative: vary your tone, add a relevant emoji occasionally (💰 📊 ✅), and give one practical tip when relevant.",
        "",
        "When the user asks for the date or time, use this exact information:",
        f"Today's date: {current_date}.",
        f"Current time: {current_time}.",
        "",
        "Use the following current account data to answer. Always use this data for balance, transactions, or spending:",
        "",
        f"Current balance: ₹{balance}",
        "",
        "Recent transactions (amount, type, date):",
    ]
    for tx in transactions:
        lines.append(f"  - ₹{tx.get('amount')} ({tx.get('type')}) on {tx.get('date')}")
    if monthly:
        lines.append("")
        lines.append("Monthly spending:")
        for month, amount in monthly.items():
            lines.append(f"  - {month}: ₹{amount}")
    lines.append("")
    lines.append("For non-account questions, answer helpfully from general banking knowledge. Always use Indian Rupee (₹) for money.")
    return "\n".join(lines)


def ask_ai(message: str, context: dict | None = None) -> str:
    """Get a dynamic AI reply using the given account context."""
    context = context or {}
    system_content = _build_system_prompt(context)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": message.strip() or "Hello"},
        ],
        temperature=0.5,
    )

    return response.choices[0].message.content or "I couldn't generate a response. Please try again."