from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_conversion_keyboard():
    """Konvertatsiya turini tanlash uchun klaviatura"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📄 TO PDF", callback_data="mode_to_pdf"),
            InlineKeyboardButton(text="📤 FROM PDF", callback_data="mode_from_pdf")
        ]
    ])
    return keyboard


def get_to_pdf_keyboard():
    """TO PDF konvertatsiya variantlari"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🖼 JPG → PDF", callback_data="conv_jpg_pdf")],
        [InlineKeyboardButton(text="📝 WORD → PDF", callback_data="conv_word_pdf")],
        [InlineKeyboardButton(text="📊 POWERPOINT → PDF", callback_data="conv_ppt_pdf")],
        [InlineKeyboardButton(text="📈 EXCEL → PDF", callback_data="conv_excel_pdf")],
        [InlineKeyboardButton(text="🌐 HTML → PDF", callback_data="conv_html_pdf")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main")]
    ])
    return keyboard


def get_from_pdf_keyboard():
    """FROM PDF konvertatsiya variantlari"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📷 PDF → JPG", callback_data="conv_pdf_jpg")],
        [InlineKeyboardButton(text="📝 PDF → WORD", callback_data="conv_pdf_word")],
        [InlineKeyboardButton(text="📊 PDF → POWERPOINT", callback_data="conv_pdf_ppt")],
        [InlineKeyboardButton(text="📈 PDF → EXCEL", callback_data="conv_pdf_excel")],
        [InlineKeyboardButton(text="📋 PDF → PDF/A", callback_data="conv_pdf_pdfa")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main")]
    ])
    return keyboard
