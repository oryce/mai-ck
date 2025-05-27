import os

from ollama import Client


def get_document_type(document_text: str, allowed_types: list[str], model: str) -> str:
    """
    Отправляет оцифрованный текст документа в модель Ollama для классификации его типа.

    :param text: Оцифрованный текст документа.
    :param allowed_types: Допустимые типы документа (например, "договор", "счет", "накладная").
    """

    system_prompt = f"""
You are a document-classification assistant. You will be given the plain text output of an OCR engine. 
Your sole task is to assign the document to **exactly one** of the following types:

{"\n".join(map(lambda ty: f"* {ty}", allowed_types))}

**Requirements:**

* Always choose one—and only one—type from the list above.
* Reply **only** with the chosen type's name, matching it character-for-character (including capitalization),
  and **nothing else**.
* If the document contains a phrase that includes one of the allowed types as a whole word (e.g., "Приказ" in
 "Судебный приказ"), you must still reply with the base type ("Приказ").
* Do not add any punctuation, comments, or extra words.
* If the document does not clearly match any of the types, reply with `Unknown`.
"""

    client = Client(os.getenv("OLLAMA_URL"))

    response = client.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": document_text},
        ],
    )

    return response.message.content.strip()
