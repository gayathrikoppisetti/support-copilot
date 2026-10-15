import os
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

load_dotenv()

print("Testing Groq...")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role": "user", "content": "Say hello in one short sentence."}]
)
print("Groq response:", response.choices[0].message.content)

print("\nTesting local embeddings...")
model = SentenceTransformer("all-MiniLM-L6-v2")
embedding = model.encode("This is a test sentence.")
print("Embedding shape:", embedding.shape)
print("First 5 numbers:", embedding[:5])
