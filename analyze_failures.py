from run_eval import load_test_set, hit_at_k, eval_vector_only, eval_bm25_only, eval_hybrid

methods = {"vector": eval_vector_only, "bm25": eval_bm25_only, "hybrid": eval_hybrid}

for row in load_test_set("eval/questions_heldout.csv"):
    q, correct = row["question"], row["correct_chunk_id"]
    got = {name: fn(q, 3) for name, fn in methods.items()}
    hybrid_top1 = hit_at_k(got["hybrid"], correct, 1)
    any_miss3 = any(not hit_at_k(r, correct, 3) for r in got.values())
    if hybrid_top1 and not any_miss3:
        continue
    print("Q:", q)
    print("  correct:", correct)
    for name, r in got.items():
        print(f"  {name:<7} top-3: {r}  top-1 hit: {hit_at_k(r, correct, 1)}  top-3 hit: {hit_at_k(r, correct, 3)}")
    print()
