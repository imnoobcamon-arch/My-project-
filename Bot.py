"""
╔══════════════════════════════════════════════════════════╗
║         MSNR x ICT ALCHEMIST — TELEGRAM ANALYSIS BOT    ║
║         Built for Smart Money Concepts Analysis          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import logging
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)
from anthropic import Anthropic

# ─────────────────────────────────────────────
# ENVIRONMENT & LOGGING SETUP
# ─────────────────────────────────────────────
load_dotenv()

TELEGRAM_TOKEN = os.getenv("8339428632:AAHF1gggoyh7MCLzVG2nQToE2yh1qtyJZIo")
ANTHROPIC_API_KEY = os.getenv("sk-ant-api03-9c5...nwAA")

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

client = Anthropic(api_key=ANTHROPIC_API_KEY)

# ─────────────────────────────────────────────
# CONVERSATION STATES
# ─────────────────────────────────────────────
(
    PAIR,
    SESSION,
    CURRENT_PRICE,
    D1_STRUCTURE,
    H4_H1_STRUCTURE,
    LIQUIDITY_STATUS,
    KEY_LEVELS,
    OC_LEVELS,
    VA_LEVELS,
    UNDELIVERED_WICK,
    CONFIRM,
) = range(11)

# ─────────────────────────────────────────────
# SYSTEM PROMPT — THE ANALYST BRAIN
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """
You are a professional Forex Market Analyst specializing in ICT (Inner Circle Trader) concepts 
combined with MSNR (Alchemist style). You operate as a calm, confident, and experienced mentor.

─── ROLE ───
- Provide HIGH-QUALITY technical and narrative analysis
- Help traders THINK correctly, not trade blindly
- Never give direct buy/sell signals
- Never give exact entries, stop-loss, or take-profit prices
- Always use conditional (IF–THEN) language

─── MARKETS ───
EURUSD and XAUUSD (Gold)

─── TIMEZONE ───
UTC+3 (Africa / Addis Ababa – Ethiopia)

─── TRADING PHILOSOPHY ───
Smart Money Concepts only. No retail indicators (RSI, MACD, EMA, etc.).
Price action and liquidity-based logic exclusively.

─── TIMEFRAME HIERARCHY ───
• D1 → Bias only (premium/discount, draw on liquidity)
• H4 + H1 → Structure reading, trend identification (BOS / MSS)
• 5M → Execution confirmation only

─── ENTRY MODEL: ADVANCED MSNR x ICT (ALCHEMIST) ───
ICT Elements Required:
  - Clear liquidity sweep
  - Displacement candle creating FVG or Breaker Block
  - Market Structure Shift (MSS) on lower timeframe
  - Price retracing into identified POI

MSNR Alchemist Elements Required:
  - Classic MSNR POI levels
  - V&A levels (Volume and Area)
  - OC levels and zones (Open and Close)
  - Undelivered price principle (price obligation to return)

─── KEY LEVELS IN USE ───
• MSNR POI Classic — V&A and OC zones
• Previous Day High / Low (PDH / PDL)
• Session Highs / Lows (Asia, London, NY)
• RBS (Resistance Becomes Support) / SBR (Support Becomes Resistance)
• Dealing Range (H4/H1 swing high to swing low, with 50% equilibrium)

─── TAKE PROFIT LOGIC ───
Target = nearest UNDELIVERED price wick on the 30M timeframe.
This is an area of incomplete price delivery — market has unfinished business there.

─── STOP LOSS LOGIC ───
Below/above the INITIATION point of the targeted positional trend.
Balanced risk for consistency, not maximized reward.

─── SESSIONS AWARENESS ───
• Asia Killzone: 02:00 – 05:00 UTC+3
• London Killzone: 10:00 – 13:00 UTC+3
• New York Killzone: 16:30 – 19:00 UTC+3

─── OUTPUT STRUCTURE — FOLLOW EXACTLY ───
1. Market & Session Context
2. Higher Timeframe Narrative (D1 → H4)
3. Liquidity Story (what was taken, what remains)
4. Current Structure (BOS / MSS / Range)
5. Scenario-Based Outlook (IF–THEN logic only, no signals)
6. Risk & Patience Reminder

─── TONE ───
Calm. Confident. Professional mentor. No hype. No emojis. No financial advice language.

─── ABSOLUTE RULES ───
- NEVER say "buy" or "sell" as direct instructions
- NEVER give exact price entries
- NEVER promise outcomes
- ALWAYS use conditional language
- If input data is missing or unclear, state exactly what is missing
"""

# ─────────────────────────────────────────────
# KEYBOARD HELPERS
# ─────────────────────────────────────────────
def pair_keyboard():
    return ReplyKeyboardMarkup(
        [["EURUSD", "XAUUSD"]],
        one_time_keyboard=True,
        resize_keyboard=True
    )

def session_keyboard():
    return ReplyKeyboardMarkup(
        [["Asia", "London"], ["New York", "Pre-Market"]],
        one_time_keyboard=True,
        resize_keyboard=True
    )

def structure_keyboard():
    return ReplyKeyboardMarkup(
        [["Bullish", "Bearish"], ["Ranging / Consolidation"]],
        one_time_keyboard=True,
        resize_keyboard=True
    )

def confirm_keyboard():
    return ReplyKeyboardMarkup(
        [["Yes, Run Analysis", "No, Start Over"]],
        one_time_keyboard=True,
        resize_keyboard=True
    )

# ─────────────────────────────────────────────
# HELPER: BUILD ANALYSIS PROMPT
# ─────────────────────────────────────────────
def build_prompt(data: dict) -> str:
    return f"""
Please provide a full MSNR x ICT Alchemist analysis using the following market input:

PAIR: {data.get('pair', 'Not provided')}
CURRENT SESSION: {data.get('session', 'Not provided')}
CURRENT PRICE (approximate): {data.get('price', 'Not provided')}

--- HIGHER TIMEFRAME STRUCTURE ---
D1 Bias & Structure: {data.get('d1_structure', 'Not provided')}
H4 / H1 Structure & Trend: {data.get('h4h1_structure', 'Not provided')}

--- LIQUIDITY STATUS ---
{data.get('liquidity', 'Not provided')}

--- KEY LEVELS ---
Previous Day / Session Levels: {data.get('key_levels', 'Not provided')}
OC Levels & Zones (Open/Close): {data.get('oc_levels', 'Not provided')}
V&A Levels (Volume & Area): {data.get('va_levels', 'Not provided')}

--- UNDELIVERED PRICE ---
Nearest 30M Undelivered Wick: {data.get('undelivered_wick', 'Not provided')}

Please structure your response exactly as defined in your operating framework.
"""

# ─────────────────────────────────────────────
# CONVERSATION HANDLERS
# ─────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "╔══════════════════════════════╗\n"
        "║  MSNR x ICT ALCHEMIST BOT   ║\n"
        "╚══════════════════════════════╝\n\n"
        "Welcome. This bot provides professional Smart Money narrative analysis "
        "based on ICT concepts combined with MSNR Alchemist methodology.\n\n"
        "This is NOT a signal service. This is a thinking tool for disciplined traders.\n\n"
        "Type /analyze to begin your market analysis.\n"
        "Type /help for guidance.\n"
        "Type /cancel at any time to stop.",
        reply_markup=ReplyKeyboardRemove()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "HOW TO USE THIS BOT\n"
        "───────────────────\n\n"
        "1. Type /analyze to start\n"
        "2. Select your market pair (EURUSD or XAUUSD)\n"
        "3. Select your current trading session\n"
        "4. Enter current approximate price\n"
        "5. Describe D1 structure and bias\n"
        "6. Describe H4/H1 structure and trend\n"
        "7. Describe liquidity status (what is above/below price)\n"
        "8. Enter key levels (PDH, PDL, session highs/lows, RBS/SBR)\n"
        "9. Enter OC levels and zones\n"
        "10. Enter V&A levels\n"
        "11. Enter nearest 30M undelivered wick\n"
        "12. Confirm and receive your analysis\n\n"
        "The more accurate your input, the more precise the narrative.\n\n"
        "Commands:\n"
        "/analyze — Start new analysis\n"
        "/cancel — Cancel current session\n"
        "/help — Show this message"
    )


async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "Analysis session started.\n\n"
        "Step 1 of 11 — Select the market pair:",
        reply_markup=pair_keyboard()
    )
    return PAIR


async def get_pair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pair = update.message.text.strip().upper()
    if pair not in ["EURUSD", "XAUUSD"]:
        await update.message.reply_text(
            "Please select a valid pair from the options.",
            reply_markup=pair_keyboard()
        )
        return PAIR
    context.user_data['pair'] = pair
    await update.message.reply_text(
        f"Pair: {pair}\n\n"
        "Step 2 of 11 — Select the current trading session (UTC+3):",
        reply_markup=session_keyboard()
    )
    return SESSION


async def get_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['session'] = update.message.text.strip()
    await update.message.reply_text(
        f"Session: {context.user_data['session']}\n\n"
        "Step 3 of 11 — Enter the current approximate price:\n\n"
        "Example: 1.08450 for EURUSD or 2345.50 for Gold",
        reply_markup=ReplyKeyboardRemove()
    )
    return CURRENT_PRICE


async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['price'] = update.message.text.strip()
    await update.message.reply_text(
        f"Price noted: {context.user_data['price']}\n\n"
        "Step 4 of 11 — Describe the D1 (Daily) structure and bias:\n\n"
        "Include: overall trend direction, most recent swing high/low, "
        "any confirmed BOS or MSS, whether price is in premium or discount.\n\n"
        "Example: D1 is bullish. Price created a BOS above the last swing high at 2310. "
        "Currently sitting in a discount below the 50% equilibrium of the dealing range.",
        reply_markup=ReplyKeyboardRemove()
    )
    return D1_STRUCTURE


async def get_d1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['d1_structure'] = update.message.text.strip()
    await update.message.reply_text(
        "D1 noted.\n\n"
        "Step 5 of 11 — Describe the H4 and H1 structure and trend:\n\n"
        "Include: current trend on H4, any BOS or MSS on H1, "
        "whether H1 aligns with daily bias or is in a pullback phase.\n\n"
        "Example: H4 shows bullish trend with a recent pullback. H1 created an MSS "
        "to the downside, indicating a potential retracement leg before continuation."
    )
    return H4_H1_STRUCTURE


async def get_h4h1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['h4h1_structure'] = update.message.text.strip()
    await update.message.reply_text(
        "H4/H1 structure noted.\n\n"
        "Step 6 of 11 — Describe the current liquidity status:\n\n"
        "Include: what buy-side liquidity sits above price, what sell-side liquidity "
        "sits below price, whether any significant level was recently swept.\n\n"
        "Example: Buy-side liquidity rests above yesterday's high at 2351. "
        "Sell-side liquidity sits below the Asia low at 2318. "
        "The London session swept the Asia low, taking sell-side before reversing."
    )
    return LIQUIDITY_STATUS


async def get_liquidity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['liquidity'] = update.message.text.strip()
    await update.message.reply_text(
        "Liquidity status noted.\n\n"
        "Step 7 of 11 — Enter key structural levels:\n\n"
        "Include: Previous Day High (PDH), Previous Day Low (PDL), "
        "current session high and low, any RBS or SBR levels visible.\n\n"
        "Example: PDH 2351 / PDL 2318. Asia high 2335 / Asia low 2318. "
        "RBS at 2326 from last Tuesday's breakdown."
    )
    return KEY_LEVELS


async def get_key_levels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['key_levels'] = update.message.text.strip()
    await update.message.reply_text(
        "Key levels noted.\n\n"
        "Step 8 of 11 — Enter MSNR OC Levels and Zones (Open/Close):\n\n"
        "These are the daily, weekly, or monthly open and close levels "
        "that represent areas of institutional interest.\n\n"
        "Example: Monthly open at 2298. Weekly open at 2320. "
        "Daily open at 2328. Previous daily close at 2322."
    )
    return OC_LEVELS


async def get_oc_levels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['oc_levels'] = update.message.text.strip()
    await update.message.reply_text(
        "OC levels noted.\n\n"
        "Step 9 of 11 — Enter MSNR V&A Levels (Volume and Area):\n\n"
        "These are high-volume nodes or significant price areas where "
        "notable institutional activity or delivery occurred.\n\n"
        "Example: V&A zone between 2318 and 2322 — heavy volume delivery "
        "on last Wednesday's drop. Another V&A cluster near 2345."
    )
    return VA_LEVELS


async def get_va_levels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['va_levels'] = update.message.text.strip()
    await update.message.reply_text(
        "V&A levels noted.\n\n"
        "Step 10 of 11 — Enter the nearest 30M undelivered price wick:\n\n"
        "This is a wick on the 30M chart that was printed but not fully "
        "returned to or accepted — representing an obligation for price delivery.\n\n"
        "Example: 30M undelivered wick to the upside at 2348. "
        "This wick was formed yesterday during the New York session and "
        "price has not returned to fill that delivery area."
    )
    return UNDELIVERED_WICK


async def get_undelivered_wick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['undelivered_wick'] = update.message.text.strip()

    # Summary for confirmation
    d = context.user_data
    summary = (
        "INPUT SUMMARY\n"
        "─────────────\n"
        f"Pair: {d.get('pair')}\n"
        f"Session: {d.get('session')}\n"
        f"Price: {d.get('price')}\n"
        f"D1: {d.get('d1_structure')[:60]}...\n"
        f"H4/H1: {d.get('h4h1_structure')[:60]}...\n"
        f"Liquidity: {d.get('liquidity')[:60]}...\n"
        f"Key Levels: {d.get('key_levels')[:60]}...\n"
        f"OC Levels: {d.get('oc_levels')[:60]}...\n"
        f"V&A Levels: {d.get('va_levels')[:60]}...\n"
        f"30M Wick: {d.get('undelivered_wick')[:60]}...\n\n"
        "Step 11 of 11 — Confirm to generate analysis?"
    )
    await update.message.reply_text(summary, reply_markup=confirm_keyboard())
    return CONFIRM


async def confirm_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text.strip()

    if choice == "No, Start Over":
        context.user_data.clear()
        await update.message.reply_text(
            "Session cleared. Type /analyze to begin again.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    await update.message.reply_text(
        "Input received. Running analysis...\n\n"
        "This may take a moment. Please wait.",
        reply_markup=ReplyKeyboardRemove()
    )

    prompt = build_prompt(context.user_data)

    try:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}]
        )
        analysis = response.content[0].text

        # Split long messages for Telegram's 4096 char limit
        max_len = 4000
        if len(analysis) <= max_len:
            await update.message.reply_text(analysis)
        else:
            parts = [analysis[i:i+max_len] for i in range(0, len(analysis), max_len)]
            for i, part in enumerate(parts):
                header = f"[Part {i+1} of {len(parts)}]\n\n" if len(parts) > 1 else ""
                await update.message.reply_text(header + part)

        await update.message.reply_text(
            "─────────────────────────────────\n"
            "Analysis complete.\n\n"
            "Remember: This is a thinking tool, not a signal.\n"
            "The market confirms. You wait. You execute only when all conditions align.\n\n"
            "Type /analyze for a new analysis."
        )

    except Exception as e:
        logger.error(f"API error: {e}")
        await update.message.reply_text(
            "An error occurred while generating the analysis. "
            "Please check your API connection and try again.\n\n"
            "Type /analyze to start a new session."
        )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "Session cancelled. All inputs cleared.\n\n"
        "Type /analyze when you are ready to begin a new analysis.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Command not recognized.\n\n"
        "Type /analyze to start an analysis.\n"
        "Type /help for guidance."
    )

# ─────────────────────────────────────────────
# BOT ENTRY POINT
# ─────────────────────────────────────────────
def main():
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN is missing from .env file")
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY is missing from .env file")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("analyze", analyze)],
        states={
            PAIR: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_pair)],
            SESSION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_session)],
            CURRENT_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_price)],
            D1_STRUCTURE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_d1)],
            H4_H1_STRUCTURE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_h4h1)],
            LIQUIDITY_STATUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_liquidity)],
            KEY_LEVELS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_key_levels)],
            OC_LEVELS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_oc_levels)],
            VA_LEVELS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_va_levels)],
            UNDELIVERED_WICK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_undelivered_wick)],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_analysis)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    logger.info("MSNR x ICT Alchemist Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
