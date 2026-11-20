"""
O'qishni nazorat qilish Telegram boti.
Haftalik reja: nazariya -> amaliyot -> takrorlash -> dam olish.
"""
import datetime
import os
import zoneinfo

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()
BOT_TOKEN = os.getenv("9077200448:AAEhCQpODrwqPJlxlpBzeTDoG2VMQID70GU")
ISM = os.getenv("Eslatma", "Afruzbek")
TZ = zoneinfo.ZoneInfo("Asia/Tashkent")
ESLATMA_VAQTI = datetime.time(8, 0, tzinfo=TZ)  # har kuni ertalab 08:00

# weekday(): 0 = dushanba ... 6 = yakshanba
REJA = {
    0: ("Dushanba", "📖 Nazariy o'qish kuni"),
    1: ("Seshanba", "📖 Nazariy o'qish kuni"),
    2: ("Chorshanba", "💻 Amaliy kun"),
    3: ("Payshanba", "💻 Amaliy kun"),
    4: ("Juma", "💻 Amaliy kun"),
    5: ("Shanba", "🔁 Takrorlash kuni"),
    6: ("Yakshanba", "😴 Dam olish kuni\n⏱ Lekin 1 soat yangi mavzuni ko'rib chiqing"),
}

MENU = ReplyKeyboardMarkup([["📅 Bugun", "🗓 Haftalik reja"]], resize_keyboard=True)


def bugun_matni() -> str:
    kun = datetime.datetime.now(TZ).weekday()
    nom, vazifa = REJA[kun]
    return f"Bugun {nom}.\n{vazifa}"


def hafta_matni() -> str:
    qatorlar = [f"{nom}: {vazifa.splitlines()[0]}" for nom, vazifa in REJA.values()]
    qatorlar[-1] += " (+ 1 soat yangi mavzu)"
    return "🗓 Haftalik reja:\n\n" + "\n".join(qatorlar)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.application.bot_data.setdefault("chats", set()).add(update.effective_chat.id)
    await update.message.reply_text(
        f"Salom! Mening ismim {ISM} 👋\n\n{bugun_matni()}",
        reply_markup=MENU,
    )


async def bugun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(bugun_matni(), reply_markup=MENU)


async def hafta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(hafta_matni(), reply_markup=MENU)


async def eslatma(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in context.application.bot_data.get("chats", set()):
        await context.bot.send_message(chat_id, f"Xayrli tong, {ISM}! ☀️\n\n{bugun_matni()}")


def main():
    if not BOT_TOKEN:
        raise SystemExit("BOT_TOKEN topilmadi. .env faylini yarating (.env.example ga qarang).")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bugun", bugun))
    app.add_handler(CommandHandler("hafta", hafta))
    app.add_handler(MessageHandler(filters.Regex("^📅 Bugun$"), bugun))
    app.add_handler(MessageHandler(filters.Regex("^🗓 Haftalik reja$"), hafta))
    app.job_queue.run_daily(eslatma, ESLATMA_VAQTI)
    app.run_polling()


if __name__ == "__main__":
    main()
