from logger import logger
from bot import multiproc_app, start_app_on_one_thread
from load_virtual_variables import MULTIPROCESS_CONFIG


if __name__ == "__main__":
    match MULTIPROCESS_CONFIG.upper():
        case "ON":
            logger.info("Start on multiprocessing mod")
            multiproc_app()
        case _:
            logger.info("Start on one thread mod")
            start_app_on_one_thread()
