from typing import Any


def rearrange_text(ocr_result: list[tuple[Any, ...]]) -> str:
    return " ".join([result[1] for result in ocr_result])