import pytesseract
from PIL.Image import Image


def ocr(images: list[Image]) -> str:
    """
    Принимает список изображений (страниц документа),
    возвращает объединённый результат OCR по всем страницам.
    """
    full_text = []

    for i, img in enumerate(images):
        try:
            text = pytesseract.image_to_string(img, lang='rus+eng')
            full_text.append(text)
        except Exception as e:
            full_text.append(f"[Ошибка при распознавании страницы {i}: {e}]")

    return "\n".join(full_text)