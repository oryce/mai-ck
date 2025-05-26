import requests


def get_document_type(text: str) -> str:
    """
    Отправляет оцифрованный текст документа в модель Ollama для классификации его типа.

    :param text: Оцифрованный текст документа.
    :return: Тип документа (например, "Договор", "Счет", "Накладная").
    """

    prompt = (f"Отвечай на русском."
              f"Определите тип этого документа на основе текста. Ответьте только типом документа,"
              f"никаких дополнительных слов, помимо типа докмуента. "
              f"Тип документа - это весшь ваш ответ, например, 'договор купли-продажи' и все, больше ничего."
              f"Текст докмуента:\n{text}\n")
    ollama_api_url = 'http://ollama:11434/api/generate'

    payload = {
        "prompt": prompt,
        "model": "llama2",
        "stream": False
    }

    response = requests.post(ollama_api_url, json=payload)

    if response.status_code == 200:
        response_data = response.json()
        document_type = response_data["response"]
        return document_type
    else:
        raise Exception(f"Ошибка при запросе к Ollama API: {response.status_code} - {response.text}")
