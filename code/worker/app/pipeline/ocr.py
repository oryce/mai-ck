from PIL.Image import Image
from pytesseract import image_to_string


def ocr(images: list[Image]) -> str:
    """
    Принимает список изображений (страниц документа),
    возвращает объединённый результат OCR по всем страницам.
    """
    full_text = []

    for i, img in enumerate(images):
        try:
            text = image_to_string(img, lang="rus")
            full_text.append(text)
        except Exception as e:
            full_text.append(f"[Ошибка при распознавании страницы {i}: {e}]")

    return "\n".join(full_text)
