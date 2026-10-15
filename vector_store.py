import chromadb
from sentence_transformers import SentenceTransformer
from chunker import chunk_all_documents


def build_vector_store(docs_folder="docs", db_path="chroma_db"):
    chunks = chunk_all_documents(docs_folder)

    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts).tolist()

    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection("taskly_docs")

    collection.add(
        ids=[c["chunk_id"] for c in chunks],
        embeddings=embeddings,
        documents=texts,
        metadatas=[{"source": c["source"], **c["metadata"]} for c in chunks],
    )

    return collection


if __name__ == "__main__":
    collection = build_vector_store()
    print("Chunks stored:", collection.count())
