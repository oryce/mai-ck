from typing import List

import requests


def get_document_type(text: str, tag_names: List[str]) -> str:
    """
    Отправляет оцифрованный текст документа в модель Ollama для классификации его типа.

    :param text: Оцифрованный текст документа.
    :param tag_names: Список тегов
    :return: Тип документа (например, "Договор", "Счет", "Накладная").
    """

    prompt = (f"Answer in Russian."
              f"Determine the type of this document based on the text. Answer only with the document type, "
              f"no additional words besides the document type.  "
              f"The type of the document is your entire response, "
              f"for example, 'purchase and sale agreement' and that's it, nothing more."
              f"Choose one document type from the following list : {tag_names}"
              f"Text of the document:\n{text}\n")
    ollama_api_url = 'http://ollama:11434/api/generate'

    payload = {
        "prompt": prompt,
        "model": "gemma3",
        "stream": False
    }

    response = requests.post(ollama_api_url, json=payload)

    if response.status_code == 200:
        response_data = response.json()
        document_type = response_data["response"]
        return document_type
    else:
        raise Exception(f"Ошибка при запросе к Ollama API: {response.status_code} - {response.text}")
