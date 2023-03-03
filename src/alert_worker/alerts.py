import time
import functools
import redis
from emoji import emojize
from aiogram.utils import markdown, exceptions
from aiohttp.client_exceptions import ClientConnectorError
from loader import bot
from logger import logger
from alert_worker import http_req
from alert_worker.alerts_exception_handler import UnexpectedException
from load_virtual_variables import MAIN_ADMIN
from middleware import async_get_all_users, update_users_list_async


class NotificationAlerter:
    USERS_CACHE = {}

    @staticmethod
    def exception_middleware(func):
            @functools.wraps(func)
            async def wrapped(self) -> None:
                try:
                    return await func(self)
                except ClientConnectorError:
                    logger.exception("Telegram connection refused. Timeout 10 second activated")
                    time.sleep(10)
                except (TypeError, AttributeError, redis.exceptions.ConnectionError) as ex:
                    logger.exception(f"Exception on alerts loop: {ex}")
                    for tg_id, state in self.USERS_CACHE.items():
                        if state == "ACTIVATED":
                            await UnexpectedException(tg_id, bot).exception_handler()
                    raise SystemError
            return wrapped

    async def update_user_cache(self) -> None:
        """
        Updating cache after app launching or after adding new user
        """
        self.USERS_CACHE = await async_get_all_users()

    @exception_middleware
    async def background_task(self) -> None:
        """
        Mainloop with requests to backend and sending notifications to telegram users
        """
        await update_users_list_async()
        while True:
            await self.update_user_cache()
            raw_data = await http_req.exchanges_data_collector()
            content = await http_req.give_finished_text(*raw_data)
            await self.send_message(content)

    async def send_message(self, content: list) -> None:
        if content != [] and self.USERS_CACHE:
            for tg_id, data in self.USERS_CACHE.items():
                if data["state"] == "ACTIVATED":
                    try:
                        await bot.send_message(chat_id=int(tg_id),
                                               text=emojize(markdown.text(*content), language="alias"),
                                               parse_mode="html")
                    except exceptions.BotBlocked as ex:
                        logger.warning(f"Message didn't send to user {tg_id}. {ex}")
                        await bot.send_message(chat_id=MAIN_ADMIN, text=f"Message not sent to user {tg_id}. "
                                                                        f"He is blocked bot")
