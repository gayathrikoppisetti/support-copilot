import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("taskly_docs")
model = SentenceTransformer("all-MiniLM-L6-v2")


def search(query, n_results=3):
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
    )
    return results


if __name__ == "__main__":
    query = "why am I not getting notifications"
    results = search(query)

    for i in range(len(results["ids"][0])):
        print("---")
        print("chunk_id:", results["ids"][0][i])
        print("distance:", results["distances"][0][i])
        print("text:", results["documents"][0][i][:150])
