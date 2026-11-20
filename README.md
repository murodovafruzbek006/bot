# Study Bot

O'qishni nazorat qiluvchi Telegram bot.

## Haftalik reja
- Dushanba, Seshanba: nazariy o'qish
- Chorshanba, Payshanba, Juma: amaliy kun
- Shanba: takrorlash
- Yakshanba: dam olish (+ 1 soat yangi mavzu)

Har kuni ertalab 08:00 da (Toshkent vaqti) eslatma yuboradi.

## Buyruqlar
- `/start` - salomlashadi va bugungi vazifani ko'rsatadi
- `/bugun` - bugungi vazifa
- `/hafta` - haftalik reja

## O'rnatish
```bash
git clone <repo-url>
cd study-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # so'ng .env ichiga tokenni yozing
python bot.py
```
