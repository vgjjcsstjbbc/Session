import traceback

from Data import Data
from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from StringSessionBot.generate import generate_session


# Callbacks
@Client.on_callback_query()
async def _callbacks(bot: Client, callback_query: CallbackQuery):
    user = await bot.get_me()
    # user_id = callback_query.from_user.id
    mention = user["mention"]
    query = callback_query.data.lower()
    if query.startswith("home"):
        if query == "home":
            chat_id = callback_query.from_user.id
            message_id = callback_query.message.message_id
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=Data.START.format(callback_query.from_user.mention, mention),
                reply_markup=InlineKeyboardMarkup(Data.buttons),
            )
    elif query == "about":
        chat_id = callback_query.from_user.id
        message_id = callback_query.message.message_id
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=Data.ABOUT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons),
        )
    elif query == "help":
        chat_id = callback_query.from_user.id
        message_id = callback_query.message.message_id
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="**كيف تستخدمني**\n" + Data.HELP,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons),
        )
    elif query == "generate":
        await callback_query.message.reply(
            "يرجى اختيار الجلسة المطلوبة إذا كنت تريد جلسة بايروجرام اختر بايروجرام وإذا كنت تريد تليثون اختر تيرمكس",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("بايروجرام", callback_data="pyrogram"),
                        InlineKeyboardButton("تليثون", callback_data="telethon"),
                    ]
                ]
            ),
        )
    elif query in ["pyrogram", "telethon"]:
        await callback_query.answer()
        try:
            if query == "pyrogram":
                await generate_session(bot, callback_query.message)
            else:
                await generate_session(bot, callback_query.message, telethon=True)
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            await callback_query.message.reply(ERROR_MESSAGE.format(str(e)))


ERROR_MESSAGE = (
    "اوبس هناك خطأ \n\n**خطأ** : {} "
    "\n\nأرجو مراسلة  قم بتحويل هذه الرسالة الى مطورين البوت "
    "أو يمكنك إعادة استخراج الجلسة"
    "وشكرًا لاستخدام البوت المقدم من : @q5_u8"
)
