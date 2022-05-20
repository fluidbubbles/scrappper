import logging


from db.session import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def con_check() -> None:

    try:
        # Try to create session to check if DB is awake
        engine.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e
