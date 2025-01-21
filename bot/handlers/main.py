from aiogram import Router, html, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from bot.buttons.reply import *

router1 = Router()
router2 = Router()


@router1.message(CommandStart())
async def bot_handlers(message: Message):
    await message.answer_photo("AgACAgQAAxkBAAMGZ4nEpYDX_PRPUJgYShoElwMKcaAAAlusMRtQnIRTbwFQOIH-t34BAAMCAANtAAM2BA")
    await message.reply(f"Heloo , {html.bold(message.from_user.first_name)}", reply_markup=main_button())


@router2.message(F.text == company_about)
async def company_about_handler(message: Message) -> None:
    caption = """
            EVOS ® tez xizmat ko'rsatish restoranlari tarmog'i bir joyda turmaydi, siz uchun va siz bilan doimo o'sib boradi va rivojlanadi! Biz geografiyamizni kengaytiramiz va deyarli har oyda yangi filiallarni ochamiz.
            Endi bizning tarmog'imizning O'zbekiston bo'ylab 50 dan ortiq filiali mavjud. Biz doimo jamoamizning bir qismi bo'lishni xohlaydigan va EVOS ® da o'z faoliyatini boshlashga tayyor bo'lgan dinamik va faol odamlarni qidiramiz.
            EVOS ® –  bu ishonchli brenddir. EVOS ® da ishlash – barqaror daromad va martaba istiqbollari kafolati.
            EVOS ® da o'z karyerangizni boshlang! """
    await message.answer_photo("AgACAgIAAxkBAAMIZ4nFPGZiYmfaLIxx4IKZaIOPAcAAAq3kMRvZfwlKYn7xj6Z63ZUBAAMCAAN5AAM2BA",
                               caption=caption)


@router1.message(F.text == branchs)
async def vocations_handler(message: Message) -> None:
    caption = """
    EVOS - O'zbekistondagi eng yirik fastfud kompaniyasi.
    Ayni paytda 49 ta chakana savdo shoxobchasi va
    zamonaviy diversifikatsiyalangan ishlab chiqarish ochiq.
    Kompaniya xodimlari birgalikda rivojlanib, kundan -kunga o'sib borayotgan katta oila.
    EVOS har kuni kengayib bormoqda, bugungi kunda bizda bir yarim mingdan ortiq odam bor.
     Bizning jamoamizga a'zo bo'ling, EVOS oilasiga xush kelibsiz!
    """
    await message.answer_photo("AgACAgQAAxkBAAMKZ4nF62yEcqxu_i2qodIusqz9ODcAApOsMRvcRIVRkFFcc-tXmoUBAAMCAAN4AAM2BA",
                               caption=caption, reply_markup=branchs_btns())


@router1.message(F.text == vocations)
async def branchs_handler(message: Message) -> None:
    await message.answer(text="EVOS jamoasiga qo'shiling!")
    await message.answer(text="📍 Shaharni tanlang.", reply_markup=make_region_btns())


@router1.message(F.text == menu)
async def sayt_handler(message: Message):
    await message.answer_photo("AgACAgQAAxkBAAMMZ4nLdfVQ2ruCAs8rsug9qkrH09sAArusMRsa1ERTmxYVky7vtxsBAAMCAAN5AAM2BA",
                               caption=" [Evos saytiga o'tish ](https://evos.uz/)", parse_mode="Markdown")
    await message.answer(
        "[Instagram ](https://www.instagram.com/evosuzbekistan/)|[Telegram](https://t.me/evosdeliverybot)|[Facebook](https://www.facebook.com/evosuzbekistan/)"
        , parse_mode="Markdown")


@router1.message(F.text == news)
async def news_handler(message: Message) -> None:
    text = """
    Kompaniya yangiliklari
    Aksiya
    Yangi filiallar
    Yangi tortlar va hk.
    """
    await message.answer(text=text)


@router1.message(F.text == contact_address)
async def contact_address_handler(message: Message) -> None:
    text = """Manzil: Furqat ko'chasi 175, kirish 1, 
2-qavat.
Mo'ljal: MAKRO THE TOWER

Kontakt: +998 71 203 12 12"""
    await message.answer_photo("AgACAgIAAxkBAANAZ2uom39vG8VYd8WhtY2mKYnEjXQAAq3kMRvZfwlKgEHBxwYcKBsBAAMCAAN5AAM2BA",
                               caption=text)
    await message.answer_location(latitude=41.325505, longitude=69.232752)


@router1.message(F.text == language)
async def branchs_handler(message: Message) -> None:
    await message.answer(text="Tilni o'zgartirish !", reply_markup=lang_butns())


@router1.message(F.text == back)
async def nearest_handler(message: Message) -> None:
    await message.answer(text="Eng yaqin filialni topish uchun joylashuvingizni yuboring!",
                         reply_markup=nearest_branch())



