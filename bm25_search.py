import re
from rank_bm25 import BM25Okapi
from chunker import chunk_all_documents

STOPWORDS = {
    "a", "an", "the", "in", "on", "at", "of", "to", "for", "and", "or",
    "is", "are", "was", "were", "be", "do", "does", "did", "how", "what",
    "when", "why", "i", "my", "me", "you", "your", "it", "this", "that",
    "with", "from", "by", "can", "if", "will",
}


def tokenize(text):
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS]


def build_bm25_index(docs_folder="docs"):
    chunks = chunk_all_documents(docs_folder)
    tokenized = [tokenize(c["text"]) for c in chunks]
    bm25 = BM25Okapi(tokenized)
    return bm25, chunks


def bm25_search(query, bm25, chunks, n_results=3):
    tokenized_query = tokenize(query)
    scores = bm25.get_scores(tokenized_query)

    ranked = sorted(
        zip(chunks, scores), key=lambda pair: pair[1], reverse=True
    )
    return ranked[:n_results]


if __name__ == "__main__":
    bm25, chunks = build_bm25_index()
    results = bm25_search("E-4012", bm25, chunks)

    for chunk, score in results:
        print("---")
        print(chunk["chunk_id"], "| score:", score)
        print(chunk["text"][:100])
