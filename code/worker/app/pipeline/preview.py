from pathlib import Path

from PIL import Image as PILImage
from PIL.Image import Image


def create_preview(document_path: str, images: list[Image]) -> str:
    """
    Сохраняет превью первой страницы в JPG-файл <имя>_preview.jpg
    рядом с исходным PDF. Превью ~300×300 px (длинная сторона = 300 px).

    :param document_path: Путь к исходному PDF (например, /path/to/file.pdf)
    :param images: Список PIL-изображений страниц документа
    :return: Путь к созданному превью
    """
    if not images:
        raise ValueError("Список images пуст — превью создать невозможно")

    # Копируем первую страницу, чтобы не мутировать оригинал
    preview_img = images[0].copy()

    # JPEG требует RGB
    if preview_img.mode != "RGB":
        preview_img = preview_img.convert("RGB")

    # Масштабируем: длинная сторона → 300 px
    w, h = preview_img.size
    long_side = max(w, h)
    if long_side != 300:  # перерасчёт даже для маленьких картинок
        scale = 300 / long_side
        new_size = (int(round(w * scale)), int(round(h * scale)))
        preview_img = preview_img.resize(new_size, PILImage.LANCZOS)

    # Имя файла: file_preview.jpg
    doc_path = Path(document_path)
    preview_path = doc_path.with_name(f"{doc_path.stem}_preview.jpg")

    # Сохраняем с разумным качеством
    preview_img.save(
        preview_path, format="JPEG", quality=85, optimize=True, progressive=True
    )

    return str(preview_path)
