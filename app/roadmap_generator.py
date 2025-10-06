import ollama
from app.query_embeddings import search
from app.youtube_search import search_youtube

def generate_roadmap(skill: str, duration: str, level: str):
    # Retrieve relevant skills from embeddings
    query = f"{skill} {level} {duration}"
    results = search(query, top_k=5)
    related_skills = [m.get("skill") for m in results["metadatas"][0] if "skill" in m]

    # Fetch YouTube links for each skill
    resources = {}
    for s in related_skills[:3]:  # only top 3 to keep it short
        resources[s] = search_youtube(f"{s} tutorial {level}")

    # Build prompt for roadmap generation
    prompt = f"""
    The user wants to learn {skill} in {duration}.
    Current level: {level}.
    Relevant skills: {", ".join(related_skills)}.

    Generate a step-by-step roadmap. 
    For each step, suggest 1–2 YouTube resources from this list:
    {resources}
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]
