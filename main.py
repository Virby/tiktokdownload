from aiogram import Bot, Dispatcher, executor, types
import requests
import re

API_TOKEN = '336188380:AAEmoL5G2qZtTN_0MsAfqYQs2PNzkCbc-Jk'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Функция для получения ссылки на видео без водяного знака
def get_tiktok_video(url):
    api_url = "https://api.tikmate.app/api/lookup"
    try:
        # Получаем ID видео
        video_id = re.search(r"video/(\d+)", url).group(1)
        res = requests.get(f"{api_url}?url=https://www.tiktok.com/@user/video/{video_id}")
        data = res.json()
        download_url = f"https://tikmate.app/download/{data['token']}/{data['id']}.mp4"
        return download_url
    except Exception as e:
        print("Error:", e)
        return None

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Отправь мне ссылку на видео из TikTok, и я пришлю его без водяного знака.")

@dp.message_handler()
async def handle_tiktok_link(message: types.Message):
    url = message.text.strip()
    if "tiktok.com" not in url:
        await message.answer("Пожалуйста, пришли корректную ссылку на видео TikTok.")
        return

    await message.answer("🔄 Загружаю видео...")

    video_url = get_tiktok_video(url)
    if video_url:
        await bot.send_video(message.chat.id, video_url)
    else:
        await message.answer("❌ Не удалось получить видео. Попробуйте позже.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
