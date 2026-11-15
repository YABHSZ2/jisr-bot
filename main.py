import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def start_handler(message: Message):
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📚 تعلّم الإشارات", callback_data="learn")],
            [InlineKeyboardButton(text="🔍 القاموس", callback_data="dict")],
            [InlineKeyboardButton(text="🎥 ترجم إشارتي", callback_data="translate")]
        ])
        await message.answer(
            f"مرحباً {message.from_user.first_name} 👋\n"
            "أنا *جسر* — جسر التواصل بلغة الإشارة العربية.\n"
            "اختر ما تريد:",
            reply_markup=kb,
            parse_mode="Markdown"
        )

    @dp.callback_query(F.data == "dict")
    async def dict_handler(callback: CallbackQuery):
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👋 تحيات", callback_data="dict_greet")],
            [InlineKeyboardButton(text="🔙 عودة للقائمة", callback_data="back_to_main")]
        ])
        await callback.message.edit_text("اختر فئة من القاموس:", reply_markup=kb)
        await callback.answer()

    @dp.callback_query(F.data == "dict_greet")
    async def dict_greet_handler(callback: CallbackQuery):
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 عودة للقاموس", callback_data="dict")]
        ])
        await callback.message.edit_text("كلمة (مرحباً): هنا سيتم عرض فيديو الإشارة قريباً جداً! 🎥", reply_markup=kb)
        await callback.answer()

    @dp.callback_query(F.data == "back_to_main")
    async def back_handler(callback: CallbackQuery):
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📚 تعلّم الإشارات", callback_data="learn")],
            [InlineKeyboardButton(text="🔍 القاموس", callback_data="dict")],
            [InlineKeyboardButton(text="🎥 ترجم إشارتي", callback_data="translate")]
        ])
        await callback.message.edit_text("أنا *جسر* — جسر التواصل بلغة الإشارة العربية.\nاختر ما تريد:", reply_markup=kb, parse_mode="Markdown")
        await callback.answer()

    @dp.callback_query(F.data == "learn")
    async def learn_handler(callback: CallbackQuery):
        await callback.message.answer("هنا سنضع دروس تعلم الإشارات قريباً! 🚀")
        await callback.answer()

    @dp.callback_query(F.data == "translate")
    async def translate_handler(callback: CallbackQuery):
        await callback.message.answer("هنا ستتمكن من إرسال فيديو لترجمته قريباً! 🎥")
        await callback.answer()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
