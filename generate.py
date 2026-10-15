import os
from dotenv import load_dotenv
from groq import Groq
from hybrid_search import hybrid_retrieve

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a support assistant for Taskly, a project management tool.
Answer the user's question using ONLY the reference material provided below.
Cite which source each fact came from using the format [source: filename].
If the reference material does not contain enough information to answer confidently,
say so clearly instead of guessing. Do not use outside knowledge."""


def build_context(chunks):
    parts = []
    for c in chunks:
        parts.append(f"[source: {c['chunk_id']}]\n{c['text']}")
    return "\n\n---\n\n".join(parts)


def answer_question(question, n_results=3):
    chunks = hybrid_retrieve(question, n_results=n_results)
    context = build_context(chunks)

    user_prompt = f"""Reference material:

{context}

Question: {question}"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    return {
        "answer": response.choices[0].message.content,
        "sources_used": [c["chunk_id"] for c in chunks],
    }


if __name__ == "__main__":
    result = answer_question("why am I not getting notifications")
    print(result["answer"])
    print("\nSources:", result["sources_used"])
