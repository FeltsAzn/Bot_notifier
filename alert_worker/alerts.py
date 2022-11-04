from loader import bot
import asyncio
import random


async def background_alerts():
    while True:
        text = "** Уведомление с изменением цен **"
        # await bot.send_message(chat_id=5703780641, text=text)
        await asyncio.sleep(random.randint(5, 20))

# TODO Обращение к сервису

