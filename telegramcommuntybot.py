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
        {"name": "Python أسامة زيرو", "url": "https://t.me/c/2651762294/806"},
        {"name": "C++ جمال تك", "url": "https://t.me/c/2651762294/675"},
    ],
    
    "الأمن السيبراني الأساسي": [
        {"name": "اختراق اخلاقي من الصفر", "url": "https://t.me/c/2651762294/528"},
        {"name": "كيف ابدا في الامن السيبراني", "url": "https://t.me/c/2651762294/334"},
        {"name": "Linux+", "url": "https://t.me/c/2651762294/411"},
    ],
    
    "الأمن السيبراني المتقدم": [
        {"name": "صانع برامج الاختراق", "url": "https://t.me/c/2651762294/1176"},
        {"name": "اختراق المواقع واكتشاف الثغرات", "url": "https://t.me/c/2651762294/319"},
        {"name": "تطوير المالوير من الصفر", "url": "https://t.me/c/2651762294/319"},
        {"name": "كورس Red Team مميز", "url": "https://t.me/c/2651762294/652"},
    ],
    
    "كورسات مخصصة": [
        {"name": "حسام شادي - BUG BOUNTY", "url": "https://t.me/c/2651762294/700"},
        {"name": "حسام شادي - دبلومة RED TEAM", "url": "https://t.me/c/2651762294/1350"},
        {"name": "نت رايدر - EWPTV2", "url": "https://t.me/c/2651762294/160"},
        {"name": "نت رايدر - ECPPTV2", "url": "https://t.me/c/2651762294/3"},
        {"name": "نت رايدر - Security+", "url": "https://t.me/c/2651762294/437"},
        {"name": "سيف مخارزة - اختبار اختراق متقدم", "url": "https://t.me/c/2651762294/669"},
        {"name": "ايهاب ابو عليا - Active Directory", "url": "https://t.me/c/2651762294/1532"},
    ],
    
    "شهادات معتمدة": [
        {"name": "EJPTv2 أحمد سلطان", "url": "https://t.me/c/2651762294/1730"},
        {"name": "EJPTv2 نت رايدر", "url": "https://t.me/c/2651762294/1730"},
        {"name": "Security+", "url": "https://t.me/c/2651762294/437"},
        {"name": "MCSA محمد زهدي", "url": "https://t.me/c/2651762294/337"},
    ],
    
    "تطوير البرمجيات": [
        {"name": "FLEXCOURSES - Python", "url": "https://t.me/c/2651762294/695"},
        {"name": "علوم الحاسوب - حسوب", "url": "https://t.me/c/2651762294/656"},
    ],
    
    "كورسات Zsecurity": [
        {"name": "Bug Bounty 2024", "url": "https://t.me/c/2651762294/3106"},
        {"name": "Ethical Hacking 2024", "url": "https://t.me/c/2651762294/2491"},
        {"name": "Social Engineering 2024", "url": "https://t.me/c/2651762294/3334"},
    ],
    
    "مهارات تطويرية": [
        {"name": "اللغة الإنجليزية - عبد الرحمن حجازي", "url": "https://t.me/c/2651762294/322"},
    ],
    
    "تطوير المالوير": [
        {"name": "MALDEVACADEMY", "url": "https://t.me/c/2651762294/794"},
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
            InlineKeyboardButton("🧑💻 البرمجة", callback_data="programming"),
            InlineKeyboardButton("🛡️ أساسيات الأمن", callback_data="cybersecurity")
        ],
        [
            InlineKeyboardButton("🔐 الأمن المتقدم", callback_data="advanced_cyber"),
            InlineKeyboardButton("🕵️ كورسات مخصصة", callback_data="special_courses")
        ],
        [
            InlineKeyboardButton("📜 شهادات معتمدة", callback_data="certifications"),
            InlineKeyboardButton("🦠 تطوير المالوير", callback_data="malware_dev")
        ],
        [
            InlineKeyboardButton("🛠️ تطوير البرمجيات", callback_data="software_dev"),
            InlineKeyboardButton("🔍 Zsecurity", callback_data="zsecurity")
        ],
        [
            InlineKeyboardButton("🚀 مهارات تطويرية", callback_data="skills")
        ],
        [InlineKeyboardButton("👉 انضم هنا أولاً", url=COMMUNITY_LINK)]
    ]
    
    text = (
        "🌟 *مرحبا بك في بوت كورسات مجتمع التقنية!* 🌟\n"
        "▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
        "اختر القسم المطلوب:"
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
            ]),
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
            "مرحبا! للوصول للكورسات يجب الانضمام للمجموعة أولاً:",
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
        elif data == "programming":
            await show_courses(update, context, "البرمجة")
        elif data == "cybersecurity":
            await show_courses(update, context, "الأمن السيبراني الأساسي")
        elif data == "advanced_cyber":
            await show_courses(update, context, "الأمن السيبراني المتقدم")
        elif data == "special_courses":
            await show_courses(update, context, "كورسات مخصصة")
        elif data == "certifications":
            await show_courses(update, context, "شهادات معتمدة")
        elif data == "malware_dev":
            await show_courses(update, context, "تطوير المالوير")
        elif data == "software_dev":
            await show_courses(update, context, "تطوير البرمجيات")
        elif data == "zsecurity":
            await show_courses(update, context, "كورسات Zsecurity")
        elif data == "skills":
            await show_courses(update, context, "مهارات تطويرية")
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
