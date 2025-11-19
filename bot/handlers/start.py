import asyncio
import os
from os import getenv
from datetime import datetime

import zipfile
import shutil

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from bot.buttons.inline import get_conversion_keyboard, get_to_pdf_keyboard, get_from_pdf_keyboard
from bot.function.databese_func.db_func import get_user, create_user, add_invited_user, unblock_user, \
    increment_conversion, check_and_block_user
from bot.function.from_pdf.main import pdf_to_images, pdf_to_docx, pdf_to_pptx, pdf_to_xlsx, pdf_to_pdfa
from bot.function.to_pdf_func.to_pdf import image_to_pdf, docx_to_pdf, pptx_to_pdf, xlsx_to_pdf, html_to_pdf
from bot.loger_info.main import logger
from bot.text.main import welcome_text
from db.models import SessionLocal, User
from utils.settings import ENV_PATH

load_dotenv(ENV_PATH)

# Bot tokeningizni kiriting
BOT_TOKEN = getenv("BOT_TOKEN")
ADMIN_CHANNEL = getenv("ADMIN_CHANNEL")
ADMIN_ID = getenv("ADMIN_ID")


# FSM States
class ConversionState(StatesGroup):
    waiting_for_conversion_type = State()


# Bot va Dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()


# ============ HANDLERS ============

@router.message(CommandStart())
async def start_handler(message: Message):
    db = SessionLocal()
    try:
        user = get_user(db, message.from_user.id)

        # Referal link tekshirish
        args = message.text.split()
        invited_by = None
        if len(args) > 1 and args[1].startswith('ref'):
            try:
                invited_by = int(args[1][3:])
            except:
                pass

        if not user:
            create_user(
                db,
                message.from_user.id,
                message.from_user.username,
                message.from_user.full_name,
                invited_by
            )

            # Agar kimdir taklif qilgan bo'lsa
            if invited_by:
                count = add_invited_user(db, invited_by)
                inviter = get_user(db, invited_by)

                # Agar 2 ta do'st taklif qilgan bo'lsa - unblock
                if inviter and inviter.is_blocked and count >= 2:
                    unblock_user(db, invited_by)
                    await bot.send_message(
                        invited_by,
                        "🎉 Tabriklaymiz! Siz 2 ta do'stingizni taklif qildingiz.\n"
                        "Endi botdan qayta foydalanishingiz mumkin!"
                    )

        await message.answer(welcome_text, reply_markup=get_conversion_keyboard(), parse_mode="HTML")
    finally:
        db.close()


@router.callback_query(F.data == "mode_to_pdf")
async def to_pdf_mode(callback: CallbackQuery):
    await callback.message.edit_text(
        "📥 <b>TO PDF Konvertatsiya</b>\n\n"
        "Qaysi formatdan PDF ga o'tkazmoqchisiz?\n"
        "Tanlang 👇",
        reply_markup=get_to_pdf_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "mode_from_pdf")
async def from_pdf_mode(callback: CallbackQuery):
    await callback.message.edit_text(
        "📤 <b>FROM PDF Konvertatsiya</b>\n\n"
        "PDF ni qaysi formatga o'tkazmoqchisiz?\n"
        "Tanlang 👇",
        reply_markup=get_from_pdf_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "🔄 Konvertatsiya turini tanlang:",
        reply_markup=get_conversion_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("conv_"))
async def conversion_type_selected(callback: CallbackQuery, state: FSMContext):
    conversion_type = callback.data.replace("conv_", "")
    await state.update_data(conversion_type=conversion_type)
    await state.set_state(ConversionState.waiting_for_conversion_type)

    # Conversion type bo'yicha xabar
    messages = {
        "jpg_pdf": "🖼 JPG rasmni yuboring, men uni PDF ga aylantirib beraman!",
        "word_pdf": "📝 WORD faylni yuboring (.docx)",
        "ppt_pdf": "📊 POWERPOINT faylni yuboring (.pptx)",
        "excel_pdf": "📈 EXCEL faylni yuboring (.xlsx)",
        "html_pdf": "🌐 HTML faylni yuboring (.html)",
        "pdf_jpg": "📷 PDF faylni yuboring, men uni JPG rasmlar ga aylantirib beraman!",
        "pdf_word": "📝 PDF faylni yuboring, men uni WORD ga aylantirib beraman!",
        "pdf_ppt": "📊 PDF faylni yuboring, men uni POWERPOINT ga aylantirib beraman!",
        "pdf_excel": "📈 PDF faylni yuboring, men uni EXCEL ga aylantirib beraman!",
        "pdf_pdfa": "📋 PDF faylni yuboring, men uni PDF/A formatiga aylantirib beraman!"
    }

    await callback.message.edit_text(messages.get(conversion_type, "Faylni yuboring!"))
    await callback.answer()


@router.message(ConversionState.waiting_for_conversion_type)
async def process_conversion(message: Message, state: FSMContext):
    db = SessionLocal()
    try:
        user = get_user(db, message.from_user.id)

        if not user:
            create_user(
                db,
                message.from_user.id,
                message.from_user.username,
                message.from_user.full_name
            )
            user = get_user(db, message.from_user.id)

        # Foydalanuvchi bloklangan bo'lsa
        if user.is_blocked:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="📢 Kanalga obuna bo'lish",
                    url=f"https://t.me/{ADMIN_CHANNEL.replace('@', '')}"
                )],
                [InlineKeyboardButton(
                    text="✅ Obunani tekshirish",
                    callback_data="check_subscription"
                )]
            ])

            await message.answer(
                f"⚠️ Siz limitingizni tugattdingiz!\n\n"
                f"📢 Iltimos, avval {ADMIN_CHANNEL} kanaliga obuna bo'ling va "
                f"2 ta do'stingizni botga taklif qiling.\n\n"
                f"👥 Sizning referal linkingiz:\n"
                f"https://t.me/{(await bot.get_me()).username}?start=ref{message.from_user.id}\n\n"
                f"Taklif qilganlar: {user.invited_count}/2",
                reply_markup=keyboard
            )
            await state.clear()
            return

        # Fayl tekshirish
        if not message.document and not message.photo:
            await message.answer("❌ Iltimos, fayl yuboring!")
            return

        # State dan conversion type olish
        data = await state.get_data()
        conversion_type = data.get('conversion_type')

        if not conversion_type:
            await message.answer("❌ Xatolik! Iltimos, /start dan boshlang.")
            await state.clear()
            return

        # Status xabari
        status_msg = await message.answer("⏳ Fayl yuklab olinmoqda...")

        # Fayl yuklab olish
        file_id = message.document.file_id if message.document else message.photo[-1].file_id
        file = await bot.get_file(file_id)

        # Fayl nomini aniqlash
        if message.document:
            original_name = message.document.file_name
        else:
            original_name = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

        # Fayllarni saqlash
        input_path = f"downloads/{message.from_user.id}_{original_name}"
        os.makedirs("downloads", exist_ok=True)
        await bot.download_file(file.file_path, input_path)

        await status_msg.edit_text("🔄 Konvertatsiya qilinmoqda...")

        # Konvertatsiya
        success = False
        output_files = []

        if conversion_type == "jpg_pdf":
            output_path = f"downloads/{message.from_user.id}_output.pdf"
            success = await image_to_pdf(input_path, output_path)
            output_files = [output_path]

        elif conversion_type == "word_pdf":
            output_path = f"downloads/{message.from_user.id}_output.pdf"
            success = await docx_to_pdf(input_path, output_path)
            output_files = [output_path]

        elif conversion_type == "ppt_pdf":
            output_path = f"downloads/{message.from_user.id}_output.pdf"
            success = await pptx_to_pdf(input_path, output_path)
            output_files = [output_path]

        elif conversion_type == "excel_pdf":
            output_path = f"downloads/{message.from_user.id}_output.pdf"
            success = await xlsx_to_pdf(input_path, output_path)
            output_files = [output_path]

        elif conversion_type == "html_pdf":
            output_path = f"downloads/{message.from_user.id}_output.pdf"
            success = await html_to_pdf(input_path, output_path)
            output_files = [output_path]

        elif conversion_type == "pdf_jpg":
            output_folder = f"downloads/{message.from_user.id}_images"
            image_paths = await pdf_to_images(input_path, output_folder)
            if image_paths:
                success = True
                output_files = image_paths

        elif conversion_type == "pdf_word":
            output_path = f"downloads/{message.from_user.id}_output.docx"
            success = await pdf_to_docx(input_path, output_path)
            output_files = [output_path]

        elif conversion_type == "pdf_ppt":
            output_path = f"downloads/{message.from_user.id}_output.pptx"
            success = await pdf_to_pptx(input_path, output_path)
            output_files = [output_path]

        elif conversion_type == "pdf_excel":
            output_path = f"downloads/{message.from_user.id}_output.xlsx"
            success = await pdf_to_xlsx(input_path, output_path)
            output_files = [output_path]

        elif conversion_type == "pdf_pdfa":
            output_path = f"downloads/{message.from_user.id}_output_pdfa.pdf"
            success = await pdf_to_pdfa(input_path, output_path)
            output_files = [output_path]

        if success and output_files:
            await status_msg.edit_text("📤 Konvertatsiya muvaffaqiyatli! Fayl yuborilmoqda...")

            # Konvertatsiya sonini oshirish
            new_count = increment_conversion(db, message.from_user.id)

            # Agar bir nechta fayl bo'lsa (PDF -> JPG)
            if len(output_files) > 1:
                # ZIP yaratish
                zip_path = f"downloads/{message.from_user.id}_images.zip"
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for img_path in output_files:
                        zipf.write(img_path, os.path.basename(img_path))

                # ZIP faylni yuborish
                await message.answer_document(
                    FSInputFile(zip_path),
                    caption=f"✅ Konvertatsiya muvaffaqiyatli!\n"
                            f"📊 Sizning konvertatsiyalar soni: {new_count}/5"
                )

                # Temp fayllarni tozalash
                os.remove(zip_path)
                shutil.rmtree(output_folder, ignore_errors=True)

            else:
                # Bitta faylni yuborish
                await message.answer_document(
                    FSInputFile(output_files[0]),
                    caption=f"✅ Konvertatsiya muvaffaqiyatli!\n"
                            f"📊 Sizning konvertatsiyalar soni: {new_count}/5"
                )

            # Agar 5 marta konvertatsiya bo'lsa, bloklash
            if new_count >= 5:
                check_and_block_user(db, message.from_user.id)

                # Kanal linkini yuborish
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text="📢 Kanalga obuna bo'lish",
                        url=f"https://t.me/{ADMIN_CHANNEL.replace('@', '')}"
                    )],
                    [InlineKeyboardButton(
                        text="👥 Do'stlarni taklif qilish",
                        callback_data="invite_friends"
                    )]
                ])

                await message.answer(
                    f"⚠️ Siz 5 marta konvertatsiya qildingiz!\n\n"
                    f"📢 Iltimos, {ADMIN_CHANNEL} kanaliga obuna bo'ling va "
                    f"2 ta do'stingizni botga taklif qiling.\n\n"
                    f"👥 Sizning referal linkingiz:\n"
                    f"https://t.me/{(await bot.get_me()).username}?start=ref{message.from_user.id}\n\n"
                    f"Taklif qilganlar: {user.invited_count}/2",
                    reply_markup=keyboard
                )

            # Temp fayllarni tozalash
            for file_path in output_files + [input_path]:
                if os.path.exists(file_path):
                    os.remove(file_path)

        else:
            await status_msg.edit_text("❌ Konvertatsiya muvaffaqiyatsiz! Iltimos, boshqa fayl yuboring.")

        await state.clear()

    except Exception as e:
        logger.error(f"Conversion error: {e}")
        await message.answer("❌ Xatolik yuz berdi! Iltimos, qaytadan urinib ko'ring.")
        await state.clear()
    finally:
        db.close()


@router.callback_query(F.data == "check_subscription")
async def check_subscription(callback: CallbackQuery):
    db = SessionLocal()
    try:
        user = get_user(db, callback.from_user.id)

        if not user:
            await callback.answer("Xatolik! /start ni bosing.")
            return

        # Kanalga obuna bo'lganligini tekshirish
        try:
            member = await bot.get_chat_member(ADMIN_CHANNEL, callback.from_user.id)
            is_subscribed = member.status in ['member', 'administrator', 'creator']
        except:
            is_subscribed = False

        if is_subscribed and user.invited_count >= 2:
            unblock_user(db, callback.from_user.id)
            await callback.message.edit_text(
                "🎉 Tabriklaymiz! Siz kanalga obuna bo'ldingiz va 2 ta do'stingizni taklif qildingiz.\n\n"
                "✅ Endi botdan qayta foydalanishingiz mumkin!",
                reply_markup=get_conversion_keyboard()
            )
        else:
            await callback.answer(
                f"❌ Siz hali kanalga obuna bo'lmagansiz yoki 2 ta do'stingizni taklif qilmagansiz!\n"
                f"Taklif qilganlar: {user.invited_count}/2",
                show_alert=True
            )

    finally:
        db.close()


@router.callback_query(F.data == "invite_friends")
async def invite_friends(callback: CallbackQuery):
    db = SessionLocal()
    try:
        user = get_user(db, callback.from_user.id)

        if not user:
            await callback.answer("Xatolik! /start ni bosing.")
            return

        bot_username = (await bot.get_me()).username
        referral_link = f"https://t.me/{bot_username}?start=ref{callback.from_user.id}"

        invite_text = (
            f"👋 Do'stlaringizni taklif qiling!\n\n"
            f"📎 Sizning taklif havolangiz:\n"
            f"<code>{referral_link}</code>\n\n"
            f"📊 Joriy holat: {user.invited_count}/2 ta do'st taklif qilgansiz\n\n"
            f"✅ 2 ta do'stingiz botga kirgandan so'ng, siz qayta foydalana olasiz!"
        )

        await callback.message.edit_text(
            invite_text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📤 Havolani ulashish", url=f"tg://msg_url?text={referral_link}")],
                [InlineKeyboardButton(text="🔄 Holatni tekshirish", callback_data="check_subscription")],
                [InlineKeyboardButton(text="🔙 Bosh menyu", callback_data="back_to_main")]
            ]),
            parse_mode="HTML"
        )

    finally:
        db.close()


@router.message(Command("stats"))
async def stats_command(message: Message):
    """Admin statistikasi"""
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Sizda bu buyruqni ishlatish huquqi yo'q!")
        return

    db = SessionLocal()
    try:
        total_users = db.query(User).count()
        active_today = db.query(User).filter(
            User.last_conversion >= datetime.now().date()
        ).count()
        total_conversions = db.query(User.conversion_count).scalar() or 0
        blocked_users = db.query(User).filter(User.is_blocked == True).count()

        stats_text = (
            "📊 <b>Bot Statistikasi</b>\n\n"
            f"👥 Jami foydalanuvchilar: {total_users}\n"
            f"📈 Bugun faol: {active_today}\n"
            f"🔄 Jami konvertatsiyalar: {total_conversions}\n"
            f"🚫 Bloklanganlar: {blocked_users}\n"
            f"📅 Hisobot vaqti: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        await message.answer(stats_text, parse_mode="HTML")

    finally:
        db.close()


@router.message(Command("broadcast"))
async def broadcast_command(message: Message):
    """Xabar yuborish (admin uchun)"""
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Sizda bu buyruqni ishlatish huquqi yo'q!")
        return

    if not message.reply_to_message:
        await message.answer("❌ Iltimos, yubormoqchi bo'lgan xabaringizni reply qiling!")
        return

    db = SessionLocal()
    try:
        users = db.query(User).all()
        total = len(users)
        success = 0
        failed = 0

        status_msg = await message.answer(f"📤 Xabar yuborilmoqda... 0/{total}")

        for user in users:
            try:
                await bot.copy_message(
                    user.user_id,
                    message.chat.id,
                    message.reply_to_message.message_id
                )
                success += 1
            except Exception as e:
                logger.error(f"Broadcast error for user {user.user_id}: {e}")
                failed += 1

            if (success + failed) % 10 == 0:
                await status_msg.edit_text(
                    f"📤 Xabar yuborilmoqda... {success + failed}/{total}\n"
                    f"✅ Muvaffaqiyatli: {success}\n"
                    f"❌ Xatolik: {failed}"
                )

        await status_msg.edit_text(
            f"✅ Xabar yuborish yakunlandi!\n"
            f"📊 Natijalar:\n"
            f"• Jami: {total}\n"
            f"• ✅ Muvaffaqiyatli: {success}\n"
            f"• ❌ Xatolik: {failed}"
        )

    finally:
        db.close()


# Error handlers
@router.errors()
async def error_handler(update, exception):
    logger.error(f"Update {update} caused error {exception}")
    return True
