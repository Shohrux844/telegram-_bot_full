from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

company_about = "🏢 Companiya haqida"
branchs = "📍Filialllar"
vocations = "💼 Bo'sh ish o'rinlari"
menu = "📱Menu"
news = "🗣Yangilikalr"
contact_address = "📞Kontakt/Manzil"
language = "Til 🇺🇿/🇷🇺"
back = "Ortga↩️"
cancel = "❌Bekor qilish❌"
back__ = "Ortga↩️"
nt = "☕️Yaqin filiallarni ko'rsatish"
head_office = "🏢Bosh ofis"
tash = "Toshkent sh."

regions = ["Toshkent", "Sirdaryo", "Xorazm", "Andijon", "Qo'qon,", "Qarshi", "Namangan", "Nukus",
           "Farg'ona", "Xorazim Viloyati", "Navoiy", "Shahrisabz", "samarqand", "Toshkent viloyati", "❌Bekor qilish❌",
           "Ortga↩️"]

brns = ["☕Yaqin filiallarni ko'rsatish", "🏢Bosh ofis", "Toshkent sh.", "⬅️Ortga"]

nearest = ["📍Geolakatsiyani yuboring ", "Ortga↩️"]

lang = ["🇷🇺 Русский", "🇺🇿 O'zbekcha", "Ortga↩️"]


def company_dis():
    caption = """
                EVOS ® tez xizmat ko'rsatish restoranlari tarmog'i bir joyda turmaydi, siz uchun va siz bilan doimo o'sib boradi va rivojlanadi! Biz geografiyamizni kengaytiramiz va deyarli har oyda yangi filiallarni ochamiz.
                Endi bizning tarmog'imizning O'zbekiston bo'ylab 50 dan ortiq filiali mavjud. Biz doimo jamoamizning bir qismi bo'lishni xohlaydigan va EVOS ® da o'z faoliyatini boshlashga tayyor bo'lgan dinamik va faol odamlarni qidiramiz.
                EVOS ® –  bu ishonchli brenddir. EVOS ® da ishlash – barqaror daromad va martaba istiqbollari kafolati.
                EVOS ® da o'z karyerangizni boshlang! """

    image = "AgACAgIAAxkBAANAZ2uom39vG8VYd8WhtY2mKYnEjXQAAq3kMRvZfwlKgEHBxwYcKBsBAAMCAAN5AAM2BA"


def main_button():
    company_about_btn = KeyboardButton(text=company_about)
    branchs_btn = KeyboardButton(text=branchs)
    vocations_btn = KeyboardButton(text=vocations)
    menu_btn = KeyboardButton(text=menu)
    news_btn = KeyboardButton(text=news)
    contact_address_btn = KeyboardButton(text=contact_address)
    language_btn = KeyboardButton(text=language)
    back_btn = KeyboardButton(text=back)
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[company_about_btn, branchs_btn, vocations_btn, menu_btn, news_btn, contact_address_btn, language_btn,
              back_btn])
    rkb.adjust(2, 1, 2, 2)
    return rkb.as_markup(resize_keyboard=True)


def make_region_btns():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[KeyboardButton(text=region) for region in regions])
    rkb.adjust(2, repeat=True)
    return rkb.as_markup(resize_keyboard=True)


def branchs_btns():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[KeyboardButton(text=i) for i in brns])
    rkb.adjust(1, 2, 1, repeat=True)
    return rkb.as_markup(resize_keyboard=True)


def nearest_branch():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[KeyboardButton(text=i) for i in nearest])
    rkb.adjust(1, repeat=True)
    return rkb.as_markup(resize_keyboard=True)


def lang_butns():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[KeyboardButton(text=i) for i in lang])
    rkb.adjust(2, 1, repeat=True)
    return rkb.as_markup(resize_keyboard=True)
