import scrapper
import logging
from db import check_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Checking connection with DB")
    check_connection.con_check()
    logger.info("Success")
    scrapper.run()
