import asyncio
import io
import logging
import subprocess
import numpy as np
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters import Command
from faster_whisper import WhisperModel

# import os
# TOKEN = os.getenv("BOT_TOKEN") 
# Надо будет скрыть токен и поменять, чтобы он не лежал в открытом доступе

TOKEN = "8219545385:AAGMnxx0qn9Wp3FwnwHK9vxNeBhi4TY3HJ0"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

whisper_model = WhisperModel("tiny", device="cpu", compute_type="int8") # Silly model


def transcribe_sync(audio: io.BytesIO) -> str: # Перевод аудиофайла в текст
    pcm = subprocess.run(
        ["ffmpeg", "-i", "pipe:0", "-f", "s16le", "-ac", "1", "-ar", "16000", "pipe:1"],
        input=audio.getvalue(),
        check=True,
        capture_output=True,
    ).stdout
    samples = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0

    segments, _info = whisper_model.transcribe(
        samples, language="ru", vad_filter=True, beam_size=5
    )
    return " ".join(seg.text for seg in segments).strip()


@router.message(Command("start")) # Стартовая команда
async def cmd_start(message: types.Message):
    await message.answer("Привет! Отправь мне голосовое сообщение.")


@router.message(F.voice) # Обработка голосовых сообщений
async def handle_voice(message: types.Message):
    status = await message.answer("🎧 Распознаю...")

    try:
        file = await bot.get_file(message.voice.file_id)
        buffer = io.BytesIO()
        await bot.download_file(file.file_path, destination=buffer)
        buffer.seek(0)

        text = await asyncio.to_thread(transcribe_sync, buffer)

        await status.edit_text(f"📝 {text}" if text else "Речь не распознана.")
    except Exception as e:
        logging.exception("Ошибка распознавания")
        await status.edit_text(f"❌ Ошибка: {e}")


@router.message() # Информация для отладки
async def debug_all(message: types.Message):
    logging.info("Получено: content_type=%s, chat=%s", message.content_type, message.chat.type)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())