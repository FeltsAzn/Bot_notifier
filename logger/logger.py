import logging

logging.basicConfig(filename='logs.txt',
                    filemode='w',
                    format='%(asctime)s %(message)s',
                    encoding='utf-8',
                    level='DEBUG', )
logger = logging.getLogger('Program_logger')
