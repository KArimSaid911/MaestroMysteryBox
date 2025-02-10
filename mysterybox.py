import os
import secrets
import logging
import json
from datetime import datetime, time
import pytz
import random
import sys
from telegram import Update, Chat
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, JobQueue
from telegram.error import TelegramError

# Load environment variables (ensure you set BOT_TOKEN in your environment)
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("Error: BOT_TOKEN is missing. Set it as an environment variable.")
    sys.exit(1)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def generate_url_token(length=16):
    """Generates a secure random URL-safe token."""
    return secrets.token_urlsafe(length)

# Constants
MAX_WINNERS = 10
LEBANON_TIMEZONE = pytz.timezone("Asia/Beirut")
ADMIN_ID = 6923408088  # Admin Telegram ID
GROUP_ID_FILE = "group_id.json"  # Store the group ID persistently

# Prize pool
PRIZES = [
    "1 Maestro premium account for 1 month",
    "2 Maestro premium accounts for 1 week",
    "3 Maestro premium accounts for 1 week",
    "4 Maestro premium accounts for 1 week",
    "5 Maestro premium accounts for 1 week",
    "6 Maestro premium accounts for 1 week",
    "7 Maestro premium accounts for 3 days",
    "8 Maestro premium accounts for 3 days",
    "9 Maestro premium accounts for 1 day",
    "10 Maestro premium accounts for 1 day",
]

# Storage for winners, prizes, and link usage tracking
winners = {}  # Stores winner info
available_prizes = PRIZES[:]  # List of prizes available
users_clicked = set()  # Tracks users who clicked the link
user_prizes = {}  # Stores user_id: {"prize": prize, "token": token, "claimed": False}

def load_group_id():
    """Loads the group ID from a file (if exists)."""
    if os.path.exists(GROUP_ID_FILE):
        with open(GROUP_ID_FILE, "r") as file:
            return json.load(file).get("group_id")
    return None

def save_group_id(group_id):
    """Saves the group ID to a file."""
    with open(GROUP_ID_FILE, "w") as file:
        json.dump({"group_id": group_id}, file)

GROUP_ID = load_group_id()

async def check_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check if the user is the admin."""
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text(
            f"🚫 Only the admin can use this command. Your ID: {user_id}"
        )
        return False
    return True

async def start_mmb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the bot and save the group ID."""
    global GROUP_ID

    if not await check_admin(update, context):
        return

    if update.effective_chat.type not in [Chat.GROUP, Chat.SUPERGROUP]:
        await update.message.reply_text("📌 Please add me to a group and use /start_mmb there!")
        return

    GROUP_ID = update.effective_chat.id
    save_group_id(GROUP_ID)
    await update.message.reply_text("✅ MysteryBox Bot activated! Use /send_mmb to send links manually.")

async def send_mmb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a mystery box link manually."""
    if not await check_admin(update, context):
        return

    if not GROUP_ID:
        await update.message.reply_text("⚠️ Please use /start_mmb in a group first!")
        return

    try:
        if len(users_clicked) < MAX_WINNERS and available_prizes:
            prize = random.choice(available_prizes)
            available_prizes.remove(prize)
            token = generate_url_token()
            link = f"https://karimsaid911.github.io/MaestroMysteryBox/#t={token}"

            user_prizes[token] = {
                "prize": prize,
                "claimed": False,
                "user_id": None,
            }

            message = f"""🎁 New Mystery Box Available!
            
🎯 <a href="{link}">Click to Open Mystery Box</a>"""

            await context.bot.send_message(
                chat_id=GROUP_ID, text=message, parse_mode=ParseMode.HTML, disable_web_page_preview=True
            )
        else:
            await update.message.reply_text("❌ No more prizes available today!")
    except Exception as e:
        logger.error(f"Error sending prize link: {e}")

async def winners_mmb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show recent winners."""
    if not await check_admin(update, context):
        return

    winners_text = "🏆 <b>Recent Winners:</b>\n\n"
    if winners:
        for user_id, data in winners.items():
            winners_text += f"👤 <b>{data['username']}</b>\n🎁 {data['prize']}\n🕒 {data['date']}\n\n"
    else:
        winners_text += "No winners yet.\n"

    await update.message.reply_text(winners_text, parse_mode=ParseMode.HTML)

async def reset_mmb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reset winners and prize availability."""
    if not await check_admin(update, context):
        return

    winners.clear()
    available_prizes[:] = PRIZES
    users_clicked.clear()
    user_prizes.clear()
    await update.message.reply_text("✅ All winners and clicks have been reset!")

async def restart_mmb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Restart the bot without stopping the job queue."""
    if not await check_admin(update, context):
        return

    winners.clear()
    available_prizes[:] = PRIZES
    users_clicked.clear()
    user_prizes.clear()
    await update.message.reply_text("✅ Bot has been restarted successfully!")

async def help_mmb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message."""
    help_text = """🤖 Available Commands:

/start_mmb - Activate the bot
/help_mmb - Show this help message
/send_mmb - Send a new mystery box
/winners_mmb - View recent winners
/reset_mmb - Reset winners and clicks
/restart_mmb - Restart the bot

Note: All commands are admin-only."""
    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)

def main():
    """Start the bot."""
    try:
        application = Application.builder().token(BOT_TOKEN).build()

        application.add_handler(CommandHandler("start_mmb", start_mmb))
        application.add_handler(CommandHandler("send_mmb", send_mmb))
        application.add_handler(CommandHandler("winners_mmb", winners_mmb))
        application.add_handler(CommandHandler("reset_mmb", reset_mmb))
        application.add_handler(CommandHandler("restart_mmb", restart_mmb))
        application.add_handler(CommandHandler("help_mmb", help_mmb))

        application.run_polling()
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
