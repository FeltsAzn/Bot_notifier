import os
from dotenv import load_dotenv
from src.logger import logger
from src.bot import multiproc_app, start_app_on_one_thread



if __name__ == "__main__":
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    multiproc_config = os.getenv("MULTIPROCESSORING")

    match multiproc_config.upper():
        case "ON":
            logger.info("Start on multiprocessing mod")
            multiproc_app()
        case _:
            logger.info("Start on one thread mod")
            start_app_on_one_thread()
