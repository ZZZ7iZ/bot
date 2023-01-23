from asyncio.exceptions import TimeoutError
from Data import Data
from pyrogram import Client, filters
from telethon import TelegramClient
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

ERROR_MESSAGE = "عفوًا! حدث استثناء! \n\n**خطأ** : {} " \
            "\n\nيرجى الابلاغ عن المشكلة في @Tepthon_Help  إذا كان هناك خطأ " \
            "معلومات حساسة وأنت إذا كنت تريد الإبلاغ عن هذا كـ " \
            "لم يتم تسجيل رسالة الخطأ هذه بواسطتنا!"


@Client.on_message(filters.private & ~filters.forwarded & filters.command('generate'))
async def main(_, msg):
    await msg.reply(
        "اختــــــر احــــد الــــجلـــســــات الآتـــــيـة :-",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("بايــــــروجــــرام", callback_data="pyrogram"),
            InlineKeyboardButton("تـــــلــــيــــثـــــون", callback_data="telethon")
        ]])
    )


async def generate_session(bot, msg, telethon=False):
    await msg.reply("بـدء اســــتــخراج الــــجــــلســــة{}s....".format("Telethon" if telethon else "Pyrogram"))
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, 'عليك ارسال الخاص بك  `API_ID`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply('غير صحيح API_ID (الذي يجب أن يكون عددًا صحيحًا). يرجى البدء في استخراج الجلسة مرة أخرى.', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    api_hash_msg = await bot.ask(user_id, 'الآن ارسل الخاص بك `API_HASH`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(user_id, 'الان ارسل `PHONE_NUMBER` مع رمز بلدك. \nمثال : `+628xxxxxxx`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("إرسال OTP...")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    else:
        client = Client(":memory:", api_id, api_hash)
    await client.connect()
    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply('`API_ID` و "API_HASH" غير صالحين. يرجى البدء في إنشاء الجلسة مرة أخرى.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply('`PHONE_NUMBER` غير صالح. يرجى البدء في إنشاء الجلسة مرة أخرى.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    try:
        phone_code_msg = await bot.ask(user_id, "يرجى التحقق من وجود OTP في حساب Telegram الرسمي. إذا حصلت عليه ، أرسل OTP هنا بعد قراءة التنسيق أدناه. \nIf OTP is `12345`, **من فضلك أرسلها كـ** `1 2 3 4 5`.", filters=filters.text, timeout=600)
        if await cancelled(api_id_msg):
            return
    except TimeoutError:
        await msg.reply('بلغ الحد الزمني 10 دقائق. يرجى البدء في إنشاء الجلسة مرة أخرى.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, phone_code, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply('OTP غير صالح. يرجى البدء في إنشاء الجلسة مرة أخرى.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply('انتهت صلاحية كلمة المرور لمرة واحدة. يرجى البدء في إنشاء الجلسة مرة أخرى.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(user_id, 'لقد مكّن حسابك التحقق على خطوتين. يرجى تقديم كلمة المرور.', filters=filters.text, timeout=300)
        except TimeoutError:
            await msg.reply('بلغ الحد الزمني 5 دقائق. يرجى البدء في إنشاء الجلسة مرة أخرى.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
        try:
            password = two_step_msg.text
            if telethon:
                await client.sign_in(password=password)
            else:
                await client.check_password(password=password)
            if await cancelled(api_id_msg):
                return
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await two_step_msg.reply('أدخلت كلمة مرور غير صالحة. يرجى البدء في إنشاء الجلسة مرة أخرى.', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = "**{} استخراج الجلسة** \n\n`{}` \n\استخرجت من @Tepthon".format("TELETHON" if telethon else "PYROGRAM", string_session)
    await client.send_message("me", text)
    await client.disconnect()
    await phone_code_msg.reply("تم جلب استخراج الجلسة بنجاح {}. \n\nالرجاء تفقد الرسائل المحفوظة! \n\nمن @Tepthon".format("telethon" if telethon else "pyrogram"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("تم الإلغاء!❌", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return true
    elif "/restart" in msg.text:
        await msg.reply("تم إعادة التشغيل!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("تم إلغاء استخراج الجلسة!", quote=True)
        return True
    else:
        return False


# @Client.on_message(filters.private & ~filters.forwarded & filters.command(['cancel', 'restart']))
# async def formalities(_, msg):
#     if "/cancel" in msg.text:
#         await msg.reply("Membatalkan Semua Processes!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
#         return True
#     elif "/restart" in msg.text:
#         await msg.reply("Memulai Ulang Bot!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
#         return True
#     else:
#         return False
