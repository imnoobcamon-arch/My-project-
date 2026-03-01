import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# =========================
# CONFIG
# =========================

TELEGRAM_TOKEN = os.getenv("8339428632:AAHF1gggoyh7MCLzVG2nQToE2yh1qtyJZIo")
CLAUDE_API_KEY = os.getenv("sk-ant-api03-9c5...nwAA")

CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

MODEL = "claude-3-5-sonnet-20240620"

# =========================
# CLAUDE SYSTEM PROMPT
# =========================

CLAUDE_SYSTEM_PROMPT = """
You are a professional Forex Market Analyst specializing in ICT (Inner Circle Trader)
and advanced MSNR (Alchemist framework).

Core Structure Rules:
- D1: Bias determination AND structure 
- H4 & H1: Structure reading and trend identification
- 5m: Entry model refinement ONLY

Concepts you MUST use:
- ICT Market Structure (BOS, MSS)
- Liquidity (buy-side / sell-side, inducement, sweeps)
- MSNR POI Classic Levels (V & A, OC levels, zones)
- Dealing ranges
- RBS / SBR transitions

Risk Framework (DESCRIPTIVE ONLY):
- TP: Nearest 30M undelivered price wick
- SL: calculated based on RR
- Balanced R:R with consistency as the priority

ABSOLUTE RULES:
- signals
- buy/sell language
- exact prices
- financial advice
- logic ONLY

If required market input is missing, you MUST explicitly say analysis cannot be performed.
"""

# =========================
# HELPER: CALL CLAUDE
# =========================

def call_claude(user_content: str) -> str:
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    payload = {
        "model": MODEL,
        "system": CLAUDE_SYSTEM_PROMPT,
        "messages": [
            {"role": "user", "content": user_content}
        ],
        "max_tokens": 900,
        "temperature": 0.3
    }

    response = requests.post(CLAUDE_API_URL, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()["content"][0]["text"]

# =========================
# TELEGRAM COMMANDS
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ICT × MSNR (Alchemist) Analysis Engine\n\n"
        "This bot does NOT analyze without structured market input.\n\n"
        "Use /analyze and provide full framework data."
    )

# =========================
# ANALYSIS COMMAND
# =========================

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = " ".join(context.args)

    if not user_input or len(user_input) < 50:
        await update.message.reply_text(
            "Analysis refused.\n\n"
            "Required market input missing.\n\n"
            "Provide:\n"
            "- Market Pair\n"
            "- Current Session (UTC+3)\n"
            "- D1 & H4 structure\n"
            "- H1 or M15 behavior\n"
            "- Liquidity status\n"
            "- Key levels\n"
            "- Approximate current price"
        )
        return

    structured_prompt = f"""
The framework is clear, and the role is accepted.

Before any analysis can be structured, the required market input must be provided.
Without it, any narrative would be speculation dressed as analysis.

Market Input Provided:
{user_input}

Construct a full top-down narrative using the required format:

1. Market & Session Context
2. Daily Bias (D1)
3. H4 & H1 Structure Alignment
4. Liquidity Narrative
5. MSNR POI & Key Levels
6. 5M Entry Model Logic (DESCRIPTIVE)
7. Risk & Execution Discipline
"""

    try:
        analysis = call_claude(structured_prompt)
        await update.message.reply_text(analysis)
    except Exception as e:
        await update.message.reply_text(f"Error generating analysis:\n{str(e)}")

# =========================
# MAIN
# =========================

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analyze", analyze))

    print("ICT × MSNR Analysis Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
