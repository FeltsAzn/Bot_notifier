import datetime
import logging

logging.basicConfig(filename=f'logs/logs_{datetime.datetime.now()}.txt',
                    filemode='w',
                    format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s",
                    encoding='utf-8',
                    level='DEBUG', )
logger = logging.getLogger('MAIN_LOGGER')

