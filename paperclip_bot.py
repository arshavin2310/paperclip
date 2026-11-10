import os
import subprocess
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Mengambil token secara aman dari Environment GitHub Secrets atau menggunakan token langsung
TOKEN = os.getenv("TELEGRAM_TOKEN", "9092798479:AAG7VoZHuDzqDHpPlc7gKj_k4WkXQk-cz54")

# Tombol menu interaktif di Telegram
async def start(update: Update, context: ContextTypes.DefaultContext):
    keyboard = [
        ["📂 Cek Status Repo", "📋 Lihat Struktur File"],
        ["🚀 Panduan Cepat", "❓ Bantuan"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Halo! Bot Paperclip Anda siap digunakan.\n"
        "Pilih menu di bawah ini atau ketik perintah untuk mulai mengeksplorasi repo:",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DefaultContext):
    text = update.message.text

    if text == "📂 Cek Status Repo":
        await update.message.reply_text("🔍 Memeriksa status repositori Paperclip...")
        if os.path.exists(".git"):
            result = subprocess.run(["git", "status"], capture_output=True, text=True)
            output = result.stdout if result.stdout else "Repo bersih."
        else:
            output = "Direktori git tidak ditemukan di lingkungan ini."
        await update.message.reply_text(f"```\n{output}\n```", parse_mode="Markdown")

    elif text == "📋 Lihat Struktur File":
        await update.message.reply_text("📂 Mengambil daftar file utama...")
        files = os.listdir(".")
        # Ambil 15 file/folder pertama agar tidak kepanjangan
        file_list = "\n".join(files[:15])
        await update.message.reply_text(f"Daftar file di repo:\n```\n{file_list}\n```", parse_mode="Markdown")

    elif text == "🚀 Panduan Cepat":
        guide = (
            "📌 **Paperclip Quickstart Guide**:\n\n"
            "Paperclip adalah aplikasi untuk mengelola tim agen AI untuk pekerjaan.\n"
            "Silakan cek file README.md di repo Anda untuk instruksi lengkapnya."
        )
        await update.message.reply_text(guide, parse_mode="Markdown")

    else:
        await update.message.reply_text(f"Pesan diterima: '{text}'. Ketik atau pilih menu yang tersedia!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot Telegram Paperclip sedang berjalan...")
    app.run_polling()
