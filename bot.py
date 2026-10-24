import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command

# Замените 'YOUR_BOT_TOKEN' на токен, полученный от BotFather
TOKEN = "8219545385:AAGMnxx0qn9Wp3FwnwHK9vxNeBhi4TY3HJ0"

# Включаем логирование, чтобы видеть ошибки и статус
logging.basicConfig(level=logging.INFO)

# Инициализируем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
  await message.answer("Привет! Я твой новый бот на Python.")


# Обработчик любых текстовых сообщений (эхо-бот)
@dp.message()
async def echo_message(message: types.Message):
  await message.send_copy(chat_id=message.chat.id)


async def main():
  # Запуск процесса опроса серверов Telegram
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())
