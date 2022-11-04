from aiogram import executor
from loader import dp
import heandlers
from alert_worker import alerts


def start_bot():
    try:
        dp.loop.create_task(alerts.background_alerts())
        executor.start_polling(dp, skip_updates=True)
    except Exception as ex:
        print(ex)
        start_bot()


if __name__ == '__main__':
    start_bot()


