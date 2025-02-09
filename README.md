# 🎁 MysteryBox Telegram Bot

A Telegram bot that distributes mystery prizes to users in a group. The bot manages a daily prize pool and ensures fair distribution of rewards.

## ✨ Features

- 🎯 Daily prize distribution system
- 🔒 One prize per user
- ⏰ Automatic daily reset (Lebanon timezone)
- 🎫 Secure token-based prize claiming
- 📊 Winner tracking and management

## 🚀 Setup

1. Install required dependencies:
```bash
pip install python-telegram-bot pytz
```

2. Configure the bot:
- Set your bot token in `mysterybox.py`
- Configure admin ID and group settings
- Customize prize pool if needed

## 💻 Commands

- `/start_mmb` - Initialize bot in a group
- `/send_mmb` - Send a new mystery box link
- `/winners_mmb` - View current winners
- `/reset_mmb` - Reset all prizes and clicks
- `/restart_mmb` - Restart the bot
- `/test_mmb` - Check bot status
- `/help_mmb` - Show help message

## 🔐 Security Features

- Token-based prize verification
- Anti-duplicate claiming system
- Admin-only command restrictions

## 🌐 Prize Distribution

- Maximum 10 winners per day
- Prizes reset at midnight (Lebanon time)
- Random prize selection from pool
- Secure claim verification system

## 📝 Notes

- All commands are admin-only
- Bot must be added to a group to function
- Links are one-time use only
- Prizes are distributed on a first-come, first-served basis

## 🤝 Contributing

Feel free to submit issues and enhancement requests! 