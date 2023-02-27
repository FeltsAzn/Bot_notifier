import logging
import sys


logging.basicConfig(format="%(asctime)s — %(name)s — %(levelname)s — %(filename)s/%(funcName)s:%(lineno)d — %(message)s",
                    encoding="utf-8",
                    level="INFO",)
handler = logging.StreamHandler(stream=sys.stdout)
logger = logging.getLogger("MAIN_LOGGER")
logger.addHandler(handler)
