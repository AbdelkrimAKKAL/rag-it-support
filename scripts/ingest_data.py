import os
import shutil
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from dotenv import load_dotenv
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.document_loaders import TextLoader
    print("✅ Core imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_DIR = os.path.join(BASE_DIR, "backend", "chroma_db")
ENV_PATH = os.path.join(BASE_DIR, "backend", ".env")

# Load API Key
load_dotenv(ENV_PATH)

def main():
    print("=" * 60)
    print("IT Support RAG - Data Ingestion Pipeline")
    print("=" * 60)
    
    print(f"\n📁 Data directory: {DATA_DIR}")
    print(f"💾 Database directory: {DB_DIR}")
    
    # Check if data directory exists
    if not os.path.exists(DATA_DIR) or not os.path.isdir(DATA_DIR):
        print(f"❌ Error: Data directory not found at {DATA_DIR}")
        return

    documents = []
    
    # Load all supported files in the data folder
    print("\n📖 Loading documents...")
    for filename in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, filename)
        if filename.endswith(".md"):
            print(f"  ✓ Loading Markdown: {filename}")
            try:
                loader = TextLoader(file_path, encoding='utf-8')
                documents.extend(loader.load())
            except Exception as e:
                print(f"    ⚠️  Error loading {filename}: {e}")
        elif filename.endswith(".txt"):
            print(f"  ✓ Loading Text file: {filename}")
            try:
                loader = TextLoader(file_path, encoding='utf-8')
                documents.extend(loader.load())
            except Exception as e:
                print(f"    ⚠️  Error loading {filename}: {e}")

    if not documents:
        print("❌ No supported documents (.txt, .md) found in the data directory.")
        return

    print(f"\n✅ Loaded {len(documents)} document(s)")

    # Split text into manageable chunks
    chunk_size = int(os.getenv("CHUNK_SIZE", 1000))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP", 200))
    
    print(f"\n✂️  Splitting documents (chunk_size={chunk_size}, overlap={chunk_overlap})...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Split into {len(chunks)} chunks")

    # Import Chroma and embeddings
    print("\n🔄 Initializing vector store...")
    try:
        from langchain_chroma import Chroma
        from langchain_mistralai import MistralAIEmbeddings
        
        # Clear existing DB to avoid dimension mismatch
        if os.path.exists(DB_DIR):
            print(f"🗑️  Deleting existing database at {DB_DIR}...")
            shutil.rmtree(DB_DIR)

        # Initialize embedding model
        print("🧠 Initializing Mistral embeddings...")
        embeddings = MistralAIEmbeddings(model="mistral-embed", max_retries=5)

        # Create Chroma vector store
        print(f"💾 Creating vector database at {DB_DIR}...")
        vectorstore = Chroma.from_documents(
            documents=chunks, 
            embedding=embeddings, 
            persist_directory=DB_DIR,
            collection_name="it_support_collection"
        )
        print("✅ Ingestion complete. Database is ready!")
        print(f"📊 Total chunks vectorized: {len(chunks)}")
        
    except Exception as e:
        print(f"❌ Error during vectorization: {e}")
        print("\n⚠️  Note: Chroma database creation failed.")
        print(f"   Error details: {str(e)}")
        return

if __name__ == "__main__":
    main()


