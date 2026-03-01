MSNR x ICT ALCHEMIST — TELEGRAM BOT
Complete Setup & Usage Guide
WHAT THIS BOT DOES
This bot provides professional Smart Money narrative analysis based on:
ICT (Inner Circle Trader) concepts
MSNR Alchemist methodology
Top-down analysis: D1 → H4/H1 → 5M execution framework
It is NOT a signal bot. It is a thinking tool that helps traders understand
market narrative through liquidity, structure, and price delivery logic.
FILES IN THIS PROJECT
forex_bot/
├── bot.py            ← The main bot code (everything is here)
├── requirements.txt  ← Python libraries needed
├── .env.example      ← Template for your secret keys
├── .gitignore        ← Prevents secret files from being shared
└── README.md         ← This guide
STEP-BY-STEP SETUP
STEP 1 — INSTALL PYTHON
You need Python 3.10 or higher.
Check if you have it:
python --version
If not installed, download from: https://www.python.org/downloads/
STEP 2 — GET YOUR TELEGRAM BOT TOKEN
Open Telegram and search for: @BotFather
Send the message: /newbot
BotFather will ask for a name → Enter any name you like
Example: MSNR Analyst
BotFather will ask for a username → Must end in "bot"
Example: msnr_ict_analyst_bot
BotFather will give you a TOKEN that looks like this:
7123456789:AAFxxxxxxxxxxxxxxxxxxxxxxxx
COPY and SAVE this token. You will need it in Step 5.
STEP 3 — GET YOUR ANTHROPIC API KEY
Go to: https://console.anthropic.com
Sign up or log in
Click on "API Keys" in the left menu
Click "Create Key"
Give it a name (example: forex-bot)
COPY the key. It looks like: sk-ant-api03-xxxxxxxxxxxxxxxx
SAVE it. You will need it in Step 5.
NOTE: Anthropic API requires a paid account for production use.
You can add credit at: https://console.anthropic.com/settings/billing
STEP 4 — DOWNLOAD THE BOT FILES
Option A — If you received the files directly:
Just place all files into a folder on your computer.
Example folder: C:\Users\YourName\forex_bot (Windows)
or /home/yourname/forex_bot (Mac/Linux)
Option B — If using Git:
git clone [your-repo-url]
cd forex_bot
STEP 5 — CREATE YOUR .env FILE
Find the file called: .env.example
Make a COPY of it in the same folder
Rename the copy to exactly: .env  (remove the word "example")
Open .env with any text editor (Notepad, VS Code, etc.)
Replace the placeholder values with your real keys:
TELEGRAM_TOKEN=7123456789:AAFxxxxxxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxx
Save the file.
IMPORTANT: Never share your .env file with anyone.
IMPORTANT: The file must be named exactly ".env" — not ".env.txt"
STEP 6 — INSTALL REQUIRED LIBRARIES
Open your terminal (Command Prompt on Windows, Terminal on Mac/Linux).
Navigate to your project folder:
cd path/to/forex_bot
Install a virtual environment (recommended):
python -m venv venv
Activate the virtual environment:
Windows:   venv\Scripts\activate
Mac/Linux: source venv/bin/activate
Install the required libraries:
pip install -r requirements.txt
Wait for installation to complete. This may take 1-2 minutes.
STEP 7 — RUN THE BOT
Make sure you are in the forex_bot folder with your virtual environment active.
Run:
python bot.py
You should see:
MSNR x ICT Alchemist Bot is running...
The bot is now live. Do NOT close this terminal window while using the bot.
STEP 8 — OPEN YOUR BOT ON TELEGRAM
Open Telegram
Search for your bot by the username you created in Step 2
Click on it
Press "Start" or type /start
The bot will greet you and explain how to use it
HOW TO USE THE BOT
Commands:
/start   → Welcome message
/analyze → Begin a new analysis session
/help    → Show usage instructions
/cancel  → Cancel current session at any time
Analysis Flow (11 Steps):
When you type /analyze, the bot will guide you through:
Select pair: EURUSD or XAUUSD
Select session: Asia / London / New York / Pre-Market
Enter current price (approximate)
Describe D1 structure (bias, trend, BOS/MSS on daily)
Describe H4/H1 structure (trend, alignment with D1, any MSS)
Describe liquidity status (what is above and below price, any sweeps)
Enter key levels (PDH, PDL, session highs/lows, RBS/SBR)
Enter OC levels and zones (daily/weekly/monthly open and close)
Enter V&A levels (volume and area zones)
Enter nearest 30M undelivered wick
Confirm and receive full narrative analysis
Input Quality = Output Quality
The more specific and accurate your inputs, the more precise the analysis.
Do not rush through inputs. Take time to describe what you actually see on the chart.
ANALYSIS OUTPUT STRUCTURE
Every analysis follows this exact structure:
Market & Session Context
Higher Timeframe Narrative (D1 → H4)
Liquidity Story (what was taken, what remains)
Current Structure (BOS / MSS / Range)
Scenario-Based Outlook (IF-THEN logic)
Risk & Patience Reminder
KEEPING THE BOT RUNNING 24/7
Running bot.py on your personal computer means the bot stops when you close
your computer. For continuous operation, consider these options:
Option A — Free Cloud Hosting (Railway.app)
Go to: https://railway.app
Sign up with GitHub
Create a new project
Upload your code (without the .env file)
Add your environment variables in Railway's settings panel
Deploy
Option B — VPS (Virtual Private Server)
Get a cheap VPS from DigitalOcean, Vultr, or Hetzner
Upload your files via SSH or FTP
Install Python and run the bot using a process manager like:
pip install pm2
pm2 start bot.py --interpreter python3
pm2 save
pm2 startup
Option C — Render.com (Free Tier Available)
Go to: https://render.com
Create a new Web Service
Connect your GitHub repository
Set environment variables in the dashboard
Deploy
TROUBLESHOOTING
Bot not responding:
Make sure the terminal running bot.py is still open
Check that your TELEGRAM_TOKEN in .env is correct
Try sending /start again
"TELEGRAM_TOKEN is missing" error:
Make sure your file is named ".env" not ".env.example"
Make sure the .env file is in the same folder as bot.py
"API error" during analysis:
Check your ANTHROPIC_API_KEY is correct
Check your Anthropic account has available credit
Visit: https://console.anthropic.com/settings/billing
Library not found errors:
Make sure you ran: pip install -r requirements.txt
Make sure your virtual environment is activated
IMPORTANT DISCLAIMER
This bot is a MARKET NARRATIVE TOOL only.
It does not provide:
Buy or sell signals
Exact entry prices
Stop-loss or take-profit prices
Guaranteed outcomes
It is designed to help traders THINK correctly using Smart Money Concepts.
All trading decisions are entirely your own responsibility.
Trading forex and commodities involves significant risk of loss.
Only risk capital you can afford to lose.
SUPPORT & UPDATES
If you want to expand the bot, possible upgrades include:
Adding a /history command to save past analyses
Adding a /journal command to log trade notes
Adding multi-user support with session isolation
Adding a webhook-based deployment for faster response
Built on: MSNR Alchemist x ICT Framework
Timezone: UTC+3 (Addis Ababa, Ethiopia)
Markets: EURUSD, XAUUSD
