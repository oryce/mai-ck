import requests


def get_document_type(text: str) -> str:
    """
    Отправляет оцифрованный текст документа в модель Ollama для классификации его типа.

    :param text: Оцифрованный текст документа.
    :return: Тип документа (например, "Договор", "Счет", "Накладная").
    """

    prompt = f"Определите тип этого документа на основе текста:\n{text}\nОтветьте только типом документа."

    ollama_api_url = 'http://ollama:11431/v1/complete'

    payload = {
        "prompt": prompt,
        "model": "llama-2",
    }

    response = requests.post(ollama_api_url, json=payload)

    if response.status_code == 200:
        response_data = response.json()
        document_type = response_data.get("text", "").strip()
        return document_type
    else:
        raise Exception(f"Ошибка при запросе к Ollama API: {response.status_code} - {response.text}")
