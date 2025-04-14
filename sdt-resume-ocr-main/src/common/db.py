import logging

import psycopg2
from psycopg2 import OperationalError

from src.common.config import DBConfig

logger = logging.getLogger(__name__)


class DB:
    def __init__(self, db_config: DBConfig):
        try:
            self.connection = psycopg2.connect(
                database=db_config.database,
                user=db_config.username,
                password=db_config.password,
                host=db_config.host,
                port=db_config.port,
            )

            logger.info(f'Connected to database: {db_config.host}:{db_config.port}/{db_config.database}')
        except OperationalError as e:
            logger.error('Failed to connect to database: %s', e)
            raise
