import secrets
import logging
import urllib.parse
from datetime import datetime, time
import pytz
import random
import sys
import os
import subprocess
from telegram import Update, Chat
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, JobQueue
from telegram.error import TelegramError
import base64

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def generate_url_token(length=16):
    """Generates a secure random URL-safe token."""
    return secrets.token_urlsafe(length)

# Bot token
BOT_TOKEN = "7920715621:AAFwnwCN9p-C0hVfIjTH4L0wCMJSxzeuqPc"

# Constants
MAX_WINNERS = 10
LEBANON_TIMEZONE = pytz.timezone('Asia/Beirut')
ADMIN_ID = 6923408088  # Updated admin ID
GROUP_ID = None  # Will store the group ID when admin uses /start

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
    "10 Maestro premium accounts for 1 day"
]

# Store winners, prizes, and users who clicked the link
winners = {}  # Store winner IDs and their prizes with dates
used_tokens = set()  # Prevent token reuse
available_prizes = PRIZES.copy()  # List of prizes still available today
users_clicked = set()  # Track users who clicked the link

async def check_admin(update: Update) -> bool:
    """Check if the user is admin."""
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text(f"Sorry, only the admin can use this command. Your ID: {user_id}")
        return False
    return True

async def start_mmb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command for the bot."""
    global GROUP_ID

    if not await check_admin(update):
        return

    chat_type = update.effective_chat.type
    if chat_type not in [Chat.GROUP, Chat.SUPERGROUP]:
        await update.message.reply_text("Please add me to a group and use /start_mmb there!")
        return

    GROUP_ID = update.effective_chat.id
    
    # Initialize prizes if empty
    if not available_prizes:
        available_prizes.extend(PRIZES)
        random.shuffle(available_prizes)
        logger.info(f"Prizes initialized: {available_prizes}")
    
    await update.message.reply_text("MysteryBox Bot activated! Use /send_mmb to send links manually.")

async def send_mmb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manually send a mystery box link."""
    if not await check_admin(update):
        return

    if not GROUP_ID:
        await update.message.reply_text("Please use /start_mmb in a group first!")
        return

    try:
        user = update.effective_user
        user_id = user.id

        # Check if the user has already won
        if user_id in winners:
            await update.message.reply_text(
                "❌ Oops, frens! You already hit the jackpot once, no double dipping! 🎰"
            )
            return  # Stop execution here

        # Select a prize
        if len(users_clicked) < MAX_WINNERS and available_prizes:
            prize = random.choice(available_prizes)
            available_prizes.remove(prize)

            token = secrets.token_hex(16)  # Unique token per user

            current_time = datetime.now(LEBANON_TIMEZONE)

            # Store winner details
            winners[user_id] = {
                'username': user.username or user.first_name,
                'prize': prize,
                'token': token,  # Store the token to prevent reuse
                'date': current_time.strftime('%Y-%m-%d %H:%M:%S')
            }
            users_clicked.add(user_id)

            # Encode prize & token for URL
            encoded_prize = urllib.parse.quote(prize, safe='')
            encoded_token = urllib.parse.quote(token, safe='')

            # Generate link with token
            link = f"https://karimsaid911.github.io/MaestroMysteryBox/index.html?prize={encoded_prize}&t={encoded_token}"

            message = f"""🎁 New Mystery Box Available!

🎯 <a href="{link}">MaestroMysteryBox</a>"""

            await context.bot.send_message(
                chat_id=GROUP_ID,
                text=message,
                parse_mode="HTML",
                disable_web_page_preview=True
            )
        else:
            await update.message.reply_text("❌ No more prizes available for today!")
    except Exception as e:
        await update.message.reply_text(f"Error sending prize link: {e}")

async def winners_mmb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show current winners and remaining clicks."""
    if not await check_admin(update):
        return

    try:
        winners_text = """🏆 Recent Winners:"""
        
        if winners:
            for user_id, data in winners.items():
                winners_text += f"""
👤 {data['username']}
🎁 {data['prize']}
🕒 {data['date']}"""
        else:
            winners_text += "\nNo winners yet."

        await update.message.reply_text(winners_text, parse_mode=ParseMode.HTML)
    except Exception as e:
        await update.message.reply_text(f"Error showing winners: {e}")

async def reset_mmb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reset all winners and clicks."""
    if not await check_admin(update):
        return

    try:
        winners.clear()
        available_prizes.clear()
        users_clicked.clear()
        used_tokens.clear()  # Clear token storage
        available_prizes.extend(PRIZES)
        random.shuffle(available_prizes)
        await update.message.reply_text("✅ All winners and clicks have been reset!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error resetting bot: {e}")

async def restart_mmb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Restart the bot instantly."""
    if not await check_admin(update):
        return

    try:
        await update.message.reply_text("🔄 Restarting bot...")
        
        # Reset all states
        winners.clear()
        available_prizes.clear()
        users_clicked.clear()
        used_tokens.clear()  # Clear token storage
        available_prizes.extend(PRIZES)
        random.shuffle(available_prizes)
        
        # Get the path to the current script
        script_path = os.path.abspath(__file__)
        
        # Start a new instance of the bot
        subprocess.Popen([sys.executable, script_path])
        
        # Send confirmation and exit current instance
        await update.message.reply_text("✅ Bot has been restarted successfully! New instance is starting...")
        sys.exit(0)
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error restarting bot: {e}")

async def send_prize_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send the prize link, ensuring users cannot claim more than once."""
    if not GROUP_ID:
        await update.message.reply_text("Please use /start_mmb in a group first!")
        return

    try:
        user = update.effective_user
        user_id = user.id

        # 🛑 Check if the user has already won
        if user_id in winners:
            await update.message.reply_text("❌ Oops, frens! You already hit the jackpot once, no double dipping! 🎰")
            return  # Stop execution immediately

        # ✅ Select a prize if available
        if len(users_clicked) < MAX_WINNERS and available_prizes:
            prize = random.choice(available_prizes)
            available_prizes.remove(prize)

            token = secrets.token_hex(16)  # Generate a unique token
            used_tokens.add(token)  # Store token to prevent reuse

            current_time = datetime.now(LEBANON_TIMEZONE)

            # 🏆 Store winner details (PLACE IT HERE!)
            winners[user_id] = {
                'username': user.username or user.first_name,
                'prize': prize,
                'token': token,  # Store the token to prevent reuse
                'date': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                'claimed': False  # Add this flag
            }
            users_clicked.add(user_id)

            # 🎯 Encode prize & token for URL
            claim_status = "unclaimed"  # Default status for new prizes
            encoded_prize = urllib.parse.quote(prize, safe='')
            encoded_token = urllib.parse.quote(token, safe='')

            # 📢 Generate link with token
            link = f"https://karimsaid911.github.io/MaestroMysteryBox/index.html?prize={encoded_prize}&t={encoded_token}"

            message = f"""🎁 New Mystery Box Available!

🎯 <a href="{link}">MaestroMysteryBox</a>"""

            await update.message.reply_text(message, parse_mode="HTML", disable_web_page_preview=True)
        else:
            await update.message.reply_text("❌ No more prizes available for today!")

    except Exception as e:
        await update.message.reply_text(f"Error sending prize link: {e}")

async def reset_daily_users(context: ContextTypes.DEFAULT_TYPE):
    """Reset the winners list, available prizes, and users who clicked the link for a new day."""
    winners.clear()
    available_prizes.clear()
    users_clicked.clear()
    used_tokens.clear()  # Clear token storage
    available_prizes.extend(PRIZES)
    random.shuffle(available_prizes)
    logger.info("🔄 Reset winners list, shuffled prizes, and cleared clicked users for new day")

async def help_mmb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message with all available commands."""
    help_text = """🤖 Available Commands:

/start_mmb - Start the bot in a group
/send_mmb - Send a new mystery box link
/winners_mmb - View current winners
/reset_mmb - Reset all prizes and clicks
/restart_mmb - Restart the bot
/test_mmb - Check bot status
/help_mmb - Show this help message

Note: All commands are admin-only."""

    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)

async def test_mmb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check bot status."""
    if not await check_admin(update):
        return

    try:
        remaining_clicks = MAX_WINNERS - len(users_clicked)
        total_winners = len(winners)
        prizes_left = len(available_prizes)
        
        status_text = f"""📊 Bot Status:

🎯 Remaining Clicks: {remaining_clicks}
🎁 Available Prizes: {prizes_left}
🏆 Total Winners: {total_winners}
✅ Bot Active: Yes
⏰ Current Time (Lebanon): {datetime.now(LEBANON_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')}"""

        await update.message.reply_text(status_text, parse_mode=ParseMode.HTML)
    except Exception as e:
        await update.message.reply_text(f"❌ Error checking status: {e}")

def main():
    """Start the bot."""
    try:
        # Initialize the bot
        application = Application.builder().token(BOT_TOKEN).build()

        # Add command handlers
        application.add_handler(CommandHandler("start_mmb", start_mmb))
        application.add_handler(CommandHandler("send_mmb", send_mmb))
        application.add_handler(CommandHandler("winners_mmb", winners_mmb))
        application.add_handler(CommandHandler("reset_mmb", reset_mmb))
        application.add_handler(CommandHandler("restart_mmb", restart_mmb))
        application.add_handler(CommandHandler("help_mmb", help_mmb))
        application.add_handler(CommandHandler("test_mmb", test_mmb))
        application.add_handler(CommandHandler("send_prize_link", send_prize_link))

        # Set up job queue
        if application.job_queue:
            # Initialize available prizes
            available_prizes.extend(PRIZES)
            random.shuffle(available_prizes)

            # Schedule daily reset at midnight Lebanon time
            lebanon_tz = pytz.timezone('Asia/Beirut')
            midnight = time(0, 0, tzinfo=lebanon_tz)
            application.job_queue.run_daily(
                reset_daily_users,
                time=midnight
            )

            logger.info("Bot started! Ready to send prize links.")

        # Start the bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 