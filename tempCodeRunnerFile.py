from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = '8146396115:AAGcO5Z7kTLQp4Hl9sjMHlzE-OWXYQjcZtY'  # ضع توكن البوت هنا

courses = [
    {"name": "دورة بايثون", "url": "https://t.me"},
    {"name": "دورة php", "url": "https://t.me"},
    {"name": "دورة اختراق المواقع", "url": "https://t.me"},
]

def start(update: Update, context: CallbackContext):
    keyboard = []
    for course in courses:
        keyboard.append([InlineKeyboardButton(course["name"], url=course["url"])])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text("مرحبا بك في بوت lime الكورسات", reply_markup=reply_markup)

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':  # التصحيح هنا
    main()