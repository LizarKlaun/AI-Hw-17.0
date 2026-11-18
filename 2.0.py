import os
import re
import chromadb
from sentence_transformers import SentenceTransformer
import ollama

chromadb_client = chromadb.PersistentClient(path="./chroma_db")
collection_name = "local_base"
collection = chromadb_client.get_or_create_collection(name=collection_name)

embending_model = SentenceTransformer("all-MiniLM-L6-v2")

DATASET_FILE = "dataset.md" if os.path.exists("dataset.md") else "./base/dataset.md"

print("check docs")

if os.path.exists(DATASET_FILE) and collection.count() == 0:
    with open(DATASET_FILE, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Удаляем только первую строку с общим заголовком, сохраняя doc_1!
    raw_text = re.sub(r"^# Unique Projects Dataset.*?\n+", "", raw_text).strip()

    # Режем ровно по разделителю проектов "---"
    blocks = [b.strip() for b in raw_text.split("---") if b.strip()]

    print(f"Индексируем {len(blocks)} проектов...")

    ids = [f"proj_{i+1}" for i in range(len(blocks))]
    metadatas = [{"source": os.path.basename(DATASET_FILE), "item": i+1} for i in range(len(blocks))]
    vectors = embending_model.encode(blocks, batch_size=64, show_progress_bar=True).tolist()

    collection.add(
        documents=blocks,
        embeddings=vectors,
        ids=ids,
        metadatas=metadatas,
    )
    print(f"Added {len(blocks)} projects to base!")

if collection.count() == 0:
    print("База пуста! Проверь путь к dataset.md.")
    exit()

user_query = input("input your question: ").strip()

if not user_query:
    user_query = "What is project Vanguard_1 and what technologies does it use?"

print("Search question ...")

query_embendding = embending_model.encode([user_query]).tolist()

# Ищем в вопросе упоминание конкретного имени проекта (например, Vanguard_1 или doc_1)
exact_match = re.search(r"\b([A-Za-z]+_\d+)\b", user_query)

if exact_match:
    keyword = exact_match.group(1)
    results = collection.query(
        query_embeddings=query_embendding,
        n_results=3,
        where_document={"$contains": keyword}
    )
    # Если по точному имени ничего не нашлось, откатываемся к обычному векторному поиску
    if not results["documents"][0]:
        results = collection.query(query_embeddings=query_embendding, n_results=3)
else:
    results = collection.query(query_embeddings=query_embendding, n_results=3)

retrieved_chunks = results["documents"][0]
sources = results["metadatas"][0]

print("Data is ready")

for i, (chunk, meta) in enumerate(zip(retrieved_chunks, sources)):
    print(f"[{i+1}] Document: {meta['source']} (item #{meta['item']})\n{chunk}\n")

context = "\n\n".join(retrieved_chunks)

promt = f"""Use ONLY the following contextual data from the files to answer the question.
If the context does not answer the question, say: "I don't have that information in my knowledge base."

Context:
{context}

User query:
{user_query}"""

responce = ollama.chat(
    model="qwen2.5",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a clever assistant who gives answers only in English and only about the provided files."
            )
        },
        {
            "role": "user",
            "content": promt
        }
    ]
)

print("\n--- Response ---")
print(responce["message"]["content"])