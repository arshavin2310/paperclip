import os
import subprocess
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Token Telegram Anda
TOKEN = "9092798479:AAG7VoZHuDzqDHpPlc7gKj_k4WkXQk-cz54"

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
    chat_id = update.effective_chat.id

    if text == "📂 Cek Status Repo":
        await update.message.reply_text("🔍 Memeriksa status repositori Paperclip...")
        # Simulasi atau cek status folder lokal jika repo sudah di-clone
        if os.path.exists("paperclip"):
            result = subprocess.run(["git", "-C", "paperclip", "status"], capture_output=True, text=True)
            output = result.stdout if result.stdout else "Repo bersih."
        else:
            output = "Folder repo 'paperclip' belum di-clone di direktori bot ini."
        await update.message.reply_text(f"```\n{output}\n```", parse_mode="Markdown")

    elif text == "📋 Lihat Struktur File":
        await update.message.reply_text("📂 Mengambil daftar file utama...")
        target_dir = "paperclip" if os.path.exists("paperclip") else "."
        files = os.listdir(target_dir)
        # Ambil 15 file/folder pertama agar tidak kepanjangan
        file_list = "\n".join(files[:15])
        await update.message.reply_text(f"Daftar file di repo:\n```\n{file_list}\n```", parse_mode="Markdown")

    elif text == "🚀 Panduan Cepat":
        guide = (
            "📌 **Paperclip Quickstart Guide**[span_1](start_span)[span_1](end_span):\n\n"
            "Paperclip adalah aplikasi untuk mengelola tim agen AI untuk pekerjaan[span_2](start_span)[span_2](end_span).\n"
            "Untuk menjalankan secara lokal:\n"
            "1. Pastikan Node.js / Docker aktif.\n"
            "2. Ikuti instruksi di README.md repo GitHub Anda."
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
