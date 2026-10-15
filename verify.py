import os
from dotenv import load_dotenv
from groq import Groq
from generate import answer_question, build_context
from hybrid_search import hybrid_retrieve

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

VERIFY_PROMPT = """You are a strict fact-checker. You will be given a SOURCE TEXT and an ANSWER.
Check whether every factual claim in the ANSWER is actually supported by the SOURCE TEXT.

Respond in exactly this format:
VERDICT: SUPPORTED or UNSUPPORTED or PARTIALLY_SUPPORTED
ISSUES: a short list of any claims not supported by the source, or "none" if fully supported"""


def verify_answer(question, n_results=3):
    chunks = hybrid_retrieve(question, n_results=n_results)
    context = build_context(chunks)

    generated = answer_question(question, n_results=n_results)
    answer_text = generated["answer"]

    verify_prompt = f"""SOURCE TEXT:
{context}

ANSWER TO CHECK:
{answer_text}"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": VERIFY_PROMPT},
            {"role": "user", "content": verify_prompt},
        ],
    )

    return {
        "question": question,
        "answer": answer_text,
        "verification": response.choices[0].message.content,
        "sources_used": generated["sources_used"],
    }


if __name__ == "__main__":
    result = verify_answer("why am I not getting notifications")
    print("ANSWER:")
    print(result["answer"])
    print("\nVERIFICATION:")
    print(result["verification"])
