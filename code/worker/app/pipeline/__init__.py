from dataclasses import dataclass
from enum import Enum
from typing import Generator

from .ocr import ocr
from .preview import create_preview
from .signature_stamp import find_signature_stamp
from .split import split_pdf_to_images
from .type import get_document_type


class Status(Enum):
    PREPROCESSING = 1
    PROCESSING = 2
    FINISHED = 3


@dataclass
class Result:
    type: str
    signature: bool
    stamp: bool


def run(
    document_path: str, allowed_types: list[str], model: str
) -> Generator[Status | Result, None, None]:
    yield Status.PREPROCESSING
    images = split_pdf_to_images(document_path)
    create_preview(document_path, images)
    signature, stamp = find_signature_stamp(images)

    yield Status.PROCESSING
    text = ocr(images)
    type = get_document_type(text, allowed_types, model)

    yield Result(type, signature, stamp)
    yield Status.FINISHED
