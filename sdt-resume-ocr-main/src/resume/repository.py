import logging
from typing import Optional

from psycopg2 import OperationalError

from src.common import DB
from .resume import Resume

logger = logging.getLogger(__name__)


class ResumeRepository:
    def __init__(self, db: DB):
        self._db = db
        self._table_name = 'resume'

    def find_by_id(self, resume_id: int) -> Optional[Resume]:
        try:
            query = f'select * from {self._table_name} where id = %s;'

            cursor = self._db.connection.cursor()
            cursor.execute(query, (resume_id,))

            row = cursor.fetchone()
            if row is None:
                return None

            return Resume(
                resume_id=row[0],
                object_path=row[1],
                ocr_result=row[2],
                parse_result=row[3],
                state=row[4],
            )
        except OperationalError as e:
            logger.error('Database error: %s', e)
            raise

    def update_state(self, resume_id: int, state: Resume.State) -> None:
        try:
            query = f'update {self._table_name} set state = %s where id = %s;'

            cursor = self._db.connection.cursor()
            cursor.execute(query, (state.name, resume_id))

            self._db.connection.commit()
        except OperationalError as e:
            logger.error('Database error: %s', e)
            raise

    def update_ocr_result(self, resume_id: int, ocr_result: str) -> None:
        try:
            query = f'update {self._table_name} set ocr_result = %s where id = %s;'

            cursor = self._db.connection.cursor()
            cursor.execute(query, (ocr_result, resume_id))

            self._db.connection.commit()
        except OperationalError as e:
            logger.error('Database error: %s', e)
            raise
