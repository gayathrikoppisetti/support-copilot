import re
from loader import load_all_documents


def chunk_document(doc):
    text = doc["text"]
    parts = re.split(r"\n(?=## )", text)

    chunks = []
    for i, part in enumerate(parts):
        part = part.strip()
        if not part or len(part) < 40:
            continue
        chunks.append({
            "chunk_id": f"{doc['source']}::{i}",
            "source": doc["source"],
            "metadata": doc["metadata"],
            "text": doc["metadata"].get("title", doc["source"]) + "\n" + part,
        })
    return chunks


def chunk_all_documents(folder):
    all_chunks = []
    for doc in load_all_documents(folder):
        all_chunks.extend(chunk_document(doc))
    return all_chunks


if __name__ == "__main__":
    chunks = chunk_all_documents("docs")
    print("Total chunks:", len(chunks))
    for c in chunks[:3]:
        print("---")
        print(c["chunk_id"])
        print(c["text"][:150])
