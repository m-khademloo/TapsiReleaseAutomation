import os

from dotenv import load_dotenv
from loguru import logger
from telegram.ext import ApplicationBuilder, CommandHandler

from db.mongo import MongoDB

load_dotenv()
TOKEN = os.getenv("TelegramToken")

from telegram import Update
from telegram.ext import ContextTypes

async def whoami_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user:
        username = user.username or "N/A"
        telegram_id = user.id
        response = f"Username: `{username}`\nid: `{telegram_id}`"
    else:
        response = "Unable to retrieve user info."

    await update.message.reply_text(response, parse_mode="Markdown")

async def next_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) >= 2:
        version = context.args[0]
        date = context.args[1]
        logger.info(f"/next command received with version={version} and date={date}")
        await update.message.reply_text(f"Scheduled version {version} for {date}")
    else:
        await update.message.reply_text("Usage: /next <version> <date>")

async def register_team_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        team = context.args[0]
        logger.info(f"/register_team command received for team={team}")
        await update.message.reply_text(f"Team {team} registered")
    else:
        await update.message.reply_text("Usage: /register_team <team>")

async def register_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) >= 2:
        name = context.args[0]
        team = context.args[1]
        logger.info(f"/register command received for name={name}, team={team}")
        await update.message.reply_text(f"{name} registered to team {team}")
    else:
        await update.message.reply_text("Usage: /register <name> <team>")

async def qa_approve_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("/qa_approve command received")
    await update.message.reply_text("QA approved")

async def register_member_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 4:
        await update.message.reply_text(
            "Usage: /register_member <name> <team> <telegram_username> <telegram_id>"
        )
        return

    name = context.args[0]
    team = context.args[1].lower()
    telegram_username = context.args[2]
    telegram_id_str = context.args[3]

    try:
        telegram_id = int(telegram_id_str)
    except ValueError:
        await update.message.reply_text("Error: telegram_id must be a number.")
        return

    db = MongoDB()

    try:
        await db.register_member(
            telegram_id=telegram_id,
            telegram_username=telegram_username,
            name=name,
            team=team
        )
        await update.message.reply_text(
            f"✅ Registered `{name}` to team `{team}`",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(str(e))


if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("whoami", whoami_handler))
    app.add_handler(CommandHandler("next", next_handler))
    app.add_handler(CommandHandler("register_team", register_team_handler))
    app.add_handler(CommandHandler("register", register_handler))
    app.add_handler(CommandHandler("qa_approve", qa_approve_handler))
    app.add_handler(CommandHandler("register_member", register_member_handler))

    logger.info("Bot is starting...")
    app.run_polling()
