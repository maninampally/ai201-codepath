import os
from groq import Groq
from dotenv import load_dotenv
from embed import retrieve

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a helpful assistant for FAU students looking up professor reviews.
Answer the user's question using ONLY the information provided in the retrieved review chunks below.
Do not use any outside knowledge. If the retrieved chunks do not contain enough information to answer
the question, say "I don't have enough information in my documents to answer that."
Always cite which professor and source file the information came from."""

def ask(question):
    chunks = retrieve(question, k=8)
    
    context = ""
    for i, chunk in enumerate(chunks):
        context += f"\n[Source {i+1}: {chunk['source']}]\n{chunk['text']}\n"
    
    prompt = f"""Here are relevant student reviews retrieved for your question:
{context}

Question: {question}

Answer using only the reviews above. Cite the source files in your answer."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )

    answer = response.choices[0].message.content
    sources = list(set(chunk["source"] for chunk in chunks))
    
    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks
    }


if __name__ == "__main__":
    test_questions = [
        "Does Professor Agarwal respond to emails?",
        "What is Alhalabi's class like?",
    ]
    
    for q in test_questions:
        print(f"\nQuestion: {q}")
        result = ask(q)
        print(f"Answer: {result['answer']}")
        print(f"Sources: {result['sources']}")
        print("-" * 60)
