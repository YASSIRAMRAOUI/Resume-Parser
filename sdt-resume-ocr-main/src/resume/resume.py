from enum import Enum


class Resume:
    class State(Enum):
        WAITING = 'WAITING'
        OCR_QUEUED = 'OCR_QUEUED'
        OCR_IN_PROGRESS = 'OCR_IN_PROGRESS'
        OCR_DONE = 'OCR_DONE'
        OCR_FAILED = 'OCR_FAILED'
        PARSE_IN_PROGRESS = 'PARSE_IN_PROGRESS'
        PARSE_DONE = 'PARSE_DONE'
        PARSE_FAILED = 'PARSE_FAILED'

    def __init__(self, resume_id: int, object_path: str, ocr_result: str, parse_result: str, state: State):
        self.id = resume_id
        self.object_path = object_path
        self.ocr_result = ocr_result
        self.parse_result = parse_result
        self.state = state
