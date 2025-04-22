import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatMemberStatus
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters
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

class BotStats:
    def __init__(self):
        self.total_users = 0
        self.course_clicks = {}

stats = BotStats()

# تعريف الدورات بحسب الأقسام
COURSES = {
    "كورسات صحيح": [
        {"name": "صانع برامج الاختراق", "url": "https://t.me/c/2651762294/1176"},
        {"name": "اختراق اخلاقي من الصفر", "url": "https://t.me/c/2651762294/528"},
        {"name": "اختراق المواقع واكتشاف الثغرات", "url": "https://t.me/c/2651762294/319"},
        {"name": "تطوير المالوير من الصفر", "url": "https://t.me/c/2651762294/794"},
    ],
    "كورسات حسام شادي RED NEXUS": [
        {"name": "BUG BOUNTY اكتشاف الثغرات", "url": "https://t.me/c/2651762294/700"},
        {"name": "دبلومة RED TEAM", "url": "https://t.me/c/2651762294/1350"},
        {"name": "LINUX+", "url": "https://t.me/c/2651762294/411"},
    ],
    "كورسات اسامة زيرو البرمجة": [
        {"name": "Python", "url": "https://t.me/c/2651762294/806"},
        {"name": "C++", "url": "https://t.me/c/2651762294/961"},
    ],
    "كورسات نت رايدر": [
        {"name": "EWPTV2", "url": "https://t.me/c/2651762294/160"},
        {"name": "ECPPTV2", "url": "https://t.me/c/2651762294/3"},
        {"name": "Security+", "url": "https://t.me/c/2651762294/437"},
        {"name": "EJPTV2", "url": "https://t.me/c/2651762294/1730"},
    ],
    "كورسات FLEXCOURSES": [
        {"name": "Python", "url": "https://t.me/c/2651762294/695"},
    ],
    "كورسات سيف مخارزة": [
        {"name": "اختبار اختراق متقدم", "url": "https://t.me/c/2651762294/669"},
        {"name": "اختراق مواقع", "url": "https://t.me/hackingchannelcol/1203"},
    ],
    "اكاديمية حسوب": [
        {"name": "علوم الحاسوب", "url": "https://t.me/c/2651762294/656"},
        {"name": "الذكاء الاصطناعي", "url": "https://t.me/c/2651762294/8484"},
        {"name": "تطوير واجهات الويب", "url": "https://t.me/c/2651762294/10551"},
        {"name": "PHP", "url": "https://t.me/c/2651762294/18500"},
        {"name": "بايثون - أكاديمية حسوب", "url": "https://t.me/c/2651762294/20668"},
    ],
    "كورسات محمد زهدي": [
        {"name": "MCSA", "url": "https://t.me/c/2651762294/337"},
    ],
    "كورسات جمال تك": [
        {"name": "C++", "url": "https://t.me/c/2651762294/675"},
    ],
    "كورسات تطوير المالوير والفايروسات": [
        {"name": "MALDEVACADEMY", "url": "https://t.me/c/2651762294/794"},
    ],
    "كورسات ايهاب ابو عليا": [
        {"name": "Ejptv2", "url": "https://t.me/c/2651762294/1053"},
        {"name": "Active Directory", "url": "https://t.me/c/2651762294/1532"},
    ],
    "كورسات Zsecurity (كلها 2024 ولله)": [
        {"name": "Zsecurity Bug Bounty 2024", "url": "https://t.me/c/2651762294/3106"},
        {"name": "Zsecurity Learn Ethical Hacking From Scratch 2024", "url": "https://t.me/c/2651762294/3106"},
        {"name": "Zsecurity Social Engineering 2024", "url": "https://t.me/c/2651762294/3334"},
    ],
    "انظمة لينكس": [
        {"name": "linux for hackers بالعربي", "url": "https://t.me/c/2651762294/6264"},
        {"name": "فليكس كورس ادارة انظمة لينكس", "url": "https://t.me/c/2651762294/3469"},
        {"name": "LINUX+ حسام شادي", "url": "https://t.me/c/2651762294/411"},
    ],
    "كورس ريد تيم مميز": [
        {"name": "Red Team مميز", "url": "https://t.me/c/2651762294/652"},
    ],
    "كيف ابدا في الامن السيبراني": [
        {"name": "كيف ابدا في الامن السيبراني", "url": "https://t.me/c/2651762294/334"},
    ],
}

# تجميع جميع الكورسات للبحث
ALL_COURSES = []
for lst in COURSES.values():
    ALL_COURSES.extend(lst)

async def is_member(user_id: int, bot) -> bool:
    try:
        member = await bot.get_chat_member(COMMUNITY_CHAT_ID, user_id)
        return member.status not in (ChatMemberStatus.LEFT, ChatMemberStatus.BANNED)
    except Exception as e:
        logger.error(f"خطأ في التحقق من العضوية: {e}")
        return False

async def show_main_menu(update: Update, is_callback: bool = False):
    keyboard = [[InlineKeyboardButton(sec, callback_data=sec)] for sec in COURSES.keys()]
    keyboard.append([InlineKeyboardButton("👉 انضم هنا أولاً", url=COMMUNITY_LINK)])
    text = (
        "🌟 *مرحبا بك في بوت كورسات مجتمع التقنية!* 🌟\n"
        "▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
        "اختر القسم أو اكتب في القروب:\n"
        "`بحث <اسم القسم أو الكورس>`"
    )
    reply_markup = InlineKeyboardMarkup(keyboard)
    if is_callback:
        q = update.callback_query
        await q.answer()
        await q.edit_message_text(text=text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup, parse_mode="Markdown")

async def show_courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    section = q.data
    await q.answer()
    if not await is_member(q.from_user.id, context.bot):
        await q.edit_message_text(
            "⚠️ *يجب الانضمام للمجموعة أولاً!*\n"
            f"انضم هنا: {COMMUNITY_LINK}\n"
            "ثم اضغط تحديث:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 تأكيد الانضمام", callback_data="show_main")]]),
            parse_mode="Markdown"
        )
        return
    buttons = [[InlineKeyboardButton(c["name"], url=c["url"])] for c in COURSES[section]]
    buttons.append([InlineKeyboardButton("🔙 رجوع", callback_data="show_main")])
    stats.course_clicks[section] = stats.course_clicks.get(section, 0) + 1
    await q.edit_message_text(f"📚 *{section}*\n▬▬▬▬▬▬▬▬▬▬▬▬▬", reply_markup=InlineKeyboardMarkup(buttons), parse_mode="Markdown")

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not text.startswith("بحث"):
        return
    term = text[4:].strip().lower()
    reply_parts = []

    # بحث في أسماء الأقسام
    matched_sections = [sec for sec in COURSES.keys() if term in sec.lower()]
    for sec in matched_sections:
        reply_parts.append(f"📂 *{sec}*:")
        for c in COURSES[sec]:
            reply_parts.append(f"- [{c['name']}]({c['url']})")
        reply_parts.append("")

    # بحث في أسماء الكورسات
    matched_courses = [c for c in ALL_COURSES if term in c["name"].lower()]
    for c in matched_courses:
        reply_parts.append(f"🔹 *{c['name']}*\n🔗 {c['url']}")
        reply_parts.append("")

    if not reply_parts:
        reply = "❌ لم أتمكن من العثور على أي نتائج تطابق بحثك."
    else:
        reply = "\n".join(reply_parts).strip()

    await update.message.reply_text(reply, parse_mode="Markdown", disable_web_page_preview=True)

async def handle_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    if data == "show_main":
        await show_main_menu(update, is_callback=True)
    elif data in COURSES:
        await show_courses(update, context)
    else:
        await update.callback_query.answer()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats.total_users += 1
    await show_main_menu(update)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callbacks))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^بحث"), handle_search))
    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
