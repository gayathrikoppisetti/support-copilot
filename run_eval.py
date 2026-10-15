import csv
from search_test import search as embedding_search
from bm25_search import build_bm25_index, bm25_search
from hybrid_search import hybrid_retrieve

bm25_index, bm25_chunks = build_bm25_index()


def load_test_set(path="eval/questions.csv"):
    with open(path) as f:
        return list(csv.DictReader(f))


def hit_at_k(retrieved_ids, correct_id, k):
    return any(x in retrieved_ids[:k] for x in correct_id.split("|"))


def eval_vector_only(question, k):
    results = embedding_search(question, n_results=k)
    return results["ids"][0]


def eval_bm25_only(question, k):
    results = bm25_search(question, bm25_index, bm25_chunks, n_results=k)
    return [chunk["chunk_id"] for chunk, score in results]


def eval_hybrid(question, k):
    results = hybrid_retrieve(question, n_results=k)
    return [r["chunk_id"] for r in results]


def run_eval(path="eval/questions.csv"):
    test_set = load_test_set(path)
    methods = {
        "vector_only": eval_vector_only,
        "bm25_only": eval_bm25_only,
        "hybrid": eval_hybrid,
    }
    k_values = [1, 3, 5]

    scores = {m: {k: 0 for k in k_values} for m in methods}

    for row in test_set:
        question = row["question"]
        correct_id = row["correct_chunk_id"]

        for method_name, method_fn in methods.items():
            retrieved = method_fn(question, max(k_values))
            for k in k_values:
                if hit_at_k(retrieved, correct_id, k):
                    scores[method_name][k] += 1

    n = len(test_set)
    print(f"Evaluated on {n} questions from {path}\n")
    print(f"{'Method':<15} {'Top-1':<10} {'Top-3':<10} {'Top-5':<10}")
    for method_name in methods:
        row = scores[method_name]
        print(f"{method_name:<15} "
              f"{row[1]/n:.0%}".ljust(25) +
              f"{row[3]/n:.0%}".ljust(10) +
              f"{row[5]/n:.0%}")


if __name__ == "__main__":
    import sys
    run_eval(sys.argv[1] if len(sys.argv) > 1 else "eval/questions.csv")


def diagnose():
    test_set = load_test_set()
    for row in test_set:
        question = row["question"]
        correct_id = row["correct_chunk_id"]

        vec = eval_vector_only(question, 3)
        hyb = eval_hybrid(question, 3)

        vec_hit = hit_at_k(vec, correct_id, 3)
        hyb_hit = hit_at_k(hyb, correct_id, 3)

        if vec_hit and not hyb_hit:
            print(f"Q: {question}")
            print(f"  correct: {correct_id}")
            print(f"  vector top-3: {vec}")
            print(f"  hybrid top-3: {hyb}")
            print()
