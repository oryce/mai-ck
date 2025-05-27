from pdf2image import convert_from_path
from PIL.Image import Image


def split_pdf_to_images(document_path: str) -> list[Image]:
    """
    Разбивает PDF-документ на изображения для каждой страницы.

    :param pdf_path: Путь к PDF-файлу.
    :return: Список изображений (PIL.Image).
    """
    return convert_from_path(document_path)
