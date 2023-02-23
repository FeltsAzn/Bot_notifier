import datetime
import logging
import os

logs_path = os.path.join(os.path.dirname(__file__), "../logs")
if not os.path.exists(logs_path):
    os.makedirs(logs_path)
logging.basicConfig(filename=f"logs/logs_{datetime.datetime.now()}.log",
                    filemode="w",
                    format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s",
                    encoding="utf-8",
                    level="INFO",)
logger = logging.getLogger("MAIN_LOGGER")

