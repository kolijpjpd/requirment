import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatMemberStatus
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler
)

# إعدادات التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = '8146396115:AAGcO5Z7kTLQp4Hl9sjMHlzE-OWXYQjcZtY'
COMMUNITY_CHAT_ID = -1002651762294
COMMUNITY_LINK = "https://t.me/+5JrSHhoH1jw3MjIx"

COURSES = {
    "البرمجة": [
        {"name": "C++ أسامة زيرو", "url": "https://t.me/c/2651762294/961"},
        {"name": "C++ عبد الرحمن المجيد", "url": "https://t.me/c/2651762294/1956"},
        {"name": "C++ جمال تك", "url": "https://t.me/c/2651762294/675"},
    ],
    "الأمن السيبراني": [
        {"name": "EJPTv2 أحمد سلطان (كامل)", "url": "https://t.me/c/2651762294/1730"},
        {"name": "EWPTv2 أحمد سلطان", "url": "https://t.me/c/2651762294/160"},
        {"name": "Social Engineering مترجم", "url": "https://t.me/c/2651762294/3727"},
        {"name": "Zsecurity Social Engineering 2024", "url": "https://t.me/c/2651762294/3334"},
        {"name": "Zsecurity Bug Bounty 2024", "url": "https://t.me/c/2651762294/3106"},
        {"name": "Zsecurity Ethical Hacking 2024", "url": "https://t.me/c/2651762294/2491"},
    ]
}

async def is_member(user_id, bot):
    try:
        member = await bot.get_chat_member(COMMUNITY_CHAT_ID, user_id)
        return member.status not in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]
    except Exception as e:
        logger.error(f"خطأ في التحقق: {e}")
        return False

async def show_main_menu(update: Update, is_callback: bool = False):
    keyboard = [
        [
            InlineKeyboardButton("🧑💻 كورسات البرمجة", callback_data="programming"),
            InlineKeyboardButton("🛡️ كورسات الأمن السيبراني", callback_data="cybersecurity")
        ],
        [InlineKeyboardButton("👉 انضم هنا أولاً", url=COMMUNITY_LINK)]
    ]
    
    text = (
        "🌟 *مرحبا بك في بوت كورسات مجتمع التقنية!* 🌟\n"
        "▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
        "اختر نوع الكورسات:"
    )
    
    if is_callback:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

async def show_courses(update: Update, context: ContextTypes.DEFAULT_TYPE, course_type: str):
    query = update.callback_query
    await query.answer()
    
    if not await is_member(query.from_user.id, context.bot):
        await query.edit_message_text(
            "⚠️ *يجب الانضمام للمجموعة أولاً!*\n"
            f"انضم هنا: {COMMUNITY_LINK}\n"
            "ثم اضغط تحديث:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 تأكيد الانضمام", callback_data="verify")]
            ]),  # تم إصلاح القوس هنا
            parse_mode="Markdown"
        )
        return
    
    courses = COURSES.get(course_type, [])
    buttons = [[InlineKeyboardButton(c["name"], url=c["url"])] for c in courses]
    buttons.append([InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main")])
    
    await query.edit_message_text(
        f"📚 *كورسات {course_type}:*\n"
        "▬▬▬▬▬▬▬▬▬▬▬▬▬",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await is_member(update.effective_user.id, context.bot):
        await show_main_menu(update)
    else:
        await update.message.reply_text(
            "مرحبا! للوصول للكورات يجب الانضمام للمجموعة أولاً:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("انضم للمجموعة هنا", url=COMMUNITY_LINK)],
                [InlineKeyboardButton("✅ تأكيد الانضمام", callback_data="verify")]
            ])
        )

async def handle_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    
    try:
        if data == "verify":
            await verify_membership(update, context)
        elif data == "main":
            await show_main_menu(update, is_callback=True)
        elif data in ["programming", "cybersecurity"]:
            category = "البرمجة" if data == "programming" else "الأمن السيبراني"
            await show_courses(update, context, category)
    except Exception as e:
        logger.error(f"خطأ في التعامل مع الأوامر: {str(e)}")
        await query.answer("حدث خطأ، حاول مرة أخرى!", show_alert=True)

async def verify_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if await is_member(query.from_user.id, context.bot):
        await show_main_menu(update, is_callback=True)
    else:
        await query.edit_message_text(
            "❌ لم يتم التحقق بعد!\n"
            "تأكد من:\n"
            "1. الانضمام الفعلي للمجموعة\n"
            "2. عدم استخدام حساب مخفي\n"
            "3. الانتظار 10 ثواني بعد الانضمام",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 حاول مجدداً", callback_data="verify")],
                [InlineKeyboardButton("الذهاب للمجموعة", url=COMMUNITY_LINK)]
            ])
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callbacks))
    
    logger.info("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()