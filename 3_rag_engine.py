"""
ÉTAPE 3: MOTEUR RAG avec Mistral API (via requests) + FAISS
Avec troncature du contexte pour éviter les erreurs 400.
"""

import os
import requests
import numpy as np
from typing import List, Dict
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# CONFIGURATION
# ============================================================================
VECTOR_DB_PATH = "./vector_db_faiss"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-small-latest")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1000"))
MAX_CONTEXT_CHARS = 6000  # Limite la taille du contexte pour éviter les overflow

# ============================================================================
# APPEL MISTRAL API VIA REQUESTS
# ============================================================================
def call_mistral(messages: List[Dict]) -> str:
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MISTRAL_MODEL,
        "messages": messages,
        "temperature": LLM_TEMPERATURE,
        "max_tokens": LLM_MAX_TOKENS
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            return f"Erreur API ({response.status_code}): {response.text[:200]}"
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Erreur requête: {e}"

# ============================================================================
# CHARGER LA BASE VECTORIELLE FAISS
# ============================================================================
def load_vector_store() -> FAISS:
    if not os.path.exists(VECTOR_DB_PATH):
        raise FileNotFoundError(f"Base vectorielle non trouvée dans {VECTOR_DB_PATH}. Lance d'abord 2_ingest_vectorize.py")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL, model_kwargs={'device': 'cpu'})
    return FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)

# ============================================================================
# RECHERCHE
# ============================================================================
def retrieve_relevant_docs(vector_store, query: str, k: int = 3) -> List[Dict]:
    results = vector_store.similarity_search_with_score(query, k=k)
    docs = []
    for doc, score in results:
        docs.append({
            "content": doc.page_content,
            "metadata": doc.metadata,
            "similarity_score": score,
        })
    return docs

# ============================================================================
# CONSTRUCTION DU CONTEXTE AVEC TRONCATURE
# ============================================================================
def build_rag_context(docs: List[Dict]) -> tuple:
    context_parts = []
    sources_info = []
    total_chars = 0
    for i, d in enumerate(docs, 1):
        meta = d["metadata"]
        score = d["similarity_score"]
        if meta.get("source") == "ticket_historique":
            part = (
                f"\n--- TICKET #{i} (score:{score:.2f}) ---\n"
                f"ID: {meta.get('ticket_id')}\nCatégorie: {meta.get('categorie')}\n"
                f"{d['content']}"
            )
            sources_info.append({"type": "ticket", "id": meta.get('ticket_id'), "score": float(score)})
        else:
            part = (
                f"\n--- DOCUMENTATION #{i} (score:{score:.2f}) ---\n"
                f"Fichier: {meta.get('filename')}\n{d['content'][:1000]}"
            )
            sources_info.append({"type": "doc", "filename": meta.get('filename'), "score": float(score)})
        
        if total_chars + len(part) > MAX_CONTEXT_CHARS:
            # Ajoute un indicateur de troncature
            context_parts.append("\n... (contexte tronqué pour limiter la taille) ...")
            break
        context_parts.append(part)
        total_chars += len(part)
    
    context = "\n".join(context_parts)
    return context, sources_info

# ============================================================================
# GÉNÉRATION DE LA RÉPONSE
# ============================================================================
def generate_response(user_query: str, context: str) -> str:
    system_prompt = """Tu es un expert support IT. Fournis des solutions claires, étape par étape.
Cite tes sources. Sois concis mais complet."""
    
    user_prompt = f"""Contexte (tickets et documentation):
{context}

---

Question: {user_query}

Réponds avec:
1. Diagnostic court
2. Étapes de résolution détaillées
3. Sources utilisées
4. Quand contacter le support avancé"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    return call_mistral(messages)

# ============================================================================
# MOTEUR RAG
# ============================================================================
class RAGEngine:
    def __init__(self):
        if not MISTRAL_API_KEY:
            raise RuntimeError("MISTRAL_API_KEY non définie. Utilisez .env ou variable d'environnement.")
        self.vector_store = load_vector_store()

    def resolve_ticket(self, user_query: str, k: int = 3) -> Dict:
        print(f"\n📝 Requête: {user_query}")
        docs = retrieve_relevant_docs(self.vector_store, user_query, k)
        context, sources = build_rag_context(docs)
        print(f"📏 Taille du contexte: {len(context)} caractères")
        response = generate_response(user_query, context)
        return {
            "user_query": user_query,
            "response": response,
            "sources": sources,
            "num_sources": len(docs),
        }

# ============================================================================
# MAIN
# ============================================================================
def main():
    print("\n" + "="*80)
    print("🚀 MOTEUR RAG avec Mistral API + FAISS (contexte limité)")
    print("="*80)
    try:
        engine = RAGEngine()
        query = "Mon Cisco AnyConnect tourne en boucle et ne se connecte pas"
        result = engine.resolve_ticket(query, k=2)  # On limite à 2 sources pour réduire
        print("\n✅ RÉPONSE:\n", result['response'])
        print("\n📚 SOURCES:", result['sources'])
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()