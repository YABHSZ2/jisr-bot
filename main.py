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
        await message.answer("أرسل لي الفيديو الآن لأعطيك الكود الخاص به.")

    @dp.message(F.video)
    async def get_video_id(message: Message):
        # هذه المرة سنرسل الكود في رسالة قابلة للنسخ بضغطة واحدة
        await message.answer(
            f"هذا هو الكود الخاص بالفيديو، اضغط عليه لنسخه:\n\n<code>{message.video.file_id}</code>", 
            parse_mode="HTML"
        )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())