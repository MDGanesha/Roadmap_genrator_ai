import json
import os
import pickle
import ollama
import chromadb

# Cache file for faster reloads
CACHE_FILE = "data/embeddings_cache.pkl"

def index_resources(
    path="data/roadmaps.json",
    collection_name="knowledge_base",
    model_name="mxbai-embed-large",  # or "nomic-embed-text" for faster runs
    use_cache=True
):
    # Ensure collection name is valid
    if len(collection_name) < 3:
        collection_name += "_db"

    # Load dataset
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Dataset not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        docs = json.load(f)

    # Load from cache if available
    if use_cache and os.path.exists(CACHE_FILE):
        print("🔄 Loading embeddings from cache...")
        with open(CACHE_FILE, "rb") as f:
            cache = pickle.load(f)
        ids, documents, embeddings, metadatas = (
            cache["ids"], cache["documents"], cache["embeddings"], cache["metadatas"]
        )
    else:
        print("⚡ Generating new embeddings...")
        texts = [(doc.get("text") or doc.get("title") or doc.get("skill") or "")[:1000] for doc in docs]

        # Batch embedding
        resp = ollama.embed(model=model_name, input=texts)
        embeddings = resp["embeddings"]

        ids = [str(i) for i in range(len(docs))]
        documents = texts

        # ✅ Clean metadata (Chroma only accepts primitives)
        def clean_metadata(doc):
            cleaned = {}
            for k, v in doc.items():
                if isinstance(v, (str, int, float, bool)) or v is None:
                    cleaned[k] = v
                else:
                    cleaned[k] = json.dumps(v)  # flatten lists/dicts
            return cleaned

        metadatas = [clean_metadata(doc) for doc in docs]

        # Save to cache
        if use_cache:
            os.makedirs("data", exist_ok=True)
            with open(CACHE_FILE, "wb") as f:
                pickle.dump(
                    {
                        "ids": ids,
                        "documents": documents,
                        "embeddings": embeddings,
                        "metadatas": metadatas,
                    },
                    f,
                )
            print("💾 Embeddings cached for future runs.")

    # ✅ Persistent ChromaDB (saves to disk)
    client = chromadb.PersistentClient(path="data/chroma")

    # Reset collection if it exists
    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass

    col = client.create_collection(name=collection_name)
    col.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)

    print(f"✅ Indexed {len(ids)} documents into persistent collection '{collection_name}'.")

if __name__ == "__main__":
    index_resources()
