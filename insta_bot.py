
import os
import re
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN") or "7734188960:AAGObwsdTNUtocyHzxLLwjHYVDI1QtbY4xU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Welcome {update.effective_user.first_name}!
I'm your Insta Reset Bot. Use /reset@username or /reset email to send a reset link.")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    match = re.search(r"/reset[@"]?([\w.@]+)", text)
    if not match:
        await update.message.reply_text("❌ Invalid format. Use `/reset@username` or `/reset email@example.com`", parse_mode="Markdown")
        return

    target = match.group(1)
    url = "https://www.instagram.com/accounts/account_recovery_send_ajax/"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "X-CSRFToken": "missing",
        "X-Requested-With": "XMLHttpRequest"
    }
    data = {
        "email_or_username": target,
        "recaptcha_challenge_field": ""
    }
    try:
        r = requests.post(url, headers=headers, data=data)
        if r.status_code == 200 and "status" in r.json() and r.json()["status"] == "ok":
            await update.message.reply_text(f"✅ Reset link sent to **{target}**!", parse_mode="Markdown")
        else:
            await update.message.reply_text(f"❌ *Invalid Instagram account.* `{target}` doesn't exist.", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text("⚠️ An error occurred while processing your request.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    print("Bot is running...")
    app.run_polling()
