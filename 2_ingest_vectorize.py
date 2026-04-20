"""
ÉTAPE 2: INGESTION ET VECTORISATION avec FAISS (sans ChromaDB)
"""

import os
import csv
import glob
import pickle
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# ============================================================================
# CONFIGURATION
# ============================================================================
VECTOR_DB_PATH = "./vector_db_faiss"
CSV_FILE = "tickets_historiques.csv"
DOCS_FOLDER = "./docs"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ============================================================================
# CHARGER LES TICKETS CSV
# ============================================================================
def load_tickets_from_csv(csv_path: str) -> List[Document]:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"{csv_path} introuvable !")
    
    documents = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            content = f"""
Ticket ID: {row['Ticket_ID']}
Titre: {row['Titre']}
Catégorie: {row['Catégorie']}
Sévérité: {row['Sévérité']}

Description:
{row['Description']}

Solution:
{row['Résolution_Apportée']}
            """.strip()
            metadata = {
                "source": "ticket_historique",
                "ticket_id": row['Ticket_ID'],
                "categorie": row['Catégorie'],
                "severite": row['Sévérité'],
                "date_resolution": row['Date_Résolution'],
            }
            documents.append(Document(page_content=content, metadata=metadata))
    
    print(f"{len(documents)} tickets chargés")
    return documents

# ============================================================================
# CHARGER LES GUIDES MARKDOWN
# ============================================================================
def load_markdown_docs(folder_path: str) -> List[Document]:
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"{folder_path} introuvable !")
    
    documents = []
    md_files = glob.glob(os.path.join(folder_path, "*.md"))
    for md_file in md_files:
        filename = os.path.basename(md_file)
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        category = filename.replace("_Guide.md", "").replace("_", " ")
        metadata = {"source": "knowledge_base", "filename": filename, "categorie": category}
        documents.append(Document(page_content=content, metadata=metadata))
    
    print(f" {len(documents)} guides chargés")
    return documents

# ============================================================================
# DÉCOUPAGE (CHUNKING)
# ============================================================================
def chunk_documents(documents: List[Document], chunk_size=500, chunk_overlap=100) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunked = splitter.split_documents(documents)
    print(f" {len(documents)} documents → {len(chunked)} chunks")
    return chunked

# ============================================================================
# CRÉER LA BASE VECTORIELLE AVEC FAISS
# ============================================================================
def create_vector_store(chunked_docs: List[Document], db_path: str):
    print(f"\n🤖 Chargement du modèle d'embeddings: {EMBEDDING_MODEL}")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
    )
    print("📊 Création de FAISS...")
    vector_store = FAISS.from_documents(chunked_docs, embeddings)
    
    # Sauvegarde locale
    os.makedirs(db_path, exist_ok=True)
    vector_store.save_local(db_path)
    print(f" Base vectorielle FAISS sauvegardée dans {db_path}")
    return vector_store

# ============================================================================
# TEST RAPIDE
# ============================================================================
def test_vector_store(vector_store: FAISS, query="VPN ne se connecte pas"):
    print(f"\n🧪 Test recherche: '{query}'")
    results = vector_store.similarity_search(query, k=3)
    for i, doc in enumerate(results, 1):
        meta = doc.metadata
        print(f"\n[{i}] {meta.get('source', '?')} - {meta.get('filename', meta.get('ticket_id', ''))}")
        print(doc.page_content[:150].replace('\n', ' ') + "...")

# ============================================================================
# MAIN
# ============================================================================
def main():
    print("\n" + "="*80)
    print("ÉTAPE 2: INGESTION ET VECTORISATION AVEC FAISS")
    print("="*80)
    
    if not os.path.exists(CSV_FILE) or not os.path.exists(DOCS_FOLDER):
        print("Fichiers manquants. Lance d'abord: python 1_generate_data.py")
        return
    
    tickets = load_tickets_from_csv(CSV_FILE)
    docs = load_markdown_docs(DOCS_FOLDER)
    all_docs = tickets + docs
    print(f"➕ Total documents bruts: {len(all_docs)}")
    
    chunked = chunk_documents(all_docs)
    vector_store = create_vector_store(chunked, VECTOR_DB_PATH)
    test_vector_store(vector_store)
    
    print("\n✨ ÉTAPE 2 TERMINÉE")
    print(f" Prochaine étape: modifier 3_rag_engine.py pour utiliser FAISS (chemin: {VECTOR_DB_PATH})\n")

if __name__ == "__main__":
    main()