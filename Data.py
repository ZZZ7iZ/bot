from pyrogram.types import InlineKeyboardButton


class Data:
    # Start Message
    START = """
أهلًا 👋 {}

انـا بـوت اقـوم بـإســتــخـراج الجلسات،
1) جـلسـة بـايـثـون
2) جـلـسة بــــايــــروجــــرام

قناة السورس 🧸♥️ : @ZZZ7iZ
    """

    # Home Button
    home_buttons = [
        [InlineKeyboardButton("بـدء اســـتــــخـــراج جلـــــســــة 🧸♥️", callback_data="generate")],
        [InlineKeyboardButton(text=" 📍الـقــائـــمـــة الـــرئــــــيـــــسية", callback_data="home")]
    ]

    generate_button = [
        [InlineKeyboardButton("بـدء اســـــتــــخــــراج جـــــلــــســــة ♥️🧸", callback_data="generate")]
    ]

    # Rest Buttons
    buttons = [
        [InlineKeyboardButton("بـــدء اســـتـــــخــــراج جــــلـسـة ♥️🧸", callback_data="generate")],
        [InlineKeyboardButton("المطور 👤", url="https://t.me/IIIlIIv")],
        [
            InlineKeyboardButton("كيف تـــستـــخدمــنـــــي  ❓", callback_data="help"),
            InlineKeyboardButton("حـــــول الــــبوت 🌐", callback_data="about")
      ],
        [InlineKeyboardButton("قـــنـــــاة الــــــســـــورس 💡", url="https://t.me/ZZZ7iZ")],
    ]


    # Help Message
    HELP = """
✨ **الأوامـــــــر الــــــمــــــتـــــاحـــة** ✨

/about - حول البوت
/help - مساعدة
/start - بدء البوت
/generate - بدء استخراج الجلسة
/cancel - إلغاء الاستخراج
/restart - اعادة تشغيل البوت
"""

    # About Message
    ABOUT = """
**حـــــول الــــبـــوت 🌐** 

بوت تلكرام لاستخراج كود تيرمكس وبايروجرام قناة السورس 🧸♥️ : @ZZZ7iZ

سورس سبارك: [اضغط هنا](https://t.me/ZZZ7iZ)

إطار العمل : [Pyrogram](docs.pyrogram.org)

اللغة : [Python](www.python.org)

الـــمــــطـــور 💡 : @IIIlIIv
    """
