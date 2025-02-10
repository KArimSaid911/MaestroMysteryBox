import secrets
import logging
from datetime import datetime, time
import pytz
import random
import sys
from telegram import Update, Chat
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, JobQueue
from telegram.error import TelegramError

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
available_prizes = []  # List of prizes still available today
users_clicked = set()  # Track users who clicked the link
user_prizes = {}  # Store user_id: {"prize": prize, "token": token, "claimed": False}

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
    await update.message.reply_text("MysteryBox Bot activated! Use /send_mmb to send links manually.")

async def send_mmb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manually send a mystery box link."""
    if not await check_admin(update):
        return

    if not GROUP_ID:
        await update.message.reply_text("Please use /start_mmb in a group first!")
        return

    try:
        if len(users_clicked) < MAX_WINNERS and available_prizes:
            prize = random.choice(available_prizes)
            available_prizes.remove(prize)
            token = generate_url_token()
            link = f"https://karimsaid911.github.io/MaestroMysteryBox/#t={token}"
            message = """🎁 New Mystery Box Available!

🎯 Click to Open Mystery Box:
{link}""".format(link=link)
            
            # Store the token and prize for later verification
            user_prizes[token] = {
                "prize": prize,
                "claimed": False,
                "user_id": None
            }
            
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
        winners_text = """🏆 <b>Recent Winners:</b>

"""
        if winners:
            for user_id, data in winners.items():
                winners_text += f"👤 <b>{data['username']}</b>\n"
                winners_text += f"🎁 {data['prize']}\n"
                winners_text += f"🕒 {data['date']}\n\n"
        else:
            winners_text += "No winners yet.\n"

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
        user_prizes.clear()  # Clear user prizes dictionary
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
        user_prizes.clear()  # Clear user prizes dictionary
        available_prizes.extend(PRIZES)
        random.shuffle(available_prizes)
        
        # Reinitialize job queue
        if context.job_queue:
            context.job_queue.stop()
            context.job_queue.start()
            
        await update.message.reply_text("✅ Bot has been restarted successfully!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error restarting bot: {e}")

async def send_prize_link(context: ContextTypes.DEFAULT_TYPE):
    """Send the prize link to all group members."""
    if not GROUP_ID:
        return

    # Check if current time is between 10 PM and 3 AM Lebanon time
    lebanon_tz = pytz.timezone('Asia/Beirut')
    current_time = datetime.now(lebanon_tz)
    
    # Only send between 10 PM (22:00) and 3 AM (03:00)
    current_hour = current_time.hour
    if not (current_hour >= 22 or current_hour < 6):
        return

    try:
        # Only send the link if there are still spots for users
        if len(users_clicked) < MAX_WINNERS:
            # Randomly select a prize
            if available_prizes:
                prize = random.choice(available_prizes)
                available_prizes.remove(prize)
                token = generate_url_token()
                
                # Check if user has already claimed a prize
                user_id = context.user_data.get('user_id')
                if user_id in user_prizes and user_prizes[user_id].get('claimed', False):
                    link = f"https://karimsaid911.github.io/MaestroMysteryBox/#error=already-claimed"
                else:
                    link = f"https://karimsaid911.github.io/MaestroMysteryBox/#prize={prize.replace(' ', '%20')}&token={token}"
                    if user_id:
                        user_prizes[user_id] = {
                            "prize": prize,
                            "token": token,
                            "claimed": True,
                            "date": current_time.strftime("%Y-%m-%d %H:%M:%S")
                        }

                message = f"<a href='{link}'>MeastroMysterybox</a>"
                
                try:
                    await context.bot.send_message(
                        chat_id=GROUP_ID,
                        text=message,
                        parse_mode="HTML",
                        disable_web_page_preview=True
                    )
                except TelegramError as e:
                    logger.error(f"Failed to send to group {GROUP_ID}: {e}")

    except Exception as e:
        logger.error(f"Error in send_prize_link: {e}")

async def reset_daily_users(context: ContextTypes.DEFAULT_TYPE):
    """Reset the winners list, available prizes, and users who clicked the link for a new day."""
    winners.clear()
    available_prizes.clear()
    users_clicked.clear()
    user_prizes.clear()  # Clear user prizes dictionary
    available_prizes.extend(PRIZES)
    random.shuffle(available_prizes)
    logger.info("Reset winners list, shuffled prizes, and cleared clicked users for new day")

async def help_mmb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message with all available commands."""
    help_text = """🤖 Available Commands:

/start_mmb - Start the bot
/help_mmb - Show this help message
/send_mmb - Send a new mystery box
/winners_mmb - View current winners
/reset_mmb - Reset clicks back to 10
/test_mmb - Check remaining clicks
/restart_mmb - Restart the bot

Note: All commands are admin-only"""

    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)

async def test_mmb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check remaining clicks."""
    if not await check_admin(update):
        return

    try:
        remaining_clicks = MAX_WINNERS - len(users_clicked)
        total_winners = len(winners)
        
        status_text = """📊 Bot Status:

🎯 Remaining Clicks: {remaining}
🏆 Total Winners: {total}
✅ Bot Active: Yes""".format(remaining=remaining_clicks, total=total_winners)

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

        # Set up job queue
        if application.job_queue:
            # Initialize available prizes
            available_prizes.extend(PRIZES)
            random.shuffle(available_prizes)

            # Send prize link once per day between 2 PM and 6 PM Lebanon time
            lebanon_tz = pytz.timezone('Asia/Beirut')
            
            # Calculate a random hour between 14 (2 PM) and 17 (6 PM)
            random_hour = random.randint(14, 17)
            random_minute = random.randint(0, 59)
            
            # Create a time object for the scheduled time
            scheduled_time = time(hour=random_hour, minute=random_minute)
            
            # Schedule the job to run daily at the random time
            application.job_queue.run_daily(
                send_prize_link,
                time=scheduled_time.replace(tzinfo=lebanon_tz),
                days=(0, 1, 2, 3, 4, 5, 6)  # Run every day
            )

            # Schedule reset at midnight Lebanon time
            lebanon_tz = pytz.timezone('Asia/Beirut')
            midnight = time(0, 0, tzinfo=lebanon_tz)
            application.job_queue.run_daily(
                reset_daily_users,
                time=midnight
            )

            logger.info("Bot started! Ready to send prize links between 10 PM and 3 AM Lebanon time")

        # Start the bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 