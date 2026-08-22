import os
from pathlib import Path
from typing import cast

import chromadb
import pandas as pd
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from groq import Groq
from groq.types.chat import ChatCompletionMessageParam

# -----------------------------
# Configuration
# -----------------------------

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BASE_DIR = Path(__file__).parent
FAQ_PATH = BASE_DIR / "app" / "resources" / "faq_data.csv"

COLLECTION_NAME = "faqs"


# -----------------------------
# ChromaDB
# -----------------------------

chroma_client = chromadb.PersistentClient(
    path=str(BASE_DIR / "chroma_db")
)

embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# -----------------------------
# Ingestion
# -----------------------------

def ingest_faq(path: Path):

    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function
    )

    df = pd.read_csv(path)

    documents = df["question"].astype(str).tolist()

    metadata = [
        {"answer": ans}
        for ans in df["answer"].astype(str).tolist()
    ]

    ids = [
        f"faq_{i}"
        for i in range(len(documents))
    ]

    collection.upsert(
        documents=documents,
        metadatas=metadata,
        ids=ids
    )

    print(f"Ingested {len(documents)} FAQs.")


# -----------------------------
# Retrieval
# -----------------------------

def get_relevant_qa(query: str, n_results: int = 3):

    collection = chroma_client.get_collection(
        name=COLLECTION_NAME
    )

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return results


# -----------------------------
# Context Building
# -----------------------------

def build_context(results):

    if not results["documents"] or not results["documents"][0]:
        return ""

    documents = results["documents"][0]
    metadata = results["metadatas"][0]

    context_parts = []

    for question, meta in zip(documents, metadata):
        context_parts.append(
            f"""FAQ Question: {question}
FAQ Answer: {meta["answer"]}"""
        )

    return "\n".join(context_parts)


# -----------------------------
# LLM
# -----------------------------

def generate_answer(query: str, context: str):

    if not context:
        return "I don't know based on the available information."

    messages = cast(
        list[ChatCompletionMessageParam],
        [
            {
                "role": "system",
                "content": """You are an FAQ assistant.

Answer the user's question ONLY using the provided FAQ context.

Rules:
- Do not use outside knowledge.
- Do not make up information.
- If the answer cannot be found in the context,
  say: "I don't know based on the available information."
- Keep the answer concise and direct."""
            },
            {
                "role": "user",
                "content": f"""FAQ CONTEXT:
{context}

USER QUESTION: {query}"""
            }
        ]
    )

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages
    )

    return response.choices[0].message.content


# -----------------------------
# RAG Pipeline
# -----------------------------

def faq_chain(query: str):

    results = get_relevant_qa(query)
    context = build_context(results)

    answer = generate_answer(
        query=query,
        context=context
    )

    return answer


# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":

    # Only ingest if the collection doesn't already exist / is empty.
    try:
        existing = chroma_client.get_collection(name=COLLECTION_NAME)
        if existing.count() == 0:
            ingest_faq(FAQ_PATH)
    except Exception:
        ingest_faq(FAQ_PATH)

    query = "What is your policy on defective products?"
    answer = faq_chain(query)

    print("\nAnswer:")
    print(answer)