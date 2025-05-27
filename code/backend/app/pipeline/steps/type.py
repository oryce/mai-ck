import os

from ollama import Client


def get_document_type(text: str, tag_names: list[str]) -> str:
    """
    Отправляет оцифрованный текст документа в модель Ollama для классификации его типа.

    :param text: Оцифрованный текст документа.
    :param tag_names: Список тегов
    :return: Тип документа (например, "Договор", "Счет", "Накладная").
    """

    system_prompt = f"""
You are a document-classification assistant. You will be given the plain text output of an OCR engine. 
Your sole task is to assign the document to **exactly one** of the following types:

{"\n".join(map(lambda tag: f"* {tag}", tag_names))}

**Requirements:**

* Always choose one—and only one—type from the list above.
* Reply **only** with the chosen type's name, matching it character-for-character (including capitalization),
  and **nothing else**.
* Do not add any punctuation, comments, or extra words.
* If the document does not clearly match any of the types, reply with `Unknown`.
"""

    client = Client("http://localhost:11434")

    response = client.chat(
        model=os.getenv("LLM_MODEL"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
    )

    print(response.message.content)

    return response.message.content
