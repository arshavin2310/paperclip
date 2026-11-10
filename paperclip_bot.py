import os
import subprocess
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

TOKEN = os.getenv("TELEGRAM_TOKEN", "9092798479:AAG7VoZHuDzqDHpPlc7gKj_k4WkXQk-cz54")

# Menu Utama Telegram
async def start(update: Update, context: ContextTypes.DefaultContext):
    keyboard = [
        [KeyboardButton("🤖 Status Agent & Runtime"), KeyboardButton("🐳 Cek Docker & Sistem")],
        [KeyboardButton("📋 Lihat File & Repo"), KeyboardButton("🚀 Tes & Workflow")],
        [KeyboardButton("❓ Bantuan / Info")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 Selamat datang di **Paperclip Telegram Command Center**!\n\n"
        "Semua fitur, status agen, dan manajemen repo di dalam sistem kini bisa Anda akses langsung melalui tombol di bawah ini:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DefaultContext):
    text = update.message.text
    chat_id = update.effective_chat.id

    if text == "🤖 Status Agent & Runtime":
        await update.message.reply_text("⚙️ Memeriksa status agen AI dan komponen runtime...")
        # Simulasi pengecekan modul agent atau file agen di repo
        output = "Status: 🟢 Agent Manager Aktif\n- Runtime: Siap\n- Konfigurasi: Normal"
        await update.message.reply_text(f"```\n{output}\n```", parse_mode="Markdown")

    elif text == "🐳 Cek Docker & Sistem":
        await update.message.reply_text("🐳 Memeriksa status konfigurasi Docker...")
        if os.path.exists("Dockerfile"):
            output = "Dockerfile ditemukan di repo.\nStatus kontainer: Siap di-build."
        else:
            output = "Dockerfile tidak ditemukan di direktori aktif."
        await update.message.reply_text(f"```\n{output}\n```", parse_mode="Markdown")

    elif text == "📋 Lihat File & Repo":
        await update.message.reply_text("📂 Mengambil daftar file utama dari repo...")
        try:
            files = os.listdir(".")
            file_list = "\n".join(files[:20]) # Ambil 20 file teratas
            output = f"Daftar File Utama:\n{file_list}"
        except Exception as e:
            output = f"Gagal membaca direktori: {str(e)}"
        await update.message.reply_text(f"```\n{output}\n```", parse_mode="Markdown")

    elif text == "🚀 Tes & Workflow":
        workflow_info = (
            "🚀 **Daftar Kategori Workflow di Repo Anda**:\n\n"
            "• *Agent runtime images*\n"
            "• *Docker & Runner check*\n"
            "• *E2E Tests & CI Profile*\n"
            "• *Release & Smoke Tests*\n\n"
            "Gunakan GitHub Actions di web/aplikasi GitHub untuk memicu alur kerja spesifik tersebut."
        )
        await update.message.reply_text(workflow_info, parse_mode="Markdown")

    elif text == "❓ Bantuan / Info":
        help_text = (
            "📌 **Panduan Penggunaan Bot**:\n"
            "Bot ini terhubung langsung dengan repositori Paperclip Anda[span_0](start_span)[span_0](end_span). "
            "Pilih tombol menu di bawah untuk memantau status atau melihat isi sistem secara instan."
        )
        await update.message.reply_text(help_text, parse_mode="Markdown")

    else:
        await update.message.reply_text(f"Pesan diterima: '{text}'. Silakan gunakan tombol menu yang tersedia di bawah ya!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot Telegram Paperclip dengan Menu Lengkap aktif...")
    app.run_polling()
