import ollama
import chromadb

# Load persistent Chroma collection
client = chromadb.PersistentClient(path="data/chroma")
col = client.get_collection("knowledge_base")

def search(query: str, model="mxbai-embed-large", top_k=5):
    # Embed user query
    resp = ollama.embed(model=model, input=query)
    query_embedding = resp["embeddings"][0]

    # Search in Chroma
    results = col.query(query_embeddings=[query_embedding], n_results=top_k)

    return results

if __name__ == "__main__":
    q = "Machine Learning beginner roadmap"
    results = search(q)

    print("🔍 Query:", q)
    for i, doc in enumerate(results["documents"][0]):
        print(f"\nResult {i+1}:")
        print("Document:", doc)
        print("Metadata:", results["metadatas"][0][i])

