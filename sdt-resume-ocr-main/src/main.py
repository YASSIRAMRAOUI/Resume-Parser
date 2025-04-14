import logging

from dotenv import load_dotenv

from src.common import Config, DB, Kafka, Minio
from src.ocr import OcrService
from src.resume import ResumeRepository

logger = logging.getLogger(__name__)


def main():
    load_dotenv()

    logging.basicConfig(level=logging.INFO)

    config = Config()

    db = DB(config.db_config)
    kafka = Kafka(config.kafka_config)
    minio = Minio(config.minio_config)

    resume_repository = ResumeRepository(db)

    ocr = OcrService(kafka, resume_repository, minio)

    ocr.start()


if __name__ == '__main__':
    main()
