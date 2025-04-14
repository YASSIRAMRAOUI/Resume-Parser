import logging
import os.path
import tempfile

import easyocr
from pdf2image import convert_from_bytes

from src.common import Kafka, Minio
from src.resume import ResumeRepository, Resume
from src.utils import rearrange_text

logger = logging.getLogger(__name__)


class OcrService:
    def __init__(self, kafka: Kafka, resume_repository: ResumeRepository, minio: Minio):
        self._kafka = kafka
        self._resume_repository = resume_repository
        self._minio = minio
        self._reader = easyocr.Reader(['en'])

    def start(self) -> None:
        self._kafka.listen('ocr_requests', lambda message: self._process_resume(int(message)))

    def _process_resume(self, resume_id: int) -> None:
        resume = self._resume_repository.find_by_id(resume_id)

        if resume is None:
            logger.error('Resume id=%d not found', resume_id)
            return

        try:
            logger.info('Processing resume %d', resume_id)
            self._resume_repository.update_state(resume_id, Resume.State.OCR_IN_PROGRESS)

            text = self._pdf_to_text(resume.object_path)
            self._resume_repository.update_ocr_result(resume_id, text)

            logger.info('Finished processing resume %d successfully', resume_id)
            self._resume_repository.update_state(resume_id, Resume.State.OCR_DONE)
        except RuntimeError as e:
            logger.error('Failed to process resume %d: %s', resume_id, e)
            self._resume_repository.update_state(resume_id, Resume.State.OCR_FAILED)

        self._kafka.send('ocr_responses', str(resume.id))

    def _pdf_to_text(self, object_path: str) -> str:
        bucket_name, object_name = os.path.split(object_path)
        object_bytes = self._minio.get_object_bytes(bucket_name, object_name)

        with (tempfile.TemporaryDirectory() as tmpdir):
            convert_from_bytes(object_bytes, output_folder=tmpdir, fmt='jpg')
            images = os.listdir(tmpdir)

            ocr_result = [result for image in images for result in self._reader.readtext(os.path.join(tmpdir, image))]

            return rearrange_text(ocr_result)
