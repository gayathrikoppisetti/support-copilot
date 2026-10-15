from search_test import search as embedding_search
from bm25_search import build_bm25_index, bm25_search

bm25_index, bm25_chunks = build_bm25_index()


def hybrid_retrieve(query, n_results=3, k=60):
    embed_results = embedding_search(query, n_results=10)
    embed_ids = embed_results["ids"][0]

    bm25_results = bm25_search(query, bm25_index, bm25_chunks, n_results=10)
    bm25_ids = [chunk["chunk_id"] for chunk, score in bm25_results]

    scores = {}
    for rank, chunk_id in enumerate(embed_ids):
        scores[chunk_id] = scores.get(chunk_id, 0) + 1 / (k + rank + 1)

    for rank, chunk_id in enumerate(bm25_ids):
        scores[chunk_id] = scores.get(chunk_id, 0) + 1 / (k + rank + 1)

    chunk_lookup = {c["chunk_id"]: c for c in bm25_chunks}
    ranked = sorted(scores.items(), key=lambda pair: pair[1], reverse=True)

    results = []
    for chunk_id, rrf_score in ranked[:n_results]:
        results.append({
            "chunk_id": chunk_id,
            "rrf_score": rrf_score,
            "text": chunk_lookup[chunk_id]["text"],
        })
    return results


if __name__ == "__main__":
    for query in ["why am I not getting notifications", "E-4012"]:
        print("=== Query:", query, "===")
        for r in hybrid_retrieve(query):
            print("---")
            print(r["chunk_id"], "| rrf_score:", round(r["rrf_score"], 4))
            print(r["text"][:100])
        print()
