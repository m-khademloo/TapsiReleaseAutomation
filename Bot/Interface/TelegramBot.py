import os
from dotenv import load_dotenv
from loguru import logger
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv("TelegramToken")

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

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("next", next_handler))
    app.add_handler(CommandHandler("register_team", register_team_handler))
    app.add_handler(CommandHandler("register", register_handler))
    app.add_handler(CommandHandler("qa_approve", qa_approve_handler))

    logger.info("Bot is starting...")
    app.run_polling()
