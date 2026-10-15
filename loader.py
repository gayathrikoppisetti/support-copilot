from pathlib import Path


def load_document(path):
    text = Path(path).read_text(encoding="utf-8")
    metadata = {}
    body = text

    if text.startswith("---"):
        _, header, body = text.split("---", 2)
        for line in header.strip().splitlines():
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()

    return {
        "source": Path(path).name,
        "metadata": metadata,
        "text": body.strip(),
    }


if __name__ == "__main__":
    doc = load_document("docs/faq.md")
    print(doc["source"])
    print(doc["metadata"])
    print(len(doc["text"]), "characters")
    print(doc["text"][:200])


def load_all_documents(folder):
    documents = []
    for path in Path(folder).glob("*.md"):
        documents.append(load_document(path))
    return documents
