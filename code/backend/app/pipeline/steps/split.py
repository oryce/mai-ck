from pdf2image import convert_from_path
from PIL import Image


def split_pdf_to_images(pdf_path: str) -> list[Image]:
    """
    Разбивает PDF-документ на изображения для каждой страницы.

    :param pdf_path: Путь к PDF-файлу.
    :return: Список изображений (PIL.Image).
    """
    images = convert_from_path(pdf_path)

    return images
