# Support Copilot: Hybrid-Search RAG with Answer Verification

A retrieval-augmented question-answering system built from scratch in Python (no orchestration framework). It answers support questions from a small document set, cites its sources, and fact-checks each answer against the retrieved text before showing it.

This is a learning project. The corpus is **synthetic** (six documents for a fictional product called "Taskly"), and the evaluation sets are small. See [Limitations](#limitations) before drawing conclusions from the numbers.

## Pipeline

```
documents -> loader (metadata + text) -> heading-based chunker (title prepended)
          -> embeddings (all-MiniLM-L6-v2) -> ChromaDB
          -> BM25 index (custom tokenizer, stopwords removed)

question -> dense search + BM25 -> Reciprocal Rank Fusion (k=60)
         -> top-3 chunks -> LLM answer with citations (Groq)
         -> LLM-as-judge verification -> SUPPORTED / PARTIALLY_SUPPORTED / UNSUPPORTED
```

Served through FastAPI (`api.py`) and a Streamlit chat page (`app.py`).

## Results

Metric: top-k hit rate, where a question is a hit if any chunk labeled as containing the answer appears in the top k results.

**Held-out set (20 questions, evaluated once on the final system), %:**

| Method | Top-1 | Top-3 | Top-5 |
|---|---|---|---|
| Vector only | 70 | 90 | 90 |
| BM25 only | 65 | 75 | 90 |
| Hybrid (RRF) | 75 | 90 | 100 |

Hybrid was highest or tied in every column, but its margin over vector search is at most two questions, which is within sampling noise on n=20 (the 95% confidence interval for 75% on 20 questions is roughly 53% to 89%).

**Development set (20 questions, used to guide changes, so optimistic), Top-1 / Top-3 / Top-5, %:**

| Stage | Vector | BM25 | Hybrid |
|---|---|---|---|
| Baseline | 70 / 100 / 100 | 70 / 95 / 95 | 90 / 95 / 95 |
| + document title prepended to chunks | 75 / 100 / 100 | 70 / 95 / 95 | 90 / 95 / 100 |
| + stopword removal in BM25 | 75 / 100 / 100 | 70 / 95 / 100 | 75 / 100 / 100 |

Stopword removal improved hybrid top-3 but lowered hybrid top-1, a trade-off rather than a clear win.

**Failure analysis (held-out set):** of seven questions with a miss, three were vocabulary mismatches (yearly/annual, move out/export, spreadsheet/CSV), two were fusion-ordering effects, one was caused by distractor chunks, and one affected BM25 only. Raw outputs are in `eval/`.

**Verification step:** tested manually. It marked a grounded answer SUPPORTED and flagged a deliberately fabricated answer as UNSUPPORTED. It was not scored quantitatively.

## Quick start

```bash
git clone https://github.com/YOUR_USERNAME/support-copilot.git
cd support-copilot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env        # then put your free Groq API key in .env
python3 vector_store.py     # builds the ChromaDB index (first run downloads the embedding model)

python3 -m streamlit run app.py          # chat UI
python3 -m uvicorn api:app --reload      # or the API (POST /ask)
python3 run_eval.py eval/questions_heldout.csv   # evaluation
```

Model names on Groq change. If the model in `generate.py` and `verify.py` returns a 404, run `python3 list_models.py` and use a currently listed model.

## Project structure

| File | Purpose |
|---|---|
| `docs/` | Six synthetic support documents with metadata headers |
| `loader.py` | Splits each file into metadata and text |
| `chunker.py` | Heading-based chunking, title prefix, drops tiny chunks |
| `vector_store.py` | Embeds chunks and stores them in ChromaDB |
| `bm25_search.py` | BM25 index with custom tokenizer and stopwords |
| `search_test.py` | Dense search over ChromaDB |
| `hybrid_search.py` | Reciprocal Rank Fusion of dense and BM25 results |
| `generate.py` | Grounded answer generation with citations |
| `verify.py` | LLM-as-judge fact check of the answer against sources |
| `api.py` / `app.py` | FastAPI backend / Streamlit UI |
| `run_eval.py`, `analyze_failures.py` | Evaluation and failure analysis |
| `eval/` | Test sets, saved results and failure analysis |

## Limitations

- Small synthetic corpus (29 chunks) and 20-question test sets, where each question is worth 5 percentage points.
- Held-out questions were drafted with LLM assistance. <!-- EDIT: state here whether you independently reviewed the labels, and only if you did -->
- The development-set results were used to guide changes and should not be read as accuracy.
- The verifier uses the same kind of model as the generator and was only spot-checked.
- End-to-end answer quality (faithfulness, completeness) was not measured.
- English only.

## Roadmap

Multilingual retrieval over Telugu documents, a reranking stage, filtering zero-score BM25 results before fusion, and a larger independently written test set.
