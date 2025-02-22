
from datetime import datetime

from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    Message,
)

from EmikoRobot import pbot as Client
from EmikoRobot import (
    OWNER_ID as owner_id,
    OWNER_USERNAME as owner_usn,
    SUPPORT_CHAT as log,
)
from EmikoRobot.utils.errors import capture_err


def content(msg: Message) -> [None, str]:
    text_to_return = msg.text

    if msg.text is None:
        return None
    if " " in text_to_return:
        try:
            return msg.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


@Client.on_message(filters.command("bug"))
@capture_err
async def bug(_, msg: Message):
    if msg.chat.username:
        chat_username = (f"@{msg.chat.username} / `{msg.chat.id}`")
    else:
        chat_username = (f"Private Group / `{msg.chat.id}`")

    bugs = content(msg)
    user_id = msg.from_user.id
    mention = "["+msg.from_user.first_name+"](tg://user?id="+str(msg.from_user.id)+")"
    datetimes_fmt = "%d-%m-%Y"
    datetimes = datetime.utcnow().strftime(datetimes_fmt)

    thumb = "https://telegra.ph/file/7677b3443b68632aba7e9.jpg"
    
    bug_report = f"""
**#BUG : ** **@{owner_usn}**

**From User : ** **{mention}**
**User ID : ** **{user_id}**
**Group : ** **{chat_username}**

**Bug Report : ** **{bugs}**

**Event Stamp : ** **{datetimes}**"""

    
    if msg.chat.type == "private":
        await msg.reply_text("❎ <b>This Command Only Works In Groups.</b>")
        return

    if user_id == owner_id:
        if bugs:
            await msg.reply_text(
                "❎ <b>How Can Be Owner Bot Reporting Bug??</b>",
            )
            return
        else:
            await msg.reply_text(
                "Owner Noob!"
            )
    elif user_id != owner_id:
        if bugs:
            await msg.reply_text(
                f"<b>Bug Report : {bugs}</b>\n\n"
                "✅ <b>The Bug Was Successfully Reported To The Support Group!</b>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Close", callback_data=f"close_reply")
                        ]
                    ]
                )
            )
            await Client.send_photo(
                log,
                photo=thumb,
                caption=f"{bug_report}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "View Bug", url=f"{msg.link}"),
                            InlineKeyboardButton(
                                "Get Help", url=f"http://t.me/synxrobot?start=help"),
                        ],
                        [
                            InlineKeyboardButton(
                                "Close", callback_data="close_send_photo"),
                        ]
                    ]
                )
            )
        else:
            await msg.reply_text(
                f" <b> Contoh: /bug bot musik lag</b>",
            )
        

@Client.on_callback_query(filters.regex("close_reply"))
async def close_reply(msg, CallbackQuery):
    await CallbackQuery.message.delete()

@Client.on_callback_query(filters.regex("close_send_photo"))
async def close_send_photo(_, CallbackQuery):
    is_Admin = await Client.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not is_Admin.can_delete_messages:
        return await CallbackQuery.answer(
            "You're Not Allowed To Close This.", show_alert=True
        )
    else:
        await CallbackQuery.message.delete()
        

__mod_name__ = "Bug"
