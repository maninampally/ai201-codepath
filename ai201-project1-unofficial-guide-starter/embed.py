from sentence_transformers import SentenceTransformer
import chromadb
from ingest import load_and_chunk_documents

COLLECTION_NAME = "fau_professor_reviews"

def build_vector_store():
    print("Loading chunks...")
    chunks = load_and_chunk_documents()
    print(f"Loaded {len(chunks)} chunks")

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Setting up ChromaDB...")
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Delete existing collection if rebuilding
    try:
        client.delete_collection(COLLECTION_NAME)
    except:
        pass
    
    collection = client.create_collection(COLLECTION_NAME)

    print("Embedding and storing chunks...")
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)

    collection.add(
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks],
        ids=[f"{c['source']}_{c['chunk_index']}" for c in chunks]
    )

    print(f"Stored {collection.count()} chunks in ChromaDB")
    return collection, model


def retrieve(query, k=5):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(COLLECTION_NAME)
    
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )
    
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })
    return chunks


if __name__ == "__main__":
    build_vector_store()

    print("\n--- Testing retrieval ---\n")
    test_queries = [
        "Does Professor Agarwal respond to emails?",
        "What is Alhalabi's class like?",
        "Is CAP4770 with Ibrahim hard?"
    ]

    for query in test_queries:
        print(f"Query: {query}")
        results = retrieve(query)
        for r in results:
            print(f"  [{r['distance']:.3f}] {r['source']}: {r['text'][:120]}...")
        print()
